"""Archive only manifest-listed files; user data can never enter a release."""
from pathlib import Path
import json,zipfile,hashlib
ROOT=Path(__file__).resolve().parent.parent
APP=ROOT/'dist/SRW_W_HD'

def main():
    manifest=json.loads((APP/'distribution_manifest.json').read_text())
    for name,kind in (('SRW_W_HD_Portable.zip','all'),('SRW_W_HD_Program.zip','program'),('SRW_W_HD_Assets.zip','assets')):
        output=ROOT/'dist'/name
        with zipfile.ZipFile(output,'w',allowZip64=True,compression=zipfile.ZIP_DEFLATED,compresslevel=3) as archive:
            for row in manifest['files']:
                path=Path(row['path']);asset=path.parts[0]=='graphics'
                if kind=='program' and asset or kind=='assets' and not asset:continue
                assert 'data' not in path.parts and path.suffix.lower() not in ('.nds','.state','.sav','.dsv','.srm')
                source=APP/path
                assert source.stat().st_size==row['bytes'],path
                codec=zipfile.ZIP_STORED if path.suffix.lower() in ('.png','.webp','.zip','.npz') else zipfile.ZIP_DEFLATED
                archive.write(source,'SRW_W_HD/'+path.as_posix(),compress_type=codec)
            if kind!='assets':archive.write(APP/'distribution_manifest.json','SRW_W_HD/distribution_manifest.json')
        digest=hashlib.file_digest(output.open('rb'),'sha256').hexdigest()
        output.with_suffix('.zip.sha256').write_text(digest+'  '+output.name+'\n',encoding='ascii')
        print(json.dumps(dict(path=str(output),bytes=output.stat().st_size,sha256=digest)),flush=True)

if __name__=='__main__':main()
