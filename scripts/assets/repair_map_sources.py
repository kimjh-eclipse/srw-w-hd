"""Resolve multi-IMG map groups by bounds and native tile-edge continuity."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import sys,json,struct,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(PROJECT_ROOT))
import scripts.assets.srw_graphics as g
ROOT=g.ROOT;OUT=ROOT/'graphics/map_tiles';TEST=ROOT/'test_current/map_tiles'

def draw(raw,mid,cid,iid,pid):
    m=raw(mid);c=raw(cid);im=raw(iid);p=raw(pid);w,h=struct.unpack_from('<HH',m,4);w//=2;h//=2;mi=np.frombuffer(m[8:],'<u2').reshape(h,w);cells=np.frombuffer(c[8:],'<u2').reshape(-1,6);pixels=g.pixels(im);pal=np.array(g.palette(p),'uint8');tilew=pixels.shape[1]//8
    blocks=[]
    for j,cell in enumerate(cells):
        block=np.zeros((16,16,3),'uint8')
        for t,e in enumerate(cell[:4]):
            e=int(e);tid=e&1023;tx=tid%tilew*8;ty=tid//tilew*8;idx=pixels[ty:ty+8,tx:tx+8];bank=e>>12
            if idx.shape!=(8,8) or bank*16+int(idx.max())>=len(pal):raise ValueError('bounds')
            colors=pal[bank*16:bank*16+16,:3][idx]
            if e&1024:colors=colors[:,::-1]
            if e&2048:colors=colors[::-1]
            block[t//2*8:t//2*8+8,t%2*8:t%2*8+8]=colors
        blocks.append(block)
    blocks=np.stack(blocks);canvas=blocks[mi].transpose(0,2,1,3,4).reshape(h*16,w*16,3)
    a=canvas.astype('int16');dx=np.abs(a[:,1:]-a[:,:-1]).mean(2);dy=np.abs(a[1:]-a[:-1]).mean(2)
    edge=float(dx[:,7::8].mean()+dy[7::8].mean());inside=float(dx.mean()+dy.mean());score=edge/max(inside,.001)
    atlas=np.zeros((((len(cells)+15)//16)*16,256,3),'uint8')
    for j,b in enumerate(blocks):atlas[j//16*16:j//16*16+16,j%16*16:j%16*16+16]=b
    return canvas,atlas,score

def main():
    rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();o=g.archive(rom);cache={}
    def raw(i):
        if i not in cache:cache[i]=g.decompress(rom[g.BASE+o[i]:g.BASE+o[i+1]])
        return cache[i]
    def kind(i):
        d=rom[g.BASE+o[i]:g.BASE+o[i+1]];return d[16:20] if d[:4]==b'ECD\1' else d[:4]
    path=OUT/'catalog.json';catalog=json.loads(path.read_text());rows={r['id']:r for r in catalog['maps']};phase='';pals=[];imgs=[];cid=None;repairs=[]
    for mid in range(len(o)-1):
        tag=kind(mid)
        if tag==b'PLT\0':
            if phase!='pal':pals=[];imgs=[]
            pals.append(mid);phase='pal'
        elif tag==b'IMG\0':imgs.append(mid);phase='img'
        elif tag==b'CEL\0':cid=mid;phase='cel'
        elif tag==b'MAP\0':
            if len(imgs)<2 and mid in rows:continue
            candidates=[]
            for j,iid in enumerate(imgs):
                possible=[pals[j]] if len(pals)==len(imgs) else pals
                for pid in possible:
                    try:canvas,atlas,score=draw(raw,mid,cid,iid,pid)
                    except (ValueError,IndexError):continue
                    candidates.append((score,iid,pid,canvas,atlas))
            if not candidates:continue
            score,iid,pid,canvas,atlas=min(candidates,key=lambda c:c[0]);row=rows.get(mid,dict(id=mid,cel=cid,native=f'map_{mid}_native.png',cells_image=f'cells_{cid}_native.png',cell_count=(len(raw(cid))-8)//12,status='native_extracted'))
            row.update(img=iid,pal=pid,width=canvas.shape[1],height=canvas.shape[0],source_sha256=hashlib.sha256(raw(mid)+raw(cid)+raw(iid)+raw(pid)).hexdigest(),source_edge_ratio=score)
            Image.fromarray(canvas).save(OUT/row['native']);Image.fromarray(atlas).save(OUT/row['cells_image']);rows[mid]=row;repairs.append(dict(map=mid,chosen_img=iid,chosen_pal=pid,score=score,candidates=[dict(img=c[1],pal=c[2],score=c[0]) for c in candidates]))
    catalog['maps']=sorted(rows.values(),key=lambda r:r['id']);catalog['decoded_maps']=len(rows);catalog['errors']=[e for e in catalog['errors'] if e['id'] not in rows];path.write_text(json.dumps(catalog,indent=2));(OUT/'source_repairs.json').write_text(json.dumps(repairs,indent=2))
    groups={}
    for row in rows.values():groups.setdefault((row['img'],row['pal']),[]).append(row['id'])
    jobs=[]
    for (iid,pid),mids in sorted(groups.items()):
        # Favor a source map containing the most distinct native cells.
        representative=max(mids,key=lambda mid:rows[mid]['cell_count']);row=rows[representative]
        jobs.append(dict(img=iid,pal=pid,maps=mids,representative=representative,reference=row['native'],output=f'map_{representative}_hd.png',status='indexed' if row.get('image') else 'pending'))
    (OUT/'generation_jobs.json').write_text(json.dumps(jobs,indent=2));print('maps',len(rows),'groups',len(jobs),'repaired',len(repairs))

if __name__=='__main__':main()
