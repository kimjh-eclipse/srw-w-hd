"""Replay each legal weapon choice from real native battle-selection states."""
import sys,json,time,ctypes as C
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from hd_core import Core,ROOT
from hd_renderer import HDRenderer

def main():
    pilot=sys.argv[1] if len(sys.argv)>1 else 'sandrock';out=ROOT/'test_current/combat';fixture=out/(pilot+'_weapons.state')
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'wing_saves')
    r=HDRenderer(async_parts=True,dynamic_parts=True);r.set_resolution(768);results=[]
    def steps(buttons,frames):
        c.buttons=set(buttons)
        for _ in range(frames):c.run();c.audio.clear()
        c.buttons=set()
    def render():
        return r.render_top(c.native,c.ids,c.hd,paused=True,parts=c.parts,obj=c.obj.raw,owners=c.owners,bgpriors=c.bgpriors,bgparts=c.bgparts,part_palettes=c.part_palettes,backgrounds=c.backgrounds,bg_layout=c.bg_layout,unknown=c.unknown_snapshot(),sub_parts=(c.sub_parts,c.sub_owners,c.sub_oam.raw,c.sub_palettes,c.sub_ids,c.sub_priorities))
    try:
        for weapon in ([int(x) for x in sys.argv[2].split(',')] if len(sys.argv)>2 else range(3)):
            c.load(fixture);steps([],15)
            # Fixtures are saved with the second weapon highlighted.
            if weapon!=1:steps([4 if weapon==0 else 5],5);steps([],15)
            Image.fromarray(c.native).save(out/f'{pilot}_weapon_{weapon}_menu.png')
            steps([8],5);steps([],40)
            if pilot=='duo':
                # Own-turn targeting starts on the attacker, not the enemy.
                steps([7],1);steps([],10);steps([7],1);steps([],10);steps([4],1);steps([],10)
            steps([8],5);steps([],40)
            if pilot=='duo':steps([8],5);steps([],40)
            frames=[];cutins=[];seen=set();start=time.perf_counter();battle=False;last_image=None
            for frame in range(3000):
                c.set_ready_parts(r.parts_renderer);c.run();c.audio.clear()
                ram=c.api.retro_get_memory_data(2)
                active=C.c_uint32.from_address(ram+0xa6f38).value==128 and C.c_uint32.from_address(ram+0x1e7a10).value==0
                battle|=active
                if battle and not active and frame>180:break
                if frame%8==0:
                    image=render();last_image=image
                    if c.hd[0] and int(c.hd[0]) not in cutins:
                        cutins.append(int(c.hd[0]));c.save(out/f'{pilot}_cutin.state');image.save(out/f'{pilot}_cutin_hd.png');Image.fromarray(c.native).save(out/f'{pilot}_cutin_native.png')
                    for bid in c.parts[:,0]:
                        if bid:seen.add(int(bid))
                    if active and frame%80==0:
                        panel=image.resize((384,288));ImageDraw.Draw(panel).text((2,2),f'{pilot} weapon {weapon} frame {frame}',fill='yellow');frames.append(panel)
                # Advance explicit text waits without repeatedly choosing menus.
                c.buttons={11,8} if active and frame%120<5 else set()
            if last_image:last_image.save(out/f'{pilot}_weapon_{weapon}_last.png')
            sheet=Image.new('RGB',(384*5,288*((len(frames)+4)//5)))
            for n,panel in enumerate(frames):sheet.paste(panel,(n%5*384,n//5*288))
            sheet.save(out/f'{pilot}_weapon_{weapon}_replay.png')
            record=dict(pilot=pilot,weapon_index=weapon,battle_started=battle,frames=frame,cutin_ids=cutins,observed_bindings=sorted(seen),seconds=time.perf_counter()-start,prepare_errors=dict(r.parts_renderer.prepare_errors),unmapped_misses={str(k):v for k,v in r.parts_renderer.unmapped_misses.items()})
            results.append(record);(out/(pilot+'_weapon_verification.json')).write_text(json.dumps(results,indent=2));print(pilot,weapon,'battle',battle,'frames',frame,'cutins',cutins,'bindings',len(seen),flush=True)
        assert all(row['battle_started'] for row in results)
    finally:c.close();r.parts_renderer.close()

if __name__=='__main__':main()
