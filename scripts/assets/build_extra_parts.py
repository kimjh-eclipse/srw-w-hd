"""Append observed extra textures and native palette variants without changing
existing binding IDs, the repaired face, or the base atlas.
"""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import json,zlib,sys
import numpy as np

ROOT=PROJECT_ROOT
def main():
    path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text());bindings=meta['bindings'];known={b['hash'] for b in bindings}
    manifest_path=ROOT/'graphics/kazuma_extra_parts_manifest.json'
    if manifest_path.exists():
        manifest=json.loads(manifest_path.read_text())
    else:
        manifest=dict(parts=json.loads((ROOT/'test_current/parts/extra_parts_plan.json').read_text()),palette_variants=json.loads((ROOT/'test_current/parts/palette_alias_candidates.json').read_text()))
        manifest_path.write_text(json.dumps(manifest,indent=2))
    plan=manifest['parts']
    if 'source_palette' not in manifest:
        manifest['source_palette']=np.frombuffer((ROOT/'test_current/robot/pal_65340.bin').read_bytes(),'<u2')[:16].astype('uint32').tolist()
    if '--import-audit' in sys.argv:
        raw=np.frombuffer((ROOT/'test_current/robot/vram_65340.bin').read_bytes()[:16384],dtype='uint8')
        idx=np.stack([raw&15,raw>>4],-1).reshape(16,32,8,8).transpose(0,2,1,3).reshape(128,256)
        pixels=np.where(idx!=0,idx.astype('uint16')|0x8000,0).astype('<u2');lookup={}
        for i,b in enumerate(bindings,1):
            if b.get('atlas_id') or b.get('source_binding'):continue
            x,y,w,h=[b[k] for k in ('x','y','w','h')]
            lookup.setdefault(zlib.crc32(pixels[y:y+h,x:x+w].copy().tobytes())^(w<<16)^h,i)
        by_hash={b['hash']:i for i,b in enumerate(bindings,1)}
        for b in plan['new']:lookup[b['index_hash']]=by_hash[b['hash']]
        aliases={a['hash']:a for a in manifest['palette_variants']}
        for record in json.loads((ROOT/'test_current/parts/missing_parts.json').read_text()):
            if record['hash'] not in known and record['index_hash'] in lookup:
                aliases[record['hash']]=dict(record,source_binding=lookup[record['index_hash']])
        manifest['palette_variants']=list(aliases.values())
    manifest_path.write_text(json.dumps(manifest,indent=2))
    meta.setdefault('atlases',{})['extra']=dict(image='kazuma_extra_parts_hd.png',reference='kazuma_extra_parts_reference.png',native_size=plan['native_size'])
    for record in plan['existing']:
        if record['hash'] not in known:
            bindings.append({k:record[k] for k in ('hash','x','y','w','h')});known.add(record['hash'])
    for record in plan['new']:
        if record['hash'] not in known:
            bindings.append(dict(hash=record['hash'],x=record['atlas_x'],y=record['atlas_y'],w=record['w'],h=record['h'],atlas_id='extra'));known.add(record['hash'])
    source=np.array(manifest['source_palette'],dtype='uint32')
    def rgb(values):
        values=np.asarray(values,dtype='uint32');return np.stack([(values&31)*255//31,((values>>5)&31)*255//31,((values>>10)&31)*255//31],-1).astype('uint8').tolist()
    meta['source_palette_rgb']=rgb(source)
    aliases=manifest['palette_variants']
    for record in aliases:
        if record['hash'] in known:continue
        base=bindings[record['source_binding']-1]
        bindings.append(dict(hash=record['hash'],x=base['x'],y=base['y'],w=base['w'],h=base['h'],source_binding=record['source_binding'],palette_rgb=rgb(record['palette_colors'])))
        known.add(record['hash'])
    path.write_text(json.dumps(meta,indent=2));print(json.dumps(dict(bindings=len(bindings),extra_art=sum(b.get('atlas_id')=='extra' for b in bindings),palette_variants=sum('source_binding' in b for b in bindings))))

if __name__=='__main__':main()
