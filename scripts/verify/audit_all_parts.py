"""Check every baked HD part against its native part and list the ones that look wrong.

For each finished texture the native part is rebuilt from its palette slot
map and palette, and the HD picture is compared with it texel by texel:

* shape      - HD silhouette against the native silhouette (overlap, paint
               outside the native shape, native area left unpainted)
* colour     - average HD colour of each texel against the native colour
* flat       - HD that is only the native dots enlarged (no painted detail)
* key        - saturated green/magenta the native palette cannot explain
* empty      - almost nothing painted

Each test is a screen for review, not a verdict: a repainted pose may
differ from the dots on purpose. Reads only; writes
test_current/parts/full_audit/.
"""
import argparse,json,sys
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image,ImageDraw

_renderer=None
RULES=dict(shape='overlap (IoU) with the native silhouette below 0.60',outside='over 15% of the paint lies more than one texel outside the native shape',
    unpainted='over 20% of the native shape has no paint',colour='over 30% of texels differ from the native colour by 90/255 or more',
    flat='over 90% of textured texels are a single flat colour (enlarged dots)',key_green='8+ saturated green pixels with no green in the native palette',
    key_magenta='8+ saturated magenta pixels with no magenta in the native palette',empty='fewer than 16 opaque pixels although the native part has 8+ texels')


def start():
    global _renderer
    from hd_parts import PartsRenderer
    _renderer=PartsRenderer(async_prepare=False)


def palette_of(spec):
    for name in ('palette_source_rgb','original_palette_rgb'):
        value=spec.get(name)
        if value is not None:
            palette=np.asarray(value,dtype='float32')
            if palette.ndim==2 and len(palette)>=2:return palette
    return None


def analyse(binding,keep=False):
    renderer=_renderer;spec=renderer.bindings[binding-1];palette=palette_of(spec)
    if palette is None:return dict(binding=binding,skipped='no palette')
    slots=renderer.native_slot_map(binding,spec,palette)
    if slots is None:return dict(binding=binding,skipped='no native slot map')
    found=renderer.disk_cache.get(renderer.texture_key(binding,spec['w'],spec['h']))
    if found is None:return dict(binding=binding,skipped='not in store')
    art,stats=found;h,w=slots.shape
    if art.size!=(w*4,h*4):art=art.resize((w*4,h*4),Image.Resampling.LANCZOS)
    pixels=np.asarray(art);rgb=pixels[:,:,:3].astype('float32');opaque=pixels[:,:,3]>=128
    blocks=lambda array:array.reshape(h,4,w,4,*array.shape[2:]).swapaxes(1,2)          # (h,w,4,4,...)
    cover=blocks(opaque).reshape(h,w,16).mean(2);painted=cover>=.5;native=slots>0
    union=int((painted|native).sum());iou=float((painted&native).sum()/union) if union else 1.
    padded=np.pad(native,1);near=np.zeros_like(native)
    for dy in range(3):
        for dx in range(3):near|=padded[dy:dy+h,dx:dx+w]
    total=int(opaque.sum());outside=float((cover*(~near)).sum()*16/total) if total else 0.
    unpainted=float((native&(cover<.25)).sum()/max(1,int(native.sum())))
    # Colour: mean of the opaque HD pixels in each texel against the native texel colour.
    weights=blocks(opaque).reshape(h,w,16).astype('float32');sums=(blocks(rgb).reshape(h,w,16,3)*weights[...,None]).sum(2);count=weights.sum(2)
    both=native&(count>=8);mean=sums/np.maximum(count,1)[...,None];native_rgb=palette[np.minimum(slots,len(palette)-1)]
    error=np.abs(mean-native_rgb).max(2);colour_bad=float((error[both]>=90).mean()) if both.any() else 0.;colour_mean=float(error[both].mean()) if both.any() else 0.
    # Flat: texels fully painted whose 16 HD pixels are one colour, among texels that sit on a native colour change.
    full=count==16;deviation=blocks(rgb).reshape(h,w,16,3).std(2).max(2)
    edge=np.zeros_like(native);edge[:,1:]|=slots[:,1:]!=slots[:,:-1];edge[1:]|=slots[1:]!=slots[:-1];textured=full&native&edge
    flat=float((deviation[textured]<1.5).mean()) if textured.sum()>=8 else 0.
    r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2];shown=pixels[:,:,3]>=32
    green=shown&(g>=110)&(g-r>=70)&(g-b>=70);magenta=shown&(r>=140)&(b>=140)&(r-g>=90)&(b-g>=90);colours=palette[1:]
    native_green=float((colours[:,1]-np.maximum(colours[:,0],colours[:,2])).max());native_magenta=float((np.minimum(colours[:,0],colours[:,2])-colours[:,1]).max())
    flags=[]
    if total<16 and native.sum()>=8:flags.append('empty')
    else:
        if iou<.60:flags.append('shape')
        if outside>.15:flags.append('outside')
        if unpainted>.20:flags.append('unpainted')
        if colour_bad>.30:flags.append('colour')
        if flat>.90:flags.append('flat')
        if green.sum()>=8 and native_green<40:flags.append('key_green')
        if magenta.sum()>=8 and native_magenta<40:flags.append('key_magenta')
    row=dict(binding=binding,atlas=spec.get('atlas_id','base'),resource=spec.get('resource'),x=spec['x'],y=spec['y'],w=w,h=h,native_texels=int(native.sum()),
        iou=round(iou,3),outside=round(outside,3),unpainted=round(unpainted,3),colour_bad=round(colour_bad,3),colour_mean=round(colour_mean,1),flat=round(flat,3),
        green_pixels=int(green.sum()),magenta_pixels=int(magenta.sum()),registered_iou=stats.get('registered_iou'),flags=flags)
    if keep:
        reference=np.zeros((h,w,4),dtype='uint8');reference[native,:3]=native_rgb[native].astype('uint8');reference[native,3]=255
        return row,pixels,reference
    return row


