"""Verify a compound rectangle and first-seen black fade keep HD detail."""
import base64,json,zlib
import numpy as np
from hd_core import ROOT
from tile_compositor import TileCompositor
import texture_preparation as tasks
from hd_parts import PartsRenderer

def main():
    tiles=TileCompositor();candidates=[]
    for identifier, in tiles.db.execute('SELECT id FROM sources LIMIT 400'):
        s,a=tiles.source(identifier)
        if a.shape[0]>=16 and a.shape[1]>=16:
            before=len(candidates)
            for y in range(0,a.shape[0]-15,16):
                for x in range(0,a.shape[1]-15,16):
                    block=a[y:y+16,x:x+16].copy()
                    if np.count_nonzero(block)>100 and len(np.unique(block))>=4:candidates.append(block);break
                if len(candidates)>before:break
        if len(candidates)>20:break
    chosen=None
    for n in range(1,len(candidates)):
        indices=np.concatenate([candidates[0],candidates[n]],axis=1)
        art,stats=tiles.assemble(indices,[0]*16)
        if art is not None and len({g['source'] for g in stats['tile_groups']})>=2:chosen=indices;break
    assert chosen is not None,'need at least two original sources'
    tasks._renderer=PartsRenderer();tasks._renderer.async_prepare=True;tasks._tiles=tiles
    tasks._renderer.disk_cache.get=lambda key:None
    encoded=base64.b64encode(zlib.compress(chosen.tobytes())).decode()
    art,stats,key,lut=tasks.prepare_composite_task(encoded,32,16,[0]*16)
    assert art is not None and len({g['source'] for g in stats['tile_groups']})>=2,stats
    opaque=np.asarray(art)[:,:,3]>0
    assert np.max(np.asarray(art)[:,:,:3][opaque])>64,'first black palette destroyed artwork'
    renderer=tasks._renderer;binding=len(renderer.bindings)+1
    renderer.bindings.append(dict(hash=stats['reference_hash'],w=32,h=16,dynamic_palette=True,original_palette_rgb=stats['reference_palette_rgb'],index_pixels=encoded))
    renderer.prepared[binding]=art;renderer.palette_luts[key]=np.frombuffer(lut,dtype='uint8')
    row=[binding,0,0,0,stats['reference_hash'],0,16,0];normal=renderer.sprite(row,bytes(1024),stats['reference_palette_native'])
    row[4]=123;black=renderer.sprite(row,bytes(1024),[0]*16)
    p=np.asarray(black);assert not p[:,:,:3][p[:,:,3]>0].any(),'black fade did not apply'
    assert np.array_equal(np.asarray(normal)[:,:,3],p[:,:,3]),'fade altered alpha'
    out=ROOT/'test_current/parts';art.save(out/'compound_canonical.png')
    report=dict(multiple_source_groups=stats['tile_groups'],exact_tiles=stats['exact_tiles'],first_seen_black_retains_colored_art=True,black_fade_black=True,alpha_preserved=True)
    (out/'compound_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
    renderer.close();tiles.db.close()

if __name__=='__main__':main()
