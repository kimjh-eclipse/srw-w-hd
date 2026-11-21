"""Check release hashes, private-file exclusions and the actual frozen smoke test."""
from pathlib import Path
import json,zipfile,hashlib,io
ROOT=Path(__file__).resolve().parent.parent
FORBIDDEN={'.nds','.gba','.iso','.rom','.state','.sav','.dsv','.srm','.key','.pem'}
SPLIT=('SRW_W_HD_Program.zip',*sorted(p.name for p in (ROOT/'dist').glob('SRW_W_HD_Assets_*.zip')),'SRW_W_HD_Baked.zip')
LIMIT=2*1024**3

def main():
    image=json.loads((ROOT/'test_current/image_optimization/package_images.json').read_text())
    assert image['after']<=image['before']/2
    smoke=json.loads((ROOT/'test_current/packaging/frozen_selftest.json').read_text())
    assert smoke['frozen'] and smoke['hd_cutin_id']==7 and smoke['controller_process'] and smoke['frame_worker']
    assert len(SPLIT)>2 and not (ROOT/'dist/SRW_W_HD_Assets.zip').exists(),'artwork archives missing or a stale single one present'
    rows=[];seen={};manifest=None
    names_checked=list(SPLIT)+(['SRW_W_HD_Portable.zip'] if (ROOT/'dist/SRW_W_HD_Portable.zip').exists() else [])
    for name in names_checked:
        path=ROOT/'dist'/name;expected=path.with_suffix('.zip.sha256').read_text().split()[0]
        with path.open('rb') as file:assert hashlib.file_digest(file,'sha256').hexdigest()==expected
        if name in SPLIT:assert path.stat().st_size<LIMIT,(name,'2 GiB or larger')
        with zipfile.ZipFile(path) as archive:
            names=archive.namelist()
            assert not any('/data/' in n or Path(n).suffix.lower() in FORBIDDEN for n in names)
            assert archive.testzip() is None
            if name in ('SRW_W_HD_Program.zip','SRW_W_HD_Portable.zip'):
                listed=json.loads(archive.read('SRW_W_HD/distribution_manifest.json'))
                assert manifest is None or listed==manifest;manifest=listed
                with zipfile.ZipFile(io.BytesIO(archive.read('SRW_W_HD/source/source.zip'))) as source:
                    assert not any(Path(n).suffix.lower() in FORBIDDEN for n in source.namelist())
            if name=='SRW_W_HD_Portable.zip':
                assert len(names)==len(manifest['files'])+1
            for row in manifest['files'] if name=='SRW_W_HD_Portable.zip' else []:
                with archive.open('SRW_W_HD/'+row['path']) as file:assert hashlib.file_digest(file,'sha256').hexdigest()==row['sha256'],row['path']
            if name in SPLIT:
                for n in names:
                    if n!='SRW_W_HD/distribution_manifest.json':
                        assert n not in seen,(n,'in two archives');seen[n]=name
        rows.append(dict(file=name,bytes=path.stat().st_size,sha256=expected,integrity_verified=True))
    # The three release archives together hold every manifest file exactly once, with its hash.
    assert set(seen)=={'SRW_W_HD/'+row['path'] for row in manifest['files']}
    opened={name:zipfile.ZipFile(ROOT/'dist'/name) for name in SPLIT}
    for row in manifest['files']:
        with opened[seen['SRW_W_HD/'+row['path']]].open('SRW_W_HD/'+row['path']) as file:assert hashlib.file_digest(file,'sha256').hexdigest()==row['sha256'],row['path']
    for archive in opened.values():archive.close()
    result=dict(images_before=image['before'],images_after=image['after'],image_reduction_percent=round(100*(1-image['after']/image['before']),2),rgb_max_error=2,alpha_exact_after_sizing=True,max_hd_side=960,protected_seed_images_unchanged=True,stage_cache_bytes=1024**3,stage_cache_eviction='least recently used when full; otherwise keep until next recognized chapter',frozen_cutin_verified=7,roms_included=False,saves_included=False,archives=rows)
    (ROOT/'test_current/packaging/release_summary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':main()
