"""Find HD parts whose painted colours do not follow the native tile's palette slots.

A part painted for one palette is recoloured at run time when the game shows
it with another: every HD pixel is assigned a palette slot and takes that
slot's live colour. Where the painting put a colour on a spot whose native
texel uses a different slot (an orange highlight on a red fin), the pixel
follows the wrong slot and turns into whatever that slot holds in the other
palette (the eye's green). This tool measures that for every baked part.

For each part it compares the slot the renderer assigns to each opaque HD
pixel with the slots of the native texels around it (3x3, so painted edges
and antialiasing are tolerated), then recolours the part with the other
palettes the same tile shape is known to appear with and counts pixels that
end up far from what the native texel would show.

Reads only. Writes test_current/parts/palette_alignment/.
"""
import argparse,base64,json,sys,zlib
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image,ImageDraw

_renderer=None;_variants=None


def palette_of(spec,name):
    value=spec.get(name)
    if value is None:return None
    palette=np.asarray(value,dtype='float32')
    return palette if palette.ndim==2 and len(palette)>=2 else None


def native_map(renderer,binding,spec):
    if spec.get('index_pixels'):return np.frombuffer(zlib.decompress(base64.b64decode(spec['index_pixels'])),dtype='uint8').reshape(spec['h'],spec['w'])
    found=renderer.native_material_indices(binding,spec)
    if found is not None:return found
    # No stored slot map: rebuild it from the atlas's native reference picture.
    # A texel whose colour is in the palette once gives its slot; a colour held
    # by several slots is ambiguous, so the whole part is left unmeasured.
    palette=palette_of(spec,'original_palette_rgb');atlas=renderer.atlas_specs.get(spec.get('atlas_id','base'))
    if palette is None or atlas is None or not atlas.get('native_size'):return None
    references=renderer.__dict__.setdefault('audit_references',{});name=atlas['reference']
    if name not in references:
        if len(references)>6:references.clear()
        with Image.open(ROOT/'graphics'/name) as opened:picture=opened.convert('RGBA')
        if picture.size!=tuple(atlas['native_size']):picture=picture.resize(tuple(atlas['native_size']),Image.Resampling.NEAREST)
        references[name]=np.asarray(picture)
    crop=references[name][spec['y']:spec['y']+spec['h'],spec['x']:spec['x']+spec['w']]
    if crop.shape[:2]!=(spec['h'],spec['w']):return None
    five=lambda colours:np.rint(np.asarray(colours,dtype='float32')*31/255).astype('uint32');pack=lambda c:c[...,0]|c[...,1]<<5|c[...,2]<<10
    codes=pack(five(crop[:,:,:3]));slots=pack(five(palette[1:]));order=np.argsort(slots);ordered=slots[order]
    # A colour held by several slots resolves to the first of them; analyse()
    # treats slots of equal colour as interchangeable.
    position=np.clip(np.searchsorted(ordered,codes,side='left'),0,len(ordered)-1);match=ordered[position]==codes
    result=np.where(match&(crop[:,:,3]>0),order[position]+1,0).astype('uint8')
    visible=crop[:,:,3]>0
    if visible.any() and np.count_nonzero(result[visible]==0)>visible.sum()*.02:return None
    return result


def start():
    global _renderer,_variants
    from hd_parts import PartsRenderer
    _renderer=PartsRenderer(async_prepare=False);_variants=defaultdict(dict)
    # Every palette a tile shape is catalogued with: the colour sets a part may be recoloured to.
    for spec in _renderer.bindings:
        shape=spec.get('index_hash')
        if shape is None:continue
        for name in ('original_palette_rgb','palette_rgb'):
            palette=palette_of(spec,name)
            if palette is not None and len(palette)==16:_variants[shape][palette.tobytes()]=palette


