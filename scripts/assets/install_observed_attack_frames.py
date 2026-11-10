"""Register a verified painted hardware fragment without accepting its whole bank."""
import argparse,base64,json,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from painted_edges import clean_alpha

def prepare_extra_references():
    records=json.loads((ROOT/'test_current/parts/observed_attack_gaps/report.json').read_text())
    folder=ROOT/'test_current/parts/remaining_fragments';folder.mkdir(exist_ok=True);items=[]
    for row in records['unmatched_rectangles']:
        candidates=[c for c in row['candidates'] if c['resource'] in (1775,11202)]
        if not candidates:continue
        path=ROOT/f'test_current/combat/named_attacks/unit_{row["unit_id"]}/unit_{row["unit_id"]}_weapon_{row["weapon_id"]}_unknown.npz'
        with np.load(path) as data:
            found=next(((r.copy(),p.copy(),pal.copy()) for r,p,pal in zip(data['rows'],data['pixels'],data['palettes']) if int(r[0])==row['index_hash']),None)
        if found is None:continue
        raw,pixels,palette=found;w,h=map(int,raw[1:3]);a=pixels[:w*h].reshape(h,w)
        q=palette.astype('uint32');rgb=np.stack([(q&31)*255//31,((q>>5)&31)*255//31,((q>>10)&31)*255//31],-1).astype('uint8')
        rgba=np.dstack([rgb[a],(a!=0).astype('uint8')*255]);rgba[a==0]=0
        Image.fromarray(rgba).resize((w*8,h*8),Image.Resampling.NEAREST).save(folder/f'{row["index_hash"]}.png')
        items.append(dict(resource=candidates[0]['resource'],index_hash=row['index_hash'],native_material_hash=int(raw[7]),rgb_hash=int(raw[6]),unit_id=row['unit_id'],weapon_id=row['weapon_id'],w=w,h=h,index_pixels=base64.b64encode(zlib.compress(a.tobytes())).decode('ascii'),palette_native=palette.tolist(),name=f'observed_{row["index_hash"]}',source=f'fragment_{row["index_hash"]}_generated.png'))
    library=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text())
    original=next(b for b in library['bindings'] if b.get('atlas_id')=='rouge_connector')
    rgb=np.asarray(original['original_palette_rgb'],dtype='float64');q=np.rint(rgb*31/255).astype('uint16');palette=q[:,0]|q[:,1]<<5|q[:,2]<<10
    items.insert(0,dict(resource=7656,index_hash=original['index_hash'],native_material_hash=2221642217,rgb_hash=original['hash'],unit_id=39,weapon_id=165,w=32,h=16,index_pixels=original['index_pixels'],palette_native=palette.tolist(),name='rouge_connector',source='rouge_connector_generated.png'))
    destination=ROOT/'graphics/named_attack_frames/observed_plan.json'
    prior={r['index_hash']:r for r in json.loads(destination.read_text())['items']} if destination.exists() else {}
    for item in items:
        item['style_approved']=item['name']=='rouge_connector'
        for key in ('source','style_approved'):
            if key in prior.get(item['index_hash'],{}):item[key]=prior[item['index_hash']][key]
    destination.write_text(json.dumps(dict(items=items),indent=2));print('Saved exact fragment inputs:',len(items))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');parser.add_argument('--prepare-extras',action='store_true');args=parser.parse_args()
    if args.prepare_extras:return prepare_extra_references()
    folder=ROOT/'graphics/named_attack_frames'
    path=ROOT/'graphics/kazuma_parts_library.json';library=json.loads(path.read_text());rows=[]
    for item in json.loads((folder/'observed_plan.json').read_text())['items']:
        if not (folder/item['source']).exists():rows.append(dict(index_hash=item['index_hash'],accepted=False,reason='drawing pending'));continue
        w,h=item['w'],item['h'];indices=np.frombuffer(zlib.decompress(base64.b64decode(item['index_pixels'])),dtype='uint8').reshape(h,w);expected=indices!=0
        encoded=np.where(indices,indices.astype('uint16')|0x8000,0).astype('<u2')
        assert zlib.crc32(encoded.tobytes())^(w<<16)^h==item['index_hash']
        source=clean_alpha(Image.open(folder/item['source']).convert('RGBA'))
        gy,gx=np.where(np.asarray(source)[:,:,3]>64);ys,xs=np.where(expected)
        if not len(gx):rows.append(dict(index_hash=item['index_hash'],accepted=False,reason='empty drawing'));continue
        box=(int(gx.min()),int(gy.min()),int(gx.max()+1),int(gy.max()+1));target=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1))
        scale=8;dest=tuple(v*scale for v in target);art=Image.new('RGBA',(w*scale,h*scale))
        art.paste(source.crop(box).resize((dest[2]-dest[0],dest[3]-dest[1]),Image.Resampling.LANCZOS),dest[:2])
        mask=np.asarray(art.getchannel('A').resize((w,h),Image.Resampling.BOX))>64
        iou=float((mask&expected).sum()/max(1,(mask|expected).sum()))
        style_approved=bool(item.get('style_approved'))
        row=dict(resource=item['resource'],index_hash=item['index_hash'],alpha_iou=iou,geometry_accepted=iou>=.82,style_approved=style_approved,accepted=iou>=.82 and style_approved,unit_id=item['unit_id'],weapon_id=item['weapon_id']);rows.append(row)
        if not args.apply or not row['accepted']:continue
        palette=np.asarray(item['palette_native'],dtype='uint16')
        colors=palette.astype('uint32');rgb=np.stack([(colors&31)*255//31,((colors>>5)&31)*255//31,((colors>>10)&31)*255//31],-1).astype('uint8')
        native=np.dstack([rgb[indices],expected.astype('uint8')*255]);native[~expected]=0
        rgba=np.array(art);rgba[rgba[:,:,3]==0]=0;art=Image.fromarray(rgba)
        name=item['name'];image=f'named_attack_frames/{name}_hd.png';reference=f'named_attack_frames/{name}_native.png'
        art.save(ROOT/'graphics'/image,optimize=True);Image.fromarray(native).save(ROOT/'graphics'/reference)
        library['atlases'][name]=dict(image=image,reference=reference,native_size=[w,h],lazy=True)
        if not any(b.get('atlas_id')==name for b in library['bindings']):
            library['bindings'].append(dict(hash=item['rgb_hash'],index_hash=item['index_hash'],rgb_enabled=True,indexed_safe=True,dynamic_palette=True,original_palette_rgb=rgb.tolist(),index_pixels=item['index_pixels'],x=0,y=0,w=w,h=h,atlas_id=name,resource=item['resource'],source_x=0,source_y=0,named_attack_frame=True,observed_native_rectangle=True,auto_shared_attack=True))
    if args.apply:
        temporary=path.with_suffix('.tmp.json');temporary.write_text(json.dumps(library,indent=2));temporary.replace(path)
    report=dict(applied=args.apply,rows=rows,whole_resources_verified=False)
    (folder/('observed_registration.json' if args.apply else 'observed_review.json')).write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
