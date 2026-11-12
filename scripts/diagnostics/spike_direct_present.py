"""Feasibility check: a second process draws with OpenGL straight into a Tk canvas.

The player composes in one process and displays in another, so every frame is
read back from the GPU and uploaded again. This verifies, on the current
machine, that the composing process can instead own a child window of the UI
canvas and present there with the same GL context it composes in.
"""
import ctypes as C,json,multiprocessing as mp,sys,time
from ctypes import wintypes as W
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/gpu_py'))

class PFD(C.Structure):
    _fields_=[('nSize',W.WORD),('nVersion',W.WORD),('dwFlags',W.DWORD),('iPixelType',C.c_byte),('cColorBits',C.c_byte),('pad',C.c_byte*13),('cDepthBits',C.c_byte),('cStencilBits',C.c_byte),('cAuxBuffers',C.c_byte),('iLayerType',C.c_byte),('bReserved',C.c_byte),('dwLayerMask',W.DWORD),('dwVisibleMask',W.DWORD),('dwDamageMask',W.DWORD)]

def child_window(parent,size):
    user=C.WinDLL('user32',use_last_error=True);gdi=C.WinDLL('gdi32',use_last_error=True);gl=C.WinDLL('opengl32',use_last_error=True)
    user.CreateWindowExW.restype=W.HWND;user.CreateWindowExW.argtypes=[W.DWORD,W.LPCWSTR,W.LPCWSTR,W.DWORD,C.c_int,C.c_int,C.c_int,C.c_int,W.HWND,W.HMENU,W.HINSTANCE,W.LPVOID]
    user.GetDC.restype=W.HDC;user.GetDC.argtypes=[W.HWND];gl.wglCreateContext.restype=W.HANDLE;gl.wglCreateContext.argtypes=[W.HDC];gl.wglMakeCurrent.argtypes=[W.HDC,W.HANDLE]
    gdi.ChoosePixelFormat.argtypes=[W.HDC,C.POINTER(PFD)];gdi.SetPixelFormat.argtypes=[W.HDC,C.c_int,C.POINTER(PFD)];gdi.SwapBuffers.argtypes=[W.HDC]
    # WS_CHILD|WS_VISIBLE|WS_DISABLED: a disabled child lets clicks reach the Tk canvas.
    hwnd=user.CreateWindowExW(0,'STATIC','',0x40000000|0x10000000|0x08000000,0,0,size[0],size[1],parent,None,None,None)
    if not hwnd:raise OSError(C.get_last_error(),'CreateWindowEx')
    dc=user.GetDC(hwnd);pfd=PFD();pfd.nSize=C.sizeof(PFD);pfd.nVersion=1;pfd.dwFlags=0x4|0x20|0x1;pfd.cColorBits=32
    fmt=gdi.ChoosePixelFormat(dc,C.byref(pfd))
    if not fmt or not gdi.SetPixelFormat(dc,fmt,C.byref(pfd)):raise OSError(C.get_last_error(),'pixel format')
    ctx=gl.wglCreateContext(dc)
    if not ctx or not gl.wglMakeCurrent(dc,ctx):raise OSError(C.get_last_error(),'wgl context')
    return user,gdi,hwnd,dc

def pump(user):
    msg=W.MSG()
    while user.PeekMessageW(C.byref(msg),None,0,0,1):user.TranslateMessage(C.byref(msg));user.DispatchMessageW(C.byref(msg))

