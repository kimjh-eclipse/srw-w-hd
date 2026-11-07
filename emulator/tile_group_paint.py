"""Sample adjacent matching tiles as one image, retaining continuous ink lines."""
import numpy as np
from PIL import Image

def complete_origins(tiles,votes,find):
    origins=votes.most_common(192);seen={key for key,_ in origins}
    for x,y,tile in tiles:
        for identifier,sx,sy in find(tile.tobytes())[:4]:
            key=(identifier,sx-x,sy-y)
            if key not in seen:origins.append((key,votes[key]));seen.add(key)
    return origins

def paint_group(renderer,canvas,s,a,paint,indices,target,ox,oy,matches,tiles):
    h,w=indices.shape;grid=np.zeros((h//8,w//8),dtype='uint8')
    for n in matches:x,y,_=tiles[n];grid[y//8,x//8]=255
    original=grid.copy()
    for ty in range(h//8):
        for tx in range(w//8):
            sx,sy=ox+tx*8,oy+ty*8
            if indices[ty*8:ty*8+8,tx*8:tx*8+8].any():continue
            if not original[max(0,ty-1):ty+2,max(0,tx-1):tx+2].any():continue
            if 0<=sx<=s['w']-8 and 0<=sy<=s['h']-8 and not a[sy:sy+8,sx:sx+8].any():grid[ty,tx]=255
    gy,gx=np.nonzero(grid);l,u,r,b=int(gx.min())*8,int(gy.min())*8,(int(gx.max())+1)*8,(int(gy.max())+1)*8
    sx,sy=s['x']+ox+l,s['y']+oy+u;xs=paint.width/s['native_size'][0];ys=paint.height/s['native_size'][1]
    art=paint.crop((round(sx*xs),round(sy*ys),round((sx+r-l)*xs),round((sy+b-u)*ys))).resize(((r-l)*8,(b-u)*8),Image.Resampling.LANCZOS)
    art=renderer.recolor(art,a[oy+u:oy+b,ox+l:ox+r],s['palette'],target)
    mask=Image.fromarray(grid[u//8:b//8,l//8:r//8]).resize(art.size,Image.Resampling.NEAREST)
    art.putalpha(Image.fromarray((np.asarray(art.getchannel('A'),dtype='uint16')*np.asarray(mask,dtype='uint16')//255).astype('uint8')))
    canvas.alpha_composite(art,dest=(l*8,u*8))
