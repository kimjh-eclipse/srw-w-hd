"""CPU-heavy registration runs in a process so it cannot hold the game GIL."""
import os,time,threading
_renderer=None
_tiles=None

def start_texture_worker(parent_pid):
    if os.environ.get('SRWW_TEXTURE_TRACE')=='1':
        import faulthandler
        faulthandler.dump_traceback_later(10,repeat=True)
    def watch_parent():
        if os.name=='nt':
            import ctypes as C
            api=C.windll.kernel32;api.OpenProcess.restype=C.c_void_p
            handle=api.OpenProcess(0x00100000,False,parent_pid)
            if not handle:os._exit(0)
            api.WaitForSingleObject.argtypes=[C.c_void_p,C.c_uint];api.WaitForSingleObject(handle,0xffffffff)
            os._exit(0)
    threading.Thread(target=watch_parent,name='HD-parent-watch',daemon=True).start()
    from hd_parts import PartsRenderer
    global _renderer
    _renderer=PartsRenderer(async_prepare=False);_renderer.async_prepare=True

def prepare_task(binding,w,h,delay=0):
    if delay:time.sleep(delay)
    aligned,stats=_renderer.prepare_texture(binding,w,h)
    import numpy as np
    source=_renderer.bindings[binding-1]
    palette=np.asarray(source.get('palette_source_rgb',source.get('original_palette_rgb',_renderer.source_palette)),dtype='float32')
    key=palette.tobytes();lut=_renderer.palette_luts.get(key)
    return aligned,stats,key,None if lut is None else lut.tobytes()

def prepare_composite_task(encoded,w,h,palette):
    import base64,zlib,hashlib
    import numpy as np
    from tile_compositor import TileCompositor
    global _tiles
    if _tiles is None:_tiles=TileCompositor()
    raw=zlib.decompress(base64.b64decode(encoded));indices=np.frombuffer(raw,dtype='uint8').reshape(h,w)
    colors=np.asarray(palette,dtype='uint16');key='assembled-canonical-v2-'+hashlib.sha256((_tiles.stamp+_renderer.registration_version+str((w,h))).encode()+raw).hexdigest()
    try:found=_renderer.disk_cache.get(key)
    except Exception:found=None
    if found:aligned,stats=found
    else:
        aligned,stats=_tiles.assemble(indices,colors)
        if aligned is None:return None,stats,None,None
        used=np.unique(indices[indices!=0]);choices=[]
        for group in stats['tile_groups']:
            source,_=_tiles.source(group['source']);candidate=np.asarray(source['palette'],dtype='uint32')[:16]
            if len(candidate)<16:candidate=np.concatenate([candidate,np.repeat(candidate[-1:],16-len(candidate),axis=0)])
            choices.append((len(np.unique(candidate[used],axis=0)),source['priority'],candidate))
        reference=max(choices,key=lambda entry:entry[:2])[2];five=np.rint(reference*31/255).astype('uint16');canonical=(five[:,0]|five[:,1]<<5|five[:,2]<<10).astype('uint16')
        if not np.array_equal(colors,canonical):
            aligned,stats=_tiles.assemble(indices,canonical)
            if aligned is None:return None,stats,None,None
        reference_rgb=np.stack([(canonical&31)*255//31,((canonical>>5)&31)*255//31,((canonical>>10)&31)*255//31],-1)
        encoded_rgb=np.where(indices,canonical[indices]|0x8000,0).astype('<u2')
        stats.update(reference_palette_native=canonical.tolist(),reference_palette_rgb=reference_rgb.tolist(),reference_hash=zlib.crc32(encoded_rgb.tobytes())^(w<<16)^h)
        try:_renderer.disk_cache.put(key,aligned,stats)
        except Exception:pass
    colors=np.asarray(stats['reference_palette_native'],dtype='uint16')
    rgb=np.stack([(colors&31)*255//31,((colors>>5)&31)*255//31,((colors>>10)&31)*255//31],-1).astype('float32');palette_key=rgb.tobytes()
    if palette_key not in _renderer.palette_luts:
        c=np.arange(32768,dtype='uint32');all_rgb=np.stack([(c&31)*255/31,((c>>5)&31)*255/31,((c>>10)&31)*255/31],-1).astype('float32')
        _renderer.palette_luts[palette_key]=(np.argmin(((all_rgb[:,None,:]-rgb[None,1:,:])**2).sum(-1),axis=1)+1).astype('uint8')
    return aligned,stats,palette_key,_renderer.palette_luts[palette_key].tobytes()
