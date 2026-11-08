"""Headless libretro smoke check with video, audio and main-RAM evidence."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import ctypes as C, json, wave, sys, os
from PIL import Image
ROOT=PROJECT_ROOT
out=ROOT/'test_current'/(sys.argv[3] if len(sys.argv)>3 else 'run');out.mkdir(parents=True,exist_ok=True)
core_path=Path(os.environ.get('SRWW_CORE_PATH',str(ROOT/'tools/desmume/desmume_libretro.dll')))
core=C.CDLL(str(core_path))
ENV=C.CFUNCTYPE(C.c_bool,C.c_uint,C.c_void_p)
VIDEO=C.CFUNCTYPE(None,C.c_void_p,C.c_uint,C.c_uint,C.c_size_t)
AUDIO=C.CFUNCTYPE(None,C.c_int16,C.c_int16)
BATCH=C.CFUNCTYPE(C.c_size_t,C.POINTER(C.c_int16),C.c_size_t)
POLL=C.CFUNCTYPE(None)
INPUT=C.CFUNCTYPE(C.c_int16,C.c_uint,C.c_uint,C.c_uint,C.c_uint)
LOG=C.CFUNCTYPE(None,C.c_int,C.c_char_p)
@LOG
def log(level,fmt):pass
class Var(C.Structure):_fields_=[('key',C.c_char_p),('value',C.c_char_p)]
class Game(C.Structure):_fields_=[('path',C.c_char_p),('data',C.c_void_p),('size',C.c_size_t),('meta',C.c_char_p)]
class Geometry(C.Structure):_fields_=[('w',C.c_uint),('h',C.c_uint),('mw',C.c_uint),('mh',C.c_uint),('aspect',C.c_float)]
class Timing(C.Structure):_fields_=[('fps',C.c_double),('sample_rate',C.c_double)]
class AV(C.Structure):_fields_=[('geometry',Geometry),('timing',Timing)]
variables={};directory=str(out).encode();pixel=0;frame=0;samples=bytearray();last_image=None;trigger_frame=None
schedule=json.loads(Path(sys.argv[6]).read_text()) if len(sys.argv)>6 else None
snapshot_interval=int(os.environ.get('SRWW_SNAPSHOT_INTERVAL','180'))
after_trigger_frames=int(os.environ.get('SRWW_AFTER_TRIGGER_FRAMES','300'))
@ENV
def env(cmd,data):
 global pixel
 if cmd in (9,30,31):C.cast(data,C.POINTER(C.c_char_p))[0]=directory;return True
 if cmd==10:pixel=C.cast(data,C.POINTER(C.c_int))[0];return True
 if cmd==27:C.cast(data,C.POINTER(C.c_void_p))[0]=C.cast(log,C.c_void_p);return True
 if cmd==3:C.cast(data,C.POINTER(C.c_bool))[0]=True;return True
 if cmd==15:
  v=C.cast(data,C.POINTER(Var));v[0].value=variables.get(v[0].key);return v[0].value is not None
 if cmd==16:
  a=C.cast(data,C.POINTER(Var));i=0
  while a[i].key:
   variables[a[i].key]=a[i].value.split(b'; ',1)[-1].split(b'|')[0];i+=1
  return True
 if cmd==17:C.cast(data,C.POINTER(C.c_bool))[0]=False;return True
 if cmd in (18,11):return True
 if cmd==52:C.cast(data,C.POINTER(C.c_uint))[0]=0;return True
 return False
@VIDEO
def video(data,w,h,pitch):
 global last_image
 if data and data!=C.c_void_p(-1).value:
  b=C.string_at(data,h*pitch)
  if pixel==1:last_image=Image.frombytes('RGB',(w,h),b,'raw','BGRX',pitch)
  else:
   import numpy as np
   a=np.frombuffer(b,dtype='<u2').reshape(h,pitch//2)[:,:w]
   if pixel==2:r=(a>>11)*255//31;g=((a>>5)&63)*255//63;b=(a&31)*255//31
   else:r=((a>>10)&31)*255//31;g=((a>>5)&31)*255//31;b=(a&31)*255//31
   last_image=Image.fromarray(np.stack([r,g,b],-1).astype('uint8'))
@AUDIO
def audio(l,r):samples.extend(bytes((C.c_int16*2)(l,r)))
@BATCH
def batch(data,n):samples.extend(C.string_at(data,n*4));return n
@POLL
def poll():pass
@INPUT
def inp(port,device,index,id):
 if trigger_frame is not None:return 0
 if isinstance(schedule,dict):
  if not any(a<=frame<b for a,b in schedule['auto_ranges']):
   return int(any(e['from']<=frame<e['to'] and id==e['button'] for e in schedule['events']))
 elif schedule is not None:return int(any(e['from']<=frame<e['to'] and id==e['button'] for e in schedule))
 if id==3 and 180<=frame%600<190:return 1
 return int(id==8 and frame>=1800 and frame%60<3)
for name,cb in [('environment',env),('video_refresh',video),('audio_sample',audio),('audio_sample_batch',batch),('input_poll',poll),('input_state',inp)]:
 getattr(core,'retro_set_'+name)(cb)
variables[b'desmume_cpu_mode']=os.environ.get('SRWW_CPU_MODE','jit').encode()
core.retro_init()
if os.environ.get('SRWW_HD')=='1' and hasattr(core,'retro_srw_set_hd_enabled'):
 core.retro_srw_set_hd_enabled(1)
path=Path(sys.argv[1]).resolve();rom=path.read_bytes();buf=C.create_string_buffer(rom)
game=Game(str(path).encode('utf-8'),C.cast(buf,C.c_void_p),len(rom),None)
core.retro_load_game.argtypes=[C.POINTER(Game)];core.retro_load_game.restype=C.c_bool
assert core.retro_load_game(C.byref(game)),'ROM load failed'
av=AV();core.retro_get_system_av_info(C.byref(av))
first_frame=0
watch=None;trigger_frame=None;voice_events=[];previous_voice_count=0;last_voice_event_frame=None
symbol_file=ROOT/'release_battle_v02/voice_probe_symbols.json'
if path==ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds' and symbol_file.exists():
 watch=json.loads(symbol_file.read_text(encoding='utf-8'))
if len(sys.argv)>4 and sys.argv[4]!='-':
 state_bytes=Path(sys.argv[4]).read_bytes();state_buf=C.create_string_buffer(state_bytes)
 core.retro_unserialize.argtypes=[C.c_void_p,C.c_size_t];core.retro_unserialize.restype=C.c_bool
 assert core.retro_unserialize(state_buf,len(state_bytes)),'Resume state rejected'
 # Resume a baseline state with the prototype's changed code regions only.
 core.retro_get_memory_data.argtypes=[C.c_uint];core.retro_get_memory_data.restype=C.c_void_p
 ptr=core.retro_get_memory_data(2)
 arm9_offset=int.from_bytes(rom[0x20:0x24],'little')
 for offset,length in [(0x1040,0x1fc0),(0x15de8,8),(0xee50,8),(0xf2e8,8),(0xf33c,8)]:
  C.memmove(ptr+offset,rom[arm9_offset+offset:arm9_offset+offset+length],length)
 first_frame=int(sys.argv[5]) if len(sys.argv)>5 else 5400
 if hasattr(core,'retro_srw_reset_code_cache'):core.retro_srw_reset_code_cache()
if os.environ.get('SRWW_LOG_ECD')=='1':
 core.retro_get_memory_data.argtypes=[C.c_uint];core.retro_get_memory_data.restype=C.c_void_p
 ptr=core.retro_get_memory_data(2)
 stub=(ROOT/'test_current/graphics/log_ecd.bin').read_bytes()
 C.memmove(ptr+0x1040,stub,len(stub));C.memset(ptr+0x1030,0,4)
 import struct
 jump=struct.pack('<I',0xea000000|(((0x2001040-0x200d420)>>2)&0xffffff))
 C.memmove(ptr+0xd418,jump,4)
for frame in range(first_frame,int(sys.argv[2]) if len(sys.argv)>2 else 900):
 core.retro_run()
 if watch:
  core.retro_get_memory_data.argtypes=[C.c_uint];core.retro_get_memory_data.restype=C.c_void_p
  ptr=core.retro_get_memory_data(2)
  count=C.c_uint32.from_address(ptr+watch['voice_match_count']-0x2000000).value
  if count>previous_voice_count:
   previous_voice_count=count;last_voice_event_frame=frame
   voice_events.append(dict(count=count,frame=frame,seconds_from_run_start=(frame-first_frame)/av.timing.fps,
                            caption_hex=C.string_at(ptr+0x1f7338,96).hex()))
   (out/'voice_events.json').write_text(json.dumps(voice_events,indent=2))
  if last_voice_event_frame is not None and frame==last_voice_event_frame+30:
   if last_image:last_image.save(out/f'voice_event_{previous_voice_count:02d}.png')
  if count and trigger_frame is None:
   trigger_frame=frame
   if last_image:last_image.save(out/'voice_trigger.png')
   (out/'voice_trigger.json').write_text(json.dumps(dict(frame=frame,seconds_from_run_start=(frame-first_frame)/av.timing.fps)))
   print('VOICE TRIGGER',frame,flush=True)
  if trigger_frame is not None and frame>=trigger_frame+after_trigger_frames:break
  if trigger_frame is not None and frame in (trigger_frame+30,trigger_frame+60,trigger_frame+120):
   if last_image:last_image.save(out/f'voice_plus_{frame-trigger_frame:03d}.png')
 if frame%snapshot_interval==snapshot_interval-1:
  if last_image:last_image.save(out/f'frame_{frame+1:05d}.png')
  print('frame',frame+1,flush=True)
  if frame>1800:
   core.retro_get_memory_data.argtypes=[C.c_uint];core.retro_get_memory_data.restype=C.c_void_p
   ptr=core.retro_get_memory_data(2)
   if ptr:
    snapshot=C.string_at(ptr,4194304)
    (out/'main_ram_latest.bin').write_bytes(snapshot)
    if os.environ.get('SRWW_TRACE_RAM')=='1':(out/f'ram_{frame+1:05d}.bin').write_bytes(snapshot)
 if os.environ.get('SRWW_DUMP_BG')=='1' and frame%30==29 and hasattr(core,'retro_srw_get_bg_info'):
  info=[]
  core.retro_srw_get_bg_info.argtypes=[C.c_uint,C.POINTER(C.c_uint)]
  core.retro_srw_copy_vram.argtypes=[C.c_uint,C.c_void_p,C.c_uint]
  for layer in range(4):
   values=(C.c_uint*9)();core.retro_srw_get_bg_info(layer,values);info.append(list(values))
   for kind,index,size in [('map',1,2048),('tiles',2,32768)]:
    memory=C.create_string_buffer(size)
    if core.retro_srw_copy_vram(values[index],memory,size):(out/f'bg{layer}_{kind}.bin').write_bytes(memory.raw)
  (out/'backgrounds.json').write_text(json.dumps(info,indent=2))
  if hasattr(core,'retro_srw_get_hd_state'):
   hd=(C.c_uint*12)();core.retro_srw_get_hd_state(hd)
   (out/'hd_state.json').write_text(json.dumps(list(hd)))
   mask=C.create_string_buffer(256*192);core.retro_srw_copy_layer_ids(mask)
   (out/'layer_ids.bin').write_bytes(mask.raw)
with wave.open(str(out/'emulator_audio.wav'),'wb') as w:
 w.setnchannels(2);w.setsampwidth(2);w.setframerate(round(av.timing.sample_rate));w.writeframes(samples)
core.retro_get_memory_size.argtypes=[C.c_uint];core.retro_get_memory_size.restype=C.c_size_t
core.retro_get_memory_data.argtypes=[C.c_uint];core.retro_get_memory_data.restype=C.c_void_p
n=core.retro_get_memory_size(2);ptr=core.retro_get_memory_data(2)
if n and ptr:(out/'main_ram.bin').write_bytes(C.string_at(ptr,n))
core.retro_serialize_size.restype=C.c_size_t
size=core.retro_serialize_size();state=C.create_string_buffer(size)
core.retro_serialize.argtypes=[C.c_void_p,C.c_size_t];core.retro_serialize.restype=C.c_bool
if core.retro_serialize(state,size):(out/'final.state').write_bytes(state.raw)
(out/'run.json').write_text(json.dumps(dict(frames=frame+1,sample_rate=av.timing.sample_rate,audio_bytes=len(samples),ram_size=n,rom=str(path),variables={k.decode():v.decode() for k,v in variables.items()}),indent=2))
core.retro_unload_game();core.retro_deinit()
