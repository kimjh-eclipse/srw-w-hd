"""Reuse approved art only after an exact observed hardware-index comparison."""
import json,zlib,hashlib,sys
from pathlib import Path
from functools import lru_cache
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import srw_graphics as g
from audit_missing_parts import SIZES
ROOT=g.ROOT;FOLDER=ROOT/'test_current/attract/observed_parts'

def main():
    path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text());bindings=meta['bindings'];prefix=hashlib.sha256(json.dumps(bindings[:5263],sort_keys=True).encode()).hexdigest()
    records=json.loads((FOLDER/'records.json').read_text())
    # Include the exact raised-arm pose reported by the user, captured earlier.
    for p in json.loads((FOLDER.parent/'obj_8910.json').read_text()):
        if p['y']>=120:continue
        raw=np.load(FOLDER.parent/'obj_8910.npz');from audit_missing_parts import decode
        _,_,idx,im,_,colors=decode(raw['vram'].tobytes(),raw['palette'][512:1024].tobytes(),p['a'],p['b'],p['c'],int.from_bytes(raw['regs'][:4].tobytes(),'little'))
        im.save(FOLDER/f"{p['hash']:08x}.png");np.save(FOLDER/f"{p['hash']:08x}.npy",idx)
        records.append(dict(hash=p['hash'],index_hash=p['index_hash'],w=p['w'],h=p['h'],first=8910,last=8910,count=1,palette_rgb=np.stack([(colors&31)*255//31,((colors>>5)&31)*255//31,((colors>>10)&31)*255//31],-1).tolist()))
    known={b['hash'] for b in bindings if b.get('rgb_enabled',True) and not b.get('disabled')};active={b.get('index_hash') for b in bindings if b.get('dynamic_palette') and b.get('indexed_safe',True) and not b.get('disabled')}-set(meta.get('indexed_collision_keys',[]))
    needed={};observed={}
    for r in records:
        if r['hash'] in known or r['index_hash'] in active:continue
        needed.setdefault(r['index_hash'],[]).append(r);observed[r['index_hash']]=np.load(FOLDER/f"{r['hash']:08x}.npy")
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    @lru_cache(maxsize=512)
    def pixels(i):return g.pixels(g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]]))
    packages={p['resource']:p for p in json.loads((ROOT/'graphics/all_units/catalog.json').read_text())['packages']};sources=[]
    for batch in json.loads((ROOT/'graphics/all_units/batches.json').read_text())['batches']:
        if not batch.get('required'):continue
        for s in batch['segments']:
            if s['resource']==7406:continue
            sources.append((pixels(s['resource']), 'all_'+batch['name'],0,s['batch_y'],packages[s['resource']]['palette_rgb']))
    for sheet in json.loads((ROOT/'graphics/animation_parts/late_attack_sheets.json').read_text())['sheets']:
        for s in sheet['segments']:sources.append((pixels(s['resource']),sheet['name'],s['x'],s['y'],s['palette_rgb']))
    for sheet in json.loads((ROOT/'graphics/animation_parts/basic_extra_sheets.json').read_text())['sheets']:
        for s in sheet['parts']:sources.append((pixels(s['image'])[s['y']:s['y']+s['h'],s['x']:s['x']+s['w']],sheet['name'],s['atlas_x'],s['atlas_y'],s['palette_rgb']))
    added=0;matches=[]
    for idx,atlas,ax,ay,palette in sources:
        height,width=idx.shape;encoded=np.where(idx,idx.astype('uint16')|0x8000,0).astype('<u2')
        for w,h in { (r['w'],r['h']) for group in needed.values() for r in group }:
            for y in range(0,height-h+1,8):
                for x in range(0,width-w+1,8):
                    key=zlib.crc32(encoded[y:y+h,x:x+w].tobytes())^(w<<16)^h
                    if key not in needed or not np.array_equal(observed[key],idx[y:y+h,x:x+w]):continue
                    used=np.unique(observed[key]);used=used[used!=0]
                    if len(used)<3 or np.count_nonzero(observed[key])<16:continue
                    for r in needed.pop(key):
                        if r['hash'] in known:continue
                        bindings.append(dict(hash=r['hash'],index_hash=key,x=ax+x,y=ay+y,w=w,h=h,atlas_id=atlas,original_palette_rgb=palette,palette_rgb=r['palette_rgb'],observed_reuse=True,dynamic_palette=False,indexed_safe=False))
                        known.add(r['hash']);added+=1
                    matches.append(dict(index_hash=key,atlas=atlas,x=ax+x,y=ay+y))
        if not needed:break
    assert prefix==hashlib.sha256(json.dumps(bindings[:5263],sort_keys=True).encode()).hexdigest()
    path.write_text(json.dumps(meta,indent=2))
    (FOLDER/'remaining.json').write_text(json.dumps([r for group in needed.values() for r in group],indent=2))
    result=dict(added_bindings=added,exact_patterns=len(matches),remaining_patterns=len(needed),total_bindings=len(bindings),prefix_preserved=True)
    (FOLDER/'reuse.json').write_text(json.dumps(dict(**result,matches=matches),indent=2));print(json.dumps(result))

if __name__=='__main__':main()
