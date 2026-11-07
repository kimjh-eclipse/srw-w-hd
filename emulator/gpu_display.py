"""SDL hardware texture presentation inside the existing Tk game canvas."""
import os
import time


class RGBFrame:
    """Keep the shared-buffer snapshot without a Pillow decode/encode roundtrip."""
    def __init__(self, pixels, size=(1440,1080)):
        self.pixels=pixels;self.size=size;self.width,self.height=size;self._image=None
        self.format='RGBA' if len(pixels)==self.width*self.height*4 else 'RGB'

    def tobytes(self):return self.pixels

    def image(self):
        if self._image is None:
            from PIL import Image
            self._image=Image.frombytes(self.format,self.size,self.pixels).convert('RGB')
        return self._image

    def resize(self,*args,**kwargs):return self.image().resize(*args,**kwargs)
    def copy(self):return self.image().copy()
    def save(self,*args,**kwargs):return self.image().save(*args,**kwargs)

    def __array__(self,dtype=None,copy=None):
        import numpy as np
        result=np.frombuffer(self.pixels,dtype='uint8').reshape(self.height,self.width,len(self.format))[:,:,:3]
        if dtype is not None:result=result.astype(dtype,copy=False)
        return result.copy() if copy else result


class GPUDisplay:
    def __init__(self, canvas):
        os.environ.setdefault('SDL_RENDER_SCALE_QUALITY', '1')
        import pygame
        from pygame._sdl2.video import Window, Renderer
        self.pygame = pygame
        self.canvas_id=canvas.winfo_id();self.forwarded_keys={};self.keyboard_events=0;self.mouse_events=0
        self.window = Window.from_window(canvas.winfo_id())
        self.renderer = Renderer(self.window, accelerated=1, vsync=False)
        self.textures = [None, None]
        self.sources = [None, None]
        self.presented = 0
        self.last_ms = 0

    def draw(self, images, rectangles):
        from pygame._sdl2.video import Texture
        start = time.perf_counter()
        self.renderer.draw_color = (16, 21, 31, 255)
        self.renderer.clear()
        for number, (image, rect) in enumerate(zip(images, rectangles)):
            if image is None or rect is None:
                continue
            if self.sources[number] is not image:
                surface = self.pygame.image.frombuffer(image.tobytes(), image.size, getattr(image,'format','RGB'))
                if self.textures[number] is None or self.sources[number] is None or self.sources[number].size!=image.size:
                    self.textures[number] = Texture(self.renderer, image.size, streaming=True)
                self.textures[number].update(surface)
                self.sources[number] = image
            self.textures[number].draw(dstrect=rect)
        self.renderer.present()
        self.presented += 1
        self.last_ms = (time.perf_counter()-start)*1000

    def clear(self):
        self.sources = [None, None]
        self.renderer.draw_color = (16, 21, 31, 255)
        self.renderer.clear()
        self.renderer.present()

    def focused(self):
        import ctypes as C
        api=C.windll.user32;api.GetForegroundWindow.restype=C.c_void_p
        api.GetAncestor.argtypes=[C.c_void_p,C.c_uint];api.GetAncestor.restype=C.c_void_p
        return api.GetForegroundWindow()==api.GetAncestor(self.canvas_id,2)

    def events(self,app):
        """Poll the foreign canvas without converting unsafe SDL window events."""
        import ctypes as C
        from types import SimpleNamespace
        if not hasattr(self,'pointer_api'):
            from ctypes import wintypes
            self.pointer_api=C.windll.user32;self.pointer_point=wintypes.POINT()
            self.pointer_api.GetCursorPos.argtypes=[C.POINTER(wintypes.POINT)]
            self.pointer_api.ScreenToClient.argtypes=[C.c_void_p,C.POINTER(wintypes.POINT)]
            self.pointer_down=False;self.pointer_tracking=False;self.pointer_last=None;self.pointer_click=None
        api=self.pointer_api;pressed=bool(api.GetAsyncKeyState(1)&0x8000)
        if app.dialog or not app.loaded or not self.focused():
            if self.pointer_tracking:app.mouse_up(None)
            self.pointer_down=pressed;self.pointer_tracking=False;return
        point=self.pointer_point;api.GetCursorPos(C.byref(point));api.ScreenToClient(self.canvas_id,C.byref(point));x,y=point.x,point.y
        inside=0<=x<app.canvas.winfo_width() and 0<=y<app.canvas.winfo_height();now=time.perf_counter()
        kind='down' if pressed else 'up';seen=getattr(app,'tk_pointer_seen',None)
        duplicate=bool(seen and seen[:3]==(kind,x,y) and now-seen[3]<.04)
        item=SimpleNamespace(x=x,y=y)
        if pressed and not self.pointer_down and inside:
            self.pointer_tracking=True;self.mouse_events+=1
            if not duplicate:
                previous=self.pointer_click
                double=previous is not None and now-previous[0]<=api.GetDoubleClickTime()/1000 and abs(x-previous[1])<=5 and abs(y-previous[2])<=5
                if double:app.double_click(item);self.pointer_click=None
                else:app.mouse_down(item);self.pointer_click=(now,x,y)
        elif not pressed and self.pointer_down and self.pointer_tracking:
            if not duplicate:app.mouse_up(item)
            self.pointer_tracking=False
        elif pressed and self.pointer_tracking and self.pointer_last!=(x,y):app.mouse_drag(item)
        self.pointer_down=pressed;self.pointer_last=(x,y)
