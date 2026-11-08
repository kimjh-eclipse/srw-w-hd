"""Keep native SDL controller discovery and rumble outside the Tk/GL process."""
import multiprocessing as mp
import os,queue,time,math
from pathlib import Path


def pad_worker(commands,updates,parent_pid,testing=False):
    import faulthandler
    crash_log=open(Path(__file__).with_name('pad_native_crash.log'),'a',encoding='utf-8')
    faulthandler.enable(file=crash_log,all_threads=True)
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'
    os.environ['SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS']='1'
    import ctypes as C
    import threading
    timer=None
    if os.name=='nt':
        timer=C.WinDLL('winmm');timer.timeBeginPeriod(1)
        def watch_parent():
            api=C.WinDLL('kernel32');api.OpenProcess.argtypes=[C.c_uint,C.c_int,C.c_uint];api.OpenProcess.restype=C.c_void_p
            handle=api.OpenProcess(0x00100000,False,parent_pid)
            if handle:
                api.WaitForSingleObject.argtypes=[C.c_void_p,C.c_uint];api.WaitForSingleObject(handle,0xffffffff);os._exit(0)
        threading.Thread(target=watch_parent,daemon=True).start()
    import pygame
    from player_controls import DEFAULT_PAD,sdl_pad_mapping
    pads={};controllers={};mapping={};virtual=None;test_result={};running=True
    try:
        pygame.display.init();pygame.joystick.init()
        from pygame._sdl2 import controller
        controller.init()
        if testing:
            sdl=C.CDLL(str(Path(pygame.__file__).parent/'SDL2.dll'))
            signatures={'SDL_JoystickAttachVirtual':([C.c_int]*4,C.c_int),'SDL_JoystickDetachVirtual':([C.c_int],C.c_int),'SDL_JoystickOpen':([C.c_int],C.c_void_p),'SDL_JoystickClose':([C.c_void_p],None),'SDL_JoystickInstanceID':([C.c_void_p],C.c_int32),'SDL_JoystickSetVirtualButton':([C.c_void_p,C.c_int,C.c_ubyte],C.c_int),'SDL_JoystickSetVirtualAxis':([C.c_void_p,C.c_int,C.c_int16],C.c_int)}
            for name,(args,result) in signatures.items():getattr(sdl,name).argtypes=args;getattr(sdl,name).restype=result
        while running:
            started=time.perf_counter()
            for _ in range(64):
                try:message=commands.get_nowait()
                except queue.Empty:break
                op=message['op']
                if op=='quit':running=False;break
                if testing and op.startswith('test_'):
                    if op=='test_attach':
                        index=sdl.SDL_JoystickAttachVirtual(1,2,16,1);handle=sdl.SDL_JoystickOpen(index)
                        if index<0 or not handle:raise RuntimeError('Virtual pad could not open')
                        virtual=(index,handle);test_result=dict(id=message['id'],instance=int(sdl.SDL_JoystickInstanceID(handle)))
                    elif op=='test_detach' and virtual:
                        index,handle=virtual;sdl.SDL_JoystickClose(handle);sdl.SDL_JoystickDetachVirtual(index);virtual=None;test_result=dict(id=message['id'])
                    elif op=='test_button' and virtual:sdl.SDL_JoystickSetVirtualButton(virtual[1],message['button'],message['value']);test_result=dict(id=message['id'])
                    elif op=='test_axis' and virtual:sdl.SDL_JoystickSetVirtualAxis(virtual[1],message['axis'],message['value']);test_result=dict(id=message['id'])
                    elif op=='test_crash':os._exit(77)
                    elif op=='test_hang':time.sleep(5)
                    continue
                device=pads.get(message.get('instance'))
                if device is not None:
                    try:
                        if op=='rumble':device.rumble(message['low'],message['high'],message['duration'])
                        elif op=='stop':device.stop_rumble()
                    except (pygame.error,RuntimeError,SystemError):pass
            if not running:break
            # No SDL window belongs to Tk in this process. Avoid event.get's
            # conversion of stale device events while still discovering pads.
            pygame.event.pump();pygame.event.clear()
            current={}
            for index in range(pygame.joystick.get_count()):
                try:
                    device=pygame.joystick.Joystick(index);instance=device.get_instance_id()
                    current[instance]=pads.get(instance,device)
                    if instance not in mapping:
                        try:
                            controllers[instance]=controller.Controller.from_joystick(device)
                            mapping[instance]=sdl_pad_mapping(controllers[instance].get_mapping())
                        except (pygame.error,RuntimeError,SystemError):mapping[instance]=dict(DEFAULT_PAD)
                except (pygame.error,RuntimeError,SystemError):continue
            for instance in pads.keys()-current.keys():
                mapping.pop(instance,None);device=controllers.pop(instance,None)
                if device is not None:
                    try:device.quit()
                    except (pygame.error,RuntimeError,SystemError):pass
            pads=current;states=[]
            for instance,device in pads.items():
                try:
                    states.append(dict(instance=instance,name=device.get_name(),guid=device.get_guid(),mapping=mapping[instance],buttons=[bool(device.get_button(i)) for i in range(device.get_numbuttons())],axes=[float(device.get_axis(i)) for i in range(device.get_numaxes())],hats=[device.get_hat(i) for i in range(device.get_numhats())]))
                except (pygame.error,RuntimeError,SystemError):continue
            try:updates.put_nowait(dict(at=time.perf_counter(),devices=states,test=test_result))
            except queue.Full:pass
            time.sleep(max(.001,.008-(time.perf_counter()-started)))
    finally:
        for device in pads.values():
            try:device.stop_rumble()
            except Exception:pass
        pygame.quit()
        if timer is not None:timer.timeEndPeriod(1)


