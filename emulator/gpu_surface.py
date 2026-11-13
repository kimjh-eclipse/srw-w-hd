"""Off-screen GPU source-over composition with Pillow-compatible draw commands."""
import sys,weakref
from pathlib import Path
from collections import OrderedDict
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools/gpu_py'))
_backend=None
_window=None

def attach_window(parent):
    """Compose in a GL context that belongs to a child window of the UI
    canvas, so finished frames can be shown without leaving the GPU."""
    global _window
    if _backend is not None:raise RuntimeError('The GPU backend already exists')
    from direct_present import PresentWindow
    _window=PresentWindow(parent);return _window

def intersect(a,b):
    box=(max(a[0],b[0]),max(a[1],b[1]),min(a[2],b[2]),min(a[3],b[3]))
    return box if box[0]<box[2] and box[1]<box[3] else None

class Backend:
    def __init__(self):
        import moderngl as gl
        self.gl=gl;self.window=_window;self.ctx=gl.create_context(require=330) if _window is not None else gl.create_standalone_context(require=330);self.textures=OrderedDict();self.frames=OrderedDict();self.coordinate_maps=OrderedDict()
        self.program=self.ctx.program(vertex_shader='''#version 330
        uniform vec2 viewport_size; uniform vec4 rectangle;
        out vec2 uv; out vec2 pixel;
        void main(){ vec2 p=vec2((gl_VertexID==1||gl_VertexID==3)?1:0,(gl_VertexID>=2)?1:0);
        uv=p;pixel=rectangle.xy+p*rectangle.zw;gl_Position=vec4(pixel.x/viewport_size.x*2-1,1-pixel.y/viewport_size.y*2,0,1); }
        ''',fragment_shader='''#version 330
        uniform sampler2D gradient; uniform int gradient_enabled; uniform sampler2D foreground; uniform int foreground_enabled; uniform vec4 foreground_rectangle; uniform sampler2D picture; uniform sampler2D opacity; uniform usampler2D source_coordinates; uniform usampler2D mask_coordinates; uniform int mask_mode; uniform int source_alpha; uniform vec4 mask_rectangle; uniform int nearest_picture; uniform vec4 rectangle; uniform vec2 viewport_size;
        in vec2 uv; in vec2 pixel; out vec4 color;
        void main(){ vec4 p;
        if(nearest_picture==1){ivec2 d=ivec2(gl_FragCoord.x,viewport_size.y-gl_FragCoord.y)-ivec2(rectangle.xy);ivec2 index=ivec2(texelFetch(source_coordinates,ivec2(d.x,0),0).r,texelFetch(source_coordinates,ivec2(d.y,1),0).r);p=texelFetch(picture,index,0);}
        else p=texture(picture,uv); float a=source_alpha==1?p.a:1.0;
        if(gradient_enabled==1){float level=dot(p.rgb,vec3(0.299,0.587,0.114));p.rgb=texture(gradient,vec2((level*255.0+0.5)/256.0,0.5)).rgb;}
        if(mask_mode>0){ivec2 d=ivec2(gl_FragCoord.x,viewport_size.y-gl_FragCoord.y)-ivec2(mask_rectangle.xy);d=clamp(d,ivec2(0),ivec2(mask_rectangle.zw)-ivec2(1));ivec2 index=ivec2(texelFetch(mask_coordinates,ivec2(d.x,0),0).r,texelFetch(mask_coordinates,ivec2(d.y,1),0).r);vec4 v=texelFetch(opacity,index,0);a*=mask_mode==2?v.a:v.r;}
        if(foreground_enabled==1){vec2 f=(pixel-foreground_rectangle.xy)/foreground_rectangle.zw;vec4 e=texture(foreground,f);p.rgb=clamp(p.rgb*(e.a*255.0/16.0)+e.rgb,0.0,1.0);}
        if(foreground_enabled==2){vec2 f=(pixel-foreground_rectangle.xy)/foreground_rectangle.zw;vec4 e=texture(foreground,f);float eva=e.r*255.0/16.0;float evb=e.g*255.0/16.0;color=vec4(p.rgb*eva*a,a*(1.0-evb));return;} color=vec4(p.rgb,a); }
        ''')
        self.vao=self.ctx.vertex_array(self.program,[]);self.program['foreground']=4;self.program['gradient']=5;self.program['picture']=0;self.program['opacity']=1;self.program['source_coordinates']=2;self.program['mask_coordinates']=3
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
        while len(self.textures)>512:self.textures.popitem(last=False)[1][1].release()
        return tex

    def coordinate_map(self,size,width,height):
        key=(size,width,height);mapping=self.coordinate_maps.pop(key,None)
        if mapping is None:
            # Use Pillow's exact nearest-neighbor tie rule for both pictures
            # and masks. Normalized GL coordinates can choose a different
            # boundary pixel from Pillow at fractional DS enlargement ratios.
            values=np.zeros((2,max(width,height)),dtype='uint16')
            values[0,:width]=np.asarray(Image.fromarray(np.arange(size[0],dtype='int32')[None,:]).resize((width,1),Image.Resampling.NEAREST))[0]
            values[1,:height]=np.asarray(Image.fromarray(np.arange(size[1],dtype='int32')[:,None]).resize((1,height),Image.Resampling.NEAREST))[:,0]
            mapping=self.ctx.texture((values.shape[1],2),1,values.tobytes(),dtype='u2',alignment=1)
        self.coordinate_maps[key]=mapping
        while len(self.coordinate_maps)>192:self.coordinate_maps.popitem(last=False)[1].release()
        return mapping

    def present(self,top,bottom,layout):
        """Draw both screens into the window and swap. No pixel leaves the GPU."""
        gl=self.gl;window=self.window;size=window.fit()
        if size is None:return False
        if getattr(self,'blit',None) is None:
            self.blit=self.ctx.program(vertex_shader="""#version 330
            out vec2 uv; void main(){ vec2 p=vec2((gl_VertexID==1||gl_VertexID==3)?1:0,(gl_VertexID>=2)?1:0);uv=p;gl_Position=vec4(p*2-1,0,1); }""",
            fragment_shader="""#version 330
            uniform sampler2D picture; in vec2 uv; out vec4 color; void main(){ color=vec4(texture(picture,uv).rgb,1.0); }""")
            self.blit_vao=self.ctx.vertex_array(self.blit,[]);self.blit['picture']=0;self.present_targets=[None,None];self.present_sources=[None,None]
        for index,surface in enumerate((top,bottom)):
            if surface is None or surface is self.present_sources[index]:continue
            target=self.present_targets[index]
            if target is None or target.size!=surface.size:
                if target is not None:target.color_attachments[0].release();target.release()
                texture=self.ctx.texture(surface.size,4);texture.filter=(gl.LINEAR,gl.LINEAR);texture.repeat_x=False;texture.repeat_y=False
                target=self.present_targets[index]=self.ctx.framebuffer([texture])
            self.render(surface,components=4,draw_only=True,target=target);self.present_sources[index]=surface
        # The layout is expressed in the UI's pixels; this window may be
        # scaled differently, so place the screens proportionally.
        width,height=size;sx=width/max(1,layout['size'][0]);sy=height/max(1,layout['size'][1])
        screen=self.ctx.screen;screen.use();self.ctx.scissor=None;self.ctx.viewport=(0,0,width,height)
        screen.clear(*[v/255 for v in layout.get('background',(16,21,31))],1)
        self.ctx.disable(gl.BLEND)
        try:
            for index,rect in enumerate(layout['rects']):
                target=self.present_targets[index]
                if rect is None or target is None:continue
                x,y,w,h=rect;self.ctx.viewport=(round(x*sx),height-round((y+h)*sy),max(1,round(w*sx)),max(1,round(h*sy)))
                target.color_attachments[0].use(0);self.blit_vao.render(gl.TRIANGLE_STRIP,vertices=4)
        finally:self.ctx.enable(gl.BLEND)
        window.swap();window.show();return True

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

    def render(self,surface,components=3,pipeline_tag=None,draw_only=False,target=None):
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
        width,height=surface.size
        if target is not None:frame=target
        else:
            frame_key=(surface.size,components);frame=self.frames.pop(frame_key,None)
            if frame is None:frame=self.ctx.simple_framebuffer(surface.size,components=components)
            self.frames[frame_key]=frame
            while len(self.frames)>3:self.frames.popitem(last=False)[1].release()
        frame.use();self.ctx.viewport=(0,0,width,height);self.ctx.scissor=None
        frame.clear(0,0,0,1)
        # Most draws repeat the previous draw's settings; send only what changed.
        sent=self.__dict__.setdefault('uniforms_sent',{});program=self.program
        def uniform(name,value):
            if sent.get(name)!=value:program[name]=value;sent[name]=value
        uniform('viewport_size',(width,height))
        for op in surface.ops:
            clip=intersect(op['clip'],(0,0,width,height))
            if clip is None:continue
            left,top,right,bottom=op['rect']
            if right<=left or bottom<=top:continue
            l,t,r,b=clip;self.ctx.scissor=(round(l),height-round(b),round(r)-round(l),round(b)-round(t))
            uniform('rectangle',(left,top,right-left,bottom-top))
            uniform('nearest_picture',int(op['nearest']))
            picture=self.texture(op['image'],op['nearest'])
            picture_coordinates=self.coordinate_map(op['image'].size,round(right-left),round(bottom-top)) if op['nearest'] else None
            mask=op['mask'];mode=0
            opacity=None;mask_coordinates=None
            if mask is not None:
                opacity=self.texture(mask,True);mode=2 if mask.mode=='RGBA' else 1
                ml,mt,mr,mb=op['mask_rect'];uniform('mask_rectangle',(ml,mt,mr-ml,mb-mt))
                mask_coordinates=self.coordinate_map(mask.size,round(mr-ml),round(mb-mt))
            # Resource creation/upload can alter texture-unit bindings. Bind
            # all four samplers only after every resource for this draw exists.
            effect=op.get('foreground');effect_texture=None
            if effect is not None:
                effect_texture=self.texture(effect,True)
                fl,ft,fr,fb=op['foreground_rect'];uniform('foreground_rectangle',(fl,ft,fr-fl,fb-ft))
            table=op.get('gradient');table_texture=self.texture(table,False) if table is not None else None
            picture.use(0)
            if table_texture is not None:table_texture.use(5)
            uniform('gradient_enabled',int(table is not None))
            if effect_texture is not None:effect_texture.use(4)
            mode_self=effect is not None and op.get('foreground_mode')==2
            uniform('foreground_enabled',(2 if mode_self else 1) if effect is not None else 0)
            # picture*EVA + behind*EVB needs premultiplied blending: out = src + dst*(1-alpha)
            if mode_self!=getattr(self,'premultiplied',False):
                self.premultiplied=mode_self;self.ctx.blend_func=(self.gl.ONE,self.gl.ONE_MINUS_SRC_ALPHA,self.gl.ONE,self.gl.ONE_MINUS_SRC_ALPHA) if mode_self else (self.gl.SRC_ALPHA,self.gl.ONE_MINUS_SRC_ALPHA,self.gl.ONE,self.gl.ONE_MINUS_SRC_ALPHA)
            if opacity is not None:opacity.use(1)
            if picture_coordinates is not None:picture_coordinates.use(2)
            if mask_coordinates is not None:mask_coordinates.use(3)
            uniform('mask_mode',mode);uniform('source_alpha',int(op['alpha']))
            self.vao.render(self.gl.TRIANGLE_STRIP,vertices=4)
        self.ctx.scissor=None
        if getattr(self,'premultiplied',False):self.premultiplied=False;self.ctx.blend_func=(self.gl.SRC_ALPHA,self.gl.ONE_MINUS_SRC_ALPHA,self.gl.ONE,self.gl.ONE_MINUS_SRC_ALPHA)
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

    def draw(self,image,rect,mask=None,nearest=False,clip=None,mask_rect=None,alpha=False,foreground=None,foreground_rect=None,foreground_mode=1,gradient=None):
        self.pixels=None
        self.ops.append(dict(gradient=gradient,image=image,rect=rect,mask=mask,mask_rect=mask_rect or rect,nearest=nearest,clip=clip or (0,0,*self.size),alpha=alpha,foreground=foreground,foreground_rect=foreground_rect or rect,foreground_mode=foreground_mode))

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
                if op.get('foreground') is not None:
                    l,t,r,b=op['foreground_rect'];op['foreground_rect']=(l+x,t+y,r+x,b+y)
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
            l,t,r,b=op['mask_rect'];op['mask_rect']=(l-left,t-top,r-left,b-top)
            if op.get('foreground') is not None:
                l,t,r,b=op['foreground_rect'];op['foreground_rect']=(l-left,t-top,r-left,b-top)
            result.ops.append(op)
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