def analyse(binding,keep_pixels=False):
    renderer=_renderer;spec=renderer.bindings[binding-1];native=native_map(renderer,binding,spec)
    source=palette_of(spec,'palette_source_rgb')
    if source is None:source=palette_of(spec,'original_palette_rgb')
    if native is None or source is None or len(source)!=16:return None
    found=renderer.disk_cache.get(renderer.texture_key(binding,spec['w'],spec['h']))
    if found is None:return None
    art=found[0];pixels=np.asarray(art);opaque=pixels[:,:,3]>=128;total=int(opaque.sum())
    if total<16:return None
    residual,slots=renderer.material_map(binding,art,source,spec);renderer.material_maps.clear()
    # Slots present in the 3x3 native neighbourhood of each texel, as a bit set.
    same=np.array([sum(1<<j for j in range(16) if np.array_equal(source[j],source[i])) for i in range(16)],dtype='uint16')
    bits=same[np.minimum(native,15)];padded=np.pad(bits,1);around=np.zeros_like(bits)
    for dy in range(3):
        for dx in range(3):around|=padded[dy:dy+native.shape[0],dx:dx+native.shape[1]]
    size=art.size;upscale=lambda array:np.asarray(Image.fromarray(array.astype('int32')).resize(size,Image.Resampling.NEAREST))
    allowed=upscale(around).astype('uint32');inside=(allowed&~np.uint32(1))!=0
    misplaced=opaque&inside&(((allowed>>slots.astype('uint32'))&1)==0)
    outside=opaque&~inside
    # The native slot under each HD pixel (transparent texels take a neighbour's slot).
    grown=np.asarray(Image.fromarray(native).filter(__import__('PIL.ImageFilter',fromlist=['MaxFilter']).MaxFilter(3)));under=upscale(np.where(native!=0,native,grown))
    worst=0;worst_palette=None;worst_mask=None
    for key,palette in list(_variants.get(spec.get('index_hash'),{}).items())[:12]:
        if np.array_equal(palette,source):continue
        difference=np.abs(palette[slots]-palette[under]).max(2)
        wrong=misplaced&(difference>=72);count=int(wrong.sum())
        if count>worst:worst=count;worst_palette=palette;worst_mask=wrong
    used=np.unique(native);used=used[used>0]
    row=dict(binding=binding,atlas=spec.get('atlas_id','base'),resource=spec.get('resource'),w=spec['w'],h=spec['h'],x=spec['x'],y=spec['y'],opaque_pixels=total,
        misplaced_share=round(int(misplaced.sum())/total,4),outside_share=round(int(outside.sum())/total,4),
        slots_never_native=sorted(int(v) for v in np.unique(slots[opaque&inside]) if v not in used and v>0),
        variants=max(0,len(_variants.get(spec.get('index_hash'),{}))-1),wrong_colour_share=round(worst/total,4),wrong_colour_pixels=worst)
    if keep_pixels:
        recoloured=None
        if worst_palette is not None:
            rgb=np.clip(np.rint(worst_palette[slots]+residual),0,255).astype('uint8');recoloured=np.dstack([rgb,pixels[:,:,3]])
        return row,pixels,misplaced,recoloured,worst_mask
    return row


def work(binding):
    try:return analyse(binding)
    except Exception as error:return dict(binding=binding,error=str(error))