class PadProxy:
    def __init__(self,client,instance):self.client=client;self.instance=instance;self.epoch=client.epoch
    def state(self):
        if self.epoch!=self.client.epoch or self.instance not in self.client.states:raise RuntimeError('Controller disconnected')
        return self.client.states[self.instance]
    def get_name(self):return self.state()['name']
    def get_guid(self):return self.state()['guid']
    def get_instance_id(self):return self.epoch,self.instance
    def get_init(self):return self.epoch==self.client.epoch and self.instance in self.client.states
    def get_numbuttons(self):return len(self.state()['buttons'])
    def get_button(self,i):return self.state()['buttons'][i]
    def get_numaxes(self):return len(self.state()['axes'])
    def get_axis(self,i):return self.state()['axes'][i]
    def get_numhats(self):return len(self.state()['hats'])
    def get_hat(self,i):return self.state()['hats'][i]
    def get_mapping(self):return self.state()['mapping']
    def rumble(self,low,high,duration):
        if not self.get_init():return False
        values=[float(low),float(high)]
        if not all(math.isfinite(v) for v in values):return False
        return self.client.send('rumble',instance=self.instance,low=max(0,min(1,values[0])),high=max(0,min(1,values[1])),duration=max(20,min(600,int(duration))))
    def stop_rumble(self):
        if self.get_init():self.client.send('stop',instance=self.instance)


class PadClient:
    def __init__(self,testing=False):
        self.ctx=mp.get_context('spawn');self.testing=testing;self.process=None;self.commands=None;self.updates=None
        self.states={};self.proxies={};self.epoch=0;self.revision=0;self.last_update=0.;self.started=0.;self.retry_at=0.;self.closed=False;self.restarts=0;self.test_result={};self.start()
    def start(self):
        self.commands=self.ctx.Queue(maxsize=32);self.updates=self.ctx.Queue(maxsize=1)
        self.epoch+=1;self.process=self.ctx.Process(target=pad_worker,args=(self.commands,self.updates,os.getpid(),self.testing),daemon=True)
        try:self.process.start()
        except (OSError,RuntimeError):
            self.dispose();self.restarts+=1;self.retry_at=time.perf_counter()+3;return
        self.started=time.perf_counter();self.last_update=self.started
    def clear(self):
        if self.states:self.states={};self.proxies={};self.revision+=1
    def dispose(self):
        if self.process is not None:
            if self.process.pid is not None:
                if self.process.is_alive():self.process.terminate()
                self.process.join(.05)
            if not self.process.is_alive():self.process.close()
            self.process=None
        for q in (self.commands,self.updates):
            if q is not None:q.cancel_join_thread();q.close()
        self.commands=self.updates=None
    def poll(self):
        if self.closed:return
        now=time.perf_counter()
        if self.process is None:
            if now>=self.retry_at:self.start()
            return
        latest=None
        try:
            while True:latest=self.updates.get_nowait()
        except queue.Empty:pass
        except (EOFError,OSError,ValueError):pass
        if latest is not None and now-latest['at']<.35:
            states={row['instance']:row for row in latest['devices']}
            if states.keys()!=self.states.keys():
                self.proxies={i:self.proxies.get(i) or PadProxy(self,i) for i in states};self.revision+=1
            self.states=states;self.last_update=latest['at'];self.test_result=latest['test']
        if now-self.last_update>.35:self.clear()
        if not self.process.is_alive() or now-self.last_update>3:
            self.clear();self.dispose();self.restarts+=1;self.retry_at=now+min(3,.3*self.restarts)
    def devices(self):return list(self.proxies.values())
    def send(self,op,**data):
        if self.closed or self.process is None or self.commands is None:return False
        try:self.commands.put_nowait(dict(op=op,**data));return True
        except (queue.Full,OSError,ValueError):return False
    def close(self):
        if self.closed:return
        self.send('quit')
        if self.process is not None:self.process.join(1)
        self.closed=True;self.clear();self.dispose()
