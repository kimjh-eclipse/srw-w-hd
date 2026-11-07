"""Render individual native OBJ parts from the HD atlas with DS OAM transforms."""
from pathlib import Path
import json,struct,hashlib,queue,base64,zlib
import math
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp,os
from collections import OrderedDict
import numpy as np
from PIL import Image
from hd_parts_registration import register_part,registration_stamp
from parts_disk_cache import PartsDiskCache
from palette_materials import material_indices
from texture_preparation import prepare_task,prepare_composite_task,start_texture_worker

ROOT=Path(__file__).resolve().parent.parent
SCALE=1440/256

class PartsRenderer:
    def __init__(self,async_prepare=False,dynamic_parts=False):
        meta=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text())
        self.bindings=meta['bindings'];self.atlas=Image.open(ROOT/'graphics'/meta['atlas']).convert('RGBA').resize((2048,1024),Image.Resampling.LANCZOS)
        self.native_atlas=Image.open(ROOT/'graphics/kazuma_parts_atlas_reference.png').convert('RGBA').resize((256,128),Image.Resampling.NEAREST)
        self.atlases={'base':(self.atlas,self.native_atlas)}
        self.atlas_specs=meta.get('atlases',{});self.lazy_atlases=OrderedDict()
        for name,extra in meta.get('atlases',{}).items():
            if extra.get('lazy'):continue
            w,h=extra['native_size']
            self.atlases[name]=(Image.open(ROOT/'graphics'/extra['image']).convert('RGBA').resize((w*8,h*8),Image.Resampling.LANCZOS),Image.open(ROOT/'graphics'/extra['reference']).convert('RGBA').resize((w,h),Image.Resampling.NEAREST))
        self.source_palette=np.array(meta.get('source_palette_rgb',[]),dtype='float32');self.palette_lut=None
        if len(self.source_palette):
            codes=np.arange(32768,dtype='uint32');rgb=np.stack([(codes&31)*255/31,((codes>>5)&31)*255/31,((codes>>10)&31)*255/31],-1).astype('float32')
            self.palette_lut=(np.argmin(((rgb[:,None,:]-self.source_palette[None,1:,:])**2).sum(-1),axis=1)+1).astype('uint8')
        self.palette_luts={self.source_palette.tobytes():self.palette_lut}
        self.prepared=OrderedDict();self.registration_stats={}
        self.registered_cache=None;self.cached_stats={}
        cache_path=ROOT/'graphics'/meta.get('registration_cache','kazuma_parts_registration.npz')
        if cache_path.exists():
            with np.load(cache_path,allow_pickle=False) as archive:
                if str(archive['stamp'])==registration_stamp(ROOT,meta):
                    self.registered_cache={key:archive[key] for key in archive.files if key.startswith('part_')}
                    self.cached_stats=json.loads(str(archive['statistics']))
        self.cache=OrderedDict();self.scaled=OrderedDict();self.material_maps=OrderedDict()
        if async_prepare and self.registered_cache is not None:
            for key in self.registered_cache:
                spec=self.bindings[int(key[5:])-1]
                palette=np.asarray(spec.get('palette_source_rgb',spec.get('original_palette_rgb',self.source_palette)),dtype='float32')
                self.get_palette_lut(palette)
        self.async_prepare=async_prepare;self.pending={};self.prepare_errors={}
        self.prepare_delay=0
        self.executor=ProcessPoolExecutor(max_workers=1,mp_context=mp.get_context('spawn'),initializer=start_texture_worker,initargs=(os.getpid(),)) if async_prepare else None
        self.disk_cache=PartsDiskCache(ROOT/'graphics/parts_registered.sqlite')
        self.registration_version=hashlib.sha256((Path(__file__).parent/'hd_parts_registration.py').read_bytes()).hexdigest()
        self.ready_generation=0;self.ready_aliases={}
        for index,binding in enumerate(self.bindings,1):self.ready_aliases.setdefault(binding.get('source_binding',index),[]).append(index)
        self.dynamic_parts=bool(dynamic_parts and async_prepare and (ROOT/'graphics/parts_tile_library.sqlite').exists())
        self.dynamic_bindings=queue.SimpleQueue();self.unmapped_pending={};self.unmapped_seen=set();self.unmapped_misses={};self.runtime_requests={}

    def schedule_unknown(self,snapshot):
        if not self.dynamic_parts or snapshot is None:return
        for key,(future,request,descriptor) in list(self.unmapped_pending.items()):
            if not future.done():continue
            del self.unmapped_pending[key]
            try:art,stats,palette_key,lut=future.result()
            except Exception as error:art=None;stats=dict(reason=str(error))
            if art is None:self.unmapped_misses[key]=stats;continue
            binding=len(self.bindings)+1
            if binding>=200000:self.unmapped_misses[key]=dict(reason='runtime texture capacity');continue
            descriptor['hash']=stats['reference_hash'];descriptor['original_palette_rgb']=stats['reference_palette_rgb']
            self.bindings.append(descriptor);self.prepared[binding]=art;self.registration_stats[binding]=stats
            self.runtime_requests[binding]=request;self.ready_aliases[binding]=[binding]
            if lut is not None:self.palette_luts[palette_key]=np.frombuffer(lut,dtype='uint8').copy()
            self.dynamic_bindings.put((key[0],key[1],binding));self.ready_generation+=1
        rows,pixels,palettes=snapshot
        for i in np.flatnonzero(rows[:,0]):
            row=rows[i];identity=(int(row[0]),int(row[7]))
            if identity in self.unmapped_seen or len(self.unmapped_pending)>=12:continue
            w,h=int(row[1]),int(row[2]);encoded=base64.b64encode(zlib.compress(pixels[i,:w*h].tobytes())).decode('ascii');palette=palettes[i].tolist()
            request=(encoded,w,h,palette);colors=np.asarray(palette,dtype='uint32');rgb=np.stack([(colors&31)*255//31,((colors>>5)&31)*255//31,((colors>>10)&31)*255//31],-1).tolist()
            descriptor=dict(hash=int(row[6]),index_hash=int(row[0]),w=w,h=h,x=0,y=0,runtime_texture=True,dynamic_palette=True,original_palette_rgb=rgb,index_pixels=encoded)
            try:future=self.executor.submit(prepare_composite_task,*request)
            except Exception as error:self.unmapped_misses[identity]=dict(reason=str(error));continue
            self.unmapped_seen.add(identity);self.unmapped_pending[identity]=(future,request,descriptor)

    def ready_bindings(self):
        sources=set(self.prepared)
        if self.registered_cache is not None:sources.update(int(k[5:]) for k in self.registered_cache)
        return [alias for source in sources for alias in self.ready_aliases.get(source,())]

    def prepare_texture(self,binding,w,h):
        source=self.bindings[binding-1];x,y=source['x'],source['y'];name=source.get('atlas_id','base')
        spec=self.atlas_specs.get(name,{'image':'kazuma_parts_atlas_facefix.png','reference':'kazuma_parts_atlas_reference.png'})
        if self.async_prepare:
            palette=np.asarray(source.get('palette_source_rgb',source.get('original_palette_rgb',self.source_palette)),dtype='float32')
            palette_key=palette.tobytes()
            if palette_key not in self.palette_luts:
                codes=np.arange(32768,dtype='uint32');colors=np.stack([(codes&31)*255/31,((codes>>5)&31)*255/31,((codes>>10)&31)*255/31],-1).astype('float32')
                self.palette_luts[palette_key]=(np.argmin(((colors[:,None,:]-palette[None,1:,:])**2).sum(-1),axis=1)+1).astype('uint8')
        identity=[self.registration_version,'native-crop-v2',x,y,w,h]
        for path in (ROOT/'graphics'/spec['image'],ROOT/'graphics'/spec['reference']):
            stat=path.stat();identity.extend([str(path),stat.st_mtime_ns,stat.st_size])
        key=hashlib.sha256(json.dumps(identity).encode()).hexdigest()
        if self.async_prepare:
            try:found=self.disk_cache.get(key)
            except Exception:found=None
            if found:return found
        paint_atlas,native_atlas=self.atlas_pair(name)
        sx=paint_atlas.width/native_atlas.width;sy=paint_atlas.height/native_atlas.height
        paint=paint_atlas.crop((round(x*sx),round(y*sy),round((x+w)*sx),round((y+h)*sy))).resize((w*8,h*8),Image.Resampling.LANCZOS)
        aligned,stats=register_part(paint,native_atlas.crop((x,y,x+w,y+h)))
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
                changed=True
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
        with Image.open(ROOT/'graphics'/extra['image']) as image:paint=image.convert('RGBA')
        with Image.open(ROOT/'graphics'/extra['reference']) as image:native=image.convert('RGBA').resize((w,h),Image.Resampling.NEAREST)
        self.lazy_atlases[name]=(paint,native)
        while len(self.lazy_atlases)>4:self.lazy_atlases.popitem(last=False)
        return paint,native

    def get_palette_lut(self,palette):
        key=palette.tobytes()
        if key not in self.palette_luts:
            codes=np.arange(32768,dtype='uint32');colors=np.stack([(codes&31)*255/31,((codes>>5)&31)*255/31,((codes>>10)&31)*255/31],-1).astype('float32')
            self.palette_luts[key]=(np.argmin(((colors[:,None,:]-palette[None,1:,:])**2).sum(-1),axis=1)+1).astype('uint8')
        return self.palette_luts[key]

    def material_map(self,binding,art,palette,spec):
        key=(binding,palette.tobytes());found=self.material_maps.pop(key,None)
        if found is None:
            rgb=np.asarray(art)[:,:,:3].astype('float32');q=np.rint(rgb*31/255).astype('uint32')
            indices=self.get_palette_lut(palette)[q[:,:,0]|q[:,:,1]<<5|q[:,:,2]<<10]
            if spec.get('index_pixels'):indices=material_indices(spec['index_pixels'],spec['w'],spec['h'],art.size,indices,palette)
            found=(rgb-palette[indices],indices)
        self.material_maps[key]=found
        while len(self.material_maps)>64:self.material_maps.popitem(last=False)
        return found

    def sprite(self,row,oam,palette=None):
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
                if self.async_prepare:
                    if source_binding not in self.pending and source_binding not in self.prepare_errors and len(self.pending)<48:
                        try:
                            if source.get('runtime_texture'):self.pending[source_binding]=self.executor.submit(prepare_composite_task,*self.runtime_requests[source_binding])
                            else:self.pending[source_binding]=self.executor.submit(prepare_task,source_binding,w,h,self.prepare_delay)
                        except Exception as error:self.prepare_errors[source_binding]=str(error)
                    return None
                aligned,stats=self.prepare_texture(source_binding,w,h)
            self.prepared[source_binding]=aligned;self.registration_stats[source_binding]=stats
            while len(self.prepared)>512:self.prepared.popitem(last=False)
            if self.async_prepare:self.ready_generation+=1
        self.prepared.move_to_end(source_binding)
        if key in self.cache:
            self.cache.move_to_end(key);return self.cache[key]
        art=self.scaled.pop(source_binding,None)
        if art is None:art=self.prepared[source_binding].resize((round(w*SCALE),round(h*SCALE)),Image.Resampling.LANCZOS)
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
            gain=float(dst_lum[1:].sum()/max(src_lum[1:].sum(),1));detail=np.minimum((dst_lum+1)/(src_lum+1),max(0,gain*1.5)).clip(0,2)
            rgb=target[indices]+residual*detail[indices,None]
            pixels[:,:,:3]=np.clip(np.rint(rgb),0,255).astype('uint8');art=Image.fromarray(pixels)
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

    def compose(self,top,parts,oam,layer_ids,owners,bgpriors,bgparts,part_palettes=None,allow_native_fallback=False):
        if self.async_prepare:self.collect_prepared()
        active=[i for i in range(128) if parts[i,0]]
        native_attrs=np.frombuffer(oam,dtype='<u2').reshape(128,4)
        native_priority=(native_attrs[:,2]>>10)&3
        tasks=[(((int(parts[i,3])>>10)&3),0,i,parts[i]) for i in active]
        if bgparts is not None:
            for index in np.flatnonzero(bgparts[:,0]):
                row=bgparts[index];tasks.append((int(row[5]),1,int(row[4]),row))
        bgprio_all=bgpriors[np.minimum(layer_ids,5)]
        objprio_all=native_priority[owners]
        for priority,kind,i,original in sorted(tasks,key=lambda task:task[:3],reverse=True):
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
            art=self.sprite(row,oam,None if kind or part_palettes is None else part_palettes[i])
            if art is None or (control&0x80000000 and not allow_native_fallback):continue
            px,py=round(x*SCALE),round(y*SCALE)
            left=max(0,math.floor(px/SCALE));upper=max(0,math.floor(py/SCALE))
            right=min(256,math.ceil((px+art.width)/SCALE)+1);lower=min(192,math.ceil((py+art.height)/SCALE)+1)
            if left>=right or upper>=lower:continue
            layers=layer_ids[upper:lower,left:right];local_owners=owners[upper:lower,left:right]
            # Compare native BG priorities and surviving native OBJ ownership.
            # This retains enemies/effects in the same relative draw order.
            bgprio=bgprio_all[upper:lower,left:right]
            visible=((layers<4)&((bgprio>priority)|((bgprio==priority)&((layers>i) if kind else True))))|(layers==5)
            # Alpha-blended BG effects retain a BG layer ID even when the
            # underlying OBJ is visible through them (e.g. the battle flash).
            if control&0xc0==0x40 and control&(1<<(8+i if kind else 12)):
                visible|=(layers<4)&(((control>>layers.astype('uint32'))&1)!=0)
            objmask=layers==4;prio=objprio_all[upper:lower,left:right]
            visible|=objmask&((prio>priority)|((prio==priority)&(local_owners>=i)&(not kind)))
            coeff=(1/SCALE,0,px/SCALE-left,0,1/SCALE,py/SCALE-upper)
            local=Image.fromarray(visible.astype('uint8')*255).transform(art.size,Image.Transform.AFFINE,coeff,Image.Resampling.NEAREST)
            mask=Image.fromarray((np.asarray(art.getchannel('A'),dtype='uint16')*np.asarray(local,dtype='uint16')//255).astype('uint8'))
            if not kind and (a>>10)&3==1:
                eligible=((control>>(8+layers.astype('uint32')))&1).astype('uint8')
                blend=Image.fromarray(eligible*255).transform(art.size,Image.Transform.AFFINE,coeff,Image.Resampling.NEAREST)
                opacity=np.where(np.asarray(blend)>0,min(int(row[6])&31,16)/16,1.)
                mask=Image.fromarray((np.asarray(mask)*opacity).astype('uint8'))
            top.paste(art,(px,py),mask)
        return len(tasks)
