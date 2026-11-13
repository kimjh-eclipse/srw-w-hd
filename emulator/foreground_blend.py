"""Blend native raster BG first-target colors into painted OBJ pixels."""
import numpy as np
from PIL import Image


class _Frame:pass
_frame=None
ENERGY_TIES=True


def begin_frame(packed,priorities):
    """Unpack this frame's records once; every part and cut-in reuses them.

    The 64-bit records are split into small per-field arrays here, so the
    per-part test works on bytes of a small region instead of re-deriving
    each field from the whole 64-bit screen.
    """
    global _frame
    _frame=None
    if packed is None or not SHORTCUTS:return
    f=_Frame();f.packed=packed;f.priorities=priorities
    lo=packed.astype('uint32');hi=(packed>>32).astype('uint32');table=np.asarray(priorities)
    # The 3-bit fields index small tables directly (same values as clipping first).
    field=((lo>>15)&7).astype('uint8');f.layer=field.astype('int8')-1;f.front_priority=table[[0,0,1,2,3,4,5,5]][field]
    f.destination=((hi>>5)&7).astype('uint8');f.destination_priority=table[[0,1,2,3,4,5,5,5]][f.destination];f.memo={}
    f.additive=(((lo>>18)&31)>0)&(((lo>>23)&31)==16);f.targets=(hi&255).astype('uint8');f.inside=(f.layer>=0)&(f.layer<4);f.lo=lo;f.colour=None
    _frame=f


def _fast(f,box,layers,priority,target):
    s=(slice(None),slice(None)) if box is None else (slice(box[1],box[3]),slice(box[0],box[2]))
    layer=f.layer[s];front_priority=f.front_priority[s];destination=f.destination[s];destination_priority=f.destination_priority[s]
    front=(front_priority<priority)|((front_priority==priority)&(layer<target)&(target<4))
    # Energy presentation: additive beam BGs must cover painted unit pixels
    # even on an OBJ/BG priority tie. Keep opaque scenery and BG cut-ins on
    # the hardware tie rule. The caller still checks surviving OBJ ownership.
    energy=ENERGY_TIES&(target==4)&f.additive[s]&(front_priority==priority)
    front|=energy
    behind=(destination<4)&((destination_priority>priority)|((destination_priority==priority)&((target==4)|(destination>target))))
    adjacent=(destination==target)|(destination==5)|behind
    return f.inside[s]&((layers==layer)|(energy&(layers==4)))&((f.targets[s]&(1<<target))!=0)&front&adjacent


def eligibility_box(packed,box,layers,priorities,priority,target=4):
    """eligibility() for the native rectangle box=(left,upper,right,lower); layers is already cropped."""
    f=_frame
    if f is not None and f.packed is packed and f.priorities is priorities and 0<=target<8:return _fast(f,box,layers,priority,target)
    return eligibility(packed[box[1]:box[3],box[0]:box[2]],layers,priorities,priority,target)


def _whole(f,layers,priority,target):
    # Many parts share one priority: test the whole screen once, crop per part.
    key=(priority,target,id(layers));found=f.memo.get(key)
    if found is None or found[0] is not layers:found=f.memo[key]=(layers,_fast(f,None,layers,priority,target))
    return found[1]


def eligibility_region(packed,box,layers,priorities,priority,target=4):
    """eligibility() cropped to box=(left,upper,right,lower); layers is the whole screen. Read-only result."""
    f=_frame
    if f is not None and f.packed is packed and f.priorities is priorities and 0<=target<8:return _whole(f,layers,priority,target)[box[1]:box[3],box[0]:box[2]]
    return eligibility(packed[box[1]:box[3],box[0]:box[2]],layers[box[1]:box[3],box[0]:box[2]],priorities,priority,target)


def eligibility(packed,layers,priorities,priority,target=4):
    f=_frame
    if f is not None and f.packed is packed and f.priorities is priorities and 0<=target<8:return _whole(f,layers,priority,target)
    layer=((packed>>15)&7).astype('int16')-1
    front_priority=np.asarray(priorities)[np.clip(layer,0,5)]
    front=(front_priority<priority)|((front_priority==priority)&(layer<target)&(target<4))
    additive=(((packed>>18)&31)>0)&(((packed>>23)&31)==16)
    energy=ENERGY_TIES&(target==4)&additive&(front_priority==priority)
    front|=energy
    destination=((packed>>37)&7).astype('uint8')
    destination_priority=np.asarray(priorities)[np.minimum(destination,5)]
    # BLDCNT flags do not make every deeper layer a second target. An opaque
    # intervening BG/OBJ must still hide the HD picture. A skipped HD OBJ can
    # replace a lower-priority BG that was its native stand-in destination.
    behind=(destination<4)&((destination_priority>priority)|((destination_priority==priority)&((target==4)|(destination>target))))
    adjacent=(destination==target)|(destination==5)|behind
    return (layer>=0)&(layer<4)&((layers==layer)|(energy&(layers==4)))&(((packed>>32)&(1<<target))!=0)&front&adjacent


