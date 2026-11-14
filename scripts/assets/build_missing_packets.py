"""Turn the ROM-wide list of parts without HD art into drawing packets.

Reads test_current/parts/missing_export/report.json (written by
export_missing_parts.py) and writes, for every source image and palette bank
that still has unconnected parts, a folder under
test_current/parts/missing_packets/ holding:

* native_bank<B>.png - the whole source image in that bank's 16 colours at
  native size (index 0 transparent). This is the reference the installer
  checks every part against, so it is exactly the ROM pixels and palette.
* contract_bank<B>.json - one row per unconnected part: atlas_box (= its
  rectangle in the image), raw indices, the bank's 16 BGR555 colours, both
  hashes, ROM resource and position. Each (shape, colour) key appears once in
  the whole packet set, so connecting a packet never duplicates a binding.
* queue_entry_bank<B>.json - the ready_candidates entry (bindings: [] plus
  new_source_keys) to append to docs/PENDING_ART_INSTALL_QUEUE.json once the
  drawing exists; only the file hashes are left for the drawer to fill.
* missing_bank<B>.png - the native image enlarged 4x with the unconnected
  rectangles outlined, for orientation only.

The drawer paints candidate_bank<B>.png (4x the native image, RGBA) and lists
the packet. Parts not seen in any retained scene use the ROM palette; the
packet says so (actual_observed false). Reads only the ROM and the report.
"""
import argparse,base64,json,shutil,sys,zlib
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image,ImageDraw
from scripts.assets import srw_graphics as g

OUT=ROOT/'test_current/parts/missing_packets'


