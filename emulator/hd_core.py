"""Small libretro frontend adapter; DeSmuME remains the emulation core."""
from pathlib import Path
import ctypes as C
import json
import hashlib,os,queue
import numpy as np
from asset_paths import asset_root

HERE=Path(__file__).resolve().parent
ROOT=asset_root(HERE.parent)
ENV=C.CFUNCTYPE(C.c_bool,C.c_uint,C.c_void_p)
VIDEO=C.CFUNCTYPE(None,C.c_void_p,C.c_uint,C.c_uint,C.c_size_t)
AUDIO=C.CFUNCTYPE(None,C.c_int16,C.c_int16)
BATCH=C.CFUNCTYPE(C.c_size_t,C.POINTER(C.c_int16),C.c_size_t)
POLL=C.CFUNCTYPE(None)
INPUT=C.CFUNCTYPE(C.c_int16,C.c_uint,C.c_uint,C.c_uint,C.c_uint)
LOG=C.CFUNCTYPE(None,C.c_int,C.c_char_p)
class Var(C.Structure):_fields_=[('key',C.c_char_p),('value',C.c_char_p)]
class Game(C.Structure):_fields_=[('path',C.c_char_p),('data',C.c_void_p),('size',C.c_size_t),('meta',C.c_char_p)]

class Core:
    def __init__(self,rom,enabled=True,demo=False,user_dir=None,frameskip=0):
        default_core=HERE/'desmume/desmume/src/frontend/libretro/desmume_libretro.dll'
        selected_core=Path(os.environ.get('SRWW_CORE_PATH',str(default_core)))
        self.api=C.CDLL(str(selected_core))
        # Developer preview windows can outlive an experimental bridge build.
        # Never interpret its older pixel layout as the current ABI. Prefer
        # the validated installed core before initializing either library.
        if hasattr(self.api,'retro_srw_copy_foreground') and not hasattr(self.api,'retro_srw_foreground_format') and selected_core.resolve()!=default_core.resolve():
            installed=C.CDLL(str(default_core))
            if hasattr(installed,'retro_srw_foreground_format') and installed.retro_srw_foreground_format()==3:
                self.api=installed;selected_core=default_core
        self.core_path=str(selected_core)
        self.frameskip=max(0,min(1,int(frameskip)));self.video_epoch=0;self.last_unknown=None
        self.rom=Path(rom).resolve();self.pixel=0;self.vars={};self.vars_changed=False;self.buttons=set();self.touch=None
        self.native=np.zeros((384,256,3),dtype='uint8');self.audio=bytearray()
        self.user=Path(user_dir) if user_dir else HERE/('demo_data' if demo else 'user_data');self.user.mkdir(parents=True,exist_ok=True);self.directory=str(self.user).encode('utf-8')
        self.callbacks=[ENV(self.environment),VIDEO(self.video),AUDIO(self.sample),BATCH(self.batch),POLL(lambda:None),INPUT(self.input),LOG(lambda level,fmt:None)]
        for name,cb in zip(['environment','video_refresh','audio_sample','audio_sample_batch','input_poll','input_state'],self.callbacks):getattr(self.api,'retro_set_'+name)(cb)
        self.vars[b'desmume_cpu_mode']=b'jit';self.vars[b'desmume_jit_block_size']=b'12';self.vars[b'desmume_opengl_mode']=b'disabled';self.vars[b'desmume_frameskip']=str(self.frameskip).encode()
        self.api.retro_init()
        self.buffer=C.create_string_buffer(self.rom.read_bytes())
        self.clean_korean=hashlib.sha256(self.buffer.raw[:-1]).hexdigest()=='0a5a22bd6bb25ebe640767e6b422b91358636e9ae1300e61d7e8ac3c5d8cd478'
        game=Game(str(self.rom).encode('utf-8'),C.cast(self.buffer,C.c_void_p),len(self.buffer)-1,None)
        self.api.retro_load_game.argtypes=[C.POINTER(Game)];self.api.retro_load_game.restype=C.c_bool
        if not self.api.retro_load_game(C.byref(game)):raise RuntimeError('롬을 열지 못했습니다.')
        self.ids=np.zeros((192,256),dtype='uint8');self.hd=(C.c_uint*12)();self.enabled=enabled
        self.cutin_layers=np.zeros((4,12),dtype='uint32')
        self.foreground_buffer=np.zeros((192,256),dtype='uint64');self.effect_foreground=None
        self.foreground_bridge=hasattr(self.api,'retro_srw_foreground_format') and self.api.retro_srw_foreground_format()==3
        if self.foreground_bridge:self.api.retro_srw_copy_foreground.argtypes=[C.c_void_p]
        # Which layers the DS window test let through on each pixel of the frame just drawn.
        self.window_buffer=np.zeros((192,256),dtype='uint8');self.window=None;self.window_bridge=hasattr(self.api,'retro_srw_copy_window')
        if self.window_bridge:self.api.retro_srw_copy_window.argtypes=[C.c_void_p]
        # Palette bank and its live colours for each BG that shows a cut-in (some are grey pictures coloured by the palette).
        self.cutin_palettes=None;self.bank_bridge=hasattr(self.api,'retro_srw_copy_bg_banks') and hasattr(self.api,'retro_srw_copy_effect_debug')
        if self.bank_bridge:
            self.api.retro_srw_copy_bg_banks.argtypes=[C.c_uint,C.c_void_p,C.c_uint,C.c_void_p];self.api.retro_srw_copy_bg_banks.restype=C.c_uint
            self.api.retro_srw_copy_effect_debug.argtypes=[C.c_void_p]*4;self.bank_buffer=np.zeros(4096,dtype='uint8');self.bg_palette=np.zeros(256,dtype='<u2')
        self.layer_cutin_bridge=hasattr(self.api,'retro_srw_get_hd_layers')
        if self.layer_cutin_bridge:self.api.retro_srw_get_hd_layers.argtypes=[C.c_void_p]
        self.robot=(C.c_int*8)()
        self.obj=C.create_string_buffer(1024)
        self.api.retro_srw_get_robot_state.argtypes=[C.POINTER(C.c_int)]
        self.parts=np.zeros((128,8),dtype='uint32');self.owners=np.zeros((192,256),dtype='uint8');self.bgpriors=np.full(6,4,dtype='uint8')
        self.bgparts=np.zeros((3200,8),dtype='uint32');self.api.retro_srw_copy_bg_parts.argtypes=[C.c_void_p]
        library=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text())
        self.menu_bindings={i for i,b in enumerate(library['bindings'],1) if b.get('atlas_id')=='favorite_menu'}
        hashes=(C.c_uint*len(library['bindings']))(*[b['hash'] if b.get('rgb_enabled',True) and not b.get('disabled') else 0 for b in library['bindings']])
        self.api.retro_srw_register_parts.argtypes=[C.POINTER(C.c_uint),C.c_uint];self.api.retro_srw_register_parts(hashes,len(hashes))
        self.effect_bridge=hasattr(self.api,'retro_srw_register_effect_parts')
        # A source alias may have its own binding ID in the core. Inherit
        # explicit source classification, while permitting an explicit false
        # on an alias and rejecting malformed/cyclic references.
        def is_effect_part(identifier):
            seen=set()
            while isinstance(identifier,int) and 0<identifier<=len(library['bindings']) and identifier not in seen:
                seen.add(identifier);spec=library['bindings'][identifier-1]
                if spec.get('disabled'):return False
                if 'effect_part' in spec:return spec['effect_part'] is True
                identifier=spec.get('source_binding')
            return False
        self.effect_part_ids=[i for i in range(1,len(library['bindings'])+1) if is_effect_part(i)]
        if self.effect_bridge:
            self.api.retro_srw_register_effect_parts.argtypes=[C.POINTER(C.c_uint),C.c_uint]
            effect_ids=(C.c_uint*len(self.effect_part_ids))(*self.effect_part_ids)
            self.api.retro_srw_register_effect_parts(effect_ids,len(effect_ids))
        self.part_palettes=np.zeros((128,16),dtype='uint16')
        blocked_index_keys=set(library.get('indexed_collision_keys',[]))
        indexed=[(b['index_hash'],i) for i,b in enumerate(library['bindings'],1) if b.get('dynamic_palette') and b.get('indexed_safe',True) and not b.get('disabled') and b['index_hash'] not in blocked_index_keys]
        self.indexed_bridge=hasattr(self.api,'retro_srw_register_indexed_parts')
        if indexed and not self.indexed_bridge:raise RuntimeError('전체 기체용 코어를 업데이트해야 합니다.')
        if self.indexed_bridge:
            self.api.retro_srw_register_indexed_parts.argtypes=[C.POINTER(C.c_uint),C.POINTER(C.c_uint),C.c_uint]
            self.api.retro_srw_copy_part_palettes.argtypes=[C.c_void_p]
            count=len(indexed);keys=(C.c_uint*count)(*[v[0] for v in indexed]);ids=(C.c_uint*count)(*[v[1] for v in indexed])
            self.api.retro_srw_register_indexed_parts(keys,ids,count)
        self.ready_generation=None
        self.dynamic_bridge=hasattr(self.api,'retro_srw_dynamic_parts')
        if self.dynamic_bridge:
            self.api.retro_srw_add_dynamic_part.argtypes=[C.c_uint,C.c_uint,C.c_uint]
            self.api.retro_srw_copy_unknown_parts.argtypes=[C.c_void_p,C.c_void_p,C.c_void_p]
        self.backgrounds=[];self.bg_layout=[];self.background_specs={};self.background_maps={};self.configuration_background_ids={7,8}
        background_path=ROOT/'graphics/backgrounds/library.json'
        if background_path.exists():
            for item in json.loads(background_path.read_text())['backgrounds']:
                if item.get('menu_configuration'):self.configuration_background_ids.add(item['id'])
                for signature in item['signatures']:
                    self.background_specs[(item['layer'],*signature)]=item['id']
                    self.background_maps.setdefault((item['layer'],signature[1]),[]).append(item)

        if hasattr(self.api,'retro_srw_set_ready_parts'):self.api.retro_srw_set_ready_parts.argtypes=[C.POINTER(C.c_uint),C.c_uint]
        cutins_path=ROOT/'graphics/cutins_library.json'
        if cutins_path.exists() and hasattr(self.api,'retro_srw_register_cutins'):
            rows=[]
            for cutin in json.loads(cutins_path.read_text())['cutins']:
                if not (ROOT/'graphics'/cutin['image']).exists():continue
                if cutin.get('map_window_entries') and not hasattr(self.api,'retro_srw_register_cutin_map_windows'):continue
                for signature in cutin['signatures']:
                    mode={'image_origin':256,'origin_8192':512,'row_padded':768}.get(cutin.get('signature_mode'),0)
                    for layer in cutin.get('layers',[cutin['layer']]):rows.extend([signature,cutin['id'],layer|mode,*cutin['native_size']])
            self.api.retro_srw_register_cutins.argtypes=[C.POINTER(C.c_uint),C.c_uint]
            values=(C.c_uint*len(rows))(*rows);self.api.retro_srw_register_cutins(values,len(rows)//5)
            if hasattr(self.api,'retro_srw_register_cutin_maps'):
                maps=[]
                for cutin in json.loads(cutins_path.read_text())['cutins']:
                    if 'map_signature' in cutin:maps.extend([cutin['id'],cutin['map_signature']])
                self.api.retro_srw_register_cutin_maps.argtypes=[C.POINTER(C.c_uint),C.c_uint]
                packed=(C.c_uint*len(maps))(*maps);self.api.retro_srw_register_cutin_maps(packed,len(maps)//2)
            if hasattr(self.api,'retro_srw_register_cutin_map_windows'):
                windows=[]
                for cutin in json.loads(cutins_path.read_text())['cutins']:
                    if cutin.get('map_window_entries'):windows.extend([cutin['id'],cutin['map_window_signature'],cutin['map_window_entries']])
                self.api.retro_srw_register_cutin_map_windows.argtypes=[C.POINTER(C.c_uint),C.c_uint]
                packed=(C.c_uint*len(windows))(*windows);self.api.retro_srw_register_cutin_map_windows(packed,len(windows)//3)
        self.api.retro_srw_copy_parts.argtypes=[C.c_void_p,C.c_void_p]
        self.api.retro_srw_set_hd_enabled(int(enabled))
        self.api.retro_srw_copy_layer_ids.argtypes=[C.c_void_p]
        self.api.retro_srw_get_hd_state.argtypes=[C.POINTER(C.c_uint)]
        self.sub_parts=np.zeros((128,8),dtype='uint32');self.sub_owners=np.zeros((192,256),dtype='uint8')
        self.sub_oam=C.create_string_buffer(1024);self.sub_palettes=np.zeros((128,16),dtype='uint16')
        self.sub_ids=np.zeros((192,256),dtype='uint8');self.sub_priorities=np.full(6,4,dtype='uint8')
        self.sub_bridge=hasattr(self.api,'retro_srw_copy_sub_parts')
        if self.sub_bridge:self.api.retro_srw_copy_sub_parts.argtypes=[C.c_void_p]*6
        self.sub_unknown_bridge=hasattr(self.api,'retro_srw_copy_sub_unknown_parts')
        if self.sub_unknown_bridge:self.api.retro_srw_copy_sub_unknown_parts.argtypes=[C.c_void_p]*3

    def environment(self,cmd,data):
        if cmd in (9,30,31):C.cast(data,C.POINTER(C.c_char_p))[0]=self.directory;return True
        if cmd==27:C.cast(data,C.POINTER(C.c_void_p))[0]=C.cast(self.callbacks[6],C.c_void_p);return True
        if cmd==3:C.cast(data,C.POINTER(C.c_bool))[0]=True;return True
        if cmd==10:self.pixel=C.cast(data,C.POINTER(C.c_int))[0];return True
        if cmd==15:
            v=C.cast(data,C.POINTER(Var));v[0].value=self.vars.get(v[0].key);return v[0].value is not None
        if cmd==16:
            values=C.cast(data,C.POINTER(Var));i=0
            while values[i].key:
                self.vars[values[i].key]=values[i].value.split(b'; ',1)[-1].split(b'|')[0];i+=1
            return True
        if cmd==17:
            C.cast(data,C.POINTER(C.c_bool))[0]=self.vars_changed;self.vars_changed=False;return True
        if cmd==52:C.cast(data,C.POINTER(C.c_uint))[0]=0;return True
        return cmd in (11,18)

    def video(self,data,w,h,pitch):
        if not data or data==C.c_void_p(-1).value:return
        raw=C.string_at(data,pitch*h)
        if self.pixel==1:
            a=np.frombuffer(raw,'uint8').reshape(h,pitch//4,4)[:,:w]
            self.native=a[:,:,2::-1].copy()
        else:
            a=np.frombuffer(raw,'<u2').reshape(h,pitch//2)[:,:w].astype('uint32')
            if self.pixel==2:r=(a>>11)*255//31;g=((a>>5)&63)*255//63
            else:r=((a>>10)&31)*255//31;g=((a>>5)&31)*255//31
            b=(a&31)*255//31;self.native=np.stack([r,g,b],-1).astype('uint8')

        self.video_epoch+=1

    def sample(self,l,r):self.audio.extend(bytes((C.c_int16*2)(l,r)))
    def batch(self,p,n):self.audio.extend(C.string_at(p,n*4));return n
    def input(self,port,device,index,key):
        if device==1:return int(key in self.buttons)
        if device==6 and self.touch:
            if key==0:return self.touch[0]
            if key==1:return self.touch[1]
            if key==2:return 1
        return 0

    def set_ready_parts(self,renderer):
        if self.dynamic_bridge:
            while True:
                try:identity,material,binding=renderer.dynamic_bindings.get_nowait()
                except queue.Empty:break
                self.api.retro_srw_add_dynamic_part(identity,material,binding)
        if not hasattr(self.api,'retro_srw_set_ready_parts') or renderer.ready_generation==self.ready_generation:return
        generation=renderer.ready_generation
        values=np.ascontiguousarray(renderer.ready_bindings(),dtype='uint32')
        self.api.retro_srw_set_ready_parts(values.ctypes.data_as(C.POINTER(C.c_uint)),len(values));self.ready_generation=generation

    def unknown_snapshot(self):
        return self.last_unknown if self.frameskip else self._read_unknown_snapshot()

    def _read_unknown_snapshot(self):
        if not self.dynamic_bridge or not self.enabled:return None
        count=256 if self.sub_unknown_bridge else 128
        rows=np.empty((count,8),dtype='uint32');self.api.retro_srw_copy_unknown_parts(rows.ctypes.data,None,None)
        if self.sub_unknown_bridge:self.api.retro_srw_copy_sub_unknown_parts(rows[128:].ctypes.data,None,None)
        if not rows[:,0].any():return None
        pixels=np.empty((count,4096),dtype='uint8');palettes=np.empty((count,16),dtype='uint16')
        self.api.retro_srw_copy_unknown_parts(None,pixels.ctypes.data,palettes.ctypes.data)
        if self.sub_unknown_bridge:self.api.retro_srw_copy_sub_unknown_parts(None,pixels[128:].ctypes.data,palettes[128:].ctypes.data)
        return rows,pixels,palettes

    def run(self):
        epoch=self.video_epoch;self.api.retro_run()
        if self.video_epoch==epoch:return False
        self.api.retro_srw_get_hd_state(self.hd)
        if self.layer_cutin_bridge:self.api.retro_srw_get_hd_layers(self.cutin_layers.ctypes.data)
        self.api.retro_srw_copy_layer_ids(self.ids.ctypes.data);self.hd[10]=int(self.enabled)
        self.effect_foreground=self.foreground_buffer if self.foreground_bridge and self.api.retro_srw_copy_foreground(self.foreground_buffer.ctypes.data) else None
        # None unless some layer is actually shut out somewhere this frame.
        self.window=self.window_buffer if self.window_bridge and self.api.retro_srw_copy_window(self.window_buffer.ctypes.data) and bool((self.window_buffer!=0x1f).any()) else None
        self.cutin_palettes=None
        if self.bank_bridge and self.layer_cutin_bridge and int(self.cutin_layers[:,0].max())>1:
            found={};loaded=False
            for row in self.cutin_layers:
                if int(row[0])<=1:continue
                layer=int(row[5]);count=self.api.retro_srw_copy_bg_banks(layer,self.bank_buffer.ctypes.data,4096,None)
                if not count:continue
                bank=int(self.bank_buffer[0])
                if not bool((self.bank_buffer[:count]==bank).all()):continue   # only pictures drawn with a single bank
                if not loaded:self.api.retro_srw_copy_effect_debug(None,None,self.bg_palette.ctypes.data,None);loaded=True
                found[layer]=(bank,self.bg_palette[bank*16:bank*16+16].copy())
            self.cutin_palettes=found or None
        self.api.retro_srw_get_robot_state(self.robot)
        self.api.retro_srw_copy_rendered_obj(self.obj)
        self.api.retro_srw_copy_parts(self.parts.ctypes.data,self.owners.ctypes.data)
        if self.indexed_bridge:self.api.retro_srw_copy_part_palettes(self.part_palettes.ctypes.data)
        self.api.retro_srw_copy_bg_parts(self.bgparts.ctypes.data)
        if self.sub_bridge:self.api.retro_srw_copy_sub_parts(self.sub_parts.ctypes.data,self.sub_owners.ctypes.data,self.sub_oam,self.sub_palettes.ctypes.data,self.sub_ids.ctypes.data,self.sub_priorities.ctypes.data)
        self.backgrounds=[];background_layout=[]
        for layer in range(4):
            info=(C.c_uint*9)();self.api.retro_srw_get_bg_info(layer,info);self.bgpriors[layer]=info[8]
            background_layout.append(tuple(info))
            if self.enabled and info[7] and any(key[0]==layer for key in self.background_specs):
                import zlib
                maps=C.create_string_buffer(info[5]*info[6]//32);self.api.retro_srw_copy_vram(info[1],maps,len(maps));map_crc=zlib.crc32(maps.raw)
                candidates=self.background_maps.get((layer,map_crc),())
                if not candidates:continue
                tiles=C.create_string_buffer(max(item['tile_bytes'] for item in candidates));self.api.retro_srw_copy_vram(info[2],tiles,len(tiles))
                for item in candidates:
                    data=np.frombuffer(tiles.raw[:item['tile_bytes']],dtype='uint8').reshape(-1,item['tile_size'])[item['tile_indices']].tobytes()
                    bid=self.background_specs.get((layer,zlib.crc32(data),map_crc))
                    if bid:self.backgrounds.append((bid,int(info[3]),int(info[4]),layer));break

        self.bg_layout=background_layout
        if self.enabled and (any(row[0] in self.configuration_background_ids for row in self.backgrounds) or sum(int(row[0]) in self.menu_bindings for row in self.parts)>=20):
            self.backgrounds.extend((9+layer-2,int(background_layout[layer][3]),int(background_layout[layer][4]),layer) for layer in (2,3))
        if self.frameskip:self.last_unknown=self._read_unknown_snapshot()
        return True

    def refresh_video(self):
        for steps in range(1,self.frameskip+3):
            if self.run():return steps
        raise RuntimeError("게임 화면을 갱신하지 못했습니다.")

    def set_frameskip(self,value):
        value=max(0,min(7,int(value)))
        if value!=self.frameskip:
            self.frameskip=value;self.vars[b'desmume_frameskip']=str(value).encode();self.vars_changed=True

    def set_hd(self,value):self.enabled=value;self.hd[10]=int(value);self.api.retro_srw_set_hd_enabled(int(value))
    def save(self,path):
        self.api.retro_serialize_size.restype=C.c_size_t;n=self.api.retro_serialize_size();b=C.create_string_buffer(n)
        self.api.retro_serialize.argtypes=[C.c_void_p,C.c_size_t];self.api.retro_serialize.restype=C.c_bool
        if not self.api.retro_serialize(b,n):raise RuntimeError('저장하지 못했습니다.')
        Path(path).write_bytes(b.raw)
    def load(self,path,refresh_code=False):
        data=Path(path).read_bytes();b=C.create_string_buffer(data)
        self.api.retro_unserialize.argtypes=[C.c_void_p,C.c_size_t];self.api.retro_unserialize.restype=C.c_bool
        if not self.api.retro_unserialize(b,len(data)):raise RuntimeError('중간 저장을 불러오지 못했습니다.')
        if refresh_code or self.clean_korean:
            self.api.retro_get_memory_data.argtypes=[C.c_uint];self.api.retro_get_memory_data.restype=C.c_void_p
            ram=self.api.retro_get_memory_data(2);rom=self.rom.read_bytes();arm=int.from_bytes(rom[0x20:0x24],'little')
            for off,size in [(0x1040,0x1fc0),(0xee50,8),(0xf2e8,8),(0xf33c,8)]:C.memmove(ram+off,rom[arm+off:arm+off+size],size)
            self.api.retro_srw_reset_code_cache()
    def close(self):self.api.retro_unload_game();self.api.retro_deinit()
