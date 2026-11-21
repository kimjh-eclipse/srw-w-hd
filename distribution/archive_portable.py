"""Archive only manifest-listed files; user data can never enter a release.

GitHub refuses a release file of 2 GiB or more, so the release is three archives that are
extracted into the same folder: Program, Assets_N (artwork, as many parts as PART allows)
and Baked (the finished part textures, graphics/parts_baked*). --portable also writes the single complete archive for
other hosts; it is larger than the limit.
"""
from pathlib import Path
import json,zipfile,hashlib,argparse
ROOT=Path(__file__).resolve().parent.parent
APP=ROOT/'dist/SRW_W_HD'
LIMIT=2*1024**3
STORED=('.png','.webp','.zip','.npz')
# Packed bytes never exceed the files' own bytes by more than the zip directory, so a part
# of at most PART bytes of artwork stays well under LIMIT.
PART=1536*1024**2

def kind_of(path):
    if path.parts[0]!='graphics':return 'program'
    return 'baked' if path.name.startswith('parts_baked') else 'assets'

def asset_parts(files):
    """Part number of every artwork file: whole sub folders of graphics, in name order."""
    groups={}
    for row in files:
        path=Path(row['path'])
        if kind_of(path)=='assets':groups.setdefault(path.parts[1] if len(path.parts)>2 else '',[]).append(row)
    part=1;used=0;result={}
    for group in sorted(groups):
        size=sum(row['bytes'] for row in groups[group])
        if used and used+size>PART:part+=1;used=0
        used+=size
        for row in groups[group]:result[row['path']]=part
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--portable',action='store_true',help='also write the complete single archive');args=parser.parse_args()
    manifest=json.loads((APP/'distribution_manifest.json').read_text())
    parts=asset_parts(manifest['files'])
    targets=[('SRW_W_HD_Program.zip','program')]+[(f'SRW_W_HD_Assets_{n}.zip',n) for n in sorted(set(parts.values()))]+[('SRW_W_HD_Baked.zip','baked')]
    for stale in (ROOT/'dist').glob('SRW_W_HD_Assets*.zip*'):
        if stale.name.removesuffix('.sha256') not in [name for name,_ in targets]:stale.unlink()
    if args.portable:targets.append(('SRW_W_HD_Portable.zip','all'))
    else:
        for stale in (ROOT/'dist/SRW_W_HD_Portable.zip',ROOT/'dist/SRW_W_HD_Portable.zip.sha256'):stale.unlink(missing_ok=True)
    too_large=[]
    for name,kind in targets:
        output=ROOT/'dist'/name
        with zipfile.ZipFile(output,'w',allowZip64=True,compression=zipfile.ZIP_DEFLATED,compresslevel=3) as archive:
            for row in manifest['files']:
                path=Path(row['path'])
                if kind!='all' and (parts.get(row['path']) if isinstance(kind,int) else kind_of(path))!=kind:continue
                assert 'data' not in path.parts and path.suffix.lower() not in ('.nds','.state','.sav','.dsv','.srm')
                source=APP/path
                assert source.stat().st_size==row['bytes'],path
                # The baked store holds WebP pictures: deflating it again gains nothing.
                codec=zipfile.ZIP_STORED if path.suffix.lower() in STORED or path.name=='parts_baked.sqlite' else zipfile.ZIP_DEFLATED
                archive.write(source,'SRW_W_HD/'+path.as_posix(),compress_type=codec)
            if kind in ('all','program'):archive.write(APP/'distribution_manifest.json','SRW_W_HD/distribution_manifest.json')
        with output.open('rb') as file:digest=hashlib.file_digest(file,'sha256').hexdigest()
        output.with_suffix('.zip.sha256').write_text(digest+'  '+output.name+'\n',encoding='ascii')
        size=output.stat().st_size
        if kind!='all' and size>=LIMIT:too_large.append(name)
        print(json.dumps(dict(path=str(output),bytes=size,sha256=digest,under_release_limit=size<LIMIT)),flush=True)
    if too_large:raise SystemExit('2 GiB or larger, a GitHub release cannot hold it: '+', '.join(too_large))

if __name__=='__main__':main()
