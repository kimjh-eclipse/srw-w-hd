"""Check PBO pixel/tag pairing, size/paused resets, and RGBA display transport."""
import json,os,queue,threading
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import patch
import numpy as np
from PIL import Image
from gpu_surface import Surface,backend
from gpu_display import RGBFrame,GPUDisplay

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'test_current/performance'

def scene(frame,size):
    w,h=size
    native=np.empty((24,32,3),dtype='uint8');native[:]=[(frame*37)%240,(frame*59)%240,(frame*83)%240]
    native[::2,::2]=[(frame*11+70)%250,41,203]
    surface=Surface.from_native(native,size)
    expected=Image.fromarray(native).resize(size,Image.Resampling.NEAREST).convert('RGBA')
    color=((frame*7+23)%255,(frame*13+54)%255,(frame*19+87)%255,255)
    tile=Image.new('RGBA',(13,11),color);x=(frame*17)%(w-14);y=(frame*7)%(h-12)
    surface.alpha_composite(tile,(x,y));expected.alpha_composite(tile,(x,y))
    return surface,np.asarray(expected)

def verify_pbo():
    gpu=backend();gpu.reset_pipeline();expected={};markers={};records=[]
    for frame in range(15):
        size=(128,96) if frame<6 or frame>=11 else (160,120)
        surface,pixels=scene(frame,size);expected[frame]=pixels;markers[frame]=Image.new('RGB',(1,1),(frame,0,0))
        result,tag=surface.rgba_pipeline((frame,markers[frame],frame*3))
        assert tag[1] is markers[tag[0]] and tag[2]==tag[0]*3
        assert np.array_equal(result,expected[tag[0]]),(frame,tag[0],result.shape,expected[tag[0]].shape)
        records.append([frame,tag[0],*size])
    # Production paused path explicitly resets the queued read before sync draw.
    gpu.reset_pipeline();paused,paused_pixels=scene(40,(160,120))
    assert np.array_equal(paused.rgba(),paused_pixels)
    fresh,fresh_pixels=scene(41,(160,120));result,tag=fresh.rgba_pipeline(('resumed',))
    assert tag==('resumed',) and np.array_equal(result,fresh_pixels)
    return dict(distinct_moving_layers=15,pixel_tag_pairs=records,resolution_changes=True,paused_reset_drops_old_pending=True)

def verify_frame_process():
    import frame_process as fp
    gpu=backend();gpu.reset_pipeline()
    class FakeRenderer:
        def __init__(self):
            self.size=(128,96);self.bottom_generation=0
            self.parts_renderer=NS(dynamic_bindings=queue.SimpleQueue(),pending={},unmapped_pending={},ready_generation=0,ready_bindings=lambda:[])
            self.portraits=NS(pending={});self.backgrounds=NS(pending={});self.scenario_backgrounds=NS(pending={});self.battle_backgrounds=NS(pending={})
        def set_resolution(self,width):self.size=(width,width*3//4)
        def render_top(self,native,ids,hd,paused,**kwargs):return scene(int(hd[0]),self.size)[0]
        def render_bottom(self,native,hd):
            self.bottom_generation=int(hd[0])*5
            return Image.new('RGB',self.size,(int(hd[0]),23,67))
    renderer=FakeRenderer();expected={};checks=[]
    with patch.multiple(fp,_renderer=renderer,_memory=None,_lock=None,_last_bottom=None,_last_ready=-1):
        for frame,width,paused in [(1,128,False),(2,128,False),(3,128,False),(4,160,False),(5,160,True),(6,160,False),(7,160,False)]:
            expected[frame]=scene(frame,(width,width*3//4))[1]
            snapshot=(None,None,(frame,),paused,frame,{'render_width':width})
            (top,bottom,returned),ready=fp._render_snapshot(snapshot)
            pixels=top.reshape(ready[5][1],ready[5][0],4)
            assert np.array_equal(pixels,expected[returned]),('top',frame,returned)
            assert ready[4]==returned*5,('revision',frame,returned,ready[4])
            bottom_pixels=bottom.reshape(ready[5][1],ready[5][0],4)
            assert np.all(bottom_pixels[:,:,:3]==[returned,23,67]),('bottom',frame,returned)
            checks.append(dict(submitted=frame,returned=returned,bottom_revision=ready[4],paused=paused,width=width))
    gpu.reset_pipeline();offset=1440*1080*4;memory=NS(buf=bytearray(offset*2+16))
    with patch.multiple(fp,_renderer=renderer,_memory=memory,_lock=threading.Lock(),_last_bottom=None,_last_ready=-1):
        for frame in (20,21,22):
            size=(128,96);expected[frame]=scene(frame,size)[1]
            result,ready=fp._render_snapshot((None,None,(frame,),False,frame,{'render_width':size[0]}))
            assert result[:2]==(None,None)
            header=np.frombuffer(memory.buf,dtype='uint32',count=4,offset=offset*2)
            returned=result[2];assert list(header)==[*size,returned,returned*5]
            top=np.frombuffer(memory.buf,dtype='uint8',count=size[0]*size[1]*4).reshape(size[1],size[0],4)
            bottom=np.frombuffer(memory.buf,dtype='uint8',count=size[0]*size[1]*4,offset=offset).reshape(size[1],size[0],4)
            assert np.array_equal(top,expected[returned]);assert np.all(bottom[:,:,:3]==[returned,23,67])
            checks.append(dict(submitted=frame,returned=returned,bottom_revision=int(header[3]),shared_memory_header_exact=True))
    return checks

def verify_rgbframe_sdl():
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'
    import pygame
    from pygame._sdl2.video import Window,Renderer
    w,h=128,96;surface,rgba=scene(12,(w,h));raw=surface.rgba().tobytes();frame=RGBFrame(raw,(w,h))
    assert frame.format=='RGBA' and frame.tobytes()==raw
    assert np.array_equal(np.asarray(frame),rgba[:,:,:3])
    copied=frame.__array__(copy=True);copied[:]=0;assert np.any(np.asarray(frame))
    image_path=OUT/'rgba_transport_saved.png';frame.save(image_path)
    assert np.array_equal(np.asarray(Image.open(image_path)),rgba[:,:,:3])
    pygame.display.init();window=Window('RGBA transport verification',size=(w,h),hidden=True)
    display=GPUDisplay.__new__(GPUDisplay);display.pygame=pygame;display.window=window
    display.renderer=Renderer(window,accelerated=1,vsync=False);display.textures=[None,None];display.sources=[None,None];display.presented=0
    try:
        display.draw([frame,None],[(0,0,w,h),None])
        readback=pygame.surfarray.array3d(display.renderer.to_surface()).transpose(1,0,2)
        assert np.array_equal(readback,rgba[:,:,:3]),int(np.abs(readback.astype('int16')-rgba[:,:,:3]).max())
    finally:window.destroy()
    return dict(rgba_format=True,array_rgb=True,copy_isolated=True,png_rgb=True,hidden_sdl_gpu_readback_exact=True)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    report=dict(pbo=verify_pbo(),production_frame_process=verify_frame_process(),rgbframe=verify_rgbframe_sdl())
    (OUT/'rgba_transport_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
