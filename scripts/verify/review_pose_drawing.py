"""Review a whole-pose drawing before splitting.

Checks candidate.png against native.png of a pose folder: canvas size (must be
4x), silhouette IoU (drawing alpha box-downscaled >127 vs native opaque),
mean alpha outside the native silhouette, per-sprite IoU (each sprite's
visible area must be painted), and writes review.png (native 4x | drawing |
overlay of misses: red = native opaque but undrawn, blue = drawn outside).

  py -3.11 -X utf8 scripts/verify/review_pose_drawing.py <pose folder> [candidate.png]
Exit 1 when it fails (size, IoU < .90, outside alpha > 16, or a sprite < .80).
"""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts.assets.build_object_packets import compose_canvas


def main():
    folder=Path(sys.argv[1]);name=sys.argv[2] if len(sys.argv)>2 else 'candidate.png'
    native=Image.open(folder/'native.png').convert('RGBA');W,H=native.size
    cand=Image.open(folder/name).convert('RGBA')
    result=dict(pose=folder.name,size=list(cand.size),expected=[W*4,H*4])
    if cand.size!=(W*4,H*4):
        result['fail']=['canvas size'];print(json.dumps(result,ensure_ascii=False));(folder/'review.json').write_text(json.dumps(result,ensure_ascii=False,indent=1),encoding='utf-8');sys.exit(1)
    nat=np.asarray(native)[:,:,3]>0
    small=np.asarray(cand.resize((W,H),Image.Resampling.BOX)).astype('float32');drawn=small[:,:,3]>127
    iou=float((nat&drawn).sum()/max((nat|drawn).sum(),1));outside=float(small[:,:,3][~nat].mean())
    rows=json.loads((folder/'contract.json').read_text(encoding='utf-8'));_,label=compose_canvas(rows,W,H)
    sprites=[];nrgb=np.asarray(native)[:,:,:3].astype('float32')
    for k,r in enumerate(rows):
        m=label==k
        if m.sum()==0:continue
        both=m&drawn
        # Mean colour of the drawing over this sprite's visible area vs the native
        # sprite there: a large gap means the drawn part sits somewhere else.
        colour=float(np.linalg.norm(small[:,:,:3][both].mean(0)-nrgb[both].mean(0))) if both.sum()>=4 else 0.
        sprites.append(dict(oam=r['oam'],hash=r['hash'],visible=int(m.sum()),painted=round(float((drawn&m).sum()/m.sum()),3),colour=round(colour,1)))
    weak=[s for s in sprites if s['painted']<.80 or (s['colour']>70 and s['visible']>=24)]
    fails=[k for k,v in (('silhouette IoU',iou<.90),('outside alpha',outside>16),('sprites undrawn or misplaced',bool(weak))) if v]
    result.update(iou=round(iou,3),outside_alpha=round(outside,1),sprites=len(sprites),max_colour=max((s['colour'] for s in sprites),default=0),weak_sprites=weak,all_sprites=sprites,fail=fails)
    big=np.asarray(native.resize((W*4,H*4),Image.Resampling.NEAREST));c=np.asarray(cand)
    miss=np.zeros((H,W,4),'uint8');miss[nat&~drawn]=(255,40,40,255);miss[drawn&~nat]=(60,120,255,255)
    over=Image.fromarray(big.copy());over.alpha_composite(Image.fromarray(miss).resize((W*4,H*4),Image.Resampling.NEAREST))
    sheet=Image.new('RGBA',(W*12+16,H*4),(60,62,72,255))
    sheet.alpha_composite(Image.fromarray(big),(0,0));sheet.alpha_composite(cand,(W*4+8,0));sheet.alpha_composite(over,(W*8+16,0))
    sheet.save(folder/'review.png');(folder/'review.json').write_text(json.dumps(result,ensure_ascii=False,indent=1),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('weak_sprites','all_sprites')},ensure_ascii=False),'weak',[(s['oam'],s['painted'],s['colour']) for s in weak])
    sys.exit(1 if fails else 0)


if __name__=='__main__':main()
