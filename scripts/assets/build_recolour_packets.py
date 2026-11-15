"""Drawing packets that replace runtime recolouring with art drawn in the real palette.

A part whose shape has HD art in one palette is recoloured at run time when the
game shows it in another (flashes, colour variants); that is what blotches.
Once a picture drawn in that exact palette is connected under its own RGB key,
the core finds it first and nothing is recoloured.

From the recolour survey (test_current/parts/recolour_audit/report.json) this
groups the pairs by source image and palette and writes, per group, a folder
under test_current/parts/recolour_packets/ with:
  native_<P>.png        the source image in that palette (index 0 transparent)
  reference_hd_<P>.png  the current HD art of those parts, at 4x, in the BASE
                        palette - shape guide only; repaint in the new colours
  missing_<P>.png       4x native with the parts outlined
  contract_<P>.json     one row per part (atlas_box = place in the image, the
                        palette's 16 colours, both hashes) - new-part format
  queue_entry_<P>.json  ready_candidates entry; fill file_sha256 after drawing
Priority: blotch with the best runtime method, largest first.
"""
import argparse,base64,json,sys,zlib
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]));sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'verify'))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image,ImageDraw
from scripts.assets import srw_graphics as g
import audit_recolour_blotches as audit

OUT=ROOT/'test_current/parts/recolour_packets'


def main():
    parser=argparse.ArgumentParser(description=__doc__.split('\n')[0]);parser.add_argument('--min-blotch',type=float,default=.05);parser.add_argument('--min-opaque',type=int,default=64)
    args=parser.parse_args()
    report={(r['binding'],r['image']):r for r in json.loads((ROOT/'test_current/parts/recolour_audit/report.json').read_text(encoding='utf-8'))['rows'] if 'old_blotch' in r}
    meta=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text(encoding='utf-8'))
    rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();off=g.archive(rom)
    pixels_of={}
    groups=defaultdict(list)
    for p in audit.pairs():
        r=report.get((p['binding'],p['image']))
        if r is None:continue
        blotch=min(r['old_blotch'],r['smooth_blotch'])
        if blotch<args.min_blotch:continue
        if p['image'] not in pixels_of:pixels_of[p['image']]=g.pixels(g.decompress(rom[g.BASE+off[p['image']]:g.BASE+off[p['image']+1]]))
        part=pixels_of[p['image']][p['y']:p['y']+p['h'],p['x']:p['x']+p['w']]
        if int(np.count_nonzero(part))<args.min_opaque:continue
        groups[(p['image'],p['palette'].tobytes())].append(dict(p,blotch=blotch,part=part))
    OUT.mkdir(parents=True,exist_ok=True);index=[]
    from hd_parts import PartsRenderer
    renderer=PartsRenderer(async_prepare=False)
    order=sorted(groups.items(),key=lambda kv:-sum(r['blotch']*np.count_nonzero(r['part']) for r in kv[1]))
    for rank,((image,pal_bytes),rows) in enumerate(order,1):
        pal=np.frombuffer(pal_bytes,dtype='<u2').astype('uint32');rgb=np.stack([(pal&31)*255//31,((pal>>5)&31)*255//31,((pal>>10)&31)*255//31],-1).astype('uint8')
        idx=pixels_of[image];tag=f'{zlib.crc32(pal_bytes):08x}';folder=OUT/f'img{image:05d}';folder.mkdir(exist_ok=True)
        native=np.dstack([rgb[np.minimum(idx,15)],np.where(idx>0,255,0).astype('uint8')]);Image.fromarray(native).save(folder/f'native_{tag}.png')
        ref=Image.new('RGBA',(idx.shape[1]*4,idx.shape[0]*4));guide=Image.fromarray(native).resize(ref.size,Image.Resampling.NEAREST);draw=ImageDraw.Draw(guide);contract=[];seen=set()
        for r in rows:
            if r['hash'] in seen:continue
            seen.add(r['hash']);spec=meta['bindings'][r['binding']-1]
            # The renderer's own prepared texture (any atlas, including the base one).
            source=spec.get('source_binding',r['binding']);art,_=renderer.prepare_texture(source,spec['w'],spec['h'])
            art=art.convert('RGBA').resize((r['w']*4,r['h']*4),Image.Resampling.LANCZOS);ref.alpha_composite(art,(r['x']*4,r['y']*4))
            x,y,w,h=r['x'],r['y'],r['w'],r['h'];draw.rectangle((x*4,y*4,(x+w)*4-1,(y+h)*4-1),outline=(255,40,40,255))
            part=r['part']
            contract.append(dict(slot=len(contract),hash=int(r['hash']),index_hash=int(zlib.crc32(np.where(part>0,part.astype('uint16')|0x8000,0).astype('<u2').tobytes())^(w<<16)^h),
                atlas_box=[x,y,w,h],index_pixels=base64.b64encode(zlib.compress(part.astype('uint8').tobytes())).decode(),actual_palette_bgr555=[int(v) for v in pal],
                actual_palette_rgb=rgb.tolist(),resource=image,source_x=x,source_y=y,spec=dict(resource=image,source_x=x,source_y=y),w=w,h=h,render_mode='static',effect_part=bool(spec.get('effect_part')),
                replaces_recolour_of=r['binding'],blotch=round(r['blotch'],3)))
        ref.save(folder/f'reference_hd_{tag}.png');guide.save(folder/f'missing_{tag}.png')
        (folder/f'contract_{tag}.json').write_text(json.dumps(contract,ensure_ascii=False),encoding='utf-8')
        entry=dict(source=str(folder.relative_to(ROOT)).replace('\\','/'),contract=f'contract_{tag}.json',drawing=f'candidate_{tag}.png',native=f'native_{tag}.png',generated=f'generated_{tag}.png',
            bindings=[],new_source_keys=[dict(hash=c['hash'],index_hash=c['index_hash']) for c in contract],file_sha256=dict(contract=None,drawing=None,native=None,generated=None),
            note='recolour replacement: repaint reference_hd in this palette; same shapes and places')
        (folder/f'queue_entry_{tag}.json').write_text(json.dumps(entry,ensure_ascii=False,indent=1),encoding='utf-8')
        index.append(dict(rank=rank,folder=folder.name,palette=tag,image=image,parts=len(contract),mean_blotch=round(float(np.mean([c['blotch'] for c in contract])),3)))
    (OUT/'INDEX.json').write_text(json.dumps(dict(note=__doc__,packets=len(index),parts=sum(e['parts'] for e in index),packets_list=index),ensure_ascii=False,indent=1),encoding='utf-8')
    print('packets',len(index),'parts',sum(e['parts'] for e in index),'images',len({e['image'] for e in index}))


if __name__=='__main__':main()