def presenter(parent,size,frames,reply):
    try:
        import moderngl,numpy as np
        user,gdi,hwnd,dc=child_window(parent,size);ctx=moderngl.create_context()
        info=dict(renderer=ctx.info['GL_RENDERER'],version=ctx.info['GL_VERSION'])
        # Disable vsync if the driver offers it; pacing belongs to the emulator.
        gl=C.WinDLL('opengl32');gl.wglGetProcAddress.restype=C.c_void_p;gl.wglGetProcAddress.argtypes=[C.c_char_p]
        address=gl.wglGetProcAddress(b'wglSwapIntervalEXT')
        if address:C.WINFUNCTYPE(C.c_int,C.c_int)(address)(0)
        program=ctx.program(vertex_shader='#version 330\nout vec2 uv;void main(){vec2 p=vec2((gl_VertexID==1||gl_VertexID==3)?1:0,(gl_VertexID>=2)?1:0);uv=p;gl_Position=vec4(p*2-1,0,1);}',
            fragment_shader='#version 330\nuniform sampler2D picture;uniform float shift;in vec2 uv;out vec4 color;void main(){color=texture(picture,vec2(uv.x+shift,1-uv.y));}')
        vao=ctx.vertex_array(program,[])
        offscreen=ctx.simple_framebuffer((960,720),components=4);pattern=np.zeros((720,960,4),dtype='uint8');pattern[:,:,0]=np.arange(960)[None,:]//4;pattern[:,:,1]=np.arange(720)[:,None]//3;pattern[::40,:,:3]=255;pattern[:,::40,:3]=255;pattern[:,:,3]=255
        source=ctx.texture((960,720),4,pattern.tobytes());source.repeat_x=True;composed=ctx.texture((960,720),4);target=ctx.framebuffer([composed]);times=[]
        for n in range(frames):
            start=time.perf_counter()
            target.use();ctx.viewport=(0,0,960,720);source.use(0);program['shift']=n/240;vao.render(moderngl.TRIANGLE_STRIP,vertices=4)   # stands in for composition
            ctx.screen.use();ctx.viewport=(0,0,*size);composed.use(0);program['shift']=0;vao.render(moderngl.TRIANGLE_STRIP,vertices=4)      # present, no readback
            gdi.SwapBuffers(dc);times.append((time.perf_counter()-start)*1000);pump(user)
            wait=1/60-(time.perf_counter()-start)
            if wait>0:time.sleep(wait)
        times.sort();info.update(frames=frames,present_ms_median=round(times[len(times)//2],3),present_ms_p95=round(times[int(len(times)*.95)],3),present_ms_max=round(times[-1],3))
        reply.send(info)
    except Exception as error:
        import traceback;reply.send(dict(error=repr(error),trace=traceback.format_exc()))

def main():
    import tkinter as tk
    root=tk.Tk();root.title('direct present check');root.geometry('800x640+80+80')
    canvas=tk.Canvas(root,width=800,height=600,bg='#10151f',highlightthickness=0);canvas.pack();label=tk.Label(root,text='clicks on canvas: 0');label.pack()
    clicks=[0]
    def clicked(event):clicks[0]+=1;label.config(text=f'clicks on canvas: {clicks[0]}')
    canvas.bind('<Button-1>',clicked);root.update()
    ctx=mp.get_context('spawn');receive,send=ctx.Pipe(duplex=False)
    process=ctx.Process(target=presenter,args=(canvas.winfo_id(),(800,600),300,send));process.start();send.close()
    result={};shot=[None];started=time.perf_counter()
    def poll():
        if receive.poll():
            result.update(receive.recv());root.after(200,root.destroy);return
        if shot[0] is None and time.perf_counter()-started>2.5:
            # Read the screen where the canvas is: proves the picture is visible to the user.
            from PIL import ImageGrab
            x,y=canvas.winfo_rootx(),canvas.winfo_rooty();shot[0]=ImageGrab.grab((x,y,x+800,y+600))
            # A synthetic click at the canvas centre must still reach Tk.
            user=C.windll.user32;user.SetCursorPos(x+400,y+300);user.mouse_event(2,0,0,0,0);user.mouse_event(4,0,0,0,0)
        if not process.is_alive() and not receive.poll():result.setdefault('error','presenter exited without a result');root.after(100,root.destroy);return
        root.after(15,poll)
    ui_frames=[0];
    def tick():ui_frames[0]+=1;root.after(5,tick)
    tick();poll();root.mainloop();process.join(timeout=5)
    out=ROOT/'test_current/performance/direct_present'
    if shot[0] is not None:
        shot[0].save(out/'screen.png');import numpy as np;pixels=np.asarray(shot[0]);result['screen_has_picture']=bool(pixels.std()>20);result['screen_mean_rgb']=[round(float(v),1) for v in pixels.reshape(-1,3).mean(0)]
    result['tk_clicks_received']=clicks[0];result['ui_ticks_while_presenting']=ui_frames[0]
    (out/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':main()