import os
SHORTCUTS=os.environ.get('SRWW_RENDER_SHORTCUTS','1')!='0'
_neutral_planes={}
# colour(5 bit) x EVA(5 bit) -> the 8-bit term added by the blend, as the arithmetic below computes it
_COLOUR=np.array([((((colour*255+15)//31)*eva)//16)&255 for eva in range(32) for colour in range(32)],dtype='uint8')
_COLOUR32=_COLOUR.astype('<u4')

def active(packed):
    """Pixels that carry any front-BG blend record at all this frame."""
    if not SHORTCUTS:return np.ones(packed.shape,dtype=bool)
    return ((packed>>15)&7)!=0


def gpu_plane(packed,layers,priorities,priority,target=4):
    valid=eligibility(packed,layers,priorities,priority,target)
    if not SHORTCUTS:
        eva=((packed>>18)&31).astype('uint16');colors=np.stack([(packed>>shift)&31 for shift in (0,5,10)],axis=-1).astype('uint16')
        pixels=np.zeros((*packed.shape,4),dtype='uint8');pixels[:,:,3]=16
        pixels[valid,:3]=((((colors*255+15)//31)*eva[:,:,None])//16)[valid].astype('uint8');pixels[valid,3]=((packed[valid]>>23)&31).astype('uint8')
        return Image.fromarray(pixels)
    if not valid.any():
        # Nothing blends over this layer: one shared "leave the colour as it
        # is" plane, so the GPU texture is uploaded once, not every frame.
        plane=_neutral_planes.get(packed.shape)
        if plane is None:
            pixels=np.zeros((*packed.shape,4),dtype='uint8');pixels[:,:,3]=16;plane=_neutral_planes[packed.shape]=Image.fromarray(pixels)
        return plane
    f=_frame
    if f is not None and f.packed is packed:
        # Unpack colour only where this plane blends, as 32-bit values.
        where=np.flatnonzero(valid);values=f.lo.ravel()[where];row=((values>>18)&31)<<5
        # One 32-bit word per pixel (R,G,B,EVB in memory order) instead of four byte writes.
        word=_COLOUR32[row|(values&31)]|(_COLOUR32[row|((values>>5)&31)]<<8)|(_COLOUR32[row|((values>>10)&31)]<<16)|(((values>>23)&31)<<24)
        pixels=np.full(valid.size,16<<24,dtype='<u4');pixels[where]=word
        return Image.fromarray(pixels.view('uint8').reshape(*packed.shape,4))
    # Only the blended pixels need their colour unpacked.
    values=packed[valid];eva=((values>>18)&31).astype('uint16')
    colors=np.stack([(values>>shift)&31 for shift in (0,5,10)],axis=-1).astype('uint16')
    pixels=np.zeros((*packed.shape,4),dtype='uint8');pixels[:,:,3]=16
    pixels[valid,:3]=((((colors*255+15)//31)*eva[:,None])//16).astype('uint8')
    pixels[valid,3]=((values>>23)&31).astype('uint8')
    return Image.fromarray(pixels)


def blend_part(art,packed,eligible,coeff):
    # Transform coefficients exactly like the native visibility mask. Keep
    # painted alpha independent of the DS color coefficients.
    def sample(values):
        return np.asarray(Image.fromarray(values).transform(art.size,Image.Transform.AFFINE,coeff,Image.Resampling.NEAREST))
    active=sample(eligible.astype('uint8'))!=0
    values=sample(packed.astype('int32')).astype('uint32')
    eva=((values>>18)&31).astype('uint16')
    evb=((values>>23)&31).astype('uint16')
    colors=np.stack([(values>>shift)&31 for shift in (0,5,10)],axis=-1).astype('uint16')
    colors=(colors*255+15)//31
    pixels=np.array(art.convert('RGBA'))
    blended=np.minimum(255,(pixels[:,:,:3].astype('uint16')*evb[:,:,None]+colors*eva[:,:,None])//16)
    pixels[active,:3]=blended[active].astype('uint8')
    return Image.fromarray(pixels)


SELF_BLEND=os.environ.get('SRWW_SELF_BLEND','1')!='0'

def self_plane(packed,layers,layer):
    """Blend coefficients of a BG that is itself the first target (a fading cut-in).

    The records hold, for each pixel the DS blended, the first-target BG and
    the EVA/EVB in force on that scanline. When that BG is the picture being
    replaced, the HD picture has to be mixed with what lies behind it by the
    same coefficients: picture*EVA/16 + behind*EVB/16. They are scanline
    values, so each row takes the coefficients of the layer's own pixels on
    that row and rows where it has none take the nearest row's, which keeps
    the smooth HD outline outside the native silhouette on the same fade.
    Returns an RGBA picture (R=EVA, G=EVB, 0..16) or None when the layer is
    opaque everywhere (EVA 16, EVB 0) or not a blended first target at all.
    """
    if not SELF_BLEND or packed is None:return None
    own=((((packed>>15)&7).astype('int16')-1)==layer)&(np.asarray(layers)==layer)
    rows=np.flatnonzero(own.any(1))
    if not len(rows):return None
    eva=np.minimum((packed>>18)&31,16).astype('uint8');evb=np.minimum((packed>>23)&31,16).astype('uint8')
    first=own.argmax(1);row_eva=eva[np.arange(len(eva)),first];row_evb=evb[np.arange(len(evb)),first]
    if np.all(row_eva[rows]==16) and np.all(row_evb[rows]==0):return None
    nearest=rows[np.abs(np.arange(packed.shape[0])[:,None]-rows[None,:]).argmin(1)]
    plane=np.zeros((*packed.shape,4),dtype='uint8');plane[:,:,0]=row_eva[nearest][:,None];plane[:,:,1]=row_evb[nearest][:,None];plane[:,:,3]=255
    return Image.fromarray(plane)

