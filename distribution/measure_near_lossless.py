from pathlib import Path
import subprocess,json,tempfile
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent

def main():
    tool=next((ROOT/'tools/webp').rglob('cwebp.exe'));source=json.loads((ROOT/'test_current/image_optimization/codec_measurements.json').read_text());files=list(dict.fromkeys(r['path'] for r in source))[::2];rows=[]
    for name in files:
        original=np.asarray(Image.open(ROOT/name).convert('RGBA'));visible=original[:,:,3]>0
        for quality in (80,60,40):
            out=ROOT/'test_current/image_optimization/sample.webp'
            subprocess.run([str(tool),'-quiet','-near_lossless',str(quality),'-q','70','-m','4','-exact',str(ROOT/name),'-o',str(out)],check=True)
            a=np.asarray(Image.open(out).convert('RGBA'));d=original[:,:,:3].astype('float32')-a[:,:,:3];mse=float(np.mean(d[visible]**2));row=dict(path=name,quality=quality,ratio=round(out.stat().st_size/(ROOT/name).stat().st_size,3),mae=round(float(np.abs(d[visible]).mean()),3),max_error=int(np.abs(d[visible]).max()),psnr=99 if not mse else round(float(10*np.log10(255**2/mse)),2),alpha_exact=bool(np.array_equal(a[:,:,3],original[:,:,3])));rows.append(row);print(row,flush=True)
    (ROOT/'test_current/image_optimization/near_lossless_measurements.json').write_text(json.dumps(rows,indent=2))

if __name__=='__main__':main()
