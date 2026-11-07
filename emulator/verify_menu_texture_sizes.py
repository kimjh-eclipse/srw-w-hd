"""All-size pixel equivalence, no original PNG decoding, and load-time comparison."""
import json
import time
from unittest.mock import patch
from PIL import Image
from menu_texture_cache import ROOT,FOLDER,open_database,load_texture
from render_resolution import MIN_WIDTH,MAX_WIDTH

def main():
    spec=json.loads((FOLDER/'scene_runtime.json').read_text())
    basis=spec.get('source_width',1440)
    database=open_database()
    assert database is not None
    cases=0
    old_ms=[];new_ms=[]
    for filename in spec['images'].values():
        with Image.open(FOLDER/filename) as image:
            original=image.convert('RGBA')
        for width in range(MIN_WIDTH,MAX_WIDTH+1,32):
            expected=original if width==basis else original.resize(
                (round(original.width*width/basis),round(original.height*width/basis)),Image.Resampling.LANCZOS)
            with patch('PIL.Image.open',side_effect=AssertionError('Full PNG decoded during cached load')):
                actual,hit=load_texture(filename,width,database)
            assert hit and actual.size==expected.size and actual.tobytes()==expected.tobytes(),(filename,width)
            cases+=1
        # Process-level, warmed filesystem comparison; not an in-game fps test.
        for width in (768,960):
            for _ in range(3):
                start=time.perf_counter();old,_=load_texture(filename,width,None);old_ms.append((time.perf_counter()-start)*1000)
                start=time.perf_counter();new,hit=load_texture(filename,width,database);new_ms.append((time.perf_counter()-start)*1000)
                assert hit and old.tobytes()==new.tobytes()
    database.close()
    report=dict(cases=cases,pixel_exact=True,original_png_decode_on_cache_hit=False,
                mean_original_load_resize_ms=sum(old_ms)/len(old_ms),mean_display_size_load_ms=sum(new_ms)/len(new_ms),
                load_speedup=sum(old_ms)/sum(new_ms),benchmark='warmed filesystem, 12 menu textures at widths 768 and 960; not in-game fps')
    path=ROOT/'test_current/image_optimization/menu_sizes_verification.json'
    path.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))

if __name__=='__main__':
    main()
