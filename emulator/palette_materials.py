"""Disambiguate equal source colors using the original texture's material IDs."""
import base64,zlib
import numpy as np
from PIL import Image,ImageFilter

def material_indices(encoded,w,h,size,fallback,source_palette,strict=False):
    native=np.frombuffer(zlib.decompress(base64.b64decode(encoded)),dtype='uint8').reshape(h,w) if isinstance(encoded,str) else np.asarray(encoded,dtype='uint8').reshape(h,w)
    image=Image.fromarray(native);grown=np.asarray(image.filter(ImageFilter.MaxFilter(3)))
    native=np.where(native!=0,native,grown).astype('uint8')
    indices=np.asarray(Image.fromarray(native).resize(size,Image.Resampling.NEAREST))
    if strict:return np.where(indices>0,indices,fallback)
    palette=np.asarray(source_palette,dtype='float32')
    counts=np.array([np.count_nonzero(np.all(palette==color,axis=1)) for color in palette])
    ambiguous=(counts[fallback]>1)&(indices>0)&np.all(palette[indices]==palette[fallback],axis=2)
    return np.where(ambiguous,indices,fallback)


def anchored_indices(native,rgb,source_palette,fallback,reach=1):
    """Palette slot of every HD pixel, chosen among the slots native texels have nearby.

    A painted pixel may only take a slot that some native texel within
    `reach` texels of it uses, and among those it takes the one whose source
    colour is nearest to the paint. A highlight painted on a red fin can
    then follow the fin's red or white, never the green of an eye elsewhere
    on the part, whatever palette the part is later shown with. Painted
    contours stay free to sit up to `reach` texels from the native ones, so
    the native staircase is not stamped onto the picture. Pixels with no
    native texel nearby keep `fallback`.
    """
    native=np.asarray(native,dtype='uint8');palette=np.asarray(source_palette,dtype='float32');count=len(palette)
    bits=(np.uint32(1)<<np.minimum(native,count-1).astype('uint32'));padded=np.pad(bits,reach);around=np.zeros_like(bits);size=2*reach+1
    for dy in range(size):
        for dx in range(size):around|=padded[dy:dy+native.shape[0],dx:dx+native.shape[1]]
    shape=(rgb.shape[1],rgb.shape[0]);enlarge=lambda array:np.asarray(Image.fromarray(array.astype('int32')).resize(shape,Image.Resampling.NEAREST))
    allowed=enlarge(around).astype('uint32')&~np.uint32(1);inside=allowed!=0
    distance=((rgb[:,:,None,:]-palette[None,None,:,:])**2).sum(-1)
    distance[((allowed[:,:,None]>>np.arange(count,dtype='uint32'))&1)==0]=np.inf
    best=distance.argmin(2).astype(fallback.dtype)
    # Slots of equal source colour cannot be told apart by paint: keep the texel's own.
    centre=enlarge(native).astype(fallback.dtype);same=(centre>0)&inside&np.all(palette[np.minimum(centre,count-1)]==palette[best],axis=2)
    best=np.where(same,centre,best)
    return np.where(inside,best,fallback)

