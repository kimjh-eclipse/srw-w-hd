from pathlib import Path
import io,json,time
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent

def main():
    rows=[]
    for folder in ('animation_parts','map_tiles','scenario_backgrounds','all_units','battle_backgrounds','portraits','wing_parts','menu_units'):
        files=[p for p in (ROOT/'graphics'/folder).rglob('*.png') if not any(v in p.name for v in ('native','reference'))]
        for path in sorted(files,key=lambda p:p.stat().st_size,reverse=True)[:2]:
            image=Image.open(path).convert('RGBA');a=np.asarray(image);visible=a[:,:,3]>0
            for mode in ('lossless',95,92):
                stream=io.BytesIO();start=time.perf_counter()
                image.save(stream,'WEBP',lossless=mode=='lossless',quality=100 if mode=='lossless' else mode,method=4,exact=True)
                data=stream.getvalue();decoded=np.array(Image.open(io.BytesIO(data)).convert('RGBA'));delta=a[:,:,:3].astype('float32')-decoded[:,:,:3]
                mse=float(np.mean(delta[visible]**2));rows.append(dict(path=path.relative_to(ROOT).as_posix(),mode=mode,before=path.stat().st_size,after=len(data),ratio=round(len(data)/path.stat().st_size,3),mae=round(float(np.abs(delta[visible]).mean()),3),psnr=99 if not mse else round(float(10*np.log10(255**2/mse)),2),alpha_exact=bool(np.array_equal(a[:,:,3],decoded[:,:,3])),seconds=round(time.perf_counter()-start,3)))
    out=ROOT/'test_current/image_optimization/codec_measurements.json';out.write_text(json.dumps(rows,indent=2));print(json.dumps(rows))

if __name__=='__main__':main()
