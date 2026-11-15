"""Object-level drawing packets from pose captures (build_pose_packets.py output).

A frame holds several things at once (the robot, smoke, missiles, a cut-in
hand). Sprites whose boxes touch (within GAP px) form one object; the same
object layout (sprites and their offsets) seen in many frames is one drawing.
Greedy selection then keeps the fewest objects that show every sprite pixel
that is ever visible, and each kept object gets a packet:

  <out>/obj_NNN/native.png, native_4x.png (object cropped, 8 px margin),
  contract.json (sprites with object-relative boxes), frames.json

Pixels hidden in every captured frame never reach the screen; they are
reported, not drawn.

  py -3.11 -X utf8 scripts/assets/build_object_packets.py <pose dir> [--gap 2]
"""
import argparse,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts.assets.build_pose_packets import compose,sprite_pixels

MARGIN=8


def objects(rows,gap):
    n=len(rows);parent=list(range(n))
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for i in range(n):
        a=rows[i]
        for j in range(i+1,n):
            b=rows[j]
            if a['palette_bank']==b['palette_bank'] and a['screen_x']-gap<b['screen_x']+b['w'] and b['screen_x']-gap<a['screen_x']+a['w'] and a['screen_y']-gap<b['screen_y']+b['h'] and b['screen_y']-gap<a['screen_y']+a['h']:
                parent[find(i)]=find(j)
    groups={}
    for i in range(n):groups.setdefault(find(i),[]).append(i)
    return list(groups.values())


def visible_mask(rows,label,k):
    r=rows[k];x,y,w,h=r['screen_x'],r['screen_y'],r['w'],r['h'];vis=np.zeros((h,w),bool)
    y0,y1,x0,x1=max(0,y),min(192,y+h),max(0,x),min(256,x+w)
    if y1>y0 and x1>x0:vis[y0-y:y1-y,x0-x:x1-x]=label[y0:y1,x0:x1]==k
    if r['flip_y']:vis=vis[::-1]
    if r['flip_x']:vis=vis[:,::-1]
    return vis


def main():
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--gap',type=int,default=2);p.add_argument('--out',type=Path)
    a=p.parse_args();out=a.out or a.root/'objects';out.mkdir(exist_ok=True)
    found={};need={}
    for pose in sorted(d for d in a.root.glob('pose_*') if d.is_dir()):
        rows=json.loads((pose/'contract.json').read_text(encoding='utf-8'));frames=json.loads((pose/'frames.json').read_text())
        _,label=compose(rows)
        for group in objects(rows,a.gap):
            ox=min(rows[k]['screen_x'] for k in group);oy=min(rows[k]['screen_y'] for k in group)
            key=tuple(sorted((rows[k]['hash'],rows[k]['screen_x']-ox,rows[k]['screen_y']-oy,rows[k]['flip_x'],rows[k]['flip_y'],rows[k]['priority']) for k in group))
            gain={}
            for k in group:
                h=rows[k]['hash'];op=sprite_pixels(rows[k])>0
                if rows[k]['flip_y']:op=op[::-1]
                if rows[k]['flip_x']:op=op[:,::-1]
                need.setdefault(h,op);gain[h]=gain.get(h,np.zeros_like(op))|visible_mask(rows,label,k)
            if key in found:
                found[key]['frames']+=frames
                for h,v in gain.items():found[key]['gain'][h]=found[key]['gain'].get(h,np.zeros_like(v))|v
            else:found[key]=dict(rows=[rows[k] for k in group],origin=(ox,oy),frames=list(frames),gain=gain,pose=pose.name)
    ever={h:np.zeros_like(m) for h,m in need.items()}
    for o in found.values():
        for h,v in o['gain'].items():ever[h]|=v&need[h]
    covered={h:np.zeros_like(m) for h,m in need.items()};chosen=[];keys=list(found)
    while True:
        best=None
        for i,k in enumerate(keys):
            if i in chosen:continue
            add=sum(int((v&~covered[h]&need[h]).sum()) for h,v in found[k]['gain'].items())
            if best is None or add>best[1]:best=(i,add)
        if not best or best[1]<=0:break
        chosen.append(best[0])
        for h,v in found[keys[best[0]]]['gain'].items():covered[h]|=v&need[h]
    index=[]
    for n,i in enumerate(chosen):
        o=found[keys[i]];rows=o['rows'];ox,oy=o['origin']
        x1=max(r['screen_x']+r['w'] for r in rows)-ox;y1=max(r['screen_y']+r['h'] for r in rows)-oy
        W,H=x1+2*MARGIN,y1+2*MARGIN
        shifted=[dict(r,screen_x=r['screen_x']-ox+MARGIN,screen_y=r['screen_y']-oy+MARGIN) for r in rows]
        canvas,label=compose_canvas(shifted,W,H)
        folder=out/f'obj_{n:03d}';folder.mkdir(exist_ok=True)
        Image.fromarray(canvas).save(folder/'native.png');Image.fromarray(canvas).resize((W*4,H*4),Image.Resampling.NEAREST).save(folder/'native_4x.png')
        (folder/'contract.json').write_text(json.dumps([{k:v for k,v in r.items()} for r in shifted],ensure_ascii=False),encoding='utf-8')
        (folder/'frames.json').write_text(json.dumps(dict(pose=o['pose'],screen_origin=[ox-MARGIN,oy-MARGIN],frames=sorted(set(o['frames'])))),encoding='utf-8')
        index.append(dict(object=folder.name,sprites=len(rows),size=[W,H],frames=len(set(o['frames'])),with_hd=sum(1 for r in rows if r['binding_id'])))
    total=sum(int(m.sum()) for m in need.values());vis=sum(int(m.sum()) for m in ever.values());got=sum(int((covered[h]&ever[h]).sum()) for h in need)
    summary=dict(objects_seen=len(found),objects_chosen=len(chosen),sprites=len(need),sprite_pixels=total,ever_visible=vis,covered=got,
        never_visible_share=round(1-vis/max(total,1),3),objects=index)
    (out/'INDEX.json').write_text(json.dumps(summary,ensure_ascii=False,indent=1),encoding='utf-8')
    print({k:v for k,v in summary.items() if k!='objects'})
    for e in index[:40]:print(e)


def compose_canvas(rows,W,H):
    rgba=np.zeros((H,W,4),'uint8');label=np.full((H,W),-1,'int16')
    for k in sorted(range(len(rows)),key=lambda k:(rows[k]['priority'],rows[k]['oam'])):
        r=rows[k];idx=sprite_pixels(r);pal=np.array(r['original_palette_rgb'],dtype='uint8');x,y,w,h=r['screen_x'],r['screen_y'],r['w'],r['h']
        free=(label[y:y+h,x:x+w]<0)&(idx>0);label[y:y+h,x:x+w][free]=k
        rgba[y:y+h,x:x+w][free]=np.concatenate([pal[idx[free]],np.full((int(free.sum()),1),255,'uint8')],1)
    return rgba,label


if __name__=='__main__':main()
