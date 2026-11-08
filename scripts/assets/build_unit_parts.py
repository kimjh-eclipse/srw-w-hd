"""Install additional battle-part atlases and their observed palette variants."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import json,sys,math
import numpy as np
from PIL import Image

ROOT=PROJECT_ROOT
MANIFEST=ROOT/'graphics/unit_parts_manifest.json'
GROUPS={
 'valhawk_motion': [517061135,3737727271,858673778,4002610899,3681841241,56655502,3825100804,1087428907,1292123151,1396954835],
 'space_pirate': [3348799713,2802642178,2118558597,2401437050,1672101879,1608093832,2726322712,3270846021,2823991471,4087206072,1015830496,3735359036,3390420896,3752754464,4271280101,908993273,3477471526,1296290398,117151160,933183654,2120640899],
 'space_pirate_body': [3474533206,4097690812,267933028,2533926651,3757073245,3246487777,2745861844,642154062,3764066095,2159591607,1323133933,2955242735,41779406,2297591910],
}

def rgb(values):
    v=np.asarray(values,dtype='uint32')
    return np.stack([(v&31)*255//31,((v>>5)&31)*255//31,((v>>10)&31)*255//31],-1).astype('uint8').tolist()

def main():
    if '--prepare' in sys.argv:
        records=json.loads((ROOT/'test_current/parts/missing_parts.json').read_text());groups={}
        for name,keys in GROUPS.items():
            parts=[dict(next(r for r in records if r['hash']==key)) for key in keys]
            cw=max(p['w'] for p in parts);ch=32;cols=4;rows=math.ceil(len(parts)/cols)
            atlas=Image.new('RGBA',(cw*cols,ch*rows))
            for i,p in enumerate(parts):
                p.update(atlas_x=i%cols*cw,atlas_y=i//cols*ch)
                atlas.paste(Image.open(ROOT/f"test_current/parts/missing_{p['hash']:08x}.png"),(p['atlas_x'],p['atlas_y']))
            atlas.resize((atlas.width*8,atlas.height*8),Image.Resampling.NEAREST).save(ROOT/f'graphics/{name}_parts_reference.png')
            groups[name]=dict(native_size=list(atlas.size),cell=[cw,ch],parts=parts)
        MANIFEST.write_text(json.dumps(dict(groups=groups,observed=records),indent=2));return
    manifest=json.loads(MANIFEST.read_text());path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text())
    bindings=meta['bindings'];known={b['hash']:i for i,b in enumerate(bindings,1)};lookup={}
    for name,group in manifest['groups'].items():
        assert (ROOT/f'graphics/{name}_parts_hd.png').exists()
        meta.setdefault('atlases',{})[name]=dict(image=f'{name}_parts_hd.png',reference=f'{name}_parts_reference.png',native_size=group['native_size'])
        for p in group['parts']:
            if p['hash'] not in known:
                bindings.append(dict(hash=p['hash'],x=p['atlas_x'],y=p['atlas_y'],w=p['w'],h=p['h'],atlas_id=name,unit=name,original_palette_rgb=rgb(p['palette_colors'])))
                known[p['hash']]=len(bindings)
            lookup[p['index_hash']]=known[p['hash']]
    variants=0
    for p in manifest['observed']:
        if p['hash'] in known or p['palette'] not in (0,1,13) or p['index_hash'] not in lookup:continue
        source_id=lookup[p['index_hash']];source=bindings[source_id-1]
        bindings.append(dict(hash=p['hash'],x=source['x'],y=source['y'],w=source['w'],h=source['h'],unit=source['unit'],source_binding=source_id,palette_rgb=rgb(p['palette_colors']),palette_source_rgb=source['original_palette_rgb']))
        known[p['hash']]=len(bindings);variants+=1
    path.write_text(json.dumps(meta,indent=2));print(json.dumps(dict(bindings=len(bindings),new_variants=variants,groups={k:len(v['parts']) for k,v in manifest['groups'].items()})))

if __name__=='__main__':main()
