"""List every ROM animation part that has no HD art and export its native dots.

Walks every PAT record of the ROM (the same parsing catalog_named_units.py
uses for a unit's primary pattern), takes each distinct rectangle of the
pattern's image, and checks whether the part library has art for it by tile
shape or by colour. Parts without art are written out per image as an
enlarged native sheet with the missing rectangles outlined, plus a list
ordered by how much they are seen in the retained battle scenes.

Limits: only the pattern's first image is read (patterns that span several
images are counted separately), and BG-layer pictures are not OBJ parts and
are not covered here. Reads only; writes test_current/parts/missing_export/.
"""
import argparse,json,struct,sys,zlib
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image,ImageDraw
from scripts.assets import srw_graphics as g


def main():
    parser=argparse.ArgumentParser(description=__doc__.split('\n')[0]);parser.add_argument('--sheets',type=int,default=300);args=parser.parse_args()
    out=ROOT/'test_current/parts/missing_export';out.mkdir(parents=True,exist_ok=True)
    for old in out.glob('*'):
        if old.is_file():old.unlink()
    rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();offsets=g.archive(rom)
    resource=lambda i:g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    patterns=json.loads((ROOT/'test_current/rom_catalog/animation_audit.json').read_text(encoding='utf-8'))['patterns']
    library=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text(encoding='utf-8'))
    rgb={b['hash'] for b in library['bindings'] if b.get('rgb_enabled',True) and not b.get('disabled')}
    indexed={b.get('index_hash') for b in library['bindings'] if b.get('dynamic_palette') and b.get('indexed_safe',True) and not b.get('disabled')}-set(library.get('indexed_collision_keys',[]))
    catalog=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text(encoding='utf-8'))
    owner=defaultdict(list)
    for unit in catalog['units']:
        for image in (unit.get('primary_image'),unit.get('secondary_image')):
            if image is not None:owner[image].append(unit['unit_id'])
    names={u['unit_id']:(u.get('name_ko') or u['name_ja']) for u in catalog['units']}
    scene_units={int(p.name[5:]) for p in (ROOT/'test_current/combat/named_attacks').glob('unit_*') if p.name[5:].isdigit()}
    seen_frames={}
    gaps=ROOT/'test_current/combat/runtime_path/coverage_all/gaps.json'
    if gaps.exists():
        for row in json.loads(gaps.read_text(encoding='utf-8'))['parts']:seen_frames[row['index_hash']]=dict(frames=row['frames'],scenes=sorted(row['scenes'])[:6])
    images={};totals=dict(patterns=len(patterns),patterns_read=0,patterns_spanning_images=0,pattern_errors=0,rectangles=0,out_of_bounds=0,covered=0,missing=0,missing_tiny=0)
    distinct={}
    for pattern in patterns:
        if len(pattern.get('image_group',[]))>1:totals['patterns_spanning_images']+=1
        image=pattern['image'];palette_id=pattern.get('palette')
        try:
            pixels=g.pixels(resource(image));pat=resource(pattern['pattern'])
            palette=np.frombuffer(resource(palette_id)[8:],dtype='<u2') if palette_id is not None else np.zeros(16,dtype='<u2')
            count=struct.unpack_from('<I',pat,4)[0];seen=set()
            for pose in range(count):
                off=struct.unpack_from('<I',pat,8+pose*4)[0];n=struct.unpack_from('<H',pat,off)[0];off+=2
                for _ in range(n):
                    flags=struct.unpack_from('<H',pat,off)[0];off+=2
                    if flags&0x2000:off+=4
                    tile=struct.unpack_from('<H',pat,off)[0];off+=2
                    if flags&0x4000:off+=4
                    if flags&0x8000:off+=2
                    w=8<<(flags&3);h=8<<((flags>>2)&3);x=(tile&4095)%32*8;y=(tile&4095)//32*8;bank=tile>>12;seen.add((x,y,w,h,bank))
        except Exception:
            totals['pattern_errors']+=1;continue
        totals['patterns_read']+=1;entry=images.setdefault(image,dict(image=image,pattern=pattern['pattern'],palette=palette_id,size=[int(pixels.shape[1]),int(pixels.shape[0])],rectangles=0,covered=0,missing=[]))
        for x,y,w,h,bank in sorted(seen):
            totals['rectangles']+=1
            if x+w>pixels.shape[1] or y+h>pixels.shape[0]:totals['out_of_bounds']+=1;continue
            part=pixels[y:y+h,x:x+w];opaque=int(np.count_nonzero(part))
            if not opaque:continue
            index_hash=zlib.crc32(np.where(part,part.astype('uint16')|0x8000,0).astype('<u2').tobytes())^(w<<16)^h
            colours=palette[bank*16:(bank+1)*16]
            if len(colours)<=int(part.max()):colours=palette[:16]
            colour_hash=zlib.crc32(np.where(part,colours[part]|0x8000,0).astype('<u2').tobytes())^(w<<16)^h if len(colours)>int(part.max()) else None
            entry['rectangles']+=1;key=(index_hash,colour_hash)
            if index_hash in indexed or colour_hash in rgb:
                entry['covered']+=1;totals['covered']+=1;distinct.setdefault(key,True);continue
            totals['missing']+=1;totals['missing_tiny']+=opaque<16;distinct[key]=False
            entry['missing'].append(dict(x=x,y=y,w=w,h=h,bank=bank,opaque=opaque,index_hash=index_hash,hash=colour_hash,seen=seen_frames.get(index_hash)))
    rows=[]
    for image,entry in images.items():
        if not entry['missing']:continue
        units=owner.get(image,[]);frames=sum((m['seen'] or {}).get('frames',0) for m in entry['missing'])
        rows.append(dict(image=image,pattern=entry['pattern'],palette=entry['palette'],size=entry['size'],units=[dict(id=u,name=names.get(u)) for u in units[:8]],
            in_test_window=bool(set(units)&scene_units),seen_frames=frames,rectangles=entry['rectangles'],missing_parts=len(entry['missing']),
            missing_opaque=sum(m['opaque'] for m in entry['missing']),missing=entry['missing']))
    rows.sort(key=lambda row:(-row['seen_frames'],-int(row['in_test_window']),-row['missing_opaque']))
    for rank,row in enumerate(rows[:args.sheets],1):
        try:
            pixels=g.pixels(resource(row['image']));palette=np.frombuffer(resource(row['palette'])[8:],dtype='<u2') if row['palette'] is not None else None
            canvas=np.zeros((*pixels.shape,3),dtype='uint8')+np.array([40,40,48],dtype='uint8')
            banks=np.zeros(pixels.shape,dtype='uint8')
            for m in row['missing']:banks[m['y']:m['y']+m['h'],m['x']:m['x']+m['w']]=m['bank']
            if palette is not None and len(palette)>=16:
                index=np.minimum(banks.astype('int32')*16+pixels,len(palette)-1);value=palette[index].astype('uint32')
                colour=np.stack([(value&31)*255//31,((value>>5)&31)*255//31,((value>>10)&31)*255//31],-1).astype('uint8');canvas[pixels>0]=colour[pixels>0]
            else:canvas[pixels>0]=(pixels[pixels>0,None]*16).astype('uint8')
            sheet=Image.fromarray(canvas).resize((pixels.shape[1]*4,pixels.shape[0]*4),Image.Resampling.NEAREST);draw=ImageDraw.Draw(sheet)
            for m in row['missing']:draw.rectangle((m['x']*4,m['y']*4,(m['x']+m['w'])*4-1,(m['y']+m['h'])*4-1),outline=(255,40,40))
            row['sheet']=f"image_{row['image']:05d}.png";sheet.save(out/row['sheet'])
        except Exception as error:row['sheet_error']=str(error)[:120]
    report=dict(totals=totals,distinct_parts=len(distinct),distinct_missing=sum(1 for v in distinct.values() if not v),images_with_patterns=len(images),images_with_missing_parts=len(rows),
        images_fully_missing=sum(1 for row in rows if row['missing_parts']==row['rectangles']),missing_seen_in_scenes=sum(1 for row in rows if row['seen_frames']),
        order='seen in retained scenes (frames), then units selectable in the test window, then missing opaque area',images=rows)
    (out/'report.json').write_text(json.dumps(report,indent=1,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='images'},indent=1,ensure_ascii=False))
    for row in rows[:20]:print(row['image'],'seen',row['seen_frames'],'test',row['in_test_window'],'missing',row['missing_parts'],'/',row['rectangles'],[u['name'] for u in row['units'][:3]])


if __name__=='__main__':main()
