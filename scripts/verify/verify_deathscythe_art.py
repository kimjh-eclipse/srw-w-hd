"""Inspect the three assembled parts from a real Deathscythe animation frame."""
from pathlib import Path
import sys,json,argparse
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_core import Core
import hd_parts

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--desired',type=Path,help='continuous painting used by this exact installed pose');parser.add_argument('--origin',type=int,nargs=2,default=[0,0],help='native canvas origin for an artwork including offscreen parts');args=parser.parse_args()
 out=ROOT/'test_current/parts/deathscythe';hd_parts.SCALE=4
 lib=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text())['bindings'];c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'isolated_saves');r=hd_parts.PartsRenderer()
 try:
  c.load(ROOT/'test_current/combat/duo_cutin_full.state')
  for _ in range(61):c.run();c.audio.clear()
  rows=c.parts.copy();active=[]
  for i,row in enumerate(rows):
   if row[0] and lib[int(row[0])-1].get('resource')==7108 and lib[int(row[0])-1]['y']==0 and lib[int(row[0])-1]['x']>=80:active.append(int(row[0]))
   else:rows[i]=0
  assert len(active)==3
  image=Image.new('RGBA',(1024,768));r.compose(image,rows,c.obj.raw,np.full((192,256),5,dtype='uint8'),np.zeros((192,256),dtype='uint8'),np.array([3]*6,dtype='uint8'),None,c.part_palettes,allow_native_fallback=True)
  image.save(out/'assembled_pose.png')
  desired=args.desired or out/'desired_continuous_pose.png'
  expected_image=Image.new('RGBA',image.size);expected_image.alpha_composite(Image.open(desired).convert('RGBA'),(args.origin[0]*4,args.origin[1]*4))
  expected=np.array(expected_image);actual=np.array(image)
  both=(expected[:,:,3]>224)&(actual[:,:,3]>224);diff=np.abs(actual[:,:,:3].astype('int16')-expected[:,:,:3])
  assert r.last_stats['drawn']==3 and r.last_stats['vanished']==0
  report=dict(scope='Isolated artwork/transform inspection from real frame 60; not whole-attack gameplay verification',desired=str(desired),bindings=active,stats=r.last_stats,opaque_overlap_pixels=int(both.sum()),mean_rgb_difference=float(diff[both].mean()),rgb_difference_p99=float(np.percentile(diff[both],99)))
  (out/'assembled_pose_report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
 finally:c.close();r.close()
if __name__=='__main__':main()
