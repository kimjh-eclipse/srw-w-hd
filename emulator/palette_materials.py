"""Disambiguate equal source colors using the original texture's material IDs."""
import base64,zlib
import numpy as np
from PIL import Image,ImageFilter

def material_indices(encoded,w,h,size,fallback,source_palette):
    native=np.frombuffer(zlib.decompress(base64.b64decode(encoded)),dtype='uint8').reshape(h,w)
    image=Image.fromarray(native);grown=np.asarray(image.filter(ImageFilter.MaxFilter(3)))
    native=np.where(native!=0,native,grown).astype('uint8')
    indices=np.asarray(Image.fromarray(native).resize(size,Image.Resampling.NEAREST))
    palette=np.asarray(source_palette,dtype='float32')
    counts=np.array([np.count_nonzero(np.all(palette==color,axis=1)) for color in palette])
    ambiguous=(counts[fallback]>1)&(indices>0)&np.all(palette[indices]==palette[fallback],axis=2)
    return np.where(ambiguous,indices,fallback)
