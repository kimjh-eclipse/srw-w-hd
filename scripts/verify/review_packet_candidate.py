"""Review a drawn packet before install: per contract row, compare the candidate's alpha
(4x canvas, cropped at atlas_box) with the native index silhouette.

Reports per part: native texels, HD texels (downscaled alpha>127), silhouette IoU,
mean alpha where the native is transparent (0..255), and colour distance of the
HD's mean colour inside the silhouette vs the native palette mean. Writes a
side-by-side sheet (native | candidate on grey) next to the packet.

  py -3.11 -X utf8 scripts/verify/review_packet_candidate.py <folder> <contract.json> <candidate.png> [--scale 4]
Exit code 1 when any part fails (IoU < .80 or outside alpha mean > 24 or colour distance > 60).
"""
import argparse,base64,json,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw

IOU_MIN,OUTSIDE_MAX,COLOUR_MAX=.80,24.,60.


def main():
    p=argparse.ArgumentParser();p.add_argument('folder',type=Path);p.add_argument('contract');p.add_argument('candidate');p.add_argument('--scale',type=float,default=4)
    a=p.parse_args()
    rows=json.loads((a.folder/a.contract).read_text(encoding='utf-8'))
    cand=Image.open(a.folder/a.candidate).convert('RGBA');s=a.scale
    out=[];tiles=[]
    for r in rows:
        r=r.get('source_contract',r) if 'atlas_box' not in r else r
        x,y,w,h=r['atlas_box']
        idx=np.frombuffer(zlib.decompress(base64.b64decode(r['index_pixels'])),dtype='uint8').reshape(h,w);nat=idx>0
        crop=cand.crop((round(x*s),round(y*s),round((x+w)*s),round((y+h)*s)));arr=np.asarray(crop).astype('float32')
        small=np.asarray(crop.resize((w,h),Image.Resampling.BOX)).astype('float32')
        hd=small[:,:,3]>127
        iou=float((hd&nat).sum()/max((hd|nat).sum(),1))
        outside=float(small[:,:,3][~nat].mean()) if (~nat).any() else 0.
        pal=np.array(r.get('actual_palette_rgb') or [[0,0,0]]*16,dtype='float32')
        nmean=pal[np.minimum(idx[nat],len(pal)-1)].mean(0) if nat.any() else np.zeros(3)
        inside=small[:,:,:3][nat&hd];hmean=inside.mean(0) if len(inside) else np.zeros(3)
        colour=float(np.linalg.norm(nmean-hmean))
        bad=[k for k,v in (('shape',iou<IOU_MIN),('halo',outside>OUTSIDE_MAX),('colour',colour>COLOUR_MAX)) if v]
        out.append(dict(slot=r.get('slot'),hash=r.get('hash'),atlas_box=[x,y,w,h],native=int(nat.sum()),hd=int(hd.sum()),iou=round(iou,3),outside_alpha=round(outside,1),colour=round(colour,1),bad=bad))
        k=max(1,int(96/max(w,h)))
        nimg=np.dstack([pal.astype('uint8')[np.minimum(idx,len(pal)-1)],np.where(nat,255,0).astype('uint8')])
        t=Image.new('RGBA',(w*k*2+6,h*k+12),(90,90,100,255))
        t.alpha_composite(Image.fromarray(nimg).resize((w*k,h*k),0),(0,0));t.alpha_composite(crop.resize((w*k,h*k)),(w*k+6,0))
        ImageDraw.Draw(t).text((0,h*k),f"{r.get('slot')} {iou:.2f} {outside:.0f} {'/'.join(bad)}",fill=(255,80,80) if bad else (255,255,0))
        tiles.append(t)
    cols=6;cw=max(t.width for t in tiles)+4;ch=max(t.height for t in tiles)+4
    sheet=Image.new('RGBA',(cw*cols,ch*((len(tiles)+cols-1)//cols)),(30,30,30,255))
    for i,t in enumerate(tiles):sheet.alpha_composite(t,((i%cols)*cw,(i//cols)*ch))
    stem=Path(a.candidate).stem;sheet.save(a.folder/f'review_{stem}.png')
    (a.folder/f'review_{stem}.json').write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding='utf-8')
    failed=[o for o in out if o['bad']]
    for o in out:print(o['slot'],o['atlas_box'],'native',o['native'],'hd',o['hd'],'IoU',o['iou'],'outside',o['outside_alpha'],'colour',o['colour'],o['bad'] or '')
    print('parts',len(out),'failed',len(failed),'sheet',a.folder/f'review_{stem}.png')
    sys.exit(1 if failed else 0)


if __name__=='__main__':main()
