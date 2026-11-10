"""Preserve painted contours while respecting actual foreground occluders."""
import numpy as np
from PIL import Image,ImageFilter

def clean_alpha(image):
    image=image.copy()
    # Remove isolated one-pixel matte debris without imposing a DS silhouette.
    alpha=image.getchannel('A')
    image.putalpha(alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3)))
    return image


def remove_unattached_paint(image,native):
    """Drop neighboring atlas strokes accidentally entering an OBJ crop.

    The original alpha only seeds connected painted components. It never
    clips a connected HD contour back to the native pixel staircase.
    """
    w,h=native.size;size=(w*2,h*2)
    painted=np.asarray(image.getchannel('A').resize(size,Image.Resampling.BOX))>32
    expected=np.asarray(native.getchannel('A').resize(size,Image.Resampling.NEAREST))>0
    visited=np.zeros_like(painted);unattached=np.zeros_like(painted);count=0
    for y,x in np.argwhere(painted):
        if visited[y,x]:continue
        pending=[(int(y),int(x))];visited[y,x]=True;points=[];supported=False
        while pending:
            yy,xx=pending.pop();points.append((yy,xx));supported|=bool(expected[yy,xx])
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    y2,x2=yy+dy,xx+dx
                    if 0<=y2<size[1] and 0<=x2<size[0] and painted[y2,x2] and not visited[y2,x2]:
                        visited[y2,x2]=True;pending.append((y2,x2))
        if not supported:
            yy,xx=zip(*points);unattached[yy,xx]=True;count+=1
    if not count:return image,0
    # Erase the detached stroke's antialiased rim too. Connected contours
    # remain unchanged; only unsupported, disconnected islands are removed.
    mask=Image.fromarray(unattached.astype('uint8')*255).resize(image.size,Image.Resampling.NEAREST).filter(ImageFilter.MaxFilter(3))
    pixels=np.array(image);pixels[np.asarray(mask)>0]=0
    return Image.fromarray(pixels),count

def cutin_visibility(layers,layer,priority,bgpriorities,owners=None,oam=None):
    layers=np.asarray(layers,dtype='uint8')
    priorities=np.asarray(bgpriorities)[np.minimum(layers,5)]
    blocked=(layers<4)&((priorities<priority)|((priorities==priority)&(layers<layer)))
    if owners is not None and oam is not None:
        attrs=np.frombuffer(oam,dtype='<u2').reshape(128,4)
        objprio=((attrs[:,2]>>10)&3)[np.asarray(owners)]
        blocked|=(layers==4)&(objprio<=priority)
    # Background pixels outside the old sprite are not occlusion. The HD
    # texture supplies its own smooth silhouette, even beyond the DS staircase.
    return Image.fromarray((~blocked).astype('uint8')*255)
