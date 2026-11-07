"""Pose artwork follows the live positions of the original OBJ components."""
import json,struct
from collections import OrderedDict
import numpy as np
from PIL import Image
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
SCALE=1440/256

class RobotAnimator:
    def __init__(self):
        self.sources=json.loads((ROOT/'graphics/kazuma_robot_animation.json').read_text())['sources']
        self.images={};self.cache=OrderedDict()
        for pose,name in [(1,'idle'),(2,'attack'),(3,'windup'),(4,'raise'),(5,'dash'),(6,'dash_raise')]:
            im=Image.open(ROOT/f'graphics/kazuma_robot_{name}_hd.png').convert('RGBA');im=im.crop(im.getbbox())
            box=self.sources[str(pose)]['box'];size=(round((box[2]-box[0])*SCALE),round((box[3]-box[1])*SCALE))
            self.images[pose]=im.resize(size,Image.Resampling.LANCZOS)

    def frame(self,robot,oam):
        pose,origin_x,origin_y=robot[:3];src=self.sources[str(pose)];box=src['box'];image=self.images[pose]
        current=[]
        if oam:
            for i in range(128):
                a,b,c,_=struct.unpack_from('<4H',oam,i*8)
                if a&256 or a&512 or c>>12:continue
                x=b&511;y=a&255
                if x>=256:x-=512
                if y>=192:y-=256
                current.append(((a&0xff00,b&0xfe00,c),x-origin_x,y-origin_y))
        key=(pose,tuple(current))
        if key in self.cache:
            self.cache.move_to_end(key);return self.cache[key]
        pad=round(20*SCALE);size=(image.width+pad*2,image.height+pad*2)
        padded=Image.new('RGBA',size);padded.paste(image,(pad,pad))
        targets=[];deltas=[];used=set()
        for e in src['parts']:
            part_key=(e['a']&0xff00,e['b']&0xfe00,e['c'])
            cx,cy=e['center'];sx=e['x']-box[0];sy=e['y']-box[1]
            candidates=[(j,x,y) for j,(k,x,y) in enumerate(current) if k==part_key and j not in used]
            if not candidates:continue
            j,tx,ty=min(candidates,key=lambda item:(item[1]-sx)**2+(item[2]-sy)**2);used.add(j)
            if abs(tx-sx)>40 or abs(ty-sy)>40:continue
            targets.append([(tx+cx)*SCALE+pad,(ty+cy)*SCALE+pad]);deltas.append([(sx-tx)*SCALE,(sy-ty)*SCALE])
        if len(targets)>=3 and np.max(np.abs(deltas))>.01:
            # Inverse-distance displacement at shared mesh vertices keeps each
            # original limb movement while avoiding seams between mesh cells.
            xs=np.unique(np.r_[np.arange(0,size[0],24),size[0]]);ys=np.unique(np.r_[np.arange(0,size[1],24),size[1]])
            xx,yy=np.meshgrid(xs,ys);points=np.stack([xx.ravel(),yy.ravel()],-1).astype(float)
            target=np.asarray(targets);delta=np.clip(np.asarray(deltas),-3*SCALE,3*SCALE)
            dist2=((points[:,None,:]-target[None,:,:])**2).sum(-1)
            # Artwork and native component silhouettes differ. Keep motion
            # small and spatially smooth so armor plates cannot fold or melt.
            weights=1/(dist2+48**2)**2;field=points+(weights@delta)/weights.sum(1)[:,None]
            field=field.reshape(len(ys),len(xs),2);mesh=[]
            for row in range(len(ys)-1):
                for col in range(len(xs)-1):
                    rect=(int(xs[col]),int(ys[row]),int(xs[col+1]),int(ys[row+1]))
                    quad=tuple(np.concatenate([field[row,col],field[row+1,col],field[row+1,col+1],field[row,col+1]]))
                    mesh.append((rect,quad))
            padded=padded.transform(size,Image.Transform.MESH,mesh,Image.Resampling.BICUBIC)
        value=(padded,pad)
        self.cache[key]=value
        while len(self.cache)>64:self.cache.popitem(last=False)
        return value
