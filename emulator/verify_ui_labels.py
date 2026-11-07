"""Validate exact UI labels on real frames, edited numeric values, and negatives."""
from pathlib import Path
import json,time
import numpy as np
from PIL import Image
from hd_ui_labels import UILabelRenderer,ROOT
from hd_fonts import FontRenderer

def main():
    out=ROOT/'test_current/font';r=UILabelRenderer();fonts=FontRenderer();report={'scenes':{},'false_positives':0}
    for filename in ('scene_1.png','ui_result_native.png'):
        source=np.asarray(Image.open(out/filename).convert('RGB'))[:192]
        target=Image.fromarray(source).resize((1440,1080),Image.Resampling.NEAREST)
        fonts.compose(target,source)
        assert r.compose(target,source)>0
        assert [text for x,y,text in r.last_matches]==['HP','EN','PARTS']
        assert ''.join(ch for x,y,ch in sorted(fonts.last_matches) if y==32 and 96<=x<120)=='102'
        for text,y in [('레벨',16),('정신',48),('상태',64),('발호크',80),('지형',160)]:
            assert text in ''.join(ch for x,yy,ch in sorted(fonts.last_matches) if yy==y)
        target.save(out/('ui_'+Path(filename).stem+'_hd.png'))
        report['scenes'][filename]={'image_labels':r.last_matches,'decoded_glyphs_existing_renderer':len(fonts.last_matches)}
    source=np.asarray(Image.open(out/'scene_1.png').convert('RGB'))[:192].copy()
    # Replace level 5 with the actual native 0 bitmap from morale 102.
    source[16:28,104:112]=source[32:44,104:112]
    target=Image.fromarray(source).resize((960,720),Image.Resampling.NEAREST);fonts.compose(target,source);r.compose(target,source)
    assert next(ch for x,y,ch in fonts.last_matches if (x,y)==(104,16))=='0'
    # HP values likewise remain decoded rather than a snapshot of 5000.
    source[96:104,40:48]=source[112:120,32:40]
    fonts.compose(target,source);r.compose(target,source)
    assert next(ch for x,y,ch in fonts.last_matches if (x,y)==(40,96))=='7'
    target.save(out/'ui_dynamic_numbers_hd.png');report['changed_level_and_hp_values_decoded']=True
    rng=np.random.default_rng(9)
    negatives=[np.zeros_like(source),rng.integers(0,256,source.shape,dtype='uint8')]
    negatives.extend(np.asarray(Image.open(out/f'scene_{n}.png').convert('RGB'))[s*192:(s+1)*192] for n in (0,3,4) for s in (0,1))
    wrong=source.copy();wrong[48:60,8:32]=0;negatives.append(wrong)
    for n in negatives:
        im=Image.fromarray(n);before=im.tobytes();assert r.compose(im,n)==0;assert im.tobytes()==before
    report['negative_screens_unchanged']=len(negatives)
    # Animation outside UI does not invalidate the numeric/label scan cache.
    r.compose(target,source);timings=[]
    for i in range(25):
        animated=source.copy();animated[100,200]=[i,100,30]
        start=time.perf_counter();r.compose(target,animated);timings.append((time.perf_counter()-start)*1000)
    report['warm_animated_robot_mean_ms']=round(float(np.mean(timings)),3)
    report['warm_animated_robot_p95_ms']=round(float(np.percentile(timings,95)),3)
    (out/'ui_labels_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
