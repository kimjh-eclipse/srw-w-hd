"""Repair artificial ink on proven internal OBJ crop cuts, without changing alpha.

A cut is proven only when opaque, similarly coloured native material continues
on the other side in the source atlas. Actual outlines and native panel ink
remain authoritative. Replacement RGB is sampled only from painted interiors.
"""
import numpy as np
from PIL import Image
POLICY='continuous-crop-ink-v1'
def repair_crop_ink(art,native_atlas,box):
 x,y,r,b=box;w,h=r-x,b-y
 native=np.asarray(native_atlas.convert('RGBA').crop((x-1,y-1,r+1,b+1)),dtype='int16')
 pixels=np.array(art.convert('RGBA'));changed=np.zeros(pixels.shape[:2],dtype=bool)
 def repair(view,mark,inside,outside,scale):
  if view.shape[1]<4 or scale<2:return
  count=min(view.shape[1]//3,max(1,round(scale*.5)))
  a=min(view.shape[1]-1,max(count,round(scale*.9)))
  z=min(view.shape[1]-1,max(a+1,round(scale*1.3)))
  continuous=(inside[:,3]>=250)&(outside[:,3]>=250)&(inside[:,:3].mean(1)>=90)&(np.max(np.abs(inside[:,:3]-outside[:,:3]),1)<=24)
  reference=np.asarray(Image.fromarray((continuous.astype('uint8')*255)[:,None]).resize((1,view.shape[0]),Image.Resampling.NEAREST))[:,0]>0
  first=view[:,a];second=view[:,z]
  interior=(first[:,3]>224)&(second[:,3]>224)&(first[:,:3].mean(1)>=80)&(second[:,:3].mean(1)>=80)
  ink=(view[:,:count,:3].max(2)<=64)&(view[:,:count,3]>192)&reference[:,None]&interior[:,None]
  color=((first[:,:3].astype('uint16')+second[:,:3].astype('uint16'))//2).astype('uint8')
  for col in range(count):
   mask=ink[:,col];view[mask,col,:3]=color[mask];mark[mask,col]=True
 repair(pixels,changed,native[1:-1,1],native[1:-1,0],art.width/w)
 repair(pixels[:,::-1],changed[:,::-1],native[1:-1,-2],native[1:-1,-1],art.width/w)
 repair(pixels.transpose(1,0,2),changed.T,native[1,1:-1],native[0,1:-1],art.height/h)
 repair(pixels[::-1].transpose(1,0,2),changed[::-1].T,native[-2,1:-1],native[-1,1:-1],art.height/h)
 return Image.fromarray(pixels),int(changed.sum())
