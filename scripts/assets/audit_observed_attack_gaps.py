"""Associate actual unmatched attack textures with exact ROM tiles, read-only."""
import sys,json,zlib,sqlite3
from pathlib import Path
from collections import Counter,defaultdict
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g

def main():
    base=ROOT/'test_current/combat/named_attacks';out=ROOT/'test_current/parts/observed_attack_gaps';out.mkdir(exist_ok=True)
    wanted=set();rows=[];seen=set();examples={};tile_bytes={}
    for path in sorted(base.glob('unit_*/report.json')):
        for row in json.loads(path.read_text(encoding='utf-8'))['rows']:
            rows.append(row)
            missing={tuple(map(int,k.strip('()').split(','))):v for k,v in row.get('new_unmapped_textures',{}).items()}
            wanted.update(t for v in missing.values() for t in v.get('missing_tiles',[]))
            capture=path.parent/f'unit_{row["unit_id"]}_weapon_{row["weapon_id"]}_unknown.npz'
            if not capture.exists():continue
            with np.load(capture) as data:
                for raw,pix,pal in zip(data['rows'],data['pixels'],data['palettes']):
                    identity=(int(raw[0]),int(raw[7]))
                    if identity not in missing or identity in seen:continue
                    seen.add(identity);w,h=map(int,raw[1:3]);indices=pix[:w*h].reshape(h,w).copy()
                    examples[identity]=(indices,pal.copy(),row['unit_id'],row['weapon_id'],missing[identity])
                    for y in range(0,h,8):
                        for x in range(0,w,8):
                            tile=indices[y:y+8,x:x+8].tobytes();crc=zlib.crc32(tile)
                            if crc in missing[identity].get('missing_tiles',[]):tile_bytes[crc]=tile
    print('native cases',len(rows),'unmatched rectangles',len(examples),'tile hashes',len(wanted),flush=True)
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    catalog=json.loads((ROOT/'test_current/rom_catalog/catalog.json').read_text())['records']
    matches=defaultdict(set)
    for count,record in enumerate(r for r in catalog if r['kind']=='IMG'):
        identifier=record['id']
        try:a=g.pixels(g.decompress(rom[g.BASE+offsets[identifier]:g.BASE+offsets[identifier+1]]))
        except (ValueError,IndexError,AssertionError):continue
        if a.max()>15:continue
        for y in range(0,a.shape[0]-7,8):
            for x in range(0,a.shape[1]-7,8):
                raw=a[y:y+8,x:x+8].tobytes();crc=zlib.crc32(raw)
                if crc in wanted and (crc not in tile_bytes or raw==tile_bytes[crc]):matches[crc].add(identifier)
        if count%500==0:print('IMG scanned',count,'matched missing tiles',len(matches),flush=True)
    db=sqlite3.connect((ROOT/'graphics/parts_tile_library.sqlite').as_uri()+'?mode=ro',uri=True)
    painted={json.loads(r[0]).get('resource') for r in db.execute('SELECT description FROM sources')};db.close()
    records=[];cards=[]
    for identity,(indices,pal,uid,wid,miss) in examples.items():
        votes=Counter(r for tile in miss.get('missing_tiles',[]) for r in matches.get(tile,()))
        candidates=[dict(resource=r,matched_missing_tiles=n,already_in_tile_library=r in painted) for r,n in votes.most_common(8)]
        opaque=int(np.count_nonzero(indices));h,w=indices.shape
        records.append(dict(index_hash=identity[0],material_hash=identity[1],unit_id=uid,weapon_id=wid,w=w,h=h,opaque=opaque,candidates=candidates,missing_tiles=miss.get('missing_tiles',[])))
        colors=np.asarray(pal,dtype='uint32');rgb=np.stack([(colors&31)*255//31,((colors>>5)&31)*255//31,((colors>>10)&31)*255//31],-1).astype('uint8')
        im=Image.fromarray(np.dstack([rgb[indices],(indices!=0).astype('uint8')*255]));im=im.resize((w*3,h*3),Image.Resampling.NEAREST);im.thumbnail((128,100),Image.Resampling.NEAREST)
        card=Image.new('RGB',(160,132),'#303b47');card.paste(im,(0,0),im);draw=ImageDraw.Draw(card);draw.text((2,102),f'{identity[0]:08x} u{uid}',fill='white');draw.text((2,116),'IMG '+','.join(str(c['resource']) for c in candidates[:3]),fill='white');cards.append((opaque,identity,card))
    cards.sort(key=lambda c:(-c[0],c[1]));
    for page in range((len(cards)+63)//64):
        sheet=Image.new('RGB',(1280,1056),'#303b47')
        for n,(_,_,card) in enumerate(cards[page*64:page*64+64]):sheet.paste(card,(n%8*160,n//8*132))
        sheet.save(out/f'contact_{page:02}.png')
    report=dict(scope=__doc__,attempted=len(rows),completed_replays=sum(r.get('full_replay_verified',False) for r in rows),
                failed_replays=[dict(unit_id=r['unit_id'],weapon_id=r['weapon_id'],reason=r.get('blocked_reason') or ('not_started' if not r['battle_started'] else 'unfinished')) for r in rows if not r.get('full_replay_verified')],
                distinct_missing_tiles=len(wanted),matched_rom_tiles=len(matches),unmatched_rectangles=records,
                rom_tile_matches={str(k):sorted(v) for k,v in matches.items()})
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('associated rectangles',len(records),'contact pages',(len(cards)+63)//64,flush=True)

if __name__=='__main__':main()
