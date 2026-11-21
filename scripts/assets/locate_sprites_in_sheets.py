"""Find, for every sprite of a unit's robot set, the original ROM part sheet and (u, v) it is cut from.

Searched: every package sheet in graphics/all_units/catalog.json (robot part sheets), exact index
match with flips. Writes <robot_set>/SPRITE_SOURCES.json: {hash: [resource, u, v]}.

  py -3.11 -X utf8 scripts/assets/locate_sprites_in_sheets.py 196
"""
import base64,json,sys,zlib
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g
_sheets=None


def sheets():
    global _sheets
    if _sheets is None:
        rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();off=g.archive(rom);_sheets={}
        for p in json.loads((ROOT/'graphics/all_units/catalog.json').read_text())['packages']:
            r=p['resource']
            try:_sheets[r]=g.pixels(g.decompress(rom[g.BASE+off[r]:g.BASE+off[r+1]]))
            except Exception:pass
    return _sheets


def find(idx,prefer=()):
    h,w=idx.shape;key=idx.tobytes()
    order=list(prefer)+[r for r in sheets() if r not in prefer]
    for r in order:
        s=sheets().get(r)
        if s is None or s.shape[0]<h or s.shape[1]<w:continue
        # candidate positions: rows whose first row matches
        first=idx[0].tobytes()
        for v in range(0,s.shape[0]-h+1):
            line=s[v]
            for u in range(0,s.shape[1]-w+1):
                if line[u:u+w].tobytes()==first and s[v:v+h,u:u+w].tobytes()==key:return [r,u,v]
    return None


def main():
    uid=int(sys.argv[1]);rs=ROOT/f'test_current/parts/pose_packets/unit_{uid}/robot_set'
    cat=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text(encoding='utf-8'))
    prim=next(u for u in cat['units'] if u['unit_id']==uid)['primary_image'];prefer=[prim]
    rows={}
    for c in rs.glob('pose_*/contract.json'):
        for r in json.loads(c.read_text(encoding='utf-8')):rows.setdefault(r['hash'],r)
    out={}
    for h,r in rows.items():
        idx=np.frombuffer(zlib.decompress(base64.b64decode(r['index_pixels'])),dtype='uint8').reshape(r['h'],r['w'])
        if not (idx>0).any():continue
        f=find(idx,prefer)
        if f and f[0] not in prefer:prefer.append(f[0])
        out[str(h)]=f
    (rs/'SPRITE_SOURCES.json').write_text(json.dumps(out,indent=0),encoding='utf-8')
    found=[v for v in out.values() if v]
    print('unit',uid,'sprites',len(out),'located',len(found),'sheets',sorted({v[0] for v in found}))


if __name__=='__main__':main()
