"""Render individual native OBJ parts from the HD atlas with DS OAM transforms."""
from pathlib import Path
import json,struct
from collections import OrderedDict
import numpy as np
from PIL import Image
from hd_parts_registration import register_part,registration_stamp

ROOT=Path(__file__).resolve().parent.parent
SCALE=1440/256

class PartsRenderer:
    def __init__(self):
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
                if str(archive['stamp'])==registration_stamp(ROOT):
                    self.registered_cache={key:archive[key] for key in archive.files if key.startswith('part_')}
                    self.cached_stats=json.loads(str(archive['statistics']))
        self.cache=OrderedDict()

    def atlas_pair(self,name):
        if name in self.atlases:return self.atlases[name]
        if name in self.lazy_atlases:
            self.lazy_atlases.move_to_end(name);return self.lazy_atlases[name]
        extra=self.atlas_specs[name];w,h=extra['native_size']
        with Image.open(ROOT/'graphics'/extra['image']) as image:paint=image.convert('RGBA').resize((w*8,h*8),Image.Resampling.LANCZOS)
        with Image.open(ROOT/'graphics'/extra['reference']) as image:native=image.convert('RGBA').resize((w,h),Image.Resampling.NEAREST)
        self.lazy_atlases[name]=(paint,native)
        while len(self.lazy_atlases)>4:self.lazy_atlases.popitem(last=False)
        return paint,native

    def sprite(self,row,oam,palette=None):
        binding,a,b,c,_,brightness,alpha,_=map(int,row);spec=self.bindings[binding-1]
        w,h=spec['w'],spec['h'];matrix=()
        if a&256:
            index=(b>>9)&31;matrix=tuple(struct.unpack_from('<h',oam,(index*4+k)*8+6)[0] for k in range(4))
        key=(binding,a&0x700,b&0x3000,matrix,brightness,alpha if (a>>10)&3==1 else 0,int(row[4]) if spec.get('dynamic_palette') else 0)
        if key in self.cache:
            self.cache.move_to_end(key);return self.cache[key]
        source_binding=spec.get('source_binding',binding)
        if source_binding not in self.prepared:
            source=self.bindings[source_binding-1];cache_key=f'part_{source_binding}'
            if self.registered_cache is not None and cache_key in self.registered_cache:
                aligned=Image.fromarray(self.registered_cache[cache_key]);stats=self.cached_stats[str(source_binding)]
            else:
                x,y=source['x'],source['y'];paint_atlas,native_atlas=self.atlas_pair(source.get('atlas_id','base'))
                paint=paint_atlas.crop((x*8,y*8,(x+w)*8,(y+h)*8))
                native=native_atlas.crop((x,y,x+w,y+h))
                aligned,stats=register_part(paint,native)
            self.prepared[source_binding]=aligned;self.registration_stats[source_binding]=stats
            while len(self.prepared)>512:self.prepared.popitem(last=False)
        self.prepared.move_to_end(source_binding)
        art=self.prepared[source_binding].resize((round(w*SCALE),round(h*SCALE)),Image.Resampling.LANCZOS)
        target_palette=spec.get('palette_rgb')
        if spec.get('dynamic_palette') and palette is not None:
            colors=np.asarray(palette,dtype='uint32')
            target_palette=np.stack([(colors&31)*255//31,((colors>>5)&31)*255//31,((colors>>10)&31)*255//31],-1)
            if np.array_equal(target_palette[1:],np.asarray(spec['original_palette_rgb'])[1:]):target_palette=None
        if target_palette is not None:
            source_palette=np.asarray(spec.get('palette_source_rgb',spec.get('original_palette_rgb',self.source_palette)),dtype='float32')
            palette_key=source_palette.tobytes()
            if palette_key not in self.palette_luts:
                codes=np.arange(32768,dtype='uint32');colors=np.stack([(codes&31)*255/31,((codes>>5)&31)*255/31,((codes>>10)&31)*255/31],-1).astype('float32')
                self.palette_luts[palette_key]=(np.argmin(((colors[:,None,:]-source_palette[None,1:,:])**2).sum(-1),axis=1)+1).astype('uint8')
            pixels=np.array(art);rgb=pixels[:,:,:3].astype('float32');quantized=np.rint(rgb*31/255).astype('uint32')
            codes=quantized[:,:,0]|(quantized[:,:,1]<<5)|(quantized[:,:,2]<<10);indices=self.palette_luts[palette_key][codes]
            target=np.asarray(target_palette,dtype='float32');src_lum=source_palette@np.array([.2126,.7152,.0722]);dst_lum=target@np.array([.2126,.7152,.0722])
            gain=float(dst_lum[1:].sum()/max(src_lum[1:].sum(),1));detail=np.minimum((dst_lum+1)/(src_lum+1),max(0,gain*1.5)).clip(0,2)
            rgb=target[indices]+(rgb-source_palette[indices])*detail[indices,None]
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

    def compose(self,top,parts,oam,layer_ids,owners,bgpriors,bgparts,part_palettes=None):
        active=[i for i in range(128) if parts[i,0]]
        native_attrs=np.frombuffer(oam,dtype='<u2').reshape(128,4)
        native_priority=(native_attrs[:,2]>>10)&3
        tasks=[(((int(parts[i,3])>>10)&3),0,i,parts[i]) for i in active]
        if bgparts is not None:tasks.extend((int(r[5]),1,int(r[4]),r) for r in bgparts if r[0])
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
            px,py=round(x*SCALE),round(y*SCALE)
            # Compare native BG priorities and surviving native OBJ ownership.
            # This retains enemies/effects in the same relative draw order.
            bgprio=bgpriors[np.minimum(layer_ids,5)]
            visible=((layer_ids<4)&((bgprio>priority)|((bgprio==priority)&((layer_ids>i) if kind else True))))|(layer_ids==5)
            # Alpha-blended BG effects retain a BG layer ID even when the
            # underlying OBJ is visible through them (e.g. the battle flash).
            if control&0xc0==0x40 and control&(1<<(8+i if kind else 12)):
                visible|=(layer_ids<4)&(((control>>layer_ids.astype('uint32'))&1)!=0)
            objmask=layer_ids==4;prio=native_priority[owners]
            visible|=objmask&((prio>priority)|((prio==priority)&(owners>i)&(not kind)))
            local=Image.fromarray(visible.astype('uint8')*255).transform(art.size,Image.Transform.AFFINE,(1/SCALE,0,px/SCALE,0,1/SCALE,py/SCALE),Image.Resampling.NEAREST)
            mask=Image.fromarray((np.asarray(art.getchannel('A'),dtype='uint16')*np.asarray(local,dtype='uint16')//255).astype('uint8'))
            if not kind and (a>>10)&3==1:
                eligible=((control>>(8+layer_ids.astype('uint32')))&1).astype('uint8')
                blend=Image.fromarray(eligible*255).transform(art.size,Image.Transform.AFFINE,(1/SCALE,0,px/SCALE,0,1/SCALE,py/SCALE),Image.Resampling.NEAREST)
                opacity=np.where(np.asarray(blend)>0,min(int(row[6])&31,16)/16,1.)
                mask=Image.fromarray((np.asarray(mask)*opacity).astype('uint8'))
            top.paste(art,(px,py),mask)
        return len(tasks)
