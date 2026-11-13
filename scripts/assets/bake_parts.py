"""Register every part texture ahead of time so the player only reads them.

Registration (crop, resample, alignment search) costs tens of milliseconds
per part. Done while playing, a new pose waits for it part by part. This tool
does that work once for the whole catalog and stores the finished textures in
the content-addressed store the player already reads.

Run it again after changing an atlas or the registration code; entries whose
inputs changed are rebuilt and the rest are skipped.
"""
import argparse,json,os,sys,time,zlib
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

_renderer=None


def start():
    global _renderer
    from hd_parts import PartsRenderer
    from parts_disk_cache import LegacyPartsCache
    _renderer=PartsRenderer(async_prepare=False)
    legacy=ROOT/'graphics/parts_registered.sqlite'
    if legacy.exists():_renderer.legacy_cache=LegacyPartsCache(legacy)


def bake(item):
    binding,key=item
    spec=_renderer.bindings[binding-1]
    try:image,stats=_renderer.prepare_texture(binding,spec['w'],spec['h'])
    except Exception as error:return binding,key,None,str(error)
    return binding,key,(image.width,image.height,_renderer.disk_cache.encode(image),json.dumps(stats)),None


def main():
    parser=argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--workers',type=int,default=max(1,(os.cpu_count() or 4)-4))
    parser.add_argument('--limit',type=int,default=0,help='bake at most this many missing parts')
    parser.add_argument('--resources',type=int,nargs='*',default=[],help='limit a repair bake to these original IMG resources')
    parser.add_argument('--bindings',type=int,nargs='*',default=[],help='limit a repair bake to these exact registered bindings')
    args=parser.parse_args()
    out=ROOT/'test_current/parts/bake';out.mkdir(parents=True,exist_ok=True)
    start();cache=_renderer.disk_cache;db=cache.db()
    present=cache.keys()
    todo=[];total=0
    for binding,spec in enumerate(_renderer.bindings,1):
        if args.bindings and binding not in args.bindings:continue
        if args.resources and spec.get('resource') not in args.resources:continue
        if spec.get('source_binding') or spec.get('runtime_texture') or spec.get('disabled'):continue
        total+=1;key=_renderer.texture_key(binding,spec['w'],spec['h'])
        if key not in present:todo.append((spec.get('atlas_id','base'),binding,key))
    # Neighbouring parts share an atlas; keep each worker on one at a time.
    todo.sort();todo=[(binding,key) for _,binding,key in todo]
    _renderer.save_atlas_digests()   # workers read the recorded hashes instead of each hashing every atlas
    print(f'{total} source parts, {total-len(todo)} already baked, {len(todo)} missing, {args.workers} workers',flush=True)
    if args.limit:todo=todo[:args.limit]
    started=time.perf_counter();done=0;errors={}
    with Pool(args.workers,initializer=start) as pool:
        for binding,key,result,error in pool.imap_unordered(bake,todo,chunksize=32):
            done+=1
            if error:errors[binding]=error
            else:db.execute('INSERT OR REPLACE INTO textures VALUES (?,?,?,?,?)',(key,*result))
            if done%500==0:
                db.commit();rate=done/(time.perf_counter()-started)
                print(f'{done}/{len(todo)}  {rate:.0f} parts/s  about {(len(todo)-done)/rate/60:.1f} min left',flush=True)
    db.commit()
    # Colour-to-slot tables for every source palette (about 20 ms each when
    # computed while playing).
    import hashlib,numpy as np
    palettes={}
    for spec in _renderer.bindings:
        if spec.get('source_binding'):continue
        palette=np.asarray(spec.get('palette_source_rgb',spec.get('original_palette_rgb',_renderer.source_palette)),dtype='float32')
        if len(palette)>1:palettes.setdefault(hashlib.sha1(palette.tobytes()).hexdigest(),palette)
    # A one-part repair must not recalculate hundreds of unchanged 32K tables.
    # The normal renderer already loads these by the exact float32 palette hash.
    if palettes:_renderer.baked_lut(next(iter(palettes.values())).tobytes())
    reused=sum(key in (_renderer.baked_luts or {}) for key in palettes)
    tables=np.stack([_renderer.get_palette_lut(palette) for palette in palettes.values()])
    lut_path=ROOT/'graphics/palette_luts.npz';temporary=lut_path.with_suffix('.tmp.npz')
    np.savez_compressed(temporary,keys=np.array(list(palettes)),tables=tables);temporary.replace(lut_path)
    print(len(palettes),'palette tables,',reused,'reused',flush=True)
    report=dict(palette_tables=len(palettes),palette_tables_reused=reused,source_parts=total,baked_now=done-len(errors),errors=len(errors),seconds=round(time.perf_counter()-started,1),store=str(cache.path),store_bytes=Path(cache.path).stat().st_size)
    (out/('resource_report.json' if args.resources else 'report.json')).write_text(json.dumps(dict(report,error_detail={str(k):v for k,v in list(errors.items())[:200]}),indent=2),encoding='utf-8')
    print(json.dumps(report))


if __name__=='__main__':main()
