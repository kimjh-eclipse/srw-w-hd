"""Replay native Deathscythe MAP Beam Scythe from the verified forecast state."""
import json,time,ctypes as C
from PIL import Image,ImageDraw
from hd_core import Core,ROOT
from hd_renderer import HDRenderer

def main():
    out=ROOT/'test_current/combat';c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'wing_saves');r=HDRenderer(async_parts=True,dynamic_parts=True);r.set_resolution(768);panels=[];cutins=set();bindings=set();started=False;start=time.perf_counter()
    try:
        c.load(out/'duo_map_forecast.state')
        for frame in range(6000):
            c.buttons={8} if frame<5 else {8,11} if started and frame%120<5 else set();c.set_ready_parts(r.parts_renderer);c.run();c.audio.clear()
            ram=c.api.retro_get_memory_data(2);active=C.c_uint32.from_address(ram+0xa6f38).value==128 and C.c_uint32.from_address(ram+0x1e7a10).value==0
            started|=active
            if started and not active and frame>180:break
            if frame%8==0:
                image=r.render_top(c.native,c.ids,c.hd,paused=True,parts=c.parts,obj=c.obj.raw,owners=c.owners,bgpriors=c.bgpriors,bgparts=c.bgparts,part_palettes=c.part_palettes,backgrounds=c.backgrounds,bg_layout=c.bg_layout,unknown=c.unknown_snapshot(),sub_parts=(c.sub_parts,c.sub_owners,c.sub_oam.raw,c.sub_palettes,c.sub_ids,c.sub_priorities))
                bindings.update(int(x) for x in c.parts[:,0] if x)
                if c.hd[0]:cutins.add(int(c.hd[0]));image.save(out/'duo_map_cutin_hd.png')
                if active and frame%80==0:
                    if frame==800:c.save(out/'duo_map_attack.state')
                    panel=image.resize((384,288));ImageDraw.Draw(panel).text((2,2),f'MAP beam scythe {frame}',fill='yellow');panels.append(panel)
        sheet=Image.new('RGB',(1920,288*((len(panels)+4)//5)))
        for n,panel in enumerate(panels):sheet.paste(panel,(n%5*384,n//5*288))
        sheet.save(out/'duo_map_replay.png');report=dict(started=started,frames=frame,cutin_ids=sorted(cutins),bindings=sorted(bindings),prepare_errors=r.parts_renderer.prepare_errors,seconds=time.perf_counter()-start,test_fixture_morale_override=True)
        (out/'duo_map_verification.json').write_text(json.dumps(report,indent=2));print(report);assert started
    finally:c.close();r.parts_renderer.close()

if __name__=='__main__':main()
