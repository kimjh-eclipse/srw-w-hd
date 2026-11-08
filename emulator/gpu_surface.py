"""Off-screen GPU source-over composition with Pillow-compatible draw commands."""
import sys,weakref
from pathlib import Path
from collections import OrderedDict
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools/gpu_py'))
_backend=None

def intersect(a,b):
    box=(max(a[0],b[0]),max(a[1],b[1]),min(a[2],b[2]),min(a[3],b[3]))
    return box if box[0]<box[2] and box[1]<box[3] else None

class Backend:
    def __init__(self):
        import moderngl as gl
        self.gl=gl;self.ctx=gl.create_standalone_context(require=330);self.textures=OrderedDict();self.frames=OrderedDict();self.coordinate_maps=OrderedDict()
        self.program=self.ctx.program(vertex_shader='''#version 330
        uniform vec2 viewport_size; uniform vec4 rectangle;
        out vec2 uv; out vec2 pixel;
        void main(){ vec2 p=vec2((gl_VertexID==1||gl_VertexID==3)?1:0,(gl_VertexID>=2)?1:0);
        uv=p;pixel=rectangle.xy+p*rectangle.zw;gl_Position=vec4(pixel.x/viewport_size.x*2-1,1-pixel.y/viewport_size.y*2,0,1); }
        ''',fragment_shader='''#version 330
        uniform sampler2D picture; uniform sampler2D opacity; uniform usampler2D source_coordinates; uniform int mask_mode; uniform int source_alpha; uniform vec4 mask_rectangle; uniform int nearest_picture; uniform vec4 rectangle; uniform vec2 viewport_size;
        in vec2 uv; in vec2 pixel; out vec4 color;
        void main(){ vec4 p;
        if(nearest_picture==1){ivec2 d=ivec2(gl_FragCoord.x,viewport_size.y-gl_FragCoord.y)-ivec2(rectangle.xy);ivec2 index=ivec2(texelFetch(source_coordinates,ivec2(d.x,0),0).r,texelFetch(source_coordinates,ivec2(d.y,1),0).r);p=texelFetch(picture,index,0);}
        else p=texture(picture,uv); float a=source_alpha==1?p.a:1.0;
        if(mask_mode>0){vec2 m=(pixel-mask_rectangle.xy)/mask_rectangle.zw;vec4 v=texture(opacity,m);a*=mask_mode==2?v.a:v.r;}
        color=vec4(p.rgb,a); }
        ''')
        self.vao=self.ctx.vertex_array(self.program,[]);self.program['picture']=0;self.program['opacity']=1;self.program['source_coordinates']=2
        self.ctx.enable(gl.BLEND);self.ctx.blend_func=(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA,gl.ONE,gl.ONE_MINUS_SRC_ALPHA)

    def texture(self,image,nearest=False):
        key=id(image);found=self.textures.pop(key,None)
        if found is not None and found[0]() is image:tex=found[1]
        else:
            if found is not None:found[1].release()
            source=image if image.mode in ('RGB','RGBA','L') else image.convert('RGBA')
            tex=self.ctx.texture(source.size,len(source.getbands()),source.tobytes(),alignment=1)
        tex.filter=(self.gl.NEAREST,self.gl.NEAREST) if nearest else (self.gl.LINEAR,self.gl.LINEAR)
        tex.repeat_x=False;tex.repeat_y=False;self.textures[key]=(weakref.ref(image),tex)
        while len(self.textures)>192:self.textures.popitem(last=False)[1][1].release()
        return tex

    def reset_pipeline(self):
        for name in ('paired_top','paired_bottom'):
            channel=getattr(self,name,None)
            if channel is not None:channel.reset()
        self.paired_previous_bottom=None;self.paired_bottom_pixels={}
        if getattr(self,'persistent',None) is not None:self.persistent.reset()
        for buffer in getattr(self,'read_buffers',[]):buffer.release()
        self.read_buffers=[];self.read_pending=None;self.read_size=None;self.read_slot=0

    def render_pair(self,top,bottom,tag):
        """Pipeline both screens, reading static lower screens only once."""
        from gpu_readback import PersistentPBO
        if getattr(self,'paired_top',None) is None:
            self.paired_top=PersistentPBO();self.paired_bottom=PersistentPBO()
            self.paired_previous_bottom=None;self.paired_bottom_pixels={}
        if self.paired_top.size!=top.size:self.reset_pipeline()
        top_pixels,previous=self.paired_top.read(top.size,tag,lambda:self.render(top,components=4,draw_only=True))
        if bottom is not self.paired_previous_bottom:
            pixels,source=self.paired_bottom.read(bottom.size,bottom,lambda:self.render(bottom,components=4,draw_only=True))
            self.paired_bottom_pixels[id(source)]=(source,pixels);self.paired_previous_bottom=bottom
        needed=previous[1]
        if id(needed) not in self.paired_bottom_pixels:
            pixels,source=self.paired_bottom.consume(self.paired_bottom.pending)
            self.paired_bottom_pixels[id(source)]=(source,pixels)
        pixels=self.paired_bottom_pixels[id(needed)][1]
        self.paired_bottom_pixels={k:v for k,v in self.paired_bottom_pixels.items() if v[0] is needed or v[0] is bottom}
        return top_pixels,pixels,previous

    def render(self,surface,components=3,pipeline_tag=None,draw_only=False):
        if pipeline_tag is not None and components==4 and not getattr(self,'persistent_disabled',False):
            try:
                if getattr(self,'persistent',None) is None:
                    if 'GL_ARB_buffer_storage' not in self.ctx.extensions:raise RuntimeError('Persistent readback is unavailable')
                    from gpu_readback import PersistentPBO
                    self.persistent=PersistentPBO()
                return self.persistent.read(surface.size,pipeline_tag,lambda:self.render(surface,components=4,draw_only=True))
            except Exception as error:
                self.persistent_disabled=True;self.persistent_error=str(error)
                try:
                    if getattr(self,'persistent',None) is not None:self.persistent.close()
                except Exception:pass
                self.persistent=None
        previous=None;previous_raw=None
        if pipeline_tag is not None:
            if getattr(self,'read_size',None)!=(surface.size,components):
                self.reset_pipeline();self.read_size=(surface.size,components)
                self.read_buffers=[self.ctx.buffer(reserve=surface.width*surface.height*components) for _ in range(2)]
            previous=self.read_pending
            # Read the completed previous transfer before queueing any current
            # drawing; a read after new commands can serialize the driver.
            if previous is not None:previous_raw=self.read_buffers[previous[0]].read()
        for key,(reference,texture) in list(self.textures.items()):
            if reference() is None:del self.textures[key];texture.release()
        width,height=surface.size;frame_key=(surface.size,components);frame=self.frames.pop(frame_key,None)
        if frame is None:frame=self.ctx.simple_framebuffer(surface.size,components=components)
        self.frames[frame_key]=frame
        while len(self.frames)>3:self.frames.popitem(last=False)[1].release()
        frame.use();self.ctx.viewport=(0,0,width,height);self.ctx.scissor=None
        frame.clear(0,0,0,1);self.program['viewport_size']=(width,height)
        for op in surface.ops:
            clip=intersect(op['clip'],(0,0,width,height))
            if clip is None:continue
            left,top,right,bottom=op['rect']
            if right<=left or bottom<=top:continue
            l,t,r,b=clip;self.ctx.scissor=(round(l),height-round(b),round(r)-round(l),round(b)-round(t))
            self.program['rectangle']=(left,top,right-left,bottom-top)
            self.program['nearest_picture']=int(op['nearest'])
            self.texture(op['image'],op['nearest']).use(0)
            if op['nearest']:
                source=op['image'];mapping_key=(source.size,round(right-left),round(bottom-top))
                mapping=self.coordinate_maps.pop(mapping_key,None)
                if mapping is None:
                    ow,oh=mapping_key[1:];values=np.zeros((2,max(ow,oh)),dtype='uint8')
                    values[0,:ow]=np.asarray(Image.fromarray(np.arange(source.width,dtype='uint8')[None,:]).resize((ow,1),Image.Resampling.NEAREST))[0]
                    values[1,:oh]=np.asarray(Image.fromarray(np.arange(source.height,dtype='uint8')[:,None]).resize((1,oh),Image.Resampling.NEAREST))[:,0]
                    mapping=self.ctx.texture((values.shape[1],2),1,values.tobytes(),dtype='u1',alignment=1)
                self.coordinate_maps[mapping_key]=mapping;mapping.use(2)
                while len(self.coordinate_maps)>64:self.coordinate_maps.popitem(last=False)[1].release()
            mask=op['mask'];mode=0
            if mask is not None:
                self.texture(mask,True).use(1);mode=2 if mask.mode=='RGBA' else 1
                ml,mt,mr,mb=op['mask_rect'];self.program['mask_rectangle']=(ml,mt,mr-ml,mb-mt)
            self.program['mask_mode']=mode;self.program['source_alpha']=int(op['alpha'])
            self.vao.render(self.gl.TRIANGLE_STRIP,vertices=4)
        self.ctx.scissor=None
        if draw_only:return frame
        if pipeline_tag is not None:
            slot=self.read_slot;self.read_slot=1-slot
            frame.read_into(self.read_buffers[slot],components=components,alignment=1)
            self.read_pending=(slot,pipeline_tag)
            import ctypes
            ctypes.windll.opengl32.glFlush()
            if previous is None:previous=(slot,pipeline_tag);previous_raw=self.read_buffers[slot].read()
            raw=previous_raw
            pixels=np.frombuffer(raw,dtype='uint8').reshape(height,width,components)[::-1].copy()
            return pixels,previous[1]
        raw=frame.read(components=components,alignment=1)
        return np.frombuffer(raw,dtype='uint8').reshape(height,width,components)[::-1].copy()

