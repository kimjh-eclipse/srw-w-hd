"""Rank HD/native material disagreement; candidates are NOT automatic defects.

Read-only: no textures, palettes, bindings, or baselines are rewritten. A large
score can also mean intentional HD geometry changes, so inspect the pictures
and observed runtime palette before deciding to redraw.
"""
import argparse
import base64
import json
from pathlib import Path
import sys
import zlib

import numpy as np
from PIL import Image,ImageFilter

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_parts import PartsRenderer


def measure(art,native,palette,renderer):
    # Limit the audit itself to 2x native size; this is a material survey,
    # not a visual-quality or pixel-exact rendering comparison.
    w,h=native.shape[1],native.shape[0]
    small=art.resize((w*2,h*2),Image.Resampling.BOX)
    pixels=np.asarray(small);rgb=pixels[:,:,:3].astype('float32')
    used=np.unique(native);used=used[used>0]
    if not len(used):return None
    codes=np.rint(rgb*31/255).astype('uint32')
    packed=codes[:,:,0]|codes[:,:,1]<<5|codes[:,:,2]<<10
    colors,inverse=np.unique(packed,return_inverse=True)
    values=np.stack([(colors&31)*255/31,((colors>>5)&31)*255/31,
                     ((colors>>10)&31)*255/31],-1)
    selected=used[np.argmin(((values[:,None,:]-palette[None,used,:])**2).sum(-1),axis=1)]
    nearest=selected[inverse].reshape(h*2,w*2)
    expected=np.asarray(Image.fromarray(native).resize((w*2,h*2),Image.Resampling.NEAREST))
    valid=(pixels[:,:,3]>224)&(expected>0)
    # Ignore transparent silhouettes and painted ink crossing material edges.
    interior=np.asarray(Image.fromarray((valid*255).astype('uint8')).filter(ImageFilter.MinFilter(3)))>0
    colored=rgb.max(2)>=72
    mask=interior&colored
    distance=np.max(np.abs(palette[nearest]-palette[expected]),axis=2)
    mismatch=mask&(distance>48)
    return dict(interior_pixels=int(mask.sum()),mismatch_pixels=int(mismatch.sum()),
                mismatch_ratio=float(mismatch.sum()/max(1,mask.sum())),
                used_slots=used.tolist())


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--limit',type=int,default=0)
    p.add_argument('--bindings',type=int,nargs='*')
    args=p.parse_args();r=PartsRenderer(async_prepare=False)
    rows=[];missing=0;examined=0;errors=[]
    try:
        for bid,spec in enumerate(r.bindings,1):
            if args.bindings and bid not in args.bindings:continue
            if not spec.get('dynamic_palette') or spec.get('disabled') or spec.get('source_binding'):continue
            encoded=spec.get('index_pixels')
            native=(np.frombuffer(zlib.decompress(base64.b64decode(encoded)),dtype='uint8').reshape(spec['h'],spec['w'])
                    if encoded else r.native_material_indices(bid,spec))
            if native is None:continue
            if args.limit and examined>=args.limit:break
            try:
                found=r.disk_cache.get(r.texture_key(bid,spec['w'],spec['h']))
                if not found:missing+=1;continue
                palette=np.asarray(spec.get('palette_source_rgb',spec.get('original_palette_rgb',r.source_palette)),dtype='float32')
                result=measure(found[0],native,palette,r);examined+=1
                if result and result['mismatch_pixels']>=8 and result['mismatch_ratio']>=.05:
                    rows.append(dict(binding=bid,atlas=spec.get('atlas_id','base'),resource=spec.get('resource'),**result))
            except Exception as e:errors.append(dict(binding=bid,error=str(e)))
            if examined and examined%1000==0:print('examined',examined,'candidates',len(rows),flush=True)
        rows.sort(key=lambda v:v['mismatch_pixels'],reverse=True)
        report=dict(scope='Material-layout disagreement candidates; requires picture and runtime-palette review',
            examined=examined,missing_baked=missing,errors=errors,flagged=len(rows),
            threshold=dict(rgb_distance=48,minimum_pixels=8,minimum_ratio=.05),
            automatic_fix=False,rows=rows)
        out=ROOT/'test_current/parts/palette_correspondence';out.mkdir(exist_ok=True)
        (out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
        print(json.dumps({k:v for k,v in report.items() if k!='rows'}))
    finally:r.close()


if __name__=='__main__':main()
