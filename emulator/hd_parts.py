"""Render individual native OBJ parts from the HD atlas with DS OAM transforms."""
from pathlib import Path
import json,struct,hashlib,queue,base64,zlib
import math
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp,os
from stage_cache import StageCache
from collections import OrderedDict
import numpy as np
from PIL import Image
from hd_parts_registration import register_part,registration_stamp
from parts_disk_cache import PartsDiskCache
from palette_materials import material_indices
from texture_preparation import prepare_task,prepare_composite_task,start_texture_worker
from native_composition import PartVisibility

from asset_paths import asset_root
ROOT=asset_root(Path(__file__).resolve().parent.parent)
SCALE=1440/256
# Finished textures are kept at this multiple of the native part size. The
# largest render width is 960 px (3.75x), so 4x loses nothing on screen.
STORE_SCALE=4
# SRWW_RENDER_SHORTCUTS=0 restores the earlier per-frame work for comparison.
SHORTCUTS=os.environ.get('SRWW_RENDER_SHORTCUTS','1')!='0'

def is_menu_gradient(indices,w,h):
    """Button centers and beveled ends are horizontal palette ramps, not units.

    Replacing these OBJ strips removes the native selection color needed by
    the font compositor. Keep every palette variant in the native UI path.
    """
    if h!=16 or w<16:return False
    rows=np.asarray(indices,dtype='uint8').reshape(h,w)
    counts=np.stack([np.bincount(row,minlength=256) for row in rows])
    modes=counts.argmax(1)
    return bool((counts.max(1)>=w*.8).all() and len(np.unique(modes))>=8 and (modes!=0).sum()>=14)

