"""Archive only manifest-listed files; user data can never enter a release."""
from pathlib import Path
import json,zipfile,hashlib
ROOT=Path(__file__).resolve().parent.parent
APP=ROOT/'dist/SRW_W_HD'

def main():
    manifest=json.loads((APP/'distribution_manifest.json').read_text())
    output=ROOT/'dist/SRW_W_HD_Portable.zip'
    with zipfile.ZipFile(output,'w',allowZip64=True) as archive:
        for row in manifest['files']:
            path=Path(row['path'])
            assert 'data' not in path.parts and path.suffix.lower() not in ('.nds','.state','.sav','.dsv','.srm')
            source=APP/path
            assert source.stat().st_size==row['bytes'],path
            archive.write(source,'SRW_W_HD/'+path.as_posix(),compress_type=zipfile.ZIP_STORED)
        archive.write(APP/'distribution_manifest.json','SRW_W_HD/distribution_manifest.json')
    digest=hashlib.file_digest(output.open('rb'),'sha256').hexdigest()
    output.with_suffix('.zip.sha256').write_text(digest+'  '+output.name+'\n',encoding='ascii')
    print(json.dumps(dict(path=str(output),bytes=output.stat().st_size,sha256=digest)),flush=True)

if __name__=='__main__':main()
