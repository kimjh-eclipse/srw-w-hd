"""1920x1080 W cut-in preview/player using the modified open-source core."""
from pathlib import Path
import ctypes as C
import argparse,json,time,wave,traceback
import numpy as np
from hd_core import Core,HERE,ROOT
from hd_renderer import HDRenderer

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--demo',action='store_true');parser.add_argument('--verify',action='store_true');parser.add_argument('--frames',type=int,default=0);parser.add_argument('--state',type=Path);parser.add_argument('--state-frame',type=int,default=64700)
    args=parser.parse_args();rom=ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds'
    if args.verify:
        import runpy
        runpy.run_path(str(ROOT/'scripts/verify/verify_parts.py'))['verify']()
        return
    core=Core(rom,demo=args.demo or args.verify);renderer=HDRenderer();demo_start=64700;demo_frame=demo_start
    events=json.loads((HERE/'demo_input.json').read_text()) if args.demo or args.verify else []
    if args.state:
        core.load(args.state,refresh_code=True);core.run();core.audio.clear();demo_frame=args.state_frame+1
    elif args.demo or args.verify:core.load(HERE/'demo.state',refresh_code=True)
    C.windll.user32.SetProcessDPIAware()
    import pygame
    pygame.mixer.pre_init(44100,-16,2,1024);pygame.init()
    screen=pygame.display.set_mode((1280,720),pygame.RESIZABLE);pygame.display.set_caption('슈퍼로봇대전 W · HD 컷인')
    clock=pygame.time.Clock();paused=bool(args.state);running=True;demo_paused=False;active=0;ui_frames=0;next_frame=time.perf_counter()
    channel=pygame.mixer.Channel(0) if pygame.mixer.get_init() else None
    keys={pygame.K_z:8,pygame.K_x:0,pygame.K_c:9,pygame.K_v:1,pygame.K_RETURN:3,pygame.K_RSHIFT:2,pygame.K_UP:4,pygame.K_DOWN:5,pygame.K_LEFT:6,pygame.K_RIGHT:7,pygame.K_a:10,pygame.K_s:11}
    try:
        while running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:running=False
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:running=False
                    elif event.key==pygame.K_SPACE:paused=not paused
                    elif event.key==pygame.K_F1:
                        core.set_hd(not core.enabled)
                        if paused:core.run()
                    elif event.key==pygame.K_F5:core.save(core.user/'current.state')
                    elif event.key==pygame.K_F8 and (core.user/'current.state').exists():core.load(core.user/'current.state')
                    elif event.key==pygame.K_r and args.demo:
                        core.load(HERE/'demo.state',refresh_code=True);core.audio.clear()
                        demo_frame=demo_start;demo_paused=False;active=0;paused=False;next_frame=time.perf_counter()
                        if channel:channel.stop()
            held=pygame.key.get_pressed();core.buttons={button for key,button in keys.items() if held[key]}
            if args.demo and not demo_paused:core.buttons|={e['button'] for e in events if e['from']<=demo_frame<e['to']}
            w,h=screen.get_size();scale=min(w/1920,h/1080);ox=(w-1920*scale)/2;oy=(h-1080*scale)/2
            mx,my=pygame.mouse.get_pos();x=(mx-ox)/scale;y=(my-oy)/scale
            core.touch=None
            if pygame.mouse.get_pressed()[0] and 1440<=x<1920 and 360<=y<720:
                core.touch=(int(((x-1440)/480*2-1)*32767),int(((y-360)/360*2-1)*32767))
            if not paused:
                steps=0
                while time.perf_counter()>=next_frame and steps<4 and not paused:
                    if args.demo and not demo_paused:core.buttons|={e['button'] for e in events if e['from']<=demo_frame<e['to']}
                    core.run();demo_frame+=1;steps+=1;next_frame+=1/59.8261
                    if args.demo and core.hd[0]:active+=1
                    if args.demo and demo_frame>=68001 and not demo_paused:paused=True;demo_paused=True
                if time.perf_counter()-next_frame>.25:next_frame=time.perf_counter()
                if channel and len(core.audio)>=8192 and channel.get_queue() is None:
                    sound=pygame.mixer.Sound(buffer=bytes(core.audio[:8192]));del core.audio[:8192]
                    if channel.get_busy():channel.queue(sound)
                    else:channel.play(sound)
                if len(core.audio)>44100*4:del core.audio[:-44100*4]
            else:
                next_frame=time.perf_counter()
                if channel:channel.stop();core.audio.clear()
            image=renderer.render(core.native,core.ids,core.hd,paused,robot=core.robot,obj=core.obj.raw,parts=core.parts,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes)
            surf=pygame.image.frombuffer(image.tobytes(),image.size,'RGB')
            screen.fill((0,0,0));screen.blit(pygame.transform.smoothscale(surf,(round(1920*scale),round(1080*scale))),(round(ox),round(oy)));pygame.display.flip();clock.tick(60)
            ui_frames+=1
            if args.frames and ui_frames>=args.frames:running=False
        if args.frames:
            (HERE/'ui_verification.json').write_text(json.dumps(dict(ui_frames=ui_frames,game_frame=demo_frame,hd_active_frames=active,auto_pause_reached=demo_paused,audio_device=bool(channel)),indent=2))
    finally:core.close();pygame.quit()

if __name__=='__main__':
    try:
        main()
        (HERE/'hd_player_error.log').write_text('',encoding='utf-8')
    except Exception:
        (HERE/'hd_player_error.log').write_text(traceback.format_exc(),encoding='utf-8');raise
