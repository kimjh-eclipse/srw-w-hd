"""Production-input contracts from the OBJ cache of the frame just rendered.

No emulation is advanced, no VRAM is read and no image/quality verdict is made.
Call immediately after a successful Core.run(), before the next run/load.

Example (from the repository root)::

    from scripts.assets.capture_rendered_obj_contract import capture_rendered_obj_contracts
    rows = capture_rendered_obj_contracts(core, state="capture.state", frame=54)
    # index_pixels: base64(zlib(raw uint8 indices)); palette_15bit is rendered cache.
    Path("contracts.json").write_text(json.dumps(rows, indent=2))

Only the engine represented by core.obj/core.parts is supported intentionally.
The engine selector below is the same rendered-engine selector used by Core.
A bound row must agree with both the cached hash and rendered attributes; an
unbound row (binding_id == 0) is sourced directly from the validated cache.
Screen intersection is a bounding-box filter, NOT a per-pixel window/occlusion
visibility verdict. Affine matrices and flips are recorded, not baked into bytes.
"""
from __future__ import annotations

import base64
import ctypes as C
import hashlib
import struct
import zlib

__all__ = ["capture_rendered_obj_contracts", "capture_rendered_obj_contract"]
_WIDTHS = ((8, 16, 32, 64), (16, 32, 32, 64), (8, 8, 16, 32))
_HEIGHTS = ((8, 16, 32, 64), (8, 8, 16, 32), (16, 32, 32, 64))


def capture_rendered_obj_contracts(core, *, state=None, frame=None, oams=None):
    """Return JSON-compatible production records for visible cached OBJ entries.

    Raises RuntimeError for an absent API/invalid engine or incomplete snapshot.
    Invalid/disabled/offscreen entries, cache-size mismatches and stale bound
    hashes/attributes are excluded. Does not mutate the core or player settings.
    Supports both 16-color and 256-color OBJ; consumers must not truncate palette.
    """
    if not hasattr(core.api, "retro_srw_copy_cached_obj"):
        raise RuntimeError("Core lacks retro_srw_copy_cached_obj; do not fall back to VRAM")
    raw = bytes(core.obj.raw)
    if len(raw) != 1024 or len(core.parts) != 128:
        raise RuntimeError("Expected one rendered 128-OAM snapshot")
    selector = core.api.retro_srw_copy_effect_debug
    selector.argtypes = [C.c_void_p] * 4
    selector.restype = C.c_uint
    engine = int(selector(None, None, None, None)) - 1
    if engine not in (0, 1):
        raise RuntimeError(f"Invalid rendered OBJ engine: {engine}")
    api = core.api.retro_srw_copy_cached_obj
    api.argtypes = [C.c_uint, C.c_uint, C.c_void_p, C.c_uint,
                    C.c_void_p, C.c_uint, C.c_void_p, C.c_uint]
    api.restype = C.c_uint
    selected = range(128) if oams is None else list(oams)
    if any(not isinstance(i, int) or not 0 <= i < 128 for i in selected):
        raise ValueError("OAM IDs must be integers in [0, 127]")
    records = []
    for i in selected:
        a, b, attr2 = struct.unpack_from("<HHH", raw, i * 8)
        affine = bool(a & 0x100)
        shape, size, mode = a >> 14, b >> 14, (a >> 10) & 3
        if (not affine and a & 0x200) or shape == 3 or mode >= 2:
            continue  # Disabled / invalid / OBJ-window (not a painted sprite).
        w, h = _WIDTHS[shape][size], _HEIGHTS[shape][size]
        double = affine and bool(a & 0x200)
        display_w, display_h = w * (2 if double else 1), h * (2 if double else 1)
        x, y = b & 511, a & 255
        x = x - 512 if x >= 256 else x
        y = y - 256 if y >= 192 else y
        if x >= 256 or y >= 192 or x + display_w <= 0 or y + display_h <= 0:
            continue
        row = (C.c_uint * 8)()
        pixels = (C.c_uint8 * 4096)()
        palette = (C.c_uint16 * 256)()
        if not api(engine, i, row, 8, pixels, 4096, palette, 256):
            continue
        if (int(row[0]), int(row[1])) != (w, h):
            continue
        part = [int(v) for v in core.parts[i]]
        bound = part[0] != 0
        if bound and (part[4] != int(row[2]) or part[1:4] != [a, b, attr2]):
            continue
        eight_bit = bool(row[7])
        if eight_bit != bool(a & 0x2000):
            continue
        indices = bytes(pixels[:w * h])
        count = 256 if eight_bit else 16
        if any(v >= count for v in indices):
            continue
        pal = [int(v) for v in palette[:count]]
        rgb = [[(v & 31) * 255 // 31, ((v >> 5) & 31) * 255 // 31,
                ((v >> 10) & 31) * 255 // 31] for v in pal]
        matrix_index = (b >> 9) & 31 if affine else None
        matrix = [struct.unpack_from("<h", raw, matrix_index * 32 + off)[0]
                  for off in (6, 14, 22, 30)] if affine else None
        records.append(dict(
            state=str(state) if state is not None else None, frame=frame,
            video_epoch=int(getattr(core, "video_epoch", 0)), engine=engine, oam=i,
            attributes=[a, b, attr2], screen_x=x, screen_y=y, w=w, h=h,
            display_w=display_w, display_h=display_h, priority=(attr2 >> 10) & 3,
            obj_mode=mode, eight_bit=eight_bit, palette_bank=(attr2 >> 12) & 15,
            tile_number=attr2 & 1023, affine=affine, affine_double=double,
            affine_matrix_index=matrix_index, affine_matrix_8_8=matrix,
            flip_x=bool(b & 0x1000) if not affine else False,
            flip_y=bool(b & 0x2000) if not affine else False,
            mosaic=bool(a & 0x1000), hash=int(row[2]), index_hash=int(row[3]),
            material=int(row[4]), used_mask=int(row[5]), opaque=int(row[6]),
            binding_id=part[0], bound_hash_checked=bound,
            hd_pending_or_held=bool(part[7] & 0x80000000) if bound else None,
            index_pixels=base64.b64encode(zlib.compress(indices)).decode("ascii"),
            indices_sha256=hashlib.sha256(indices).hexdigest(), palette_15bit=pal,
            original_palette_rgb=rgb, source="rendered_obj_cache",
            visibility_scope="enabled OBJ bounding box intersects screen; per-pixel window/occlusion not adjudicated",
        ))
    return records


def capture_rendered_obj_contract(core, oam, **context):
    """Return one eligible OAM contract, or None if it was excluded."""
    rows = capture_rendered_obj_contracts(core, oams=[oam], **context)
    return rows[0] if rows else None
