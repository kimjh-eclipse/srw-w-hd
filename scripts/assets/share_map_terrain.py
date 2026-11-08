"""Reuse redrawn native 8x8 terrain identities across every MAP in a group."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import argparse,json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=PROJECT_ROOT;FOLDER=ROOT/'graphics/map_tiles'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--img',type=int);parser.add_argument('--global-reuse',action='store_true');args=parser.parse_args();catalog=json.loads((FOLDER/'catalog.json').read_text());groups={}
    for row in catalog['maps']:groups.setdefault((row['img'],row['pal']),[]).append(row)
    report=[];global_lookup={}
    if args.global_reuse:
        for row in catalog['maps']:
            path=FOLDER/f"map_{row['id']}_hd.png"
            if not path.exists():continue
            native=np.asarray(Image.open(FOLDER/row['native']).convert('RGB'))>>3;h,w=native.shape[:2];art=Image.open(path).convert('RGB');sx=art.width/w;sy=art.height/h
            for y in range(0,h-7,8):
                for x in range(0,w-7,8):
                    patch=native[y:y+8,x:x+8];key=patch.tobytes()
                    if key in global_lookup:continue
                    paint=art.crop((round(x*sx),round(y*sy),round((x+8)*sx),round((y+8)*sy))).resize((24,24),Image.Resampling.LANCZOS)
                    for flip in range(4):
                        p=patch;im=paint
                        if flip&1:p=p[:,::-1];im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                        if flip&2:p=p[::-1];im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                        global_lookup.setdefault(p.tobytes(),im)
        supplement=FOLDER/'missing_batches/batches.json'
        if supplement.exists():
            for batch in json.loads(supplement.read_text()):
                path=FOLDER/batch['image']
                if not path.exists():continue
                native=np.asarray(Image.open(FOLDER/batch['native']).convert('RGB'))>>3;art=Image.open(path).convert('RGB');sx=art.width/native.shape[1];sy=art.height/native.shape[0]
                for region in batch['entries']:
                    for yy in (0,8):
                        for xx in (0,8):
                            x=region['x']+xx;y=region['y']+yy;patch=native[y:y+8,x:x+8];paint=art.crop((round(x*sx),round(y*sy),round((x+8)*sx),round((y+8)*sy))).resize((24,24),Image.Resampling.LANCZOS)
                            for flip in range(4):
                                p=patch;im=paint
                                if flip&1:p=p[:,::-1];im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                                if flip&2:p=p[::-1];im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                                global_lookup.setdefault(p.tobytes(),im)
        print('global exact native identities',len(global_lookup),flush=True)
    for group,rows in groups.items():
        if args.img is not None and group[0]!=args.img:continue
        sources=[r for r in rows if (FOLDER/f"map_{r['id']}_hd.png").exists()]
        if not sources:continue
        lookup={};quality={}
        for row in sources:
            native=np.asarray(Image.open(FOLDER/row['native']).convert('RGB'))>>3;h,w=native.shape[:2];art=Image.open(FOLDER/f"map_{row['id']}_hd.png").convert('RGB');sx=art.width/w;sy=art.height/h
            for y in range(0,h-7,8):
                for x in range(0,w-7,8):
                    patch=native[y:y+8,x:x+8];paint=art.crop((round(x*sx),round(y*sy),round((x+8)*sx),round((y+8)*sy))).resize((24,24),Image.Resampling.LANCZOS)
                    # Prefer a quiet painted sample for identical plain-color
                    # texels so a reused grass/ocean tile never gains a building.
                    score=float(np.asarray(paint,dtype='float32').std((0,1)).mean()) if np.unique(patch.reshape(-1,3),axis=0).shape[0]<3 else 0
                    for flip in range(4):
                        p=patch;im=paint
                        if flip&1:p=p[:,::-1];im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                        if flip&2:p=p[::-1];im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                        key=p.tobytes()
                        if key not in lookup or score<quality[key]:lookup[key]=im;quality[key]=score
        if args.global_reuse:
            for key,paint in global_lookup.items():lookup.setdefault(key,paint)
        for row in rows:
            if row in sources:continue
            native=np.asarray(Image.open(FOLDER/row['native']).convert('RGB'));h,w=native.shape[:2];q=native>>3;canvas=Image.fromarray(native).resize((w*3,h*3),Image.Resampling.NEAREST);covered=0;total=0
            for y in range(0,h-7,8):
                for x in range(0,w-7,8):
                    total+=1;paint=lookup.get(q[y:y+8,x:x+8].tobytes())
                    if paint is not None:canvas.paste(paint,(x*3,y*3));covered+=1
            path=FOLDER/f"map_{row['id']}_shared_hd.png";canvas.save(path,compress_level=1)
            row.update(image=path.name,status='shared_terrain_indexed',image_kind='shared_exact_8x8_tiles',image_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),hd_tile_coverage=covered/total,shared_sources=[s['id'] for s in sources]);report.append(dict(map=row['id'],img=group[0],pal=group[1],covered=covered,total=total,coverage=covered/total))
    temp=FOLDER/'catalog.tmp.json';temp.write_text(json.dumps(catalog,indent=2));temp.replace(FOLDER/'catalog.json');library=dict(maps=[r for r in catalog['maps'] if r.get('image')]);temp=FOLDER/'library.tmp.json';temp.write_text(json.dumps(library,indent=2));temp.replace(FOLDER/'library.json');(FOLDER/'shared_coverage.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
