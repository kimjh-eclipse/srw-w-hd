"""Survey every HD picture the player recolours at run time and measure blotches.

A native part whose shape has HD art but whose colours do not is drawn by
recolouring that art into the live palette. Every such (art, palette) pair in
the ROM is found by walking all animation patterns over every image of their
group (as export_missing_parts.py does), then each pair is recoloured by the
real renderer twice: the slot-per-pixel method (SRWW_RECOLOUR_SMOOTH=0) and
the smooth colour transfer. Blotches are measured as opaque pixels whose
colour jumps from their 3x3 neighbourhood although the painted art is smooth
there (new speckle), as a share of the part.

Writes test_current/parts/recolour_audit/report.json and contact sheets of
the worst pairs (painted | old | smooth). Reads only.
"""
import argparse,json,struct,sys,zlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image,ImageDraw
from scripts.assets import srw_graphics as g


def pairs():
    rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();offsets=g.archive(rom)
    resource=lambda i:g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    patterns=json.loads((ROOT/'test_current/rom_catalog/animation_audit.json').read_text(encoding='utf-8'))['patterns']
    lib=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text(encoding='utf-8'))['bindings']
    rgb={b['hash'] for b in lib if b.get('rgb_enabled',True) and not b.get('disabled')}
    indexed={}
    for i,b in enumerate(lib,1):
        if b.get('dynamic_palette') and b.get('indexed_safe',True) and not b.get('disabled') and b.get('index_hash') is not None:indexed.setdefault(b['index_hash'],i)
    found={}
    for pattern in patterns:
        palette_id=pattern.get('palette')
        if palette_id is None:continue
        try:palette=np.frombuffer(resource(palette_id)[8:],dtype='<u2')
        except Exception:continue
        rects={(p['tile'],p['w'],p['h'],p['palette_bank']) for p in pattern.get('parts',[])}
        for image in pattern.get('image_group') or [pattern['image']]:
            try:pixels=g.pixels(resource(image))
            except Exception:continue
            for tile,w,h,bank in rects:
                x=(tile&4095)%32*8;y=(tile&4095)//32*8
                if x+w>pixels.shape[1] or y+h>pixels.shape[0]:continue
                part=pixels[y:y+h,x:x+w]
                if not part.any() or int(part.max())>15:continue
                colours=palette[bank*16:(bank+1)*16]
                if len(colours)<=int(part.max()):colours=palette[:16]
                if len(colours)<=int(part.max()):continue
                ih=zlib.crc32(np.where(part,part.astype('uint16')|0x8000,0).astype('<u2').tobytes())^(w<<16)^h
                ch=zlib.crc32(np.where(part,colours[part]|0x8000,0).astype('<u2').tobytes())^(w<<16)^h
                if ch in rgb or ih not in indexed:continue
                full=np.zeros(16,dtype='<u2');full[:len(colours[:16])]=colours[:16]
                found.setdefault((indexed[ih],full.tobytes()),dict(binding=indexed[ih],palette=full,hash=int(ch),image=image,x=x,y=y,w=w,h=h))
    return list(found.values())


def speckle(rgb,alpha):
    """Share of opaque pixels whose colour leaves its 3x3 median by 40+."""
    pad=np.pad(rgb,((1,1),(1,1),(0,0)),mode='edge')
    stack=np.stack([pad[dy:dy+rgb.shape[0],dx:dx+rgb.shape[1]] for dy in range(3) for dx in range(3)],0)
    med=np.median(stack,axis=0);jump=np.abs(rgb-med).max(2)>=40
    inside=alpha>=200
    return jump&inside,inside


