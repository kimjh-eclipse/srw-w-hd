"""Archive only manifest-listed files; user data can never enter a release.

GitHub refuses a release file of 2 GiB or more, so the release is three archives that are
extracted into the same folder: Program, Assets (artwork) and Baked (the finished part
textures, graphics/parts_baked*). --portable also writes the single complete archive for
other hosts; it is larger than the limit.
"""
from pathlib import Path
import json,zipfile,hashlib,argparse
ROOT=Path(__file__).resolve().parent.parent
APP=ROOT/'dist/SRW_W_HD'
LIMIT=2*1024**3
STORED=('.png','.webp','.zip','.npz')

def kind_of(path):
    if path.parts[0]!='graphics':return 'program'
    return 'baked' if path.name.startswith('parts_baked') else 'assets'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--portable',action='store_true',help='also write the complete single archive');args=parser.parse_args()
    manifest=json.loads((APP/'distribution_manifest.json').read_text())
    targets=[('SRW_W_HD_Program.zip','program'),('SRW_W_HD_Assets.zip','assets'),('SRW_W_HD_Baked.zip','baked')]
    if args.portable:targets.append(('SRW_W_HD_Portable.zip','all'))
    else:
        for stale in (ROOT/'dist/SRW_W_HD_Portable.zip',ROOT/'dist/SRW_W_HD_Portable.zip.sha256'):stale.unlink(missing_ok=True)
    too_large=[]
    for name,kind in targets:
        output=ROOT/'dist'/name
        with zipfile.ZipFile(output,'w',allowZip64=True,compression=zipfile.ZIP_DEFLATED,compresslevel=3) as archive:
            for row in manifest['files']:
                path=Path(row['path'])
                if kind!='all' and kind_of(path)!=kind:continue
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
