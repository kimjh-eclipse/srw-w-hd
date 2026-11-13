"""Connect every PAT rectangle of one reviewed, newly painted effect bank."""
import argparse,base64,hashlib,json,sys,zlib,shutil
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g

def main():
    p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');p.add_argument('--resource',type=int,default=21340);p.add_argument('--drawing',type=Path);args=p.parse_args()
    resource=args.resource;name=f'reviewed_effect_{resource}';folder=ROOT/'graphics/reviewed_effects';folder.mkdir(exist_ok=True)
    project=folder/f'{resource}_generated.png'
    if args.drawing:shutil.copy2(args.drawing,project)
    if not project.exists():raise FileNotFoundError('Supply --drawing for the reviewed atlas')
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    raw=lambda i:g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    indices=g.pixels(raw(resource));h,w=indices.shape;palette_id=next(i for i in range(resource-1,max(0,resource-32),-1) if raw(i)[:4]==b'PLT\0');palette=np.array(g.palette(raw(palette_id)),dtype='uint8')[:16,:3]
    art=Image.open(project).convert('RGBA');mask=np.asarray(art.getchannel('A').resize((w,h),Image.Resampling.BOX))>64;expected=indices!=0
    iou=float((mask&expected).sum()/(mask|expected).sum());assert iou>=.88,iou
    reference=Image.fromarray(np.dstack([palette[indices],expected.astype('uint8')*255]))
    path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text());before=hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True).encode()).hexdigest()
    plan=[r for r in json.loads((ROOT/'test_current/rom_catalog/animation_inventory.json').read_text())['parts'] if r['image']==resource]
    known={b['hash'] for b in meta['bindings'] if b.get('rgb_enabled',True) and not b.get('disabled')};blocked=set(meta.get('indexed_collision_keys',[]));added=[]
    for r in plan:
        a=indices[r['y']:r['y']+r['h'],r['x']:r['x']+r['w']];encoded=np.where(a,a.astype('uint16')|32768,0).astype('<u2');key=zlib.crc32(encoded.tobytes())^(r['w']<<16)^r['h'];assert key==r['index_hash']
        if any(b.get('atlas_id')==name and b.get('index_hash')==key for b in meta['bindings']):continue
        colors=np.rint(palette.astype('float64')*31/255).astype('uint16');native=colors[:,0]|colors[:,1]<<5|colors[:,2]<<10
        rgbhash=zlib.crc32(np.where(a,native[a]|32768,0).astype('<u2').tobytes())^(r['w']<<16)^r['h']
        meta['bindings'].append(dict(hash=rgbhash,rgb_enabled=rgbhash not in known,index_hash=key,indexed_safe=key not in blocked,dynamic_palette=True,original_palette_rgb=palette.tolist(),index_pixels=base64.b64encode(zlib.compress(a.tobytes())).decode(),x=r['x'],y=r['y'],w=r['w'],h=r['h'],atlas_id=name,resource=resource,source_x=r['x'],source_y=r['y'],registered_attack_bank=True,preserve_canonical_paint=True,reviewed_effect_bank=True))
        added.append(len(meta['bindings']));known.add(rgbhash)
    assert before==hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True).encode()).hexdigest()
    if args.apply:
        reference.save(folder/f'{resource}_native.png');art.resize((w*4,h*4),Image.Resampling.LANCZOS).save(folder/f'{resource}_hd.png')
        meta['atlases'][name]=dict(image=f'reviewed_effects/{resource}_hd.png',reference=f'reviewed_effects/{resource}_native.png',native_size=[w,h],lazy=True)
        temp=path.with_suffix('.tmp.json');temp.write_text(json.dumps(meta,indent=2),encoding='utf-8');temp.replace(path)
    report=dict(resource=resource,applied=args.apply,source_rectangles=len(plan),new_bindings=added,alpha_iou=iou,original_prefix_preserved=True,all_units_complete=False)
    (ROOT/'test_current/parts/reviewed_effect_bank.json').write_text(json.dumps(report,indent=2));print(report)
if __name__=='__main__':main()
