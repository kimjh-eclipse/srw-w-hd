"""Preserve painted contours while respecting actual foreground occluders."""
import numpy as np
from PIL import Image,ImageFilter

def clean_alpha(image):
    image=image.copy()
    # Remove isolated one-pixel matte debris without imposing a DS silhouette.
    alpha=image.getchannel('A')
    image.putalpha(alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3)))
    return image

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