def main():
    parser=argparse.ArgumentParser(description=__doc__.split('\n')[0]);parser.add_argument('--sheets',type=int,default=120)
    args=parser.parse_args();out=ROOT/'test_current/parts/recolour_audit';out.mkdir(parents=True,exist_ok=True)
    work=pairs();print('recolour pairs',len(work),flush=True)
    import hd_parts
    from hd_parts import PartsRenderer
    parts=PartsRenderer(async_prepare=False);rows=[]
    for n,p in enumerate(work):
        b=p['binding'];spec=parts.bindings[b-1]
        row=np.array([b,0,0,0,p['hash'],0,0,0],dtype='uint32')
        try:
            hd_parts.RECOLOUR_SMOOTH=False;parts.cache.clear();old=parts.sprite(row,bytes(1024),p['palette'],required=True)
            hd_parts.RECOLOUR_SMOOTH=True;parts.cache.clear();new=parts.sprite(row,bytes(1024),p['palette'],required=True)
            art=parts.scaled.get(spec.get('source_binding',b))
        except Exception as error:rows.append(dict(binding=b,error=str(error)[:120]));continue
        if old is None or new is None or art is None:continue
        a=np.asarray(art,dtype='float32');o=np.asarray(old,dtype='float32');s=np.asarray(new,dtype='float32')
        base,inside=speckle(a[:,:,:3],a[:,:,3]);area=max(1,int(inside.sum()))
        old_j,_=speckle(o[:,:,:3],o[:,:,3]);new_j,_=speckle(s[:,:,:3],s[:,:,3])
        colours=parts.bindings[b-1].get('original_palette_rgb')
        diff=float(np.mean(np.abs(np.asarray(p['palette'],dtype='uint32')[1:,None]>>np.array([0,5,10])&31).astype(float)*255/31-np.asarray(colours)[1:16])) if colours and len(colours)>=16 else None
        rows.append(dict(binding=b,atlas=spec.get('atlas_id'),image=p['image'],palette_shift=None if diff is None else round(diff,1),
            old_blotch=round(float((old_j&~base).sum()/area),4),smooth_blotch=round(float((new_j&~base).sum()/area),4)))
        if n%200==0:print(n,len(work),flush=True)
    good=[r for r in rows if 'old_blotch' in r]
    worst=sorted(good,key=lambda r:-r['old_blotch'])
    summary=dict(pairs=len(work),measured=len(good),
        old_over_5pct=sum(r['old_blotch']>.05 for r in good),smooth_over_5pct=sum(r['smooth_blotch']>.05 for r in good),
        old_over_2pct=sum(r['old_blotch']>.02 for r in good),smooth_over_2pct=sum(r['smooth_blotch']>.02 for r in good),
        old_mean=round(float(np.mean([r['old_blotch'] for r in good])) if good else 0,4),smooth_mean=round(float(np.mean([r['smooth_blotch'] for r in good])) if good else 0,4),
        bindings_affected=len({r['binding'] for r in good if r['old_blotch']>.02}))
    (out/'report.json').write_text(json.dumps(dict(summary=summary,rows=worst),ensure_ascii=False,indent=1),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))
    # Contact sheet of the worst pairs: painted | old | smooth.
    import hd_parts as hp
    cell=110;per=4;picked=worst[:args.sheets]
    for page in range(0,len(picked),40):
        group=picked[page:page+40];sheet=Image.new('RGB',(per*cell*3,((len(group)+per-1)//per)*(cell+14)),(70,70,80));draw=ImageDraw.Draw(sheet)
        for k,r in enumerate(group):
            p=next(q for q in work if q['binding']==r['binding'] and q['image']==r['image'])
            row=np.array([r['binding'],0,0,0,p['hash'],0,0,0],dtype='uint32');imgs=[]
            hp.RECOLOUR_SMOOTH=False;parts.cache.clear();imgs.append(parts.sprite(row,bytes(1024),p['palette'],required=True))
            hp.RECOLOUR_SMOOTH=True;parts.cache.clear();imgs.append(parts.sprite(row,bytes(1024),p['palette'],required=True))
            imgs.insert(0,parts.scaled.get(parts.bindings[r['binding']-1].get('source_binding',r['binding'])))
            x0=(k%per)*cell*3;y0=(k//per)*(cell+14)
            for j,im in enumerate(imgs):
                if im is None:continue
                im=im.copy();im.thumbnail((cell-4,cell-4));sheet.paste(im,(x0+j*cell+2,y0+2),im)
            draw.text((x0+2,y0+cell),f"#{r['binding']} old {r['old_blotch']:.2f} new {r['smooth_blotch']:.2f}",fill=(255,255,255))
        sheet.save(out/f'worst_{page//40:02d}.png')


if __name__=='__main__':main()
