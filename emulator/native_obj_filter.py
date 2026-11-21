"""Pixel-art upscaling of the native OBJ layer (opt-in, SRWW_NATIVE_OBJ_FILTER=xbrz).

The native top screen is still placed with nearest scaling and the HD BG
renderers still paint over BG pixels. This adds one plane on top of that,
before cut-ins and HD OBJ parts: the frame scaled with xBRZ 4x, shown only
inside the native OBJ silhouette. The silhouette itself is the xBRZ-scaled
OBJ coverage (smooth outline), united with the nearest OBJ mask so no native
stair step survives underneath.
"""
from pathlib import Path
import ctypes
import numpy as np
from PIL import Image

OBJ_LAYER = 4
_DLL = None


def _xbrz4(argb):
    global _DLL
    if _DLL is None:
        _DLL = ctypes.CDLL(str(Path(__file__).resolve().parent.parent / 'tools/xbrz_compare.dll'))
        ptr = ctypes.POINTER(ctypes.c_uint32)
        _DLL.srww_xbrz4_argb.argtypes = [ptr, ptr, ctypes.c_int, ctypes.c_int]
        _DLL.srww_xbrz4_argb.restype = None
    h, w = argb.shape
    src = np.ascontiguousarray(argb, dtype=np.uint32)
    dst = np.empty((h * 4, w * 4), dtype=np.uint32)
    ptr = ctypes.POINTER(ctypes.c_uint32)
    _DLL.srww_xbrz4_argb(src.ctypes.data_as(ptr), dst.ctypes.data_as(ptr), w, h)
    return dst


def _pack(rgb, alpha):
    rgb = rgb.astype(np.uint32)
    return (alpha.astype(np.uint32) << 24) | (rgb[:, :, 0] << 16) | (rgb[:, :, 1] << 8) | rgb[:, :, 2]


def obj_overlay(display_native, layer_ids, size, exclude=None):
    """Return (rgb_image, mask_image, box) for the filtered OBJ plane, or None."""
    rgb = np.ascontiguousarray(display_native[:192, :, :3])
    obj = np.asarray(layer_ids[:192]) == OBJ_LAYER
    if exclude is not None:
        obj &= ~np.asarray(exclude[:192], dtype=bool)
    if not obj.any():
        return None
    ys, xs = np.nonzero(obj)
    # One native pixel of margin: xBRZ may round the outline outward.
    left, top = max(int(xs.min()) - 1, 0), max(int(ys.min()) - 1, 0)
    right, bottom = min(int(xs.max()) + 2, 256), min(int(ys.max()) + 2, 192)
    full = _xbrz4(_pack(rgb, np.full(obj.shape, 255, np.uint8)))
    cover = _xbrz4(_pack(np.where(obj[:, :, None], rgb, 0), obj.astype(np.uint8) * 255))
    colour = np.stack(((full >> 16) & 255, (full >> 8) & 255, full & 255), -1).astype(np.uint8)
    alpha = ((cover >> 24) & 255).astype(np.uint8)
    width, height = size
    sx, sy = width / 256, height / 192
    box = (int(left * sx), int(top * sy), min(width, int(np.ceil(right * sx))), min(height, int(np.ceil(bottom * sy))))
    # Crop in 4x space with the matching region, then fit the HD box.
    c4 = (left * 4, top * 4, right * 4, bottom * 4)
    out = (box[2] - box[0], box[3] - box[1])
    image = Image.fromarray(colour).crop(c4).resize(out, Image.Resampling.BICUBIC)
    smooth = Image.fromarray(alpha).crop(c4).resize(out, Image.Resampling.BILINEAR)
    nearest = Image.fromarray(obj.astype(np.uint8) * 255).crop((left, top, right, bottom)).resize(out, Image.Resampling.NEAREST)
    mask = Image.fromarray(np.maximum(np.asarray(smooth), np.asarray(nearest)))
    return image, mask, box
