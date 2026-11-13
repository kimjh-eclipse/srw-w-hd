"""Require long SCR identity for every resource-backed cut-in, not blank prefixes.

Texture RAM survives animation changes. A matching IMG probe plus a blank
16-cell map prefix is insufficient evidence that the picture is still active.
"""
import json,struct,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g
from scripts.assets.install_pilot_cutins import fnv


def main():
    path=ROOT/'graphics/cutins_library.json';library=json.loads(path.read_text())
    inventory=json.loads((ROOT/'test_current/parts/cutin_bank/inventory.json').read_text())['images']
    maps={r['image']:r['map'] for r in inventory if r.get('map') is not None}
    descriptors={r['image']:r for r in inventory}
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    rows=[];skipped=[]
    for item in library['cutins']:
        resource=item.get('source_map',maps.get(item.get('resource')))
        if resource is None:skipped.append(dict(id=item['id'],reason='no verified source SCR'));continue
        data=g.decompress(rom[g.BASE+offsets[resource]:g.BASE+offsets[resource+1]])
        assert data[:3]==b'SCR',(resource,data[:8])
        count=min(512,(len(data)-8)//2)
        entries=struct.unpack_from(f'<{count}H',data,8)
        packed=b''.join(struct.pack('<H',value&0xfff) for value in entries)
        if item.get('map_signature') not in (None,fnv(packed[:32])):
            skipped.append(dict(id=item['id'],resource=resource,reason='source prefix differs; retained existing validated signature'));continue
        assert count>16,(resource,count)
        item.update(source_map=resource,map_signature=fnv(packed[:32]),map_window_signature=fnv(packed),map_window_entries=count)
        descriptor=descriptors.get(item.get('resource'),{})
        if descriptor.get('size')==[256,256] and descriptor.get('opaque')==65536:
            item['repeat_native_plane']=True
        rows.append(dict(id=item['id'],resource=item.get('resource'),map_resource=resource,entries=count))
    path.write_text(json.dumps(library,indent=2))
    out=ROOT/'test_current/combat/foreground';out.mkdir(exist_ok=True)
    report=dict(guarded=len(rows),skipped=skipped,rows=rows)
    (out/'all_cutin_map_guards.json').write_text(json.dumps(report,indent=2));print('Guarded',len(rows),'Skipped',skipped)


if __name__=='__main__':main()