def backend():
    global _backend
    if _backend is None:_backend=Backend()
    return _backend

class Surface:
    def __init__(self,size,ops=None):
        self.size=tuple(size);self.width,self.height=self.size;self.ops=list(ops or []);self.pixels=None

    @classmethod
    def from_native(cls,native,size):
        result=cls(size);result.draw(Image.fromarray(np.asarray(native)),(0,0,*size),nearest=True);return result

    def draw(self,image,rect,mask=None,nearest=False,clip=None,mask_rect=None,alpha=False):
        self.pixels=None
        self.ops.append(dict(image=image,rect=rect,mask=mask,mask_rect=mask_rect or rect,nearest=nearest,clip=clip or (0,0,*self.size),alpha=alpha))

    def paste(self,image,box=(0,0),mask=None):
        self.pixels=None
        if isinstance(image,Surface):
            x,y=box[:2]
            if mask is not None and mask is not image and any(op['mask'] is not None or op['alpha'] for op in image.ops):
                self.paste(image.to_pil(),box,mask);return
            for original in image.ops:
                op=dict(original);l,t,r,b=op['rect'];op['rect']=(l+x,t+y,r+x,b+y)
                l,t,r,b=op['clip'];clip=intersect((l+x,t+y,r+x,b+y),(0,0,*self.size))
                if clip is None:continue
                op['clip']=clip
                l,t,r,b=op['mask_rect'];op['mask_rect']=(l+x,t+y,r+x,b+y)
                if mask is not None and mask is not image:
                    op['mask']=mask;op['mask_rect']=(x,y,x+image.width,y+image.height);op['alpha']=False
                self.ops.append(op)
            return
        if isinstance(image,(tuple,str,int)):
            image=Image.new('RGB',(1,1),image)
        x,y=box[:2];rect=tuple(box) if len(box)==4 else (x,y,x+image.width,y+image.height)
        self.draw(image,rect,None if mask is image else mask,alpha=mask is image)

    def alpha_composite(self,image,dest=(0,0)):
        self.paste(image,dest,image)

    def copy(self):return Surface(self.size,self.ops)

    def crop(self,box):
        left,top,right,bottom=box;result=Surface((right-left,bottom-top))
        for original in self.ops:
            op=dict(original);clip=intersect(op['clip'],box)
            if clip is None:continue
            l,t,r,b=op['rect'];op['rect']=(l-left,t-top,r-left,b-top)
            l,t,r,b=clip;op['clip']=(l-left,t-top,r-left,b-top)
            l,t,r,b=op['mask_rect'];op['mask_rect']=(l-left,t-top,r-left,b-top);result.ops.append(op)
        return result

    def __array__(self,dtype=None,copy=None):
        if self.pixels is None:self.pixels=backend().render(self)
        result=self.pixels
        if dtype is not None:result=result.astype(dtype,copy=False)
        return result.copy() if copy else result

    def to_pil(self):return Image.fromarray(np.asarray(self))
    def rgba(self):return backend().render(self,components=4)
    def rgba_pipeline(self,tag):return backend().render(self,components=4,pipeline_tag=tag)
    def resize(self,*args,**kwargs):return self.to_pil().resize(*args,**kwargs)
    def save(self,*args,**kwargs):return self.to_pil().save(*args,**kwargs)
    def tobytes(self):return np.asarray(self).tobytes()
