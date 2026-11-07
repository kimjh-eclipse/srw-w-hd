"""Small pre-sized menu textures, composed with their painted alpha contours."""
import json
from collections import Counter
from pathlib import Path
import numpy as np
from PIL import Image
from menu_texture_cache import open_database,load_texture
from render_resolution import DEFAULT_WIDTH

ROOT=Path(__file__).resolve().parent.parent
SCALE=DEFAULT_WIDTH/256

class MenuScene:
    def __init__(self,parts_renderer=None):
        self.folder=ROOT/'graphics/menu_units';self.art={};self.last_scene=None;self.grid_native={};self.width=DEFAULT_WIDTH
        self.parts_renderer=parts_renderer
        self.texture_database=open_database()
        self.spec=json.loads((self.folder/'scene_runtime.json').read_text()) if (self.folder/'scene_runtime.json').exists() else None

    def load(self,names):
        for name in names:
            if name not in self.art:
                art,_=load_texture(self.spec['images'][name],self.width,self.texture_database)
                self.art[name]=art

    def identify(self,rows,parts):
        if not self.spec:return None
        if {7,8}<={int(row[0]) for row in rows or []}:return 'introduction'
        if parts is not None and sum(int(row[0]) in self.spec['favorite_bindings'] for row in parts)>=20:return 'favorite'
        return None

    def grid(self,top,rows):
        positions={int(row[0]):row[1:3] for row in rows or []}
        key=tuple(positions.get(i,(0,0)) for i in (9,10))
        if getattr(self,'grid_key',None)!=key:
            samples=[]
            for name,bid in [('grid_front',9),('grid_back',10)]:
                if name not in self.grid_native:self.grid_native[name]=np.asarray(self.art[name].resize((256,256),Image.Resampling.NEAREST))
                x,y=positions.get(bid,(0,0));pixels=self.grid_native[name]
                samples.append(pixels[(np.arange(192)+y)%256][:,(np.arange(256)+x)%256])
            front,back=samples;back_rgb=np.where(back[:,:,3:4]>0,back[:,:,:3],0);rgb=back_rgb.copy();mask=front[:,:,3]>0
            rgb[mask]=np.minimum(255,(front[:,:,:3].astype('uint16')*15+back_rgb.astype('uint16')*5)//16)[mask].astype('uint8')
            self.grid_image=Image.fromarray(rgb).resize(top.size,Image.Resampling.NEAREST);self.grid_key=key
        top.paste(self.grid_image,(0,0))

    def compose(self,top,native,rows,parts,oam):
        self.last_scene=None
        if not self.spec:return parts
        scene=self.identify(rows,parts);introduction=scene=='introduction'
        if scene is None:return parts
        names=['grid_back','grid_front']+(['aircraft','kazuma'] if introduction else [g['name'] for g in self.spec['groups']])
        panel_y=top.height*5//6
        self.load(names);panel=top.crop((0,panel_y,top.width,top.height)) if not introduction else None;self.grid(top,rows)
        if introduction:
            for name in ('aircraft','kazuma'):
                art=self.art[name];top.paste(art,(0,0),art)
            self.last_scene='introduction';return parts
        attrs=np.frombuffer(oam,dtype='<u2').reshape(128,4)
        menu_rows=[]
        for i,(a,b,c,_) in enumerate(attrs):
            a,b,c=map(int,(a,b,c))
            if (not a&256 and a&512) or a>>14==3 or (a>>10)&3>=2:continue
            if c>>12>8:continue
            menu_rows.append((i,a,b,c))
        group_key=(tuple(menu_rows),tuple(int(row[0]) for row in parts),self.parts_renderer.ready_generation if self.parts_renderer else 0)
        if getattr(self,'group_key',None)!=group_key:
            if hasattr(top,'ops'):
                from gpu_surface import Surface
                self.group_overlay=Surface(top.size)
            else:self.group_overlay=Image.new('RGBA',top.size)
            tasks=[]
            for group in self.spec['groups']:
                rows=[row for row in menu_rows if row[3]>>12==group['bank']]
                if not rows:continue
                offsets={p['binding']:(p['x'],p['y']) for p in group['offsets']};votes=Counter()
                for i,a,b,c in rows:
                    binding=int(parts[i,0]);offset=offsets.get(binding)
                    if offset is None:continue
                    x=b&511;y=a&255
                    if x>=256:x-=512
                    if y>=192:y-=256
                    votes[x-offset[0],y-offset[1]]+=1
                if votes:
                    (x,y),_=votes.most_common(1)[0]
                else:
                    # Alternate PAT rectangles still share the fixed palette
                    # bank. Use their live bounds rather than fixed OAM slots.
                    points=[((b&511) if b&511<256 else (b&511)-512,(a&255) if a&255<192 else (a&255)-256) for i,a,b,c in rows]
                    x=min(p[0] for p in points)-group['bounds'][0];y=min(p[1] for p in points)-group['bounds'][1]
                priority=min((c>>10)&3 for i,a,b,c in rows);order=min(i for i,a,b,c in rows)
                tasks.append((priority,order,self.art[group['name']],(round(x*SCALE),round(y*SCALE))))
            if self.parts_renderer:
                for i,a,b,c in menu_rows:
                    if c>>12!=0 or not parts[i,0]:continue
                    art=self.parts_renderer.sprite(parts[i],oam)
                    if art is None:continue
                    x=b&511;y=a&255
                    if x>=256:x-=512
                    if y>=192:y-=256
                    tasks.append(((c>>10)&3,i,art,(round(x*SCALE),round(y*SCALE))))
            for priority,order,art,pos in sorted(tasks,key=lambda task:task[:2],reverse=True):self.group_overlay.alpha_composite(art,pos)
        self.group_key=group_key;top.paste(self.group_overlay,(0,0),self.group_overlay)
        # Text and panels remain live. The existing approved Valhawk parts
        # are drawn next with the game's own transforms and priorities.
        top.paste(panel,(0,panel_y))
        filtered=parts.copy()
        for i,a,b,c in menu_rows:filtered[i,0]=0
        self.last_scene='favorite';return filtered
