"""Read-only capture of the ROM's built-in battle demo and native resources."""
import ctypes as C,json,zlib,time
import numpy as np
from PIL import Image,ImageDraw
from hd_core import Core,ROOT
OUT=ROOT/'test_current/attract';OUT.mkdir(exist_ok=True)
TARGET=ROOT.parent.parent/'Users' # The attached target is read from its exact path below.
target=np.asarray(Image.open('C:/Users/OXP2/AppData/Local/Temp/codex-clipboard-5e0fd4bd-3539-477a-9939-a4731d56851e.png').convert('RGB').resize((256,134),Image.Resampling.NEAREST)).astype('int16')
def main():
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True,user_dir=OUT/'save_data')
    oam=C.create_string_buffer(1024);pal=C.create_string_buffer(512);regs=C.create_string_buffer(128);vram=C.create_string_buffer(131072)
    core.api.retro_srw_copy_obj_debug.argtypes=[C.c_void_p,C.c_void_p,C.c_void_p]
    best=1000;best_frame=0;frames=[];start=time.perf_counter()
    try:
        for f in range(15001):
            core.run();core.audio.clear()
            if f%15:continue
            image=Image.fromarray(core.native[:192]);score=float(np.abs(core.native[:134].astype('int16')-target).mean())
            if score<best*.98:
                best=score;best_frame=f;core.save(OUT/'target.state');image.save(OUT/'target_native.png')
                core.api.retro_srw_copy_obj_debug(oam,pal,regs);core.api.retro_srw_copy_vram(0x06400000,vram,131072)
                np.savez_compressed(OUT/'target_obj.npz',oam=np.frombuffer(oam.raw,'uint8'),palette=np.frombuffer(pal.raw,'uint8'),regs=np.frombuffer(regs.raw,'uint8'),vram=np.frombuffer(vram.raw,'uint8'))
                (OUT/'target.json').write_text(json.dumps(dict(frame=f,score=best)))
            if f%30==0:image.save(OUT/f'frame_{f:05}.png');frames.append(f)
            if f%600==0:(OUT/'progress.json').write_text(json.dumps(dict(frame=f,best_frame=best_frame,score=best,seconds=round(time.perf_counter()-start,1))))
    finally:core.close()
    for page in range((len(frames)+59)//60):
        sheet=Image.new('RGB',(1536,1200),'#18202d');draw=ImageDraw.Draw(sheet)
        for cell,f in enumerate(frames[page*60:page*60+60]):
            im=Image.open(OUT/f'frame_{f:05}.png').resize((192,144));x=cell%8*192;y=cell//8*150;sheet.paste(im,(x,y));draw.text((x+4,y+128),str(f),fill='white')
        sheet.save(OUT/f'review_{page:02}.png')
    (OUT/'capture.json').write_text(json.dumps(dict(frames=frames,best_frame=best_frame,score=best,seconds=round(time.perf_counter()-start,1)),indent=2));print(best_frame,best)
if __name__=='__main__':main()
