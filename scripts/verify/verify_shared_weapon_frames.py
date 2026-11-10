"""Require all shared punch IMG frames to assemble from exact painted texels."""
import json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g
from tile_compositor import TileCompositor

def main():
    folder=ROOT/'graphics/shared_weapon_frames';plan=json.loads((folder/'plan.json').read_text())
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom);compositor=TileCompositor();rows=[]
    for sheet in plan['sheets']:
        for item in sheet['items']:
            resource=item['resource'];a=g.pixels(g.decompress(rom[g.BASE+offsets[resource]:g.BASE+offsets[resource+1]]))
            if not a.any():rows.append(dict(resource=resource,empty_native_frame=True));continue
            q=np.rint(np.asarray(item['palette_rgb'],dtype='float64')*31/255).astype('uint16');palette=q[:,0]|q[:,1]<<5|q[:,2]<<10
            art,stats=compositor.assemble(a,palette);assert art is not None,(resource,stats)
            rows.append(dict(resource=resource,exact_tiles=stats['exact_tiles'],source_resources=sorted({compositor.source(group['source'])[0]['resource'] for group in stats['tile_groups']})))
    result=dict(scope=__doc__,native_frames=len(rows),nonempty_verified=sum(not r.get('empty_native_frame') for r in rows),all_campaign_attacks_verified=False,rows=rows)
    (folder/'coverage.json').write_text(json.dumps(result,indent=2));print(json.dumps(dict(native_frames=len(rows),nonempty_verified=result['nonempty_verified'])))

if __name__=='__main__':main()
