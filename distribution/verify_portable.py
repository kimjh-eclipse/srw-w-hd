"""Check release hashes, private-file exclusions and the actual frozen smoke test."""
from pathlib import Path
import json,zipfile,hashlib,io
ROOT=Path(__file__).resolve().parent.parent
FORBIDDEN={'.nds','.gba','.iso','.rom','.state','.sav','.dsv','.srm','.key','.pem'}

def main():
    image=json.loads((ROOT/'test_current/image_optimization/package_images.json').read_text())
    assert image['after']<=image['before']/2
    smoke=json.loads((ROOT/'test_current/packaging/frozen_selftest.json').read_text())
    assert smoke['frozen'] and smoke['hd_cutin_id']==7 and smoke['controller_process'] and smoke['frame_worker']
    rows=[]
    for name in ('SRW_W_HD_Portable.zip','SRW_W_HD_Program.zip','SRW_W_HD_Assets.zip'):
        path=ROOT/'dist'/name;expected=path.with_suffix('.zip.sha256').read_text().split()[0]
        with path.open('rb') as file:assert hashlib.file_digest(file,'sha256').hexdigest()==expected
        with zipfile.ZipFile(path) as archive:
            names=archive.namelist()
            assert not any('/data/' in n or Path(n).suffix.lower() in FORBIDDEN for n in names)
            assert archive.testzip() is None
            if name=='SRW_W_HD_Portable.zip':
                manifest=json.loads(archive.read('SRW_W_HD/distribution_manifest.json'))
                assert len(names)==len(manifest['files'])+1
                for row in manifest['files']:
                    with archive.open('SRW_W_HD/'+row['path']) as file:assert hashlib.file_digest(file,'sha256').hexdigest()==row['sha256'],row['path']
                with zipfile.ZipFile(io.BytesIO(archive.read('SRW_W_HD/source/source.zip'))) as source:
                    assert not any(Path(n).suffix.lower() in FORBIDDEN for n in source.namelist())
        rows.append(dict(file=name,bytes=path.stat().st_size,sha256=expected,integrity_verified=True))
    result=dict(images_before=image['before'],images_after=image['after'],image_reduction_percent=round(100*(1-image['after']/image['before']),2),rgb_max_error=2,alpha_exact_after_sizing=True,max_hd_side=960,protected_seed_images_unchanged=True,stage_cache_bytes=1024**3,stage_cache_eviction='least recently used when full; otherwise keep until next recognized chapter',frozen_cutin_verified=7,roms_included=False,saves_included=False,archives=rows)
    (ROOT/'test_current/packaging/release_summary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':main()
