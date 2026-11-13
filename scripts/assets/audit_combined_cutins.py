"""Find exact ROM source tiles for simultaneous pilot cut-ins in captured BGs."""
import argparse,json,sys,zlib
from pathlib import Path
from collections import defaultdict,Counter
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--folder',default='test_current/combat/named_attacks/unit_297/diagnostic_preview/weapon_1213_capture')
    parser.add_argument('--frame',default='360');parser.add_argument('--layers',default='1,2')
    args=parser.parse_args();folder=ROOT/args.folder;selected_layers=tuple(map(int,args.layers.split(',')))
    targets=defaultdict(list);details={}
    for layer in selected_layers:
        with np.load(folder/f'bg_{args.frame}_{layer}.npz') as data:
            cnt,_,_,_,_,w,h,_,_=map(int,data['info']);assert not cnt&128
            entries=np.frombuffer(data['map'].tobytes(),dtype='<u2');raw=data['tiles'];used=set()
            for y in range(16):
                for x in range(32):used.add(int(entries[(y//32*(w//256)+x//32)*1024+(y%32)*32+x%32])&1023)
            for tile in used:
                packed=raw[tile*32:(tile+1)*32];pixels=np.stack([packed&15,packed>>4],-1).reshape(8,8)
                if np.count_nonzero(pixels)<12 or len(np.unique(pixels))<3:continue
                blob=pixels.tobytes();targets[zlib.crc32(blob)].append((layer,tile,blob))
            details[layer]=dict(width=w,height=h,referenced_tiles=len(used))
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    catalog=json.loads((ROOT/'test_current/rom_catalog/catalog.json').read_text())['records'];matches=defaultdict(list)
    for count,record in enumerate(r for r in catalog if r['kind']=='IMG'):
        resource=record['id']
        try:a=g.pixels(g.decompress(rom[g.BASE+offsets[resource]:g.BASE+offsets[resource+1]]))
        except (ValueError,IndexError,AssertionError):continue
        if a.max()>15:continue
        for y in range(0,a.shape[0]-7,8):
            for x in range(0,a.shape[1]-7,8):
                blob=a[y:y+8,x:x+8].tobytes()
                for layer,tile,expected in targets.get(zlib.crc32(blob),[]):
                    if blob==expected:matches[(layer,resource)].append(dict(tile=tile,x=x,y=y))
        if count%2000==0:print('scanned IMG',count,flush=True)
    known=defaultdict(list)
    for row in json.loads((ROOT/'graphics/cutins_library.json').read_text())['cutins']:
        if row.get('resource') is not None:known[row['resource']].append(row['id'])
    result=[]
    for layer in selected_layers:
        candidates=[]
        for (which,resource),tiles in matches.items():
            if which!=layer:continue
            origins=Counter((t['tile']%32*8-t['x'],t['tile']//32*8-t['y']) for t in tiles)
            candidates.append(dict(resource=resource,exact_distinct_tiles=len({t['tile'] for t in tiles}),known_cutins=known[resource],origins=[dict(x=x,y=y,tiles=n) for (x,y),n in origins.most_common(3)],matches=tiles))
        candidates.sort(key=lambda r:-r['exact_distinct_tiles']);result.append(dict(layer=layer,**details[layer],candidates=candidates[:25]))
    (folder/'source_audit.json').write_text(json.dumps(dict(scope=__doc__,layers=result),indent=2))
    print(json.dumps([{**{k:v for k,v in r.items() if k!='candidates'},'best':[{k:v for k,v in c.items() if k!='matches'} for c in r['candidates'][:5]]} for r in result]))

if __name__=='__main__':main()
