"""Package-sized near-lossless art, with bounded RGB and exact alpha.

Native recognition references and approved seed atlases remain untouched PNGs.
Painted atlases larger than the requested 960-pixel limit are reduced once;
RGB precision is bounded to two 8-bit levels; the WebP codec is lossless.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import os,json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'build/optimized_graphics'
REPORT=ROOT/'test_current/image_optimization/package_images.json'

def protected_paths():
    meta=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text())
    flags=('auto_unit','auto_animation','auto_animation_reuse','auto_late_attack','auto_full_attack','auto_shared_attack','observed_generated','observed_reuse','disabled')
    names={b.get('atlas_id','base') for b in meta['bindings'] if not any(b.get(k) for k in flags)}
    keep={meta['atlas'],'kazuma_parts_atlas_facefix.png','kazuma_parts_atlas_reference.png'}
    for name in names-{'base'}:
        keep.update((meta['atlases'][name]['image'],meta['atlases'][name]['reference']))
    return keep

def prepare(path,protected,previous):
    relative=path.relative_to(ROOT/'graphics');stat=path.stat();key=relative.as_posix()
    base=dict(path=key,before=stat.st_size,source_mtime_ns=stat.st_mtime_ns)
    if key in protected or any(x in path.stem.lower() for x in ('native','reference')):
        return dict(base,after=stat.st_size,status='protected',output=key)
    output=OUT/relative.with_suffix('.webp');old=previous.get(key)
    reusable=old and old.get('source_mtime_ns')==stat.st_mtime_ns and old['before']==stat.st_size and (ROOT/old['encoded']).exists()
    if reusable and old.get('pipeline_version')==2:return old
    with Image.open(ROOT/old['encoded'] if reusable else path) as opened:image=opened.convert('RGBA')
    original=tuple(old['original_size']) if reusable else image.size
    if max(original)>960:image.thumbnail((960,960),Image.Resampling.LANCZOS)
    before_pixels=np.array(image);pixels=before_pixels.copy()
    # Near-lossless RGB precision: <=2/255 per channel, black/white retained.
    # Alpha is copied bit-for-bit; no YUV subsampling or alpha quantization.
    pixels[:,:,:3]=np.minimum(255,((pixels[:,:,:3].astype('uint16')+2)//4)*4).astype('uint8')
    image=Image.fromarray(pixels)
    assert np.abs(pixels[:,:,:3].astype('int16')-before_pixels[:,:,:3]).max()<=2
    assert np.array_equal(pixels[:,:,3],before_pixels[:,:,3])
    output.parent.mkdir(parents=True,exist_ok=True)
    temporary=output.with_suffix('.tmp.webp');image.save(temporary,'WEBP',lossless=True,quality=90,method=4,exact=True)
    with Image.open(temporary) as decoded:
        rgba=np.asarray(image);actual=np.asarray(decoded.convert('RGBA'))
        assert decoded.size==image.size and np.array_equal(rgba,actual),(key,'RGBA changed')
    if temporary.stat().st_size>=stat.st_size and original==image.size:
        temporary.unlink();return dict(base,after=stat.st_size,status='unchanged',output=key)
    temporary.replace(output);os.utime(output,ns=(stat.st_atime_ns,stat.st_mtime_ns))
    return dict(base,after=output.stat().st_size,status='optimized',output=relative.with_suffix('.webp').as_posix(),encoded=output.relative_to(ROOT).as_posix(),original_size=list(original),size=list(image.size),pipeline_version=2,rgb_max_error=2,alpha_exact_after_resize=True,codec_rgba_exact=True)

def main():
    protected=protected_paths();REPORT.parent.mkdir(parents=True,exist_ok=True);previous={}
    if REPORT.exists():previous={r['path']:r for r in json.loads(REPORT.read_text())['entries'] if r.get('encoded')}
    files=sorted((ROOT/'graphics').rglob('*.png'));rows=[]
    with ThreadPoolExecutor(max_workers=min(6,os.cpu_count() or 2)) as pool:
        tasks=[pool.submit(prepare,path,protected,previous) for path in files]
        for future in as_completed(tasks):
            rows.append(future.result())
            if len(rows)%250==0:print(json.dumps(dict(done=len(rows),total=len(files),saved_bytes=sum(r['before']-r['after'] for r in rows))),flush=True)
    report=dict(files=len(rows),before=sum(r['before'] for r in rows),after=sum(r['after'] for r in rows),optimized=sum(r['status']=='optimized' for r in rows),resized=sum(r.get('original_size')!=r.get('size') for r in rows if 'size' in r),compression='RGB max error 2/255 after at-most-960 sizing; alpha exact; lossless WebP codec',entries=sorted(rows,key=lambda r:r['path']))
    REPORT.write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='entries'}),flush=True)

if __name__=='__main__':main()