def work(binding):
    try:return analyse(binding)
    except Exception as error:return dict(binding=binding,skipped='error: '+str(error)[:120])


def main():
    parser=argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--workers',type=int,default=6);parser.add_argument('--bindings',type=int,nargs='*');parser.add_argument('--per-flag',type=int,default=120,help='parts drawn per defect class')
    args=parser.parse_args();out=ROOT/'test_current/parts/full_audit';out.mkdir(parents=True,exist_ok=True);start()
    if args.bindings:
        for binding in args.bindings:print(json.dumps(analyse(binding)))
        return
    for old in out.glob('*'):
        if old.is_file():old.unlink()
    todo=[];seen=set();aliases=defaultdict(int)
    for binding,spec in enumerate(_renderer.bindings,1):
        if spec.get('runtime_texture') or spec.get('disabled'):continue
        if spec.get('source_binding'):aliases[spec['source_binding']]+=1;continue
        key=_renderer.texture_key(binding,spec['w'],spec['h'])
        if key in seen:continue
        seen.add(key);todo.append(binding)
    rows=[];skipped=defaultdict(int)
    with Pool(args.workers,initializer=start) as pool:
        for done,row in enumerate(pool.imap_unordered(work,todo,chunksize=64),1):
            if 'skipped' in row:skipped[row['skipped'].split(':')[0]]+=1
            else:rows.append(row)
            if done%10000==0:print(done,'/',len(todo),flush=True)
    flagged=[row for row in rows if row['flags']];counts=defaultdict(int);by_atlas=defaultdict(lambda:defaultdict(int));by_resource=defaultdict(lambda:defaultdict(int))
    for row in rows:by_atlas[row['atlas']]['parts']+=1
    for row in flagged:
        by_atlas[row['atlas']]['flagged']+=1;by_resource[row['resource']]['flagged']+=1
        for flag in row['flags']:counts[flag]+=1;by_atlas[row['atlas']][flag]+=1;by_resource[row['resource']][flag]+=1
    severity=lambda row:(len(row['flags']),row['native_texels'])
    report=dict(measured=len(rows),skipped=dict(skipped),flagged_parts=len(flagged),clean_parts=len(rows)-len(flagged),rules=RULES,by_flag=dict(sorted(counts.items(),key=lambda item:-item[1])),
        by_atlas=sorted(({'atlas':k,**v,'flagged_share':round(v.get('flagged',0)/v['parts'],3)} for k,v in by_atlas.items() if v.get('flagged')),key=lambda e:-e['flagged']),
        by_resource=sorted(({'resource':k,**v} for k,v in by_resource.items()),key=lambda e:-e['flagged']),
        parts=sorted(flagged,key=severity,reverse=True))
    (out/'report.json').write_text(json.dumps(report,indent=1),encoding='utf-8')
    (out/'all_rows.json').write_text(json.dumps(rows),encoding='utf-8')
    cell=128;per_row=6
    for flag in RULES:
        metric=dict(shape=lambda r:r['iou'],outside=lambda r:-r['outside'],unpainted=lambda r:-r['unpainted'],colour=lambda r:-r['colour_bad'],flat=lambda r:-r['flat'],
            key_green=lambda r:-r['green_pixels'],key_magenta=lambda r:-r['magenta_pixels'],empty=lambda r:-r['native_texels'])[flag]
        group=sorted((row for row in flagged if flag in row['flags'] and row['native_texels']>=48),key=metric)[:args.per_flag]
        if not group:continue
        # Evenly spread through the ranking as well, so the sheet is not only the extreme cases.
        sheet=Image.new('RGB',(per_row*cell*2,((len(group)+per_row-1)//per_row)*(cell+14)),(40,40,48));draw=ImageDraw.Draw(sheet)
        for index,row in enumerate(group):
            _,pixels,reference=analyse(row['binding'],keep=True);x=(index%per_row)*cell*2;y=(index//per_row)*(cell+14)
            scale=min((cell-4)/pixels.shape[1],(cell-4)/pixels.shape[0]);size=(max(1,round(pixels.shape[1]*scale)),max(1,round(pixels.shape[0]*scale)))
            a=Image.fromarray(reference).resize(size,Image.Resampling.NEAREST);b=Image.fromarray(pixels).resize(size,Image.Resampling.LANCZOS)
            sheet.paste(a,(x+2,y+2),a);sheet.paste(b,(x+cell+2,y+2),b)
            draw.text((x+2,y+cell),f"#{row['binding']} {row['atlas'][:16]} iou{row['iou']:.2f} c{row['colour_bad']:.2f}",fill=(230,230,230))
        sheet.save(out/f'{flag}.png')
    print(json.dumps({k:v for k,v in report.items() if k not in ('parts','by_atlas','by_resource','rules')},indent=1))
    for entry in report['by_atlas'][:30]:print(dict(entry))


if __name__=='__main__':main()
