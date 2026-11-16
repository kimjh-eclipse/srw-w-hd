"""Prepare actual 4xBRZ generation references; never modify native sources."""
from pathlib import Path
import argparse, ctypes, hashlib, json
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def scale4(native):
    dll = ctypes.CDLL(str(ROOT / 'tools/xbrz_compare.dll'))
    ptr = ctypes.POINTER(ctypes.c_uint32)
    dll.srww_xbrz4_argb.argtypes = [ptr, ptr, ctypes.c_int, ctypes.c_int]
    dll.srww_xbrz4_argb.restype = None
    a = np.asarray(native.convert('RGBA'), dtype=np.uint32)
    src = np.ascontiguousarray(a[:, :, 3] << 24 | a[:, :, 0] << 16 |
                              a[:, :, 1] << 8 | a[:, :, 2])
    dst = np.empty((native.height * 4, native.width * 4), dtype=np.uint32)
    dll.srww_xbrz4_argb(src.ctypes.data_as(ptr), dst.ctypes.data_as(ptr),
                      native.width, native.height)
    return Image.fromarray(np.stack(((dst >> 16) & 255, (dst >> 8) & 255,
                                    dst & 255, (dst >> 24) & 255), -1).astype('uint8'))


def prepare_plate(unit, sheet):
    base = ROOT / f'test_current/parts/pose_packets/unit_{unit}/robot_set'
    folder = base / 'SHEETS' / f'sheet_{sheet:02d}'
    lp = folder / 'layout.json'
    spec = json.loads(lp.read_text(encoding='utf-8'))
    canvas = Image.new('RGBA', tuple(spec['sheet']))
    sources = []
    for entry in spec['layout']:
        p = base / entry['pose'] / 'native.png'
        original = Image.open(p).convert('RGBA')
        existing = Image.open(base / entry['pose'] / 'native_4x.png').convert('RGBA')
        nn = original.resize((original.width * 4, original.height * 4), Image.Resampling.NEAREST)
        if nn.size != existing.size or nn.tobytes() != existing.tobytes():
            raise ValueError(f'Not exact native 4x source: {p}')
        filtered = scale4(original)
        if list(filtered.size) != entry['source_canvas']:
            raise ValueError(f'Layout size mismatch: {p}')
        canvas.paste(filtered, tuple(entry['sheet_origin']))
        sources.append({'path': str(p), 'sha256': sha(p), 'pose': entry['pose']})
    target = folder / 'reference_4xbrz.png'
    canvas.save(target)
    meta = {'algorithm': 'DeSmuME bundled xBRZ 1.4, scale4, default ScalerCfg, ARGB',
            'source_cpp_sha256': sha(ROOT / 'emulator/desmume/desmume/src/filter/xbrz.cpp'),
            'dll_sha256': sha(ROOT / 'tools/xbrz_compare.dll'),
            'layout_path': str(lp), 'layout_sha256': sha(lp), 'sources': sources,
            'reference': str(target), 'reference_sha256': sha(target),
            'unfiltered_reference': str(folder / 'native_sheet_4x.png'),
            'size': list(canvas.size), 'usage': 'generation_reference_only_not_HD_candidate'}
    (folder / 'reference_4xbrz.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    return target


def prepare_image(path, input_scale):
    path = Path(path)
    original = Image.open(path).convert('RGBA')
    if input_scale == 1:
        native = original
    elif input_scale == 4:
        if original.width % 4 or original.height % 4:
            raise ValueError('4x input dimensions must divide by4')
        native = original.resize((original.width // 4, original.height // 4), Image.Resampling.NEAREST)
        if native.resize(original.size, Image.Resampling.NEAREST).tobytes() != original.tobytes():
            raise ValueError('Input is not exact nearest4x; supply original1x')
    else:
        raise ValueError('input_scale must be1 or4')
    result = scale4(native)
    target = path.with_name(path.stem + '_4xbrz.png')
    result.save(target)
    target.with_suffix('.json').write_text(json.dumps({'algorithm': 'DeSmuME xBRZ1.4 ARGB4x', 'source': str(path), 'source_sha256': sha(path), 'input_scale': input_scale, 'reference': str(target), 'reference_sha256': sha(target), 'size': list(result.size), 'usage': 'reference_only'}, ensure_ascii=False, indent=2), encoding='utf-8')
    return target


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--unit', type=int)
    p.add_argument('--sheet', type=int, default=1)
    p.add_argument('--image')
    p.add_argument('--input-scale', type=int, default=1)
    a = p.parse_args()
    print(prepare_image(a.image, a.input_scale) if a.image else prepare_plate(a.unit, a.sheet))
