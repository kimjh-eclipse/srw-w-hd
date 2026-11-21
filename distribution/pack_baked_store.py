"""Deliver the finished part textures with a release.

Writes <target>/parts_baked.sqlite (only the textures the current parts use, one plain file)
and <target>/parts_baked_atlases.json (the atlas identities those textures are stored under).
The frozen player reads both through parts_disk_cache / hd_parts.atlas_identity; its own
store stays in data/cache.

  python distribution/pack_baked_store.py dist/SRW_W_HD/graphics
"""
from pathlib import Path
import sys,json,sqlite3,os
ROOT=Path(__file__).resolve().parent.parent
LIMIT=2*1024**3  # one GitHub release file must stay under 2 GiB

def main():
    target=Path(sys.argv[1]);target.mkdir(parents=True,exist_ok=True)
    os.environ.pop('SRWW_SHIPPED_BAKED',None);sys.path.insert(0,str(ROOT/'emulator'))
    from hd_parts import PartsRenderer
    renderer=PartsRenderer(async_prepare=False);keys={}
    for binding,spec in enumerate(renderer.bindings,1):
        if spec.get('source_binding') or spec.get('runtime_texture') or spec.get('disabled') or binding in renderer.quarantine:continue
        keys[renderer.texture_key(binding,spec['w'],spec['h'])]=binding
    renderer.save_atlas_digests()
    source=sqlite3.connect(f"file:{Path(renderer.disk_cache.path).as_posix()}?mode=ro",uri=True,timeout=30)
    output=target/'parts_baked.sqlite';temporary=target/'parts_baked.sqlite.tmp'
    for stale in (temporary,target/'parts_baked.sqlite.tmp-journal'):stale.unlink(missing_ok=True)
    db=sqlite3.connect(temporary);db.execute('PRAGMA journal_mode=DELETE');db.execute('PRAGMA synchronous=OFF')
    db.execute('CREATE TABLE textures (key TEXT PRIMARY KEY,w INTEGER,h INTEGER,pixels BLOB,stats TEXT)')
    packed=set();batch=[]
    for row in source.execute('SELECT key,w,h,pixels,stats FROM textures'):
        if row[0] not in keys:continue
        batch.append(row);packed.add(row[0])
        if len(batch)>=2000:db.executemany('INSERT INTO textures VALUES (?,?,?,?,?)',batch);batch=[]
    db.executemany('INSERT INTO textures VALUES (?,?,?,?,?)',batch);db.commit();db.close();source.close()
    temporary.replace(output)
    atlases={file:[identity[1],identity[2]] for file,identity in sorted(renderer.atlas_ids.items())}
    (target/'parts_baked_atlases.json').write_text(json.dumps(dict(format=1,registration_content=renderer.registration_content,atlases=atlases),separators=(',',':')),encoding='utf-8')
    missing=sorted(binding for key,binding in keys.items() if key not in packed);size=output.stat().st_size
    report=dict(parts=len(keys),packed=len(packed),not_baked=len(missing),not_baked_first=missing[:20],atlases=len(atlases),bytes=size,under_release_limit=size<LIMIT)
    print(json.dumps(report),flush=True)
    if size>=LIMIT:raise SystemExit('parts_baked.sqlite is 2 GiB or larger: a GitHub release cannot hold it as one file')

if __name__=='__main__':main()
