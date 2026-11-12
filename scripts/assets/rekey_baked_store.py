"""Move baked textures from path-bound keys to content keys without re-baking.

Earlier keys contained each atlas's absolute path and modification time, so
the store stopped matching as soon as the project (or a packaged copy) lived
anywhere else. This renames every entry that the current catalogue still
uses to its content key. The pictures themselves are not touched.

Run it in the folder the store was baked in: the old key can only be
recomputed where the old path and file times still hold. Pass --old-root
when the files were copied elsewhere with their times preserved.
"""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT


def main():
    parser=argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--old-root',help='folder the store was baked in, when it is not this one')
    parser.add_argument('--mapping',help='write old->new keys here (enough to undo the change)')
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    import hd_parts
    from hd_parts import PartsRenderer
    renderer=PartsRenderer(async_prepare=False);cache=renderer.disk_cache;db=cache.db();present=cache.keys()
    if args.old_root:
        # Old keys spell the path the way str(Path) did at bake time.
        old_graphics=Path(args.old_root)/'graphics';real=renderer.__dict__.setdefault('atlas_stats',{})
    pairs={};already=0;absent=0;total=0
    for binding,spec in enumerate(renderer.bindings,1):
        if spec.get('source_binding') or spec.get('runtime_texture') or spec.get('disabled'):continue
        total+=1;w,h=spec['w'],spec['h']
        if args.old_root:
            atlas=renderer.atlas_specs.get(spec.get('atlas_id','base'),{'image':'kazuma_parts_atlas_facefix.png','reference':'kazuma_parts_atlas_reference.png'})
            for file in (atlas['image'],atlas['reference']):
                if file not in real:
                    stat=(hd_parts.ROOT/'graphics'/file).stat();real[file]=[str(old_graphics/file),stat.st_mtime_ns,stat.st_size]
        old=renderer.texture_key(binding,w,h,path_bound=True);new=renderer.texture_key(binding,w,h)
        if new in present:already+=1
        elif old in present:pairs[old]=new
        else:absent+=1
    renderer.save_atlas_digests()
    targets=set(pairs.values());collisions=len(pairs)-len(targets)
    report=dict(source_parts=total,store_rows_before=len(present),to_rename=len(pairs),already_content_keyed=already,not_in_store=absent,
        distinct_new_keys=len(targets),several_old_keys_to_one_new=collisions,new_key_already_taken=len(targets&present))
    if args.mapping:Path(args.mapping).write_text(json.dumps(pairs),encoding='utf-8')
    if not args.dry_run and pairs:
        if report['several_old_keys_to_one_new'] or report['new_key_already_taken']:
            print(json.dumps(report));raise SystemExit('refusing to rename: keys would collide')
        with db:db.executemany('UPDATE textures SET key=? WHERE key=?',[(new,old) for old,new in pairs.items()])
        after=cache.keys();report.update(store_rows_after=len(after),renamed_present=len(targets&after),old_keys_left=len(set(pairs)&after))
        db.execute('PRAGMA wal_checkpoint(TRUNCATE)')
    report['dry_run']=args.dry_run
    out=ROOT/'test_current/parts/bake';out.mkdir(parents=True,exist_ok=True);(out/'rekey_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2));db.close();renderer.close()


if __name__=='__main__':main()
