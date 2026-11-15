"""Register a whole-pose drawing onto its native silhouette (Claude's edge/registration step).

1. Global fit: search a small scale (x, y) and offset that maximises silhouette
   IoU between the drawing (alpha, box-downscaled) and native.png.
2. Edge fit, using only the drawing's own pixels (no recolouring, no native colours):
   - alpha outside the native silhouette (grown by half a native pixel, softened)
     goes to 0;
   - native-opaque places left unpainted are filled by growing the nearest
     painted drawing pixels outward (repeated 3x3 dilation of colour).
Writes candidate_fit.png next to the drawing and fit.json (transform, IoU before/after).

  py -3.11 -X utf8 scripts/assets/fit_pose_drawing.py <pose folder> [candidate.png]
"""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter

S=4


def iou_of(img,nat,W,H):
    a=np.asarray(img.resize((W,H),Image.Resampling.BOX))[:,:,3]>127
    return float((a&nat).sum()/max((a|nat).sum(),1))


def transform(img,sx,sy,dx,dy,size):
    w,h=img.size;nw,nh=round(w*sx),round(h*sy)
    scaled=img.resize((nw,nh),Image.Resampling.LANCZOS)
    out=Image.new('RGBA',size);out.alpha_composite(scaled,(round((w-nw)/2+dx),round((h-nh)/2+dy))) if False else None
    canvas=Image.new('RGBA',(size[0]+64,size[1]+64));canvas.paste(scaled,(32+round((w-nw)/2+dx),32+round((h-nh)/2+dy)),scaled)
    return canvas.crop((32,32,32+size[0],32+size[1]))


def grow_fill(rgba,want):
    """Fill want&~painted with colours grown from painted neighbours."""
    arr=rgba.astype('float32');painted=arr[:,:,3]>127
    col=arr[:,:,:3]*painted[...,None];cnt=painted.astype('float32')
    have=painted.copy()
    for _ in range(64):
        todo=want&~have
        if not todo.any():break
        acc=np.zeros_like(col);n=np.zeros_like(cnt)
        for oy in (-1,0,1):
            for ox in (-1,0,1):
                if ox==0 and oy==0:continue
                acc+=np.roll(np.roll(col*have[...,None],oy,0),ox,1);n+=np.roll(np.roll(have.astype('float32'),oy,0),ox,1)
        new=todo&(n>0)
        col[new]=acc[new]/n[new][:,None];have|=new
    out=arr.copy();fill=want&~painted&have
    out[fill,:3]=col[fill];out[fill,3]=255
    return out.clip(0,255).astype('uint8')


def main():
    folder=Path(sys.argv[1]);name=sys.argv[2] if len(sys.argv)>2 else 'candidate.png'
    native=Image.open(folder/'native.png').convert('RGBA');W,H=native.size;nat=np.asarray(native)[:,:,3]>0
    cand=Image.open(folder/name).convert('RGBA');size=(W*S,H*S)
    before=iou_of(cand,nat,W,H)
    # The search only needs the silhouette: alpha alone, at 2x, against the
    # native mask at 2x. Offsets stay in 4x units. Only the chosen transform is
    # applied to the full colour drawing.
    alpha2=cand.getchannel('A').resize((W*2,H*2),Image.Resampling.BOX)
    nat2=np.kron(nat,np.ones((2,2),bool))
    def score(sx,sy,dx,dy):
        w,h=alpha2.size;nw,nh=max(1,round(w*sx)),max(1,round(h*sy))
        sc=alpha2.resize((nw,nh),Image.Resampling.BILINEAR)
        canvas=Image.new('L',(w+64,h+64));canvas.paste(sc,(32+round((w-nw)/2+dx/2),32+round((h-nh)/2+dy/2)))
        a=np.asarray(canvas.crop((32,32,32+w,32+h)))>127
        return float((a&nat2).sum()/max((a|nat2).sum(),1))
    best=(score(1,1,0,0),1.,1.,0,0)
    for sx in np.arange(.80,1.2001,.02):
        for sy in np.arange(.80,1.2001,.02):
            for dx in range(-20,21,4):
                for dy in range(-20,21,4):
                    v=score(sx,sy,dx,dy)
                    if v>best[0]:best=(v,sx,sy,dx,dy)
    _,sx,sy,dx,dy=best;b=best
    for sx2 in np.arange(sx-.02,sx+.0201,.005):
        for sy2 in np.arange(sy-.02,sy+.0201,.005):
            for dx2 in range(dx-3,dx+4,2):
                for dy2 in range(dy-3,dy+4,2):
                    v=score(sx2,sy2,dx2,dy2)
                    if v>b[0]:b=(v,sx2,sy2,dx2,dy2)
    _,sx,sy,dx,dy=b
    # last pixel at 4x: alpha only, one step around the best
    alpha4=cand.getchannel('A')
    def score4(dx,dy):
        moved=transform(Image.merge('RGBA',(alpha4,alpha4,alpha4,alpha4)),sx,sy,dx,dy,size)
        return iou_of(moved,nat,W,H)
    v,dx,dy=max(((score4(dx+ox,dy+oy),dx+ox,dy+oy) for ox in (-1,0,1) for oy in (-1,0,1)),key=lambda t:t[0])
    moved=transform(cand,sx,sy,dx,dy,size)
    # edge fit
    sil=Image.fromarray((nat*255).astype('uint8')).resize(size,Image.Resampling.NEAREST)
    keep=np.asarray(sil.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.2))).astype('float32')/255
    arr=np.asarray(moved).copy();arr[:,:,3]=(arr[:,:,3].astype('float32')*keep).astype('uint8')
    want=np.asarray(sil)>127
    fitted=grow_fill(arr,want)
    out=Image.fromarray(fitted);out.save(folder/'candidate_fit.png')
    after=iou_of(out,nat,W,H)
    info=dict(source=name,iou_before=round(before,4),iou_registered=round(v,4),iou_after_edge=round(after,4),scale=[round(float(sx),4),round(float(sy),4)],offset_4x=[int(dx),int(dy)],
        filled_px=int((want&~(np.asarray(moved)[:,:,3]>127)).sum()),trimmed_px=int(((np.asarray(moved)[:,:,3]>127)&(keep<.5)).sum()))
    (folder/'fit.json').write_text(json.dumps(info,indent=1),encoding='utf-8');print(info)


if __name__=='__main__':main()