def main():
    parser=argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--workers',type=int,default=6);parser.add_argument('--bindings',type=int,nargs='*',help='only these parts (prints each row)')
    parser.add_argument('--sheets',type=int,default=200);parser.add_argument('--limit',type=int,default=0)
    args=parser.parse_args()
    out=ROOT/'test_current/parts/palette_alignment';out.mkdir(parents=True,exist_ok=True)
    start()
    if args.bindings:
        for binding in args.bindings:print(json.dumps(analyse(binding)))
        return
    for old in out.glob('*'):
        if old.is_file():old.unlink()
    todo=[];seen=set()
    for binding,spec in enumerate(_renderer.bindings,1):
        if spec.get('source_binding') or spec.get('runtime_texture') or spec.get('disabled') or not spec.get('dynamic_palette'):continue
        key=_renderer.texture_key(binding,spec['w'],spec['h'])
        if key in seen:continue
        seen.add(key);todo.append(binding)
    if args.limit:todo=todo[::max(1,len(todo)//args.limit)]
    rows=[];errors=0;skipped=0
    with Pool(args.workers,initializer=start) as pool:
        for done,row in enumerate(pool.imap_unordered(work,todo,chunksize=64),1):
            if row is None:skipped+=1
            elif 'error' in row:errors+=1
            else:rows.append(row)
            if done%5000==0:print(done,'/',len(todo),flush=True)
    rows.sort(key=lambda row:(-row['wrong_colour_pixels'],-row['misplaced_share']))
    flagged=[row for row in rows if row['wrong_colour_share']>=.02 and row['wrong_colour_pixels']>=24]
    by_atlas=defaultdict(lambda:dict(parts=0,flagged=0,wrong_pixels=0));by_resource=defaultdict(lambda:dict(flagged=0,wrong_pixels=0,atlases=set()))
    for row in rows:by_atlas[row['atlas']]['parts']+=1
    for row in flagged:
        entry=by_atlas[row['atlas']];entry['flagged']+=1;entry['wrong_pixels']+=row['wrong_colour_pixels']
        entry=by_resource[row['resource']];entry['flagged']+=1;entry['wrong_pixels']+=row['wrong_colour_pixels'];entry['atlases'].add(row['atlas'])
    shares=sorted(row['misplaced_share'] for row in rows)
    report=dict(measured=len(rows),skipped_no_native_map_or_art=skipped,errors=errors,with_other_palettes=sum(row['variants']>0 for row in rows),
        flagged=len(flagged),flag_rule='another known palette turns >=2% and >=24 opaque pixels into a colour >=72/255 away from the native texel colour',
        misplaced_share_median=shares[len(shares)//2] if shares else None,misplaced_share_p90=shares[int(len(shares)*.9)] if shares else None,
        parts_using_slots_native_never_uses=sum(bool(row['slots_never_native']) for row in rows),
        by_atlas=sorted(({'atlas':k,**v} for k,v in by_atlas.items() if v['flagged']),key=lambda e:-e['wrong_pixels']),
        by_resource=sorted(({'resource':k,'flagged':v['flagged'],'wrong_pixels':v['wrong_pixels'],'atlases':sorted(v['atlases'])} for k,v in by_resource.items()),key=lambda e:-e['wrong_pixels']),
        flagged_parts=flagged,misplaced_without_known_variant=[row for row in rows if row['variants']==0 and row['misplaced_share']>=.15][:2000])
    (out/'report.json').write_text(json.dumps(report,indent=1),encoding='utf-8')
    cell=150;per_row=4;per_sheet=per_row*5
    for start_index in range(0,min(len(flagged),args.sheets),per_sheet):
        group=flagged[start_index:start_index+per_sheet];sheet=Image.new('RGB',(per_row*cell*3,((len(group)+per_row-1)//per_row)*(cell+14)),(40,40,48));draw=ImageDraw.Draw(sheet)
        for index,row in enumerate(group):
            _,pixels,misplaced,recoloured,wrong=analyse(row['binding'],keep_pixels=True);marked=pixels.copy()
            if wrong is not None:marked[wrong]=(255,0,255,255)
            x=(index%per_row)*cell*3;y=(index//per_row)*(cell+14);scale=min((cell-4)/pixels.shape[1],(cell-4)/pixels.shape[0])
            for offset,array in ((0,pixels),(cell,recoloured if recoloured is not None else pixels),(cell*2,marked)):
                tile=Image.fromarray(array).resize((max(1,round(pixels.shape[1]*scale)),max(1,round(pixels.shape[0]*scale))),Image.Resampling.NEAREST);sheet.paste(tile,(x+offset+2,y+2),tile)
            draw.text((x+2,y+cell),f"#{row['binding']} r{row['resource']} {row['atlas']} wrong {row['wrong_colour_share']:.0%}",fill=(230,230,230))
        sheet.save(out/f'sheet_{start_index//per_sheet:02d}.png')
    print(json.dumps({k:v for k,v in report.items() if k not in ('by_atlas','by_resource','flagged_parts','misplaced_without_known_variant')},indent=1))
    for entry in report['by_atlas'][:25]:print(entry)


if __name__=='__main__':main()
