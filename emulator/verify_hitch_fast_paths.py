"""Check exact repair plans, incremental identities and joint GPU screen pixels."""
import json,time
from pathlib import Path
import numpy as np
from PIL import Image
from hd_fonts import FontRenderer,ROOT
from hd_map_icons import MapIconRenderer
from gpu_surface import Surface,backend


def reference_plan(mask):
    values=[[],[],[],[],[]]
    for y in np.flatnonzero(mask.any(1)):
        keep=np.flatnonzero(~mask[y]);xs=np.flatnonzero(mask[y])
        if not len(keep):continue
        slots=np.searchsorted(keep,xs);left=keep[np.maximum(slots-1,0)];right=keep[np.minimum(slots,len(keep)-1)]
        for out,items in zip(values,([y]*len(xs),xs,left,right,np.divide(xs-left,right-left,out=np.zeros(len(xs),dtype='float64'),where=right!=left))):out.extend(items)
    return tuple(np.asarray(a,dtype='intp') for a in values[:4])+(np.asarray(values[4],dtype='float64')[:,None],)


def main():
    rng=np.random.default_rng(31);font=FontRenderer();masks=[]
    for rate in (0,.05,.35,.8,1):
        mask=rng.random((192,256))<rate;mask[0]=True;mask[1]=False;mask[2,:50]=True;mask[3,200:]=True;masks.append(mask)
    for mask in masks:
        font.last_mask=mask
        assert all(np.array_equal(a,b) for a,b in zip(reference_plan(mask),font._heal_plan()))
    fast=MapIconRenderer();slow=MapIconRenderer();iconcases=0
    native=np.full((192,256,3),[3,7,11],dtype='uint8');resource=next(iter(fast.records));idx=fast.indices[resource];colors=fast.palettes[3938].astype('uint8')
    previous=None
    for frame in range(100):
        if previous:
            x,y=previous;native[y:y+16,x:x+16]=[3,7,11]
        x=(frame*7)%240;y=(frame*3)%176
        native[y:y+16,x:x+16]=colors[idx];previous=(x,y)
        native[180:184,frame%200:frame%200+8]=rng.integers(0,256,(4,8,3),dtype='uint8')
        result=fast.recognize(native);slow.previous_code=None;slow.cache.clear();expected=slow.recognize(native)
        assert result==expected,(frame,result,expected);iconcases+=1
    max_difference=0;gpu_cases=0
    for name,part in [('forecast_confirm_0.png',slice(192,384)),('combat_hud_native.png',slice(0,192))]:
        native=np.asarray(Image.open(ROOT/'test_current/font'/name).convert('RGB'))[part]
        for width in (768,832,960):
            size=(width,width*3//4);cpu=Image.fromarray(native).resize(size,Image.Resampling.NEAREST);gpu=Surface.from_native(native,size)
            FontRenderer().compose(cpu,native);FontRenderer().compose(gpu,native)
            diff=np.abs(np.asarray(cpu).astype('int16')-np.asarray(gpu).astype('int16'));max_difference=max(max_difference,int(diff.max()));assert diff.max()<=1
            joined=Surface((width,size[1]*2));joined.paste(gpu);joined.paste(gpu,(0,size[1]));pixels=joined.rgba();expected=gpu.rgba()
            assert np.array_equal(pixels[:size[1]],expected) and np.array_equal(pixels[size[1]:],expected);gpu_cases+=1
    pair_cases=0
    for width in (768,960,832):
        size=(width,width*3//4);bottom=None;expected={}
        for frame in range(15):
            rgb=np.full((192,256,3),[frame*9,32,76],dtype='uint8');top=Surface.from_native(rgb,size)
            if frame%3==0:
                lower=np.full((192,256,3),[12,frame*11,67],dtype='uint8');bottom=Surface.from_native(lower,size)
            expected[frame]=(rgb[0,0],lower[0,0].copy())
            upper,lower_pixels,tag=backend().render_pair(top,bottom,(frame,bottom,frame//3));a,b=expected[tag[0]]
            assert np.all(upper[:,:,:3]==a) and np.all(lower_pixels[:,:,:3]==b),(width,frame,tag[0]);pair_cases+=1
    backend().reset_pipeline()
    result=dict(repair_plans_pixel_exact=len(masks),incremental_icon_frames_exact=iconcases,font_max_channel_difference=max_difference,joint_gpu_screens_exact=gpu_cases,paired_gpu_frame_tags_exact=pair_cases)
    (ROOT/'test_current/performance/hitch_fast_paths_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))


if __name__=='__main__':main()
