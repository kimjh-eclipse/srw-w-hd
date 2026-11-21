from pathlib import Path
import json,numpy as np
from PIL import Image
P=Path(__file__).parent;S=P.parent/'borrowed_shape_rework/lost_fx20050_thirteen'
line=Image.open(P/'generated_line_v2.png').convert('RGBA');a=np.array(line.getchannel('A'));yy,xx=np.where(a>=16);xmin,xmax=int(xx.min()),int(xx.max()+1);cut=(xmin+round((xmax-xmin)*.15),0,xmax-round((xmax-xmin)*.1),line.height);own=line.crop(cut);a=np.array(own.getchannel('A'));yy,xx=np.where(a>=16);bb=(int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1));part=own.crop(bb).resize((132,48),Image.Resampling.BICUBIC)
native=Image.open(S/'frame350_native.png').convert('RGBA');src=np.array(native.crop((25,5,58,17)).getchannel('A'))>0
def fit(mask,scale):
 yy=[];xx=[];ww=[]
 for y in range(max(1,mask.shape[0]//8),mask.shape[0]-max(1,mask.shape[0]//8)):
  x=np.flatnonzero(mask[y])
  if len(x):yy.append((y+.5)*scale);xx.append((float(x.min()+x.max())/2+.5)*scale);ww.append(len(x)*scale)
 a,b=np.polyfit(yy,xx,1);return float(a),float(b),float(np.median(ww))
na,nb,nw=fit(src,4);oa,ob,ow=fit(np.array(part.getchannel('A'))>=128,1);ratio=ow/nw;coeff=[ratio,oa-ratio*na,ob-ratio*nb,0,1,0];part=part.transform(part.size,Image.Transform.AFFINE,coeff,Image.Resampling.BICUBIC)
master=Image.open(P/'generated_master350.png').convert('RGBA');master.paste((0,0,0,0),(100,20,232,68));master.alpha_composite(part,(100,20));master.save(P/'generated_master350_v3.png');art=Image.new('RGBA',(384,64));art.alpha_composite(master.crop((0,0,128,32)),(0,0));art.alpha_composite(master.crop((128,12,256,76)),(256,0));art.save(P/'candidate_atlas_v3.png');Image.alpha_composite(Image.new('RGBA',master.size,(65,65,70,255)),master).resize((1024,304)).convert('RGB').save(P/'master350_v3_gray.png');(P/'main_v3_geometry.json').write_text(json.dumps(dict(own_generated_crop=cut,own_inner_bbox=bb,native_bbox_geometry=[25,5,58,17],affine=coeff,native_width=nw,own_width=ow,native_pixels_or_alpha_copied=False,alpha_threshold_for_bbox_only=16),indent=2))
