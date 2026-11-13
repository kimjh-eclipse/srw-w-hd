"""Bake a continuous stance back through its three original OAM transforms."""
from pathlib import Path
import sys,json,struct
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_core import Core

def main():
 folder=ROOT/'graphics/rework_deathscythe';out=ROOT/'test_current/parts/deathscythe';scale=4
 lib=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text())['bindings'];native=Image.open(folder/'attack_7108_native.png').convert('RGBA')
 c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'isolated_saves')
 rows=[];union=Image.new('RGBA',(1024,768))
 try:
  c.load(ROOT/'test_current/combat/duo_cutin_full.state')
  for _ in range(61):c.run();c.audio.clear()
  for i,row in enumerate(c.parts):
   if not row[0]:continue
   b=lib[int(row[0])-1]
   if b.get('resource')!=7108 or b['y']!=0 or b['x']<80:continue
   a,attr,_,=map(int,row[1:4]);w,h=b['w'],b['h'];x=attr&511;y=a&255;x=x if x<256 else x-512;y=y if y<192 else y-256
   assert a&256
   idx=(attr>>9)&31;pa,pb,pc,pd=[struct.unpack_from('<h',c.obj.raw,(idx*4+k)*8+6)[0]/256 for k in range(4)]
   fw=w*(2 if a&512 else 1);fh=h*(2 if a&512 else 1)
   offset=np.array([w/2-fw/2*pa-fh/2*pb,h/2-fw/2*pc-fh/2*pd]);matrix=np.array([[pa,pb],[pc,pd]])
   crop=native.crop((b['x'],0,b['x']+w,h)).resize((w*4,h*4),Image.Resampling.NEAREST)
   posed=crop.transform((fw*4,fh*4),Image.Transform.AFFINE,(pa,pb,offset[0]*4,pc,pd,offset[1]*4),Image.Resampling.NEAREST)
   union.alpha_composite(posed,(x*4,y*4))
   rows.append(dict(slot=i,binding=int(row[0]),x=x,y=y,w=w,h=h,source_x=b['x'],matrix=matrix.tolist(),offset=offset.tolist()))
 finally:c.close()
 assert len(rows)==3,len(rows)
 bbox=union.getbbox();union.save(out/'native_pose_contract.png')
 corrected=folder/'pose_continuous_generated.png'
 if corrected.exists():
  piece=Image.open(corrected).convert('RGBA');piece=piece.crop(piece.getbbox())
 else:
  gen=Image.open(folder/'attack_7108_generated.png').convert('RGBA');piece=gen.crop((round(gen.width/3),0,gen.width,round(gen.height*2/3)));piece=piece.crop(piece.getbbox())
 # Keep the helmet within its central OAM output window. The wing tips
 # can start at y=0, but the central doubled-height OBJ starts lower.
 head=next(r for r in rows if r['w']==32);fitbox=list(bbox)
 for attempt in range(6):
  desired=Image.new('RGBA',(1024,768));desired.alpha_composite(piece.resize((fitbox[2]-fitbox[0],fitbox[3]-fitbox[1]),Image.Resampling.LANCZOS),fitbox[:2])
  center=desired.getchannel('A').crop((head['x']*4,0,(head['x']+head['w']*2)*4,768)).getbbox()
  missing=head['y']*4+4-center[1]
  if missing<=0:break
  fitbox[1]+=missing
 desired.save(out/'desired_continuous_pose.png')
 atlas=Image.open(folder/'attack_7108_hd.png').convert('RGBA')
 for r in rows:
  inverse=np.linalg.inv(np.array(r['matrix']));shift=np.array([r['x'],r['y']])-inverse@np.array(r['offset'])
  coeff=(inverse[0,0],inverse[0,1],shift[0]*4,inverse[1,0],inverse[1,1],shift[1]*4)
  source=desired.transform((r['w']*4,r['h']*4),Image.Transform.AFFINE,coeff,Image.Resampling.BICUBIC)
  atlas.paste(source,(r['source_x']*4,0))
 atlas.save(folder/'attack_7108_hd.png',optimize=True)
 (out/'pose_inverse_registration.json').write_text(json.dumps(dict(reference_frame=60,screen_bbox=bbox,fitted_bbox=fitbox,parts=rows,scope='One stance authored continuously, inverse-baked to the original three OAM pieces; normal animation still uses those pieces.'),indent=2))
 print('Inverse-baked',len(rows),'parts',bbox)
if __name__=='__main__':main()
