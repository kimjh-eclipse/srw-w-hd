"""Isolated emulation session. Restarting/switching a ROM never reinitializes
the legacy core twice in one process, and a core failure cannot close the UI.
"""
from pathlib import Path
import hashlib,json,time,traceback,os
import numpy as np
from multiprocessing import shared_memory
from render_resolution import SCREEN_RGBA_BYTES,DEFAULT_WIDTH,clamp_width

TOP_BYTES=SCREEN_RGBA_BYTES
BOTTOM_BYTES=SCREEN_RGBA_BYTES
FRAME_BYTES=TOP_BYTES+BOTTOM_BYTES+16

def rom_hash(path):
    digest=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(4*1024*1024),b''):digest.update(block)
    return digest.hexdigest()

def worker_main(pipe,memory_name,lock,config):
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'
    from hd_core import Core,HERE,ROOT
    from frame_compositor import FrameCompositor
    from render_budget import RenderBudget
    from battle_rumble import BattleRumble
    import pygame
    memory=shared_memory.SharedMemory(name=memory_name);core=None;channel=None;timer=None
    if os.name=='nt':
        # Windows timer precision belongs to each process. The UI's request
        # does not give this separate emulation process accurate 2ms sleeps.
        import ctypes
        candidate=ctypes.WinDLL('winmm')
        if candidate.timeBeginPeriod(1)==0:timer=candidate
    def send(event,**data):
        try:pipe.send(dict(event=event,**data))
        except (BrokenPipeError,EOFError,OSError):pass
    try:
        rom=Path(config['rom']);digest=rom_hash(rom);demo=bool(config.get('demo'))
        canonical=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').resolve()
        directory=Path(config['save_root'])/('demo' if demo else 'games')/digest[:16] if config.get('save_root') else HERE/('demo_data' if demo else 'user_data')
        if not config.get('save_root') and rom.resolve()!=canonical:directory=directory/'games'/digest[:16]
        if config.get('profile_render'):os.environ['SRWW_RENDER_PROFILE']=config['profile_render']
        else:os.environ.pop('SRWW_RENDER_PROFILE',None)
        normal_frameskip=1 if config.get('legacy_timing') else 0
        display_rate=30 if config.get('legacy_timing') else 60
        core=Core(rom,enabled=config.get('hd',True),demo=demo,user_dir=directory,frameskip=normal_frameskip)
        native_fallback=hasattr(core.api,'retro_srw_native_hd_fallback')
        compositor=FrameCompositor(async_parts=native_fallback,dynamic_parts=core.dynamic_bridge,memory_name=memory_name,lock=lock,present=config.get('present'));feedback=BattleRumble()
        compositor.render_width=clamp_width(config.get('render_width',DEFAULT_WIDTH))
        budget=RenderBudget(compositor.render_width,config.get('hd_auto_quality',True))
        compositor.render_width=budget.width
        try:
            pygame.mixer.init(44100,-16,2,1024);channel=pygame.mixer.Channel(0);channel.set_volume(config.get('volume',70)/100)
        except pygame.error as error:send('audio_unavailable',message=str(error))
        paused=bool(config.get('paused'));speed=1;frame=64700 if demo else 0
        schedule=json.loads((HERE/'demo_input.json').read_text()) if demo else []
        if demo:core.load(HERE/'demo.state',refresh_code=True)
        if config.get('state'):
            core.load(Path(config['state']),refresh_code=rom.resolve()==canonical);frame=config.get('state_frame',frame)
        if native_fallback:core.set_ready_parts(compositor.ready)
        core.buttons=set();frame+=core.refresh_video();core.audio.clear()
        sequence=0;running=True;held=set();pressed=set();touch=None;pending_touch=None;input_stamp=None;status_frame=frame;status_sequence=0;status_time=time.perf_counter();next_frame=time.perf_counter();last_draw=0;last_status=0;draw_requested=True;last_video_epoch=-1
        def slots():return [i for i in range(1,6) if (directory/f'slot_{i}.state').exists()]
        send('loaded',rom=str(rom),save_dir=str(directory),paused=paused,hd=core.enabled,slots=slots(),audio=bool(channel),rom_hash=digest,demo=demo)
        def store(path):
            path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);temp=path.with_suffix(path.suffix+'.tmp')
            core.save(temp);temp.replace(path)
            path.with_suffix(path.suffix+'.json').write_text(json.dumps(dict(rom_hash=digest,rom=rom.name,demo=demo,frame=frame)),encoding='utf-8')
        last_asset_refresh=0;video_started=False;video_ready_deadline=None
        while running:
            while pipe.poll():
                message=pipe.recv();op=message.get('op')
                try:
                    if op=='quit':running=False;break
                    if op=='input':
                        incoming=set(message.get('buttons',[]))
                        if not paused:pressed.update(incoming-held)
                        held=incoming;touch=message.get('touch')
                        if touch is not None and not paused:pending_touch=touch
                        input_stamp=message.get('sent_at') if not paused else None
                    elif op=='pause':
                        feedback.reset();send('rumble',duration=0)
                        paused=bool(message['value']);pressed.clear();pending_touch=None;next_frame=time.perf_counter();draw_requested=True;core.audio.clear()
                        if channel:channel.stop()
                        send('paused',value=paused,frame=frame)
                    elif op=='hd':
                        core.set_hd(bool(message['value']));core.buttons=set();frame+=core.refresh_video();core.audio.clear();draw_requested=True
                        send('hd',value=core.enabled)
                    elif op=='volume':
                        if channel:channel.set_volume(max(0,min(100,message['value']))/100)
                    elif op=='resolution':
                        compositor.render_width=budget.configure(width=clamp_width(message['width']));draw_requested=True
                    elif op=='layout':
                        if compositor.layout is not None:
                            compositor.layout=dict(compositor.layout,size=tuple(message['size']),rects=[tuple(r) if r else None for r in message['rects']]);draw_requested=True
                    elif op=='quality':
                        compositor.render_width=budget.configure(enabled=bool(message['value']));draw_requested=True
                    elif op=='speed':
                        requested=message.get('value',1);speed=requested if requested in (1,2,4,8,16) else 1
                        core.set_frameskip(normal_frameskip if speed==1 else 7)
                        next_frame=time.perf_counter();core.audio.clear();feedback.reset();send('rumble',duration=0)
                        if channel:channel.stop()
                        send('speed',value=speed)
                    elif op=='save':
                        path=Path(message.get('path') or directory/f"slot_{message.get('slot',1)}.state")
                        store(path);send('saved',path=str(path),slots=slots())
                    elif op=='load':
                        feedback.reset();send('rumble',duration=0)
                        path=Path(message.get('path') or directory/f"slot_{message.get('slot',1)}.state")
                        if not path.exists():raise ValueError('이 칸에는 저장된 게임이 없습니다.')
                        meta_path=path.with_suffix(path.suffix+'.json');meta=json.loads(meta_path.read_text()) if meta_path.exists() else {}
                        if meta.get('rom_hash',digest)!=digest:raise ValueError('다른 롬에서 저장한 파일입니다. 해당 롬을 먼저 열어주세요.')
                        core.load(path);frame=meta.get('frame',frame);core.buttons=set();frame+=core.refresh_video();core.audio.clear();draw_requested=True
                        # Manual loading hands control back to the player.
                        demo=False;schedule=[];paused=True;next_frame=time.perf_counter()
                        if channel:channel.stop()
                        send('state_loaded',path=str(path),paused=True,demo=False)
                    elif op=='capture':
                        image=compositor.capture(core,paused)
                        image.save(message['path']);send('captured',path=message['path'])
                except Exception as error:send('command_error',op=op,message=str(error))
            if not running:break
            now=time.perf_counter()
            if (paused or not video_started) and now-last_asset_refresh>=2:
                # Newly installed lazy art may arrive while this frame is
                # paused. Repaint it without advancing the emulated game.
                last_asset_refresh=now;draw_requested=True
            if not paused and video_started:
                steps=0
                while now>=next_frame and steps<(1 if speed==1 else 8) and not paused:
                    core.buttons=held|pressed|({e['button'] for e in schedule if e['from']<=frame<e['to']} if demo else set())
                    if native_fallback:core.set_ready_parts(compositor.ready)
                    core.touch=touch if touch is not None else pending_touch;core.run();pressed.clear();pending_touch=None;frame+=1;steps+=1;next_frame+=1/(59.8261*speed)
                    if input_stamp is not None:
                        send('input_ack',sent_at=input_stamp,applied_at=time.perf_counter(),frame=frame);input_stamp=None
                    effect=feedback.sample(core)
                    if effect and speed==1:send('rumble',frame=frame,**effect)
                    if demo and frame>=68001:
                        feedback.reset();send('rumble',duration=0)
                        paused=True;send('demo_finished',paused=True)
                if now-next_frame>.25:next_frame=now
                if speed!=1:core.audio.clear()
                if speed==1 and channel and len(core.audio)>=8192 and channel.get_queue() is None:
                    sound=pygame.mixer.Sound(buffer=bytes(core.audio[:8192]));del core.audio[:8192]
                    if channel.get_busy():channel.queue(sound)
                    else:channel.play(sound)
                if len(core.audio)>44100*4:del core.audio[:-44100*4]
            else:
                next_frame=now;core.audio.clear()
            now=time.perf_counter()
            finished=compositor.take()
            if finished is not None and paused and draw_requested and finished[2]!=frame:finished=None
            if finished is not None:
                if video_started and not paused and speed==1 and compositor.render_times and not compositor.needs_refresh:
                    compositor.render_width=budget.observe(compositor.render_times[-1])
                if not video_started:
                    if video_ready_deadline is None:video_ready_deadline=time.perf_counter()+2
                    if not compositor.needs_refresh or time.perf_counter()>=video_ready_deadline:video_started=True;next_frame=time.perf_counter()
                top,bottom,rendered_frame=finished;direct=isinstance(top,str)
                if top is not None and not direct:
                    with lock:
                        np.frombuffer(memory.buf,dtype='uint8',count=TOP_BYTES)[:]=top
                        np.frombuffer(memory.buf,dtype='uint8',count=BOTTOM_BYTES,offset=TOP_BYTES)[:]=bottom
                sequence+=1;send('frame',sequence=sequence,frame=rendered_frame,bottom_revision=compositor.bottom_revision,render_size=compositor.render_size,direct=direct)
            if native_fallback:core.set_ready_parts(compositor.ready)
            if compositor.future is None and (paused or not video_started or draw_requested or core.video_epoch!=last_video_epoch) and (draw_requested or ((paused or not video_started) and compositor.needs_refresh and now-last_draw>=.1) or (not paused and video_started and (speed==1 or now-last_draw>=1/15))):
                if compositor.submit(core,paused or not video_started,frame):
                    last_draw=now;last_video_epoch=core.video_epoch;draw_requested=False
            if now-last_status>1:
                costs=list(compositor.render_times)
                send('status',frame=frame,paused=paused,hd=core.enabled,parts=int((core.parts[:,0]>0).sum()),demo=demo,speed=speed,render_ms=sum(costs)/len(costs) if costs else None,render_p95_ms=sorted(costs)[min(len(costs)-1,int(len(costs)*.95))] if costs else None,emulation_fps=(frame-status_frame)/max(.001,now-status_time),composition_fps=(sequence-status_sequence)/max(.001,now-status_time));last_status=now;status_time=now;status_frame=frame;status_sequence=sequence
            if paused:time.sleep(.01)
            else:
                delay=next_frame-time.perf_counter()
                if delay>0:time.sleep(min(.002,delay))
    except (EOFError,BrokenPipeError):pass
    except Exception as error:
        from runtime_paths import log_path
        log_path('player_worker_error.log').write_text(traceback.format_exc(),encoding='utf-8');send('error',message=str(error))
    finally:
        if timer is not None:timer.timeEndPeriod(1)
        send('rumble',duration=0)
        if core:
            try:core.close()
            except Exception:pass
        if 'compositor' in locals():compositor.close()
        if 'renderer' in locals():renderer.parts_renderer.close()
        try:pygame.mixer.quit()
        except Exception:pass
        memory.close();send('closed');pipe.close()
