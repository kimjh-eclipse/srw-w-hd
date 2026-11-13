"""Align and connect all pieces from newly painted Deathscythe IMG7108."""
import argparse,hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
CELLS=[('small_pose',(0,0,80,32)),('fragment_0',(16,32,28,44)),('fragment_1',(32,32,50,64)),('fragment_2',(50,32,66,64)),('fragment_3',(66,32,80,64)),('fragment_4',(0,52,32,64)),('large_pose',(80,0,240,64)),('slash_0',(0,64,64,96)),('slash_1',(64,64,128,96)),('slash_2',(128,64,192,96)),('slash_3',(192,64,240,84)),('slash_4',(192,84,240,96))]
def main():
 p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');args=p.parse_args()
 folder=ROOT/'graphics/rework_deathscythe';out=ROOT/'test_current/parts/deathscythe';out.mkdir(parents=True,exist_ok=True)
 reference=Image.open(folder/'attack_7108_native.png').convert('RGBA');generated=Image.open(folder/'attack_7108_generated.png').convert('RGBA')
 aligned=Image.new('RGBA',(960,384));rows=[]
 for name,box in CELLS:
  native=reference.crop(box);expected=native.getchannel('A').point(lambda a:255 if a>64 else 0).getbbox();assert expected,name
  crop=generated.crop(tuple(round(v*generated.size[i%2]/reference.size[i%2]) for i,v in enumerate(box)))
  bbox=crop.getchannel('A').point(lambda a:255 if a>64 else 0).getbbox();assert bbox,name
  target=tuple((box[i%2]+v)*4 for i,v in enumerate(expected));piece=crop.crop(bbox).resize((target[2]-target[0],target[3]-target[1]),Image.Resampling.LANCZOS)
  aligned.alpha_composite(piece,target[:2]);rows.append(dict(name=name,cell=list(box),source_bbox=list(bbox),target_bbox=list(target)))
 rgba=np.array(aligned);rgba[rgba[:,:,3]==0]=0;aligned=Image.fromarray(rgba)
 expected=np.array(reference.getchannel('A'))>64;actual=np.array(aligned.getchannel('A').resize(reference.size,Image.Resampling.BOX))>64
 for row in rows:
  l,t,r,b=row['cell'];e=expected[t:b,l:r];a=actual[t:b,l:r];row['alpha_iou']=round(float((e&a).sum()/max(1,(e|a).sum())),5)
 aligned.save(out/'atlas_layout_preview.png',optimize=True)
 if args.apply:aligned.save(folder/'attack_7108_hd.png',optimize=True)
 path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text(encoding='utf-8'));prefix=hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True).encode()).hexdigest();changed=[]
 for identifier,b in enumerate(meta['bindings'],1):
  if b.get('resource')!=7108:continue
  assert identifier>5263
  x,y=b['source_x'],b['source_y'];assert 0<=x<x+b['w']<=240 and 0<=y<y+b['h']<=96
  b.update(atlas_id='deathscythe_7108_reviewed',x=x,y=y,registered_attack_bank=True,preserve_canonical_paint=True,paint_review_source='rework_deathscythe/attack_7108_generated.png');changed.append(identifier)
 assert len(changed)==110,len(changed)
 assert prefix==hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True).encode()).hexdigest()
 if args.apply:
  meta['atlases']['deathscythe_7108_reviewed']=dict(image='rework_deathscythe/attack_7108_hd.png',reference='rework_deathscythe/attack_7108_native.png',native_size=[240,96],lazy=True)
  tmp=path.with_suffix('.tmp.json');tmp.write_text(json.dumps(meta,indent=2),encoding='utf-8');tmp.replace(path)
  if (folder/'pose_continuous_generated.png').exists():
   from scripts.assets.fit_deathscythe_pose import main as fit
   fit()
 report=dict(resource=7108,all_source_bindings=changed,cells=rows,applied=args.apply,gameplay_verified=False,native_alpha_stamped=False,native_pixel_fill=False)
 (out/'registration.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(dict(bindings=len(changed),applied=args.apply,cells=rows)))
if __name__=='__main__':main()
