"""Bake exact observed rectangles only when every tile already has matching painted provenance."""
import argparse,base64,hashlib,json,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from tile_compositor import TileCompositor
from hd_parts import is_menu_gradient
from scripts.assets import srw_graphics as g
from functools import lru_cache

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--apply',action='store_true');args=ap.parse_args()
    old=json.loads((ROOT/'test_current/combat/runtime_path/coverage_all/gaps.json').read_text())
    wanted={r['index_hash'] for r in old['parts']}
    audit=json.loads((ROOT/'test_current/parts/observed_attack_gaps/report.json').read_text())
    proven={r['index_hash']:{s['resource'] for s in r['candidates']} for r in audit['unmatched_rectangles']}
    meta_path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(meta_path.read_text());prefix=hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True).encode()).hexdigest()
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    @lru_cache(maxsize=256)
    def source_pixels(identifier):return g.pixels(g.decompress(rom[g.BASE+offsets[identifier]:g.BASE+offsets[identifier+1]]))
    known={r['hash'] for r in meta['bindings'] if r.get('rgb_enabled',True) and not r.get('disabled')};seen=set();rows=[];tiles=TileCompositor()
    folder=ROOT/'graphics/observed_complete';folder.mkdir(exist_ok=True)
    captures=sorted((ROOT/'test_current/combat/named_attacks').rglob('*unknown.npz'))+[ROOT/'test_current/parts/rework_getter3/live_unknown.npz']
    for npz in captures:
        with np.load(npz) as data:
            for row,pix,palette in zip(data['rows'],data['pixels'],data['palettes']):
                key,material=int(row[0]),int(row[7]);rgbkey=int(row[6]);w,h=map(int,row[1:3]);identity=(key,material)
                if not key or key not in wanted or identity in seen or rgbkey in known :continue
                seen.add(identity);indices=pix[:w*h].reshape(h,w)
                if np.count_nonzero(indices)<32 or len(np.unique(indices))<4:continue
                if is_menu_gradient(indices,w,h):continue
                art,stats=tiles.assemble(indices,palette)
                result=dict(index_hash=key,material=material,rgb_hash=rgbkey,w=w,h=h,capture=str(npz.relative_to(ROOT)),accepted=False)
                if art is None:result['reason']=stats;rows.append(result);continue
                if stats.get('reference_fill_pixels',0) or stats.get('registered_iou',1)<.82:
                    result.update(reason='native fill or insufficient geometry',registration=stats);rows.append(result);continue
                sources=[tiles.source(g['source'])[0]['resource'] for g in stats['tile_groups']]
                if len(set(sources))!=1 or sources[0]<0:result.update(reason='requires multiple source banks',sources=sources);rows.append(result);continue
                source_ok=True
                for group in stats['tile_groups']:
                    description,native_source=tiles.source(group['source'])
                    if not np.array_equal(native_source,source_pixels(description['resource'])):source_ok=False;break
                if not source_ok:result.update(reason='source pixels not an exact full ROM bank',sources=sources);rows.append(result);continue
                result.update(accepted=True,sources=sources,registration=stats);rows.append(result)
                if not args.apply:continue
                name=f'observed_{key:08x}_{material:08x}';image='observed_complete/'+name+'_hd.png';reference='observed_complete/'+name+'_native.png'
                colors=palette.astype('uint32');rgb=np.stack([(colors&31)*255//31,((colors>>5)&31)*255//31,((colors>>10)&31)*255//31],-1).astype('uint8')
                art.resize((w*4,h*4),Image.Resampling.LANCZOS).save(ROOT/'graphics'/image);Image.fromarray(np.dstack([rgb[indices],(indices!=0).astype('uint8')*255])).save(ROOT/'graphics'/reference)
                meta['atlases'][name]=dict(image=image,reference=reference,native_size=[w,h],lazy=True)
                meta['bindings'].append(dict(hash=rgbkey,rgb_enabled=True,index_hash=key,indexed_safe=False,dynamic_palette=False,original_palette_rgb=rgb.tolist(),index_pixels=base64.b64encode(zlib.compress(indices.tobytes())).decode(),x=0,y=0,w=w,h=h,atlas_id=name,resource=sources[0],source_x=0,source_y=0,registered_attack_bank=True,observed_native_rectangle=True,preserve_canonical_paint=True,observed_complete=True))
                known.add(rgbkey)
    assert prefix==hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True).encode()).hexdigest()
    if args.apply and any(r['accepted'] for r in rows):
        tmp=meta_path.with_suffix('.tmp.json');tmp.write_text(json.dumps(meta,indent=2),encoding='utf-8');tmp.replace(meta_path)
    report=dict(applied=args.apply,attempted=len(rows),accepted=sum(r['accepted'] for r in rows),all_units_complete=False,rows=rows)
    (ROOT/'test_current/parts/observed_complete.json').write_text(json.dumps(report,indent=2));print({k:v for k,v in report.items() if k!='rows'})
if __name__=='__main__':main()
