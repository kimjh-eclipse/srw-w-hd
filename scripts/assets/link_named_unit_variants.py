"""Reuse HD art only when native part geometry/material partition is exact.

Palette permutations are proved pixel for pixel. No approximate shape matching,
placeholder painting, or changes to the approved first 5263 bindings.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g
import json,base64,zlib,hashlib,argparse,sqlite3
from collections import defaultdict
from functools import lru_cache
import numpy as np

def canonical(a):
    # Preserve transparency as material zero; assign other materials in first
    # occurrence order so a palette permutation cannot change the signature.
    values,first,inv=np.unique(a,return_index=True,return_inverse=True)
    order=sorted(range(len(values)),key=lambda i:(values[i]!=0,first[i]))
    ranks=np.empty(len(values),dtype='uint8')
    for rank,i in enumerate(order):ranks[i]=rank if 0 in values else rank+1
    return ranks[inv].tobytes()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    path=ROOT/'graphics/kazuma_parts_library.json';raw=path.read_bytes();lib=json.loads(raw);bindings=lib['bindings']
    prefix=hashlib.sha256(json.dumps(bindings[:5263],sort_keys=True).encode()).hexdigest()
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    @lru_cache(maxsize=256)
    def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    @lru_cache(maxsize=256)
    def pixels(i):return g.pixels(resource(i))
    layouts={}
    plan=json.loads((ROOT/'graphics/all_units/batches.json').read_text())
    for sheet in plan['batches']:
        for seg in sheet['segments']:layouts[seg['resource']]=(0,seg['batch_y'])
    for duplicate in plan['duplicates']:
        if duplicate['source'] in layouts:layouts[duplicate['resource']]=layouts[duplicate['source']]
    def indices(b):
        w,h=b['w'],b['h']
        if b.get('index_pixels'):
            return np.frombuffer(zlib.decompress(base64.b64decode(b['index_pixels'])),dtype='uint8').reshape(h,w)
        if 'resource' not in b:return None
        x=b.get('source_x',b['x']);y=b.get('source_y',b['y'])
        if b.get('auto_unit') and 'source_y' not in b and b['resource'] in layouts:
            dx,dy=layouts[b['resource']];x-=dx;y-=dy
        a=pixels(b['resource'])[y:y+h,x:x+w]
        if a.shape!=(h,w):return None
        ih=zlib.crc32(np.where(a,a.astype('uint16')|0x8000,0).astype('<u2').tobytes())^(w<<16)^h
        return a if ih==b.get('index_hash') else None
    roster=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text());wanted={};owners=defaultdict(set)
    for u in roster['units']:
        for p in u['primary_part_coverage'].get('unmapped_parts',[]):
            key=p['hash'];wanted[key]=(u,p);owners[key].add(u['unit_id'])
    keys=set()
    for u,p in wanted.values():
        a=pixels(u['primary_image'])[p['y']:p['y']+p['h'],p['x']:p['x']+p['w']]
        keys.add((p['w'],p['h'],canonical(a)))
    candidates=defaultdict(list)
    for bid,b in enumerate(bindings,1):
        if b.get('disabled') or b.get('source_binding') or not b.get('dynamic_palette'):continue
        palette=b.get('palette_source_rgb',b.get('original_palette_rgb'))
        if palette is None or len(palette)<16:continue
        try:a=indices(b)
        except (ValueError,IndexError,KeyError):continue
        if a is None:continue
        key=(b['w'],b['h'],canonical(a))
        if key in keys:candidates[key].append((bid,b,a,palette))
    # A legal hardware rectangle can span several old registered rectangles.
    # Search complete native source textures, rather than requiring identical
    # old OAM rectangle dimensions. A complex tile proposes an origin; the
    # entire requested rectangle must then pass the same exact partition test.
    probes={};probe_keys=set()
    for rh,(u,p) in wanted.items():
        a=pixels(u['primary_image'])[p['y']:p['y']+p['h'],p['x']:p['x']+p['w']]
        if candidates.get((p['w'],p['h'],canonical(a))):continue
        choices=[]
        for y in range(0,p['h'],8):
            for x in range(0,p['w'],8):
                tile=a[y:y+8,x:x+8]
                choices.append(((len(np.unique(tile)),np.count_nonzero(tile)),x,y,canonical(tile)))
        score,x,y,key=max(choices)
        if score[1]<12:continue
        probes[rh]=(x,y,key);probe_keys.add(key)
    tile_matches=defaultdict(list)
    db=sqlite3.connect((ROOT/'graphics/parts_tile_library.sqlite').as_uri()+'?mode=ro',uri=True)
    if probe_keys:
        for source,x,y,blob in db.execute('SELECT source,x,y,pixels FROM tiles'):
            a=np.frombuffer(blob,dtype='uint8')
            if np.count_nonzero(a)<12:continue
            key=canonical(a)
            if key in probe_keys:tile_matches[key].append((source,x,y))
    atlas_by_image={v['image']:k for k,v in lib['atlases'].items()}
    atlas_by_image[lib['atlas']]='base'
    @lru_cache(maxsize=256)
    def tile_source(identifier):
        description,blob=db.execute('SELECT description,indices FROM sources WHERE id=?',(identifier,)).fetchone()
        s=json.loads(description);a=np.frombuffer(zlib.decompress(blob),dtype='uint8').reshape(s['h'],s['w'])
        return s,a
    for rh,(x,y,key) in probes.items():
        u,p=wanted[rh];a=pixels(u['primary_image'])[p['y']:p['y']+p['h'],p['x']:p['x']+p['w']]
        fullkey=(p['w'],p['h'],canonical(a))
        for identifier,sx,sy in tile_matches[key]:
            s,native=tile_source(identifier);ox,oy=sx-x,sy-y
            atlas=atlas_by_image.get(s['image'])
            if atlas is None or ox<0 or oy<0 or ox+p['w']>s['w'] or oy+p['h']>s['h']:continue
            patch=native[oy:oy+p['h'],ox:ox+p['w']]
            if canonical(patch)!=fullkey[2]:continue
            b=dict(x=s['x']+ox,y=s['y']+oy,w=p['w'],h=p['h'],atlas_id=atlas,resource=s['resource'])
            # No source binding: this is a new exact crop of a painted atlas.
            candidates[fullkey].append((0,b,patch,s['palette']))
            break
    blocked=set(lib.get('indexed_collision_keys',[]));linked=[];unresolved=[]
    for rh,(u,p) in wanted.items():
        a=pixels(u['primary_image'])[p['y']:p['y']+p['h'],p['x']:p['x']+p['w']]
        matches=candidates.get((p['w'],p['h'],canonical(a)),[])
        if not matches:unresolved.append(dict(unit_ids=sorted(owners[rh]),image=u['primary_image'],**p));continue
        # Prefer the same source and then richer native material definitions.
        bid,b,source,palette=min(matches,key=lambda row:(row[1].get('resource')!=u['primary_image'],-len(np.unique(row[2])),row[0]))
        remap={int(v):int(a[source==v][0]) for v in np.unique(source)}
        assert all(np.all(a[source==old]==new) for old,new in remap.items())
        assert np.array_equal(source==0,a==0)
        src=np.asarray(palette,dtype='uint8');mapped=src.copy()
        for old,new in remap.items():mapped[new]=src[old]
        gfx=0x716d8+u['unit_id']*40;palid=int.from_bytes(rom[gfx+10:gfx+12],'little')
        colors=np.frombuffer(resource(palid)[8:],dtype='<u2');colors=colors[p['bank']*16:(p['bank']+1)*16]
        if len(colors)<16:colors=np.frombuffer(resource(palid)[8:],dtype='<u2')[:16]
        dst=np.stack([(colors&31)*255//31,((colors>>5)&31)*255//31,((colors>>10)&31)*255//31],1).astype('uint8')
        assert len(dst)==16
        spec=dict(hash=rh,rgb_enabled=True,index_hash=p['index_hash'],indexed_safe=p['index_hash'] not in blocked and p['opaque']>=16 and len(np.unique(a[a!=0]))>=3,
                  source_binding=bid,x=b['x'],y=b['y'],w=p['w'],h=p['h'],dynamic_palette=True,
                  original_palette_rgb=mapped.tolist(),palette_source_rgb=mapped.tolist(),palette_rgb=dst.tolist(),
                  index_pixels=base64.b64encode(zlib.compress(a.tobytes())).decode('ascii'),
                  resource=u['primary_image'],source_x=p['x'],source_y=p['y'],auto_unit_variant=True,auto_unit=True,
                  preserve_canonical_paint=True,unit_ids=sorted(owners[rh]),material_partition_exact=True)
        if not bid:
            del spec['source_binding'];spec['atlas_id']=b['atlas_id']
        bindings.append(spec);linked.append(dict(binding=len(bindings),source_binding=bid,image=u['primary_image'],unit_ids=spec['unit_ids'],index_permutation=remap))
    assert prefix==hashlib.sha256(json.dumps(bindings[:5263],sort_keys=True).encode()).hexdigest()
    if args.apply and linked:
        tmp=path.with_suffix('.tmp.json');tmp.write_text(json.dumps(lib,indent=2));tmp.replace(path)
    report=dict(applied=args.apply,linked=len(linked),unresolved=len(unresolved),approved_prefix_preserved=True,
                matches=linked,unresolved_parts=unresolved,total_bindings=len(bindings))
    (ROOT/'test_current/parts/named_variant_linking.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k not in ('matches','unresolved_parts')}))

if __name__=='__main__':main()