class PartsRenderer:
    def __init__(self,async_prepare=False,dynamic_parts=False):
        meta=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text())
        self.bindings=meta['bindings'];self.atlas=Image.open(ROOT/'graphics'/meta['atlas']).convert('RGBA').resize((1024,512),Image.Resampling.LANCZOS)
        self.material_slot_masks=None;self.material_slot_references={};self.material_slot_verified={}
        try:
            compiled=json.loads((ROOT/'graphics/material_slots.json').read_text())
            if compiled['library_sha256']==hashlib.sha256((ROOT/'graphics/kazuma_parts_library.json').read_bytes()).hexdigest():
                self.material_slot_masks=np.load(ROOT/'graphics/material_slots.npy',allow_pickle=False);self.material_slot_references=compiled['references']
        except (OSError,ValueError,KeyError):pass
        self.native_materials=None
        try:
            material_meta=json.loads((ROOT/'graphics/native_materials.json').read_text())
            if material_meta['library_sha256']==hashlib.sha256((ROOT/'graphics/kazuma_parts_library.json').read_bytes()).hexdigest():
                with np.load(ROOT/'graphics/native_materials.npz',allow_pickle=False) as archive:self.native_materials={key:archive[key] for key in archive.files}
        except (OSError,ValueError,KeyError):pass
        self.native_atlas=Image.open(ROOT/'graphics/kazuma_parts_atlas_reference.png').convert('RGBA').resize((256,128),Image.Resampling.NEAREST)
        self.atlases={'base':(self.atlas,self.native_atlas)}
        self.atlas_specs=meta.get('atlases',{});self.lazy_atlases=StageCache()
        for name,extra in meta.get('atlases',{}).items():
            if extra.get('lazy'):continue
            w,h=extra['native_size']
            self.atlases[name]=(Image.open(ROOT/'graphics'/extra['image']).convert('RGBA').resize((w*4,h*4),Image.Resampling.LANCZOS),Image.open(ROOT/'graphics'/extra['reference']).convert('RGBA').resize((w,h),Image.Resampling.NEAREST))
        self.source_palette=np.array(meta.get('source_palette_rgb',[]),dtype='float32');self.palette_lut=None
        if len(self.source_palette):
            codes=np.arange(32768,dtype='uint32');rgb=np.stack([(codes&31)*255/31,((codes>>5)&31)*255/31,((codes>>10)&31)*255/31],-1).astype('float32')
            self.palette_lut=(np.argmin(((rgb[:,None,:]-self.source_palette[None,1:,:])**2).sum(-1),axis=1)+1).astype('uint8')
        self.palette_luts={self.source_palette.tobytes():self.palette_lut}
        self.prepared=StageCache();self.registration_stats={}
        self.registered_cache=None;self.cached_stats={}
        cache_path=ROOT/'graphics'/meta.get('registration_cache','kazuma_parts_registration.npz')
        if cache_path.exists():
            with np.load(cache_path,allow_pickle=False) as archive:
                if str(archive['stamp'])==registration_stamp(ROOT,meta):
                    self.registered_cache={key:archive[key] for key in archive.files if key.startswith('part_')}
                    self.cached_stats=json.loads(str(archive['statistics']))
        self.cache=OrderedDict();self.scaled=OrderedDict();self.material_maps=OrderedDict();self.baked_scales={}
        if async_prepare and self.registered_cache is not None:
            for key in self.registered_cache:
                spec=self.bindings[int(key[5:])-1]
                palette=np.asarray(spec.get('palette_source_rgb',spec.get('original_palette_rgb',self.source_palette)),dtype='float32')
                self.get_palette_lut(palette)
        self.async_prepare=async_prepare;self.pending={};self.prepare_errors={}
        self.prepare_delay=0
        self.executor=ProcessPoolExecutor(max_workers=1,mp_context=mp.get_context('spawn'),initializer=start_texture_worker,initargs=(os.getpid(),)) if async_prepare else None
        self.disk_cache=PartsDiskCache(ROOT/'graphics/parts_baked.sqlite');self.legacy_cache=None
        self.registration_version=hashlib.sha256((Path(__file__).parent/'hd_parts_registration.py').read_bytes()).hexdigest()
        self.baked=set();self.baked_ready=np.zeros(0,dtype='uint32');self.miss_stamp=None
        if async_prepare and os.environ.get('SRWW_BAKED_PARTS','1')!='0':
            self.load_baked()
        self.ready_generation=0;self.ready_aliases={}
        for index,binding in enumerate(self.bindings,1):self.ready_aliases.setdefault(binding.get('source_binding',index),[]).append(index)
        self.baked_ready=np.fromiter((alias for source in self.baked for alias in self.ready_aliases.get(source,())),dtype='uint32')
        self.dynamic_parts=bool(dynamic_parts and async_prepare and (ROOT/'graphics/parts_tile_library.sqlite').exists())
        self.dynamic_bindings=queue.SimpleQueue();self.unmapped_pending={};self.unmapped_seen=set();self.unmapped_misses={};self.runtime_requests={}
        self.prepared.on_evict=lambda:setattr(self,'ready_generation',self.ready_generation+1)
        if self.dynamic_parts and os.environ.get('SRWW_ASSEMBLY_MISSES','1')!='0':self.load_misses()
        self.prefetch_groups={};self.prefetched_groups=set()
        for bid,spec in enumerate(self.bindings,1):
            if spec.get('source_binding') or spec['w']>64 or spec['h']>64:continue
            key=(spec.get('atlas_id','base'),spec.get('resource'))
            self.prefetch_groups.setdefault(key,[]).append(bid)

    def prefetch_related(self,parts):
        if not self.async_prepare or self.pending or getattr(self,'unmapped_on_screen',False):return
        # Current visible requests always win; queue a small neighboring batch
        # only when preparation is idle, never the whole 91k-part catalog.
        for raw in parts[:,0]:
            if not raw:continue
            spec=self.bindings[int(raw)-1];key=(spec.get('atlas_id','base'),spec.get('resource'))
            if key in self.prefetched_groups:continue
            queued=0;complete=True
            for bid in self.prefetch_groups.get(key,()):
                if bid in self.prepared or bid in self.pending or bid in self.prepare_errors:continue
                candidate=self.bindings[bid-1]
                self.pending[bid]=self.executor.submit(prepare_task,bid,candidate['w'],candidate['h'],self.prepare_delay)
                queued+=1
                if queued>=8:complete=False;break
            if complete:self.prefetched_groups.add(key)
            if queued:break

    def schedule_unknown(self,snapshot):
        self.unmapped_on_screen=snapshot is not None and bool(snapshot[0][:,0].any())
        if not self.dynamic_parts:return
        # Drain completed speculative work BEFORE deciding whether the queue
        # is busy. Otherwise every frame can requeue prefetch before a visible
        # unknown rectangle ever gets a turn.
        self.collect_prepared()
        for key,(future,request,descriptor) in list(self.unmapped_pending.items()):
            if not future.done():continue
            del self.unmapped_pending[key]
            try:art,stats,palette_key,lut=future.result()
            except Exception as error:art=None;stats=dict(reason=str(error))
            if art is None:
                self.unmapped_misses[key]=stats;self.record_miss(key);continue
            binding=len(self.bindings)+1
            if binding>=200000:self.unmapped_misses[key]=dict(reason='runtime texture capacity');continue
            descriptor['hash']=stats['reference_hash'];descriptor['original_palette_rgb']=stats['reference_palette_rgb']
            self.bindings.append(descriptor);self.prepared[binding]=art;self.registration_stats[binding]=stats
            self.runtime_requests[binding]=request;self.ready_aliases[binding]=[binding]
            if lut is not None:self.palette_luts[palette_key]=np.frombuffer(lut,dtype='uint8').copy()
            self.dynamic_bindings.put((key[0],key[1],binding));self.ready_generation+=1
        # Finished work still belongs in the stage cache after its source OBJ
        # disappears. Empty frames must drain the queue too.
        if snapshot is None:return
        # Speculative unknown effects must not sit ahead of visible registered
        # body parts in the single texture worker's queue.
        if self.pending:return
        rows,pixels,palettes=snapshot
        for i in sorted(np.flatnonzero(rows[:,0]),key=lambda i:-int(rows[i,1])*int(rows[i,2])):
            row=rows[i];identity=(int(row[0]),int(row[7]))
            if identity in self.unmapped_seen or len(self.unmapped_pending)>=2:continue
            w,h=int(row[1]),int(row[2])
            if is_menu_gradient(pixels[i,:w*h],w,h):
                self.unmapped_seen.add(identity);continue
            encoded=base64.b64encode(zlib.compress(pixels[i,:w*h].tobytes())).decode('ascii');palette=palettes[i].tolist()
            request=(encoded,w,h,palette);colors=np.asarray(palette,dtype='uint32');rgb=np.stack([(colors&31)*255//31,((colors>>5)&31)*255//31,((colors>>10)&31)*255//31],-1).tolist()
            descriptor=dict(hash=int(row[6]),index_hash=int(row[0]),w=w,h=h,x=0,y=0,runtime_texture=True,dynamic_palette=True,original_palette_rgb=rgb,index_pixels=encoded)
            try:future=self.executor.submit(prepare_composite_task,*request)
            except Exception as error:self.unmapped_misses[identity]=dict(reason=str(error));continue
            self.unmapped_seen.add(identity);self.unmapped_pending[identity]=(future,request,descriptor)

    def load_misses(self):
        """Runtime assemblies that already failed with the current tiles.

        Retrying them every session only occupies the texture process. The
        record is tied to the tile library and assembly code, so new art or
        a code change makes every one of them eligible again.
        """
        try:
            from tile_compositor import TileCompositor
            self.miss_stamp=hashlib.sha256((TileCompositor().stamp+self.registration_version).encode()).hexdigest()
            db=self.disk_cache.db();db.execute('CREATE TABLE IF NOT EXISTS assembly_misses (stamp TEXT,index_hash INTEGER,material INTEGER,PRIMARY KEY(stamp,index_hash,material))')
            self.unmapped_seen.update((int(a),int(b)) for a,b in db.execute('SELECT index_hash,material FROM assembly_misses WHERE stamp=?',(self.miss_stamp,)))
        except Exception:self.miss_stamp=None

    def record_miss(self,identity):
        if self.miss_stamp is None:return
        try:
            with self.disk_cache.db() as db:db.execute('INSERT OR IGNORE INTO assembly_misses VALUES (?,?,?)',(self.miss_stamp,int(identity[0]),int(identity[1])))
        except Exception:pass

    def ready_bindings(self):
        sources=set(self.prepared)|set(self.prepared.retained)
        if self.registered_cache is not None:sources.update(int(k[5:]) for k in self.registered_cache)
        sources.difference_update(self.baked)
        # One contiguous array: the list is ~90k entries once parts are baked,
        # and it crosses a process boundary and a C call whenever it changes.
        extra=np.fromiter((alias for source in sources for alias in self.ready_aliases.get(source,())),dtype='uint32')
        return np.concatenate([self.baked_ready,extra])

    def texture_key(self,binding,w,h,legacy=False,cut_policy=True):
        """Content address of one registered texture in the baked store."""
        source=self.bindings[binding-1];x,y=source['x'],source['y'];name=source.get('atlas_id','base')
        spec=self.atlas_specs.get(name,{'image':'kazuma_parts_atlas_facefix.png','reference':'kazuma_parts_atlas_reference.png'})
        registration_mode=('painted-attack-bank-v3' if source.get('registered_attack_bank') else
            'painted-mini-canvas-v1' if source.get('secondary_unit') else ('painted-wing-v2' if name=='wing_primary' else 'native-crop-v2'))
        from part_cut_edges import POLICY
        identity=[self.registration_version,registration_mode,x,y,w,h]
        if cut_policy:identity.append(POLICY)
        if not legacy:identity.append(f'store-{STORE_SCALE}x-webp')
        stats=self.__dict__.setdefault('atlas_stats',{})
        for file in (spec['image'],spec['reference']):
            if file not in stats:
                path=ROOT/'graphics'/file;stat=path.stat();stats[file]=[str(path),stat.st_mtime_ns,stat.st_size]
            identity.extend(stats[file])
        return hashlib.sha256(json.dumps(identity).encode()).hexdigest()

    def load_baked(self):
        """Bindings whose finished texture is already on disk.

        These need no registration work: the core may hide their native
        pixels at once and the renderer reads the picture when it is drawn.
        """
        self.baked=set()
        try:keys=self.disk_cache.keys()
        except Exception:return
        for binding,spec in enumerate(self.bindings,1):
            if spec.get('source_binding') or spec.get('runtime_texture') or spec.get('disabled'):continue
            try:
                if self.texture_key(binding,spec['w'],spec['h']) in keys:self.baked.add(binding)
            except (OSError,KeyError):pass

    def prepare_texture(self,binding,w,h):
        source=self.bindings[binding-1];x,y=source['x'],source['y'];name=source.get('atlas_id','base')
        spec=self.atlas_specs.get(name,{'image':'kazuma_parts_atlas_facefix.png','reference':'kazuma_parts_atlas_reference.png'})
        if self.async_prepare:
            palette=np.asarray(source.get('palette_source_rgb',source.get('original_palette_rgb',self.source_palette)),dtype='float32')
            palette_key=palette.tobytes();self.get_palette_lut(palette)
        key=self.texture_key(binding,w,h)
        if self.async_prepare:
            try:found=self.disk_cache.get(key)
            except Exception:found=None
            if found:return found
        store=(w*STORE_SCALE,h*STORE_SCALE)
        # Reuse the already aligned 4x texture when only the cut-edge policy
        # changed. No resampling or alignment search needs to be repeated.
        if not self.async_prepare:
            prior=self.disk_cache.get(self.texture_key(binding,w,h,cut_policy=False))
            if prior:
                from part_cut_edges import repair_crop_ink
                _,native_atlas=self.atlas_pair(name)
                aligned,count=repair_crop_ink(prior[0],native_atlas,(x,y,x+w,y+h))
                return aligned,dict(prior[1],artificial_cut_ink_pixels=count,reused_aligned_texture=True)
        if self.legacy_cache is not None:
            # Bake only: an identical registration from the earlier 8x store.
            try:found=self.legacy_cache.get(self.texture_key(binding,w,h,legacy=True))
            except Exception:found=None
            if found:return found[0].resize(store,Image.Resampling.LANCZOS),found[1]
        paint_atlas,native_atlas=self.atlas_pair(name)
        sx=paint_atlas.width/native_atlas.width;sy=paint_atlas.height/native_atlas.height
        paint=paint_atlas.crop((round(x*sx),round(y*sy),round((x+w)*sx),round((y+h)*sy))).resize((w*8,h*8),Image.Resampling.LANCZOS)
        if source.get('secondary_unit') or source.get('registered_attack_bank'):
            # These atlases were registered offline in exact source texel
            # coordinates. Keep shared seams at their original OAM pivots;
            # a per-crop shift would move overlapping pieces independently.
            from painted_edges import clean_alpha
            if source.get('registered_attack_bank'):
                from painted_edges import remove_unattached_paint
                aligned,removed=remove_unattached_paint(paint,native_atlas.crop((x,y,x+w,y+h)))
            else:aligned=clean_alpha(paint);removed=0
            stats=dict(dx=0,dy=0,zoom=1,offline_registered=True,reference_fill_pixels=0,filled_edge_pixels=0)
            stats['unattached_paint_components_removed']=removed
        else:aligned,stats=register_part(paint,native_atlas.crop((x,y,x+w,y+h)))
        if name=='wing_primary':
            # The native silhouette contract must not refill the painted
            # V-fin/cape contour with stair-stepped source pixels.
            from painted_edges import clean_alpha
            zoom=stats['zoom'];dx=stats['dx'];dy=stats['dy']
            coeff=(1/zoom,0,(w/2-(w/2+dx)/zoom)*8,0,1/zoom,(h/2-(h/2+dy)/zoom)*8)
            aligned=clean_alpha(paint.transform(aligned.size,Image.Transform.AFFINE,coeff,Image.Resampling.BICUBIC))
        from part_cut_edges import repair_crop_ink
        aligned,cut_pixels=repair_crop_ink(aligned,native_atlas,(x,y,x+w,y+h))
        stats=dict(stats,artificial_cut_ink_pixels=cut_pixels)
        if aligned.size!=store:aligned=aligned.resize(store,Image.Resampling.LANCZOS)
        if self.async_prepare:
            try:self.disk_cache.put(key,aligned,stats)
            except Exception:pass
        return aligned,stats

    def collect_prepared(self):
        changed=False
        for binding,future in list(self.pending.items()):
            if not future.done():continue
            del self.pending[binding]
            try:
                aligned,stats,palette_key,lut=future.result()
                if aligned is None:
                    self.prepare_errors[binding]=stats.get('reason','texture unavailable');continue
                self.prepared[binding]=aligned;self.registration_stats[binding]=stats
                if lut is not None:self.palette_luts[palette_key]=np.frombuffer(lut,dtype='uint8').copy()
                # Baked parts are already advertised; warming them in memory
                # must not resend the whole ready set to the core.
                if binding not in self.baked:changed=True
            except Exception as error:self.prepare_errors[binding]=str(error)
        while len(self.prepared)>512:self.prepared.popitem(last=False);changed=True
        if changed:self.ready_generation+=1

    def close(self):
        if self.executor:
            # Registration only writes the regenerable SQLite texture cache.
            # Do not make closing/switching a ROM wait for a cold initializer
            # or queued image filters. The game core is closed first.
            for process in list((self.executor._processes or {}).values()):
                if process.is_alive():process.terminate()
            self.executor.shutdown(wait=True,cancel_futures=False)
            self.executor=None

    def atlas_pair(self,name):
        if name in self.atlases:return self.atlases[name]
        if name in self.lazy_atlases:
            self.lazy_atlases.move_to_end(name);return self.lazy_atlases[name]
        extra=self.atlas_specs[name];w,h=extra['native_size']
        with Image.open(ROOT/'graphics'/extra['image']) as image:
            paint=image.convert('RGBA')
            if paint.width>w*4 and paint.height>h*4:paint=paint.resize((w*4,h*4),Image.Resampling.LANCZOS)
        with Image.open(ROOT/'graphics'/extra['reference']) as image:native=image.convert('RGBA').resize((w,h),Image.Resampling.NEAREST)
        self.lazy_atlases[name]=(paint,native)
        while len(self.lazy_atlases)>4:self.lazy_atlases.popitem(last=False)
        return paint,native

    def baked_lut(self,key):
        """Colour-to-palette-slot table computed by the bake, if present."""
        if getattr(self,'baked_luts',None) is None:
            self.baked_luts={}
            try:
                with np.load(ROOT/'graphics/palette_luts.npz',allow_pickle=False) as archive:
                    tables=archive['tables'];self.baked_luts={str(name):tables[i] for i,name in enumerate(archive['keys'])}
            except (OSError,ValueError,KeyError):pass
        return self.baked_luts.get(hashlib.sha1(key).hexdigest())

    def get_palette_lut(self,palette):
        key=palette.tobytes()
        if key not in self.palette_luts:
            found=self.baked_lut(key)
            if found is not None:self.palette_luts[key]=found;return found
            codes=np.arange(32768,dtype='uint32');colors=np.stack([(codes&31)*255/31,((codes>>5)&31)*255/31,((codes>>10)&31)*255/31],-1).astype('float32')
            self.palette_luts[key]=(np.argmin(((colors[:,None,:]-palette[None,1:,:])**2).sum(-1),axis=1)+1).astype('uint8')
        return self.palette_luts[key]

    def native_material_indices(self,binding,spec):
        cache=getattr(self,'native_materials',None)
        if cache is not None and binding<=len(cache['lengths']) and cache['lengths'][binding-1]==spec['w']*spec['h']:
            start=int(cache['starts'][binding-1]);length=int(cache['lengths'][binding-1])
            return cache['pixels'][start:start+length].reshape(spec['h'],spec['w'])
        return None

    def used_palette_indices(self,binding,palette,spec):
        if spec.get('index_pixels'):
            used=np.unique(np.frombuffer(zlib.decompress(base64.b64decode(spec['index_pixels'])),dtype='uint8'))
            return used[(used>0)&(used<len(palette))]
        native=self.native_material_indices(binding,spec)
        if native is not None:
            used=np.unique(native);return used[(used>0)&(used<len(palette))]
        if not hasattr(self,'used_palette_cache'):self.used_palette_cache=OrderedDict();self.native_palette_references=OrderedDict()
        source_binding=spec.get('source_binding',binding);key=(source_binding,palette.tobytes())
        if key in self.used_palette_cache:return self.used_palette_cache[key]
        source=self.bindings[source_binding-1];name=source.get('atlas_id','base');used=None
        reference_spec=self.atlas_specs.get(name,{'reference':'kazuma_parts_atlas_reference.png'})
        compiled=getattr(self,'material_slot_masks',None)
        if compiled is not None and binding<=len(compiled) and int(compiled[binding-1]):
            if name not in self.material_slot_verified:
                path=ROOT/'graphics'/reference_spec['reference']
                self.material_slot_verified[name]=path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==self.material_slot_references.get(name)
            if self.material_slot_verified[name]:
                used=np.flatnonzero(int(compiled[binding-1])&(1<<np.arange(len(palette))))
                self.used_palette_cache[key]=used;return used
        try:
            reference=self.native_palette_references.pop(name,None)
            if reference is None:
                with Image.open(ROOT/'graphics'/reference_spec['reference']) as opened:reference=opened.convert('RGBA')
                native_size=tuple(reference_spec.get('native_size',(256,128)))
                if reference.size!=native_size:reference=reference.resize(native_size,Image.Resampling.NEAREST)
            self.native_palette_references[name]=reference
            while len(self.native_palette_references)>4:self.native_palette_references.popitem(last=False)
            x,y,w,h=(source[k] for k in ('x','y','w','h'));pixels=np.asarray(reference.crop((x,y,x+w,y+h)))
            colors=pixels[:,:,:3][pixels[:,:,3]>0];five=np.rint(colors.astype('float32')*31/255).astype('uint32');codes=five[:,0]|five[:,1]<<5|five[:,2]<<10
            native=np.rint(palette*31/255).astype('uint32');slots=native[:,0]|native[:,1]<<5|native[:,2]<<10
            used=np.flatnonzero(np.isin(slots,np.unique(codes)));used=used[used>0]
        except (OSError,ValueError,KeyError):pass
        self.used_palette_cache[key]=used
        while len(self.used_palette_cache)>256:self.used_palette_cache.popitem(last=False)
        return used

    def material_map(self,binding,art,palette,spec):
        key=(binding,palette.tobytes());found=self.material_maps.pop(key,None)
        if found is None:
            rgb=np.asarray(art)[:,:,:3].astype('float32');q=np.rint(rgb*31/255).astype('uint32')
            used=self.used_palette_indices(binding,palette,spec)
            if used is not None and len(used) and len(used)<len(palette)-1:
                # Unused OBJ palette slots may be reused by muzzle flashes or
                # other units. HD antialias/shading colors must never pick an
                # unused slot merely because its old RGB happened to be close.
                packed=q[:,:,0]|q[:,:,1]<<5|q[:,:,2]<<10;codes,inverse=np.unique(packed,return_inverse=True)
                colors=np.stack([(codes&31)*255/31,((codes>>5)&31)*255/31,((codes>>10)&31)*255/31],-1).astype('float32')
                nearest=np.argmin(((colors[:,None,:]-palette[None,used,:])**2).sum(-1),axis=1)
                indices=used[nearest][inverse].reshape(q.shape[:2])
            else:indices=self.get_palette_lut(palette)[q[:,:,0]|q[:,:,1]<<5|q[:,:,2]<<10]
            native=spec.get('index_pixels')
            if native is None:native=self.native_material_indices(binding,spec)
            if native is not None:indices=material_indices(native,spec['w'],spec['h'],art.size,indices,palette,strict=True)
            residual=rgb-palette[indices]
            # Material IDs are spatial anchors. A painted highlight from a
            # different material must not turn a black edge pink/green when
            # its source palette is changed by an attack or flash.
            foreign=np.max(np.abs(residual),axis=2)>96
            ink=(rgb.max(2)<72)&((rgb.max(2)-rgb.min(2))<40)
            if foreign.any():
                light=np.clip(residual.mean(2),-16,16);residual[foreign]=light[foreign,None]
            residual=np.clip(residual,-32,32)
            # Neutral painted ink can cross a native material boundary. Keep
            # its HD contour instead of replacing it with the old bright pixel
            # blocks; saturated key-color fringes remain bounded above.
            if ink.any():
                delta=rgb.mean(2)-palette[indices].mean(2)
                residual[ink]=np.minimum(delta[ink,None],0)
            found=(residual,indices)
        self.material_maps[key]=found
        while len(self.material_maps)>64:self.material_maps.popitem(last=False)
        return found

    def rescue(self,binding,source,w,h):
        """Produce a texture now for a part the core has already hidden.

        The core decides to skip a native OBJ/BG tile from the ready set it
        held when the frame was emulated. A cache eviction or stage reset in
        this process between that decision and this draw would otherwise
        leave neither the native pixels nor the HD picture on screen.
        """
        try:
            if source.get('runtime_texture'):
                future=self.pending.get(binding)
                if future is None:future=self.pending[binding]=self.executor.submit(prepare_composite_task,*self.runtime_requests[binding])
                aligned,stats,palette_key,lut=future.result(timeout=.5)
                if aligned is None:return None
                if lut is not None:self.palette_luts[palette_key]=np.frombuffer(lut,dtype='uint8').copy()
                return aligned,stats
            return self.prepare_texture(binding,w,h)
        except Exception:return None

    def sprite(self,row,oam,palette=None,required=False):
        binding,a,b,c,_,brightness,alpha,_=map(int,row);spec=self.bindings[binding-1]
        w,h=spec['w'],spec['h'];matrix=()
        if a&256:
            index=(b>>9)&31;matrix=tuple(struct.unpack_from('<h',oam,(index*4+k)*8+6)[0] for k in range(4))
        key=(binding,a&0x700,b&0x3000,matrix,brightness,alpha if (a>>10)&3==1 else 0,int(row[4]) if spec.get('dynamic_palette') else 0)
        source_binding=spec.get('source_binding',binding)
        if source_binding not in self.prepared:
            source=self.bindings[source_binding-1];cache_key=f'part_{source_binding}'
            if self.registered_cache is not None and cache_key in self.registered_cache:
                aligned=Image.fromarray(self.registered_cache[cache_key]);stats=self.cached_stats[str(source_binding)]
            else:
                baked=source_binding in self.baked
                rescued=self.rescue(source_binding,source,w,h) if self.async_prepare and (required or baked) else None
                if rescued is not None:
                    aligned,stats=rescued
                    if not baked:self.rescued=getattr(self,'rescued',0)+1
                elif self.async_prepare:
                    if source_binding not in self.pending and source_binding not in self.prepare_errors and len(self.pending)<48:
                        try:
                            if source.get('runtime_texture'):self.pending[source_binding]=self.executor.submit(prepare_composite_task,*self.runtime_requests[source_binding])
                            else:self.pending[source_binding]=self.executor.submit(prepare_task,source_binding,w,h,self.prepare_delay)
                        except Exception as error:self.prepare_errors[source_binding]=str(error)
                    return None
                else:aligned,stats=self.prepare_texture(source_binding,w,h)
            self.prepared[source_binding]=aligned;self.registration_stats[source_binding]=stats
            while len(self.prepared)>512:self.prepared.popitem(last=False)
            # A baked binding is advertised from the start; reading it does
            # not change what the core may hide.
            if self.async_prepare and source_binding not in self.baked:self.ready_generation+=1
        self.prepared.move_to_end(source_binding)
        if key in self.cache:
            self.cache.move_to_end(key);return self.cache[key]
        art=self.scaled.pop(source_binding,None)
        if art is None:
            wanted=(round(w*SCALE),round(h*SCALE));art=self.baked_scales.get((source_binding,round(SCALE*256)))
            if art is None or art.size!=wanted:art=self.prepared[source_binding].resize(wanted,Image.Resampling.LANCZOS)
        self.scaled[source_binding]=art
        while len(self.scaled)>128:self.scaled.popitem(last=False)
        target_palette=spec.get('palette_rgb')
        if spec.get('dynamic_palette') and palette is not None and int(row[4])!=int(spec['hash']):
            colors=np.asarray(palette,dtype='uint32')
            target_palette=np.stack([(colors&31)*255//31,((colors>>5)&31)*255//31,((colors>>10)&31)*255//31],-1)
            if np.array_equal(target_palette[1:],np.asarray(spec['original_palette_rgb'])[1:]):target_palette=None
        if target_palette is not None and np.array_equal(np.asarray(target_palette),np.asarray(spec.get('original_palette_rgb',self.source_palette))):target_palette=None
        if target_palette is not None:
            source_palette=np.asarray(spec.get('palette_source_rgb',spec.get('original_palette_rgb',self.source_palette)),dtype='float32')
            residual,indices=self.material_map(binding,art,source_palette,spec)
            pixels=np.array(art)
            target=np.asarray(target_palette,dtype='float32');src_lum=source_palette@np.array([.2126,.7152,.0722]);dst_lum=target@np.array([.2126,.7152,.0722])
            used=np.unique(indices[np.asarray(art.getchannel('A'))>0]);used=used[used>0]
            gain=float(dst_lum[used].sum()/max(src_lum[used].sum(),1));detail=np.minimum((dst_lum+1)/(src_lum+1),max(0,gain*1.5)).clip(0,2)
            # Flash/monochrome palettes deliberately collapse several source
            # materials to one solid color. Do not reintroduce their old HD
            # shading as colored boxes across independently cropped pieces.
            same_target=np.all(target[:,None,:]==target[None,:,:],axis=2)
            different_source=np.any(source_palette[:,None,:]!=source_palette[None,:,:],axis=2)
            active=np.zeros(len(target),dtype=bool);active[used]=True
            collapsed=np.any(same_target&different_source&active[None,:],axis=1)
            detail[collapsed]=0
            shading=residual*detail[indices,None]
            if len(used) and np.mean(np.abs(target[used]-source_palette[used]))>48:
                # A large material recolor must not carry unrelated painted
                # RGB blocks into the new palette. Keep bounded light detail.
                shading=np.clip(shading.mean(axis=2,keepdims=True),-8,8)
            rgb=target[indices]+shading
            pixels[:,:,:3]=np.clip(np.rint(rgb),0,255).astype('uint8');art=Image.fromarray(pixels)
        elif spec.get('dynamic_palette') and source_binding>5263 and not (self.bindings[source_binding-1].get('wing_img_first') or spec.get('preserve_canonical_paint',spec.get('wing_live_palette',False))):
            source_palette=np.asarray(spec.get('palette_source_rgb',spec.get('original_palette_rgb',self.source_palette)),dtype='float32')
            residual,indices=self.material_map(binding,art,source_palette,spec)
            corrected=np.clip(np.rint(source_palette[indices]+residual),0,255).astype('uint8')
            pixels=np.array(art)
            rgb=pixels[:,:,:3].astype('float32');used=self.used_palette_indices(binding,source_palette,spec)
            if used is None or not len(used):used=np.arange(1,len(source_palette))
            colors=source_palette[used];chroma=rgb-rgb.mean(2,keepdims=True);reference_chroma=colors-colors.mean(1,keepdims=True)
            # Preserve canonical HD paint. Only reject colored key fringes
            # absent from the native materials; replacing every painted pixel
            # by a native material ID recreates the low-resolution pixel grid.
            color_distance=np.min(np.sum((rgb[:,:,None,:]-colors[None,None,:,:])**2,axis=3),axis=2)
            chroma_distance=np.min(np.sum((chroma[:,:,None,:]-reference_chroma[None,None,:,:])**2,axis=3),axis=2)
            suspect=(color_distance>32**2)&(chroma_distance>20**2)&((rgb.max(2)-rgb.min(2))>40)
            if suspect.any():
                pixels[:,:,:3][suspect]=corrected[suspect];art=Image.fromarray(pixels)
        if a&256:
            pa,pb,pc,pd=[v/256 for v in matrix];fw=w*(2 if a&512 else 1);fh=h*(2 if a&512 else 1)
            coeff=(pa,pb,(w/2-fw/2*pa-fh/2*pb)*SCALE,pc,pd,(h/2-fw/2*pc-fh/2*pd)*SCALE)
            art=art.transform((round(fw*SCALE),round(fh*SCALE)),Image.Transform.AFFINE,coeff,Image.Resampling.BICUBIC)
        else:
            if b&4096:art=art.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if b&8192:art=art.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        mode=brightness>>14;amount=min(brightness&31,16)/16
        if mode in (1,2):
            pixels=np.array(art)
            if mode==1:pixels[:,:,:3]=(pixels[:,:,:3]+(255-pixels[:,:,:3])*amount).astype('uint8')
            if mode==2:pixels[:,:,:3]=(pixels[:,:,:3]*(1-amount)).astype('uint8')
            art=Image.fromarray(pixels)
        self.cache[key]=art
        while len(self.cache)>512:self.cache.popitem(last=False)
        return art

    def prewarm_registered(self):
        """Only the small approved cache, not the 89k-part dynamic catalog."""
        from render_resolution import MIN_WIDTH,MAX_WIDTH
        for name,array in (self.registered_cache or {}).items():
            binding=int(name[5:]);spec=self.bindings[binding-1];source=Image.fromarray(array)
            for width in range(MIN_WIDTH,MAX_WIDTH+1,32):
                self.baked_scales[binding,width]=source.resize((round(spec['w']*width/256),round(spec['h']*width/256)),Image.Resampling.LANCZOS)

    def native_mask(self,left,upper,visible):
        """A part's visibility as a whole-screen native-resolution picture."""
        key=(left,upper,visible.shape,visible.tobytes());masks=self.__dict__.setdefault('native_masks',OrderedDict())
        image=masks.pop(key,None)
        if image is None:
            full=np.zeros((192,256),dtype='uint8');full[upper:upper+visible.shape[0],left:left+visible.shape[1]]=visible;image=Image.fromarray(full)
        masks[key]=image
        while len(masks)>256:masks.popitem(last=False)
        return image

    def compose(self,top,parts,oam,layer_ids,owners,bgpriors,bgparts,part_palettes=None,allow_native_fallback=False,effect_foreground=None,background_planes=()):
        if self.async_prepare:self.collect_prepared()
        active=[i for i in range(128) if parts[i,0]]
        native_attrs=np.frombuffer(oam,dtype='<u2').reshape(128,4)
        native_priority=(native_attrs[:,2]>>10)&3
        tasks=[(((int(parts[i,3])>>10)&3),0,i,parts[i]) for i in active]
        if bgparts is not None:
            for index in np.flatnonzero(bgparts[:,0]):
                row=bgparts[index];tasks.append((int(row[5]),1,int(row[4]),row))
        tasks.extend((int(priority),1,int(layer),draw) for priority,layer,draw in background_planes)
        visibility=PartVisibility(layer_ids,owners,bgpriors,native_priority)
        background_blend=int(parts[active[0],6]) if active else None
        foreground_images={}
        # Most parts are nowhere near a blending BG. Decide that once per
        # frame instead of unpacking the 64-bit records for every part.
        foreground_active=None
        if effect_foreground is not None:
            from foreground_blend import active as _active
            foreground_active=_active(effect_foreground)
            if not foreground_active.any():effect_foreground=None
        # Outcome counters, in native pixels, for the runtime-path verifier.
        # "vanished" is a part the core hid that received no HD picture.
        stats=dict(beam_tie_pixels=0,drawn=0,waiting=0,vanished=0,occluded=0,drawn_area=0,waiting_area=0,vanished_area=0);rescued=getattr(self,'rescued',0)
        self.last_stats=stats
        for priority,kind,i,original in sorted(tasks,key=lambda task:task[:3],reverse=True):
            if callable(original):
                original(top)
                continue
            if kind:
                bid,flip,x,y,layer,_,bright,control=map(int,original)
                if x>=2**31:x-=2**32
                if y>=2**31:y-=2**32
                row=np.array([bid,0,(flip&0xc00)<<2,priority<<10,0,bright,0,control],dtype='uint32')
                a,b,c=map(int,row[1:4])
            else:
                row=original;a,b,c=map(int,row[1:4]);control=int(row[7]);x=b&511;y=a&255
                if x>=256:x-=512
                if y>=192:y-=256
            native_hidden=self.async_prepare and not control&0x80000000
            art=self.sprite(row,oam,None if kind or part_palettes is None else part_palettes[i],required=native_hidden)
            spec=self.bindings[int(row[0])-1];area=spec['w']*spec['h']
            if art is None or (control&0x80000000 and not allow_native_fallback):
                outcome='vanished' if art is None and native_hidden else 'waiting'
                stats[outcome]+=1;stats[outcome+'_area']+=area;continue
            px,py=round(x*SCALE),round(y*SCALE)
            left=max(0,math.floor(px/SCALE));upper=max(0,math.floor(py/SCALE))
            right=min(256,math.ceil((px+art.width)/SCALE)+1);lower=min(192,math.ceil((py+art.height)/SCALE)+1)
            if left>=right or upper>=lower:continue
            layers=layer_ids[upper:lower,left:right]
            # Compare native BG priorities and surviving native OBJ ownership.
            # This retains enemies/effects in the same relative draw order.
            visible,visibility_state=visibility.mask(left,upper,right,lower,priority,kind,i,control,int(row[6]) if not kind else background_blend)
            foreground=None
            if effect_foreground is not None and foreground_active[upper:lower,left:right].any():
                from foreground_blend import eligibility_region
                packed=effect_foreground[upper:lower,left:right]
                eligible=eligibility_region(effect_foreground,(left,upper,right,lower),layer_ids,bgpriors,priority,i if kind else 4)
                # A surviving front OBJ (enemy, projectile or UI) must still
                # occlude the unit. Tie-promoted energy cannot reveal it.
                eligible&=(layers!=4)|(visible!=0)
                if eligible.any():
                    if not kind:
                        front_layer=((packed>>15)&7).astype('int16')-1
                        same_priority=np.asarray(bgpriors)[np.clip(front_layer,0,5)]==priority
                        stats['beam_tie_pixels']+=int(np.count_nonzero(eligible&same_priority&((packed&32767)!=0)))
                    # The DS blends the front BG color into the OBJ color;
                    # alpha attenuation alone cannot reproduce that ordering.
                    visible=visible.copy();visible[eligible]=255
                    visibility_state=1;foreground=(packed,eligible)
            # Alpha-blended BG effects retain a BG layer ID even when the
            # underlying OBJ is visible through them (e.g. the battle flash).
            if visibility_state==0:stats['occluded']+=1;continue
            stats['drawn']+=1;stats['drawn_area']+=area
            if visibility_state==2 and (kind or (a>>10)&3!=1):
                top.paste(art,(px,py),art)
                continue
            coeff=(1/SCALE,0,px/SCALE-left,0,1/SCALE,py/SCALE-upper)
            if SHORTCUTS and hasattr(top,'draw') and (kind or (a>>10)&3!=1):
                # The GPU enlarges the native-resolution mask itself (with the
                # same nearest-pixel rule), so no HD-sized mask is built or
                # uploaded here. An unchanged mask reuses its texture.
                effect=None
                if foreground is not None:
                    effect_key=(priority,i if kind else 4)
                    if effect_key not in foreground_images:
                        from foreground_blend import gpu_plane
                        foreground_images[effect_key]=gpu_plane(effect_foreground,layer_ids,bgpriors,priority,i if kind else 4)
                    effect=foreground_images[effect_key]
                top.draw(art,(px,py,px+art.width,py+art.height),mask=self.native_mask(left,upper,visible),mask_rect=(0,0,*top.size),alpha=True,foreground=effect,foreground_rect=(0,0,*top.size))
                continue
            local=Image.fromarray(visible).transform(art.size,Image.Transform.AFFINE,coeff,Image.Resampling.NEAREST)
            if foreground is not None and (not hasattr(top,'draw') or (a>>10)&3==1):
                from foreground_blend import blend_part
                art=blend_part(art,*foreground,coeff)
            if hasattr(top,'draw') and (kind or (a>>10)&3!=1):
                effect=None
                if foreground is not None:
                    effect_key=(priority,i if kind else 4)
                    if effect_key not in foreground_images:
                        from foreground_blend import gpu_plane
                        foreground_images[effect_key]=gpu_plane(effect_foreground,layer_ids,bgpriors,priority,i if kind else 4)
                    effect=foreground_images[effect_key]
                top.draw(art,(px,py,px+art.width,py+art.height),mask=local,alpha=True,foreground=effect,foreground_rect=(0,0,*top.size))
                continue
            mask=Image.fromarray((np.asarray(art.getchannel('A'),dtype='uint16')*np.asarray(local,dtype='uint16')//255).astype('uint8'))
            if not kind and (a>>10)&3==1:
                eligible=((control>>(8+layers.astype('uint32')))&1).astype('uint8')
                blend=Image.fromarray(eligible*255).transform(art.size,Image.Transform.AFFINE,coeff,Image.Resampling.NEAREST)
                opacity=np.where(np.asarray(blend)>0,min(int(row[6])&31,16)/16,1.)
                mask=Image.fromarray((np.asarray(mask)*opacity).astype('uint8'))
            top.paste(art,(px,py),mask)
        stats['rescued']=getattr(self,'rescued',0)-rescued
        self.prefetch_related(parts)
        return len(tasks)