def main():
    parser=argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--limit',type=int,default=0,help='write only the first N packets in priority order')
    parser.add_argument('--min-opaque',type=int,default=64,help='leave out parts with fewer painted texels (small dots gain nothing from HD art; they stay native)')
    args=parser.parse_args()
    report=json.loads((ROOT/'test_current/parts/missing_export/report.json').read_text(encoding='utf-8'))
    library=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text(encoding='utf-8'))['bindings']
    active={b['hash'] for b in library if b.get('rgb_enabled',True) and not b.get('disabled')}
    rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();offsets=g.archive(rom)
    resource=lambda i:g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    OUT.mkdir(parents=True,exist_ok=True)
    taken=set();packets=[];skipped=defaultdict(int)
    for image in report['images']:
        pixels=g.pixels(resource(image['image']))
        full=np.frombuffer(resource(image['palette'])[8:],dtype='<u2') if image['palette'] is not None else None
        by_bank=defaultdict(list)
        for m in image['missing']:by_bank[m['bank']].append(m)
        for bank,parts in sorted(by_bank.items()):
            if full is None:skipped['no palette']+=len(parts);continue
            # Same palette choice as export_missing_parts.py, which produced the hashes.
            colours=np.asarray(full[bank*16:(bank+1)*16],dtype='<u2')
            rows=[]
            for m in parts:
                x,y,w,h=m['x'],m['y'],m['w'],m['h'];part=pixels[y:y+h,x:x+w]
                if m['opaque']<args.min_opaque:skipped[f'fewer than {args.min_opaque} painted texels']+=1;continue
                if int(part.max())>15:skipped['more than 16 colours']+=1;continue
                if len(colours)<=int(part.max()):colours=np.asarray(full[:16],dtype='<u2')
                if len(colours)<=int(part.max()) or m['hash'] is None:skipped['palette shorter than the indices']+=1;continue
                if len(colours)<16:colours=np.concatenate([colours,np.zeros(16-len(colours),dtype='<u2')])
                mask=part>0
                ih=zlib.crc32(np.where(mask,part.astype('uint16')|0x8000,0).astype('<u2').tobytes())^(w<<16)^h
                rgb=zlib.crc32(np.where(mask,colours[part]|0x8000,0).astype('<u2').tobytes())^(w<<16)^h
                if (ih,rgb)!=(m['index_hash'],m['hash']):skipped['hash differs from report']+=1;continue
                if rgb in active:skipped['connected since the report']+=1;continue
                if rgb in taken:skipped['same key in another packet']+=1;continue
                taken.add(rgb)
                rows.append(dict(slot=len(rows),hash=int(rgb),index_hash=int(ih),atlas_box=[x,y,w,h],source_box=[x,y,w,h],
                    index_pixels=base64.b64encode(zlib.compress(part.astype('uint8').tobytes())).decode(),
                    actual_palette_bgr555=[int(v) for v in colours],actual_palette_rgb=[[int(v&31)*255//31,int((v>>5)&31)*255//31,int((v>>10)&31)*255//31] for v in colours],
                    resource=image['image'],source_x=x,source_y=y,w=w,h=h,spec=dict(resource=image['image'],source_x=x,source_y=y),
                    source_palette_resource=image['palette'],source_palette_bank=bank,render_mode='static',effect_part=not image['units'],
                    actual_observed=bool(m.get('seen')),opaque_texels=m['opaque']))
            if not rows:continue
            packets.append(dict(image=image,bank=bank,rows=rows,colours=colours,pixels=pixels,seen=sum((m.get('seen') or {}).get('frames',0) for m in parts)))
    packets.sort(key=lambda p:(-p['seen'],-int(p['image']['in_test_window']),-sum(r['opaque_texels'] for r in p['rows'])))
    if args.limit:packets=packets[:args.limit]
    index=[]
    for rank,p in enumerate(packets,1):
        image=p['image'];bank=p['bank'];folder=OUT/f"img{image['image']:05d}";folder.mkdir(exist_ok=True)
        rgba=np.zeros((*p['pixels'].shape,4),dtype='uint8');idx=np.minimum(p['pixels'],15);mask=p['pixels']>0
        value=p['colours'][idx].astype('uint32')
        rgba[...,0]=(value&31)*255//31;rgba[...,1]=((value>>5)&31)*255//31;rgba[...,2]=((value>>10)&31)*255//31;rgba[...,3]=np.where(mask,255,0)
        rgba[~mask]=0;native=Image.fromarray(rgba);native.save(folder/f'native_bank{bank}.png')
        guide=native.resize((native.width*4,native.height*4),Image.Resampling.NEAREST);draw=ImageDraw.Draw(guide)
        for r in p['rows']:
            x,y,w,h=r['atlas_box'];draw.rectangle((x*4,y*4,(x+w)*4-1,(y+h)*4-1),outline=(255,40,40,255))
        guide.save(folder/f'missing_bank{bank}.png')
        (folder/f'contract_bank{bank}.json').write_text(json.dumps(p['rows'],ensure_ascii=False),encoding='utf-8')
        entry=dict(source=str((folder).relative_to(ROOT)).replace('\\','/'),contract=f'contract_bank{bank}.json',drawing=f'candidate_bank{bank}.png',native=f'native_bank{bank}.png',
            generated=f'generated_bank{bank}.png',bindings=[],new_source_keys=[dict(hash=r['hash'],index_hash=r['index_hash']) for r in p['rows']],
            file_sha256=dict(contract=None,drawing=None,native=None,generated=None),note='')
        (folder/f'queue_entry_bank{bank}.json').write_text(json.dumps(entry,ensure_ascii=False,indent=1),encoding='utf-8')
        index.append(dict(rank=rank,folder=folder.name,bank=bank,image=image['image'],palette=image['palette'],size=image['size'],parts=len(p['rows']),
            opaque_texels=sum(r['opaque_texels'] for r in p['rows']),units=[u.get('name') for u in image['units']],likely_effect=not image['units'],
            seen_in_scenes=bool(p['seen']),in_test_window=image['in_test_window']))
    summary=dict(note='Drawing packets for parts without HD art, one per source image and palette bank, in priority order (seen in retained scenes, then selectable in the test window, then painted area).',
        packets=len(index),images=len({e['image'] for e in index}),parts=sum(e['parts'] for e in index),seen_packets=sum(e['seen_in_scenes'] for e in index),skipped=dict(skipped),packets_list=index)
    (OUT/'INDEX.json').write_text(json.dumps(summary,ensure_ascii=False,indent=1),encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k!='packets_list'},ensure_ascii=False,indent=1))


if __name__=='__main__':main()
