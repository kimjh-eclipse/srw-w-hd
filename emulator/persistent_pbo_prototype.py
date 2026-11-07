"""Independent GL 4.4 persistent readback prototype; production is untouched."""
import ctypes as C
import inspect,textwrap,time
import numpy as np

class GLFunctions:
    def __init__(self):
        self.module=C.WinDLL('opengl32');self.module.wglGetProcAddress.argtypes=[C.c_char_p];self.module.wglGetProcAddress.restype=C.c_void_p
        def load(name,result,*args):
            address=self.module.wglGetProcAddress(name.encode('ascii'))
            if address in (None,0,1,2,3,C.c_void_p(-1).value):
                fn=getattr(self.module,name);fn.restype=result;fn.argtypes=list(args);return fn
            return C.WINFUNCTYPE(result,*args)(address)
        u=C.c_uint;i=C.c_int;p=C.c_void_p;s=C.c_ssize_t
        self.gen=load('glGenBuffers',None,i,C.POINTER(u));self.delete=load('glDeleteBuffers',None,i,C.POINTER(u))
        self.bind=load('glBindBuffer',None,u,u);self.storage=load('glBufferStorage',None,u,s,p,u)
        self.map=load('glMapBufferRange',p,u,s,s,u);self.unmap=load('glUnmapBuffer',C.c_ubyte,u)
        self.read=load('glReadPixels',None,i,i,i,i,u,u,p)
        self.fence=load('glFenceSync',p,u,u);self.wait=load('glClientWaitSync',u,p,u,C.c_uint64);self.delete_sync=load('glDeleteSync',None,p)
        self.flush=load('glFlush',None);self.error=load('glGetError',u)

class PersistentPBO:
    TARGET=0x88EB
    FLAGS=0x1|0x40|0x80 # READ | PERSISTENT | COHERENT
    def __init__(self):
        self.gl=GLFunctions();self.size=None;self.ids=[];self.maps=[];self.fences=[];self.pending=None;self.slot=0
        self.metrics=[]
    def reset(self):
        gl=self.gl
        for fence in self.fences:
            if fence:gl.wait(fence,1,1_000_000_000);gl.delete_sync(fence)
        for buffer in self.ids:gl.bind(self.TARGET,buffer);gl.unmap(self.TARGET)
        gl.bind(self.TARGET,0)
        if self.ids:gl.delete(len(self.ids),(C.c_uint*len(self.ids))(*self.ids))
        self.ids=[];self.maps=[];self.fences=[];self.pending=None;self.size=None;self.slot=0
    def ensure(self,size):
        if self.size==size:return
        self.reset();self.size=tuple(size);length=size[0]*size[1]*4;ids=(C.c_uint*2)();self.gl.gen(2,ids)
        self.ids=list(ids)
        for buffer in self.ids:
            self.gl.bind(self.TARGET,buffer);self.gl.storage(self.TARGET,length,None,self.FLAGS)
            pointer=self.gl.map(self.TARGET,0,length,self.FLAGS)
            if not pointer:raise RuntimeError('Persistent mapping failed; GL error '+hex(self.gl.error()))
            self.maps.append(np.ctypeslib.as_array((C.c_ubyte*length).from_address(pointer)))
        self.gl.bind(self.TARGET,0);self.fences=[None,None]
    def consume(self,entry):
        slot,tag=entry;start=time.perf_counter()
        status=self.gl.wait(self.fences[slot],1,1_000_000_000)
        waited=time.perf_counter()
        if status not in (0x911A,0x911C):raise RuntimeError('GPU fence wait failed '+hex(status))
        w,h=self.size;pixels=self.maps[slot].reshape(h,w,4)[::-1].copy()
        end=time.perf_counter();self.metrics.append(dict(wait_ms=(waited-start)*1000,copy_ms=(end-waited)*1000))
        return pixels,tag
    def read(self,size,tag,draw):
        self.ensure(size)
        # Consume previous completion before submitting current drawing.
        previous=self.consume(self.pending) if self.pending is not None else None
        slot=self.slot;self.slot=1-slot
        if self.fences[slot]:self.gl.delete_sync(self.fences[slot]);self.fences[slot]=None
        draw()
        self.gl.bind(self.TARGET,self.ids[slot]);self.gl.read(0,0,*size,0x1908,0x1401,None)
        self.fences[slot]=self.gl.fence(0x9117,0);self.gl.bind(self.TARGET,0);self.gl.flush()
        self.pending=(slot,tag)
        return previous if previous is not None else self.consume(self.pending)
    close=reset

def production_draw_only(backend):
    """Reuse exactly the current production draw commands without its readback.

    Extracting an independent function avoids altering any live class or file.
    """
    import gpu_surface
    source=inspect.getsource(type(backend).render)
    start=source.index('        for key,(reference,texture)')
    stop=source.index('        self.ctx.scissor=None\n',start)+len('        self.ctx.scissor=None\n')
    body=source[start:stop]
    code='def draw_only(self,surface,components=4):\n'+textwrap.indent(textwrap.dedent(body),'    ')+'    return frame\n'
    namespace=dict(vars(gpu_surface));exec(compile(code,'<independent production draw-only>','exec'),namespace)
    return lambda surface:namespace['draw_only'](backend,surface,4)
