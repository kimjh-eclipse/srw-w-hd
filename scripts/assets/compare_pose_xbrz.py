"""Compare native assembled poses using DeSmuME's actual 4xBRZ implementation.

Explicit filter experiment: never changes source art, bindings, or the emulator.
RGB comparisons call Render4xBRZ; transparent references use xBRZ's ARGB mode.
"""
from pathlib import Path
import ctypes
import hashlib
import json
from datetime import datetime, timezone, timedelta
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
PACKETS = ROOT / 'test_current/parts/pose_packets'
OUT = ROOT / 'test_current/parts/xbrz_reference_compare'
BACKGROUND = (24, 30, 40, 255)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    dll = ctypes.CDLL(str(ROOT / 'tools/xbrz_compare.dll'))
    pointer = ctypes.POINTER(ctypes.c_uint32)
    for name in ('srww_xbrz4_rgb', 'srww_xbrz4_argb'):
        func = getattr(dll, name)
        func.argtypes = [pointer, pointer, ctypes.c_int, ctypes.c_int]
        func.restype = None

    def scale(image, alpha):
        array = np.asarray(image.convert('RGBA'), dtype=np.uint32)
        packed = np.ascontiguousarray((array[:, :, 3] << 24) |
                                     (array[:, :, 0] << 16) |
                                     (array[:, :, 1] << 8) | array[:, :, 2])
        result = np.empty((image.height * 4, image.width * 4), dtype=np.uint32)
        func = dll.srww_xbrz4_argb if alpha else dll.srww_xbrz4_rgb
        func(packed.ctypes.data_as(pointer), result.ctypes.data_as(pointer),
             image.width, image.height)
        rgba = np.stack(((result >> 16) & 255, (result >> 8) & 255,
                         result & 255, (result >> 24) & 255 if alpha else
                         np.full(result.shape, 255, dtype=np.uint32)), -1)
        return Image.fromarray(rgba.astype('uint8'), 'RGBA')

    cache, records, sheets = {}, [], []

    def pose(unit, name):
        key = (unit, name)
        if key in cache:
            return cache[key]
        directory = PACKETS / f'unit_{unit}/robot_set' / name
        source = directory / 'native.png'
        nearest_path = directory / 'native_4x.png'
        before = digest(source)
        native = Image.open(source).convert('RGBA')
        nearest = native.resize((native.width * 4, native.height * 4),
                                Image.Resampling.NEAREST)
        existing = Image.open(nearest_path).convert('RGBA')
        if nearest.size != existing.size or nearest.tobytes() != existing.tobytes():
            raise ValueError(f'{unit}/{name}: native_4x is not exact nearest4x')
        transparent = scale(native, True)
        native_display = Image.new('RGBA', native.size, BACKGROUND)
        native_display.alpha_composite(native)
        rgb_filtered = scale(native_display, False)
        rgb_nearest = native_display.resize(nearest.size, Image.Resampling.NEAREST)
        output = OUT / f'unit_{unit}/poses'
        output.mkdir(parents=True, exist_ok=True)
        filtered_path = output / f'{name}_4xbrz_rgba.png'
        transparent.save(filtered_path)
        rgb_filtered.save(output / f'{name}_4xbrz_display.png')
        rgb_nearest.save(output / f'{name}_nearest4x_display.png')
        record = {'unit': unit, 'pose': name, 'source': str(source),
                  'source_sha256': before, 'native_size': list(native.size),
                  'output_size': list(nearest.size),
                  'nearest4x_matches_existing': True,
                  'filtered_rgba': str(filtered_path),
                  'filtered_sha256': digest(filtered_path),
                  'source_unchanged': before == digest(source)}
        records.append(record)
        cache[key] = (transparent, rgb_nearest, rgb_filtered)
        return cache[key]

    # Current reported robot: every original sheet. Other pending robots:
    # first original sheet, for a small cross-design comparison sample.
    for unit in (404, 403, 405, 215, 380):
        source_dir = PACKETS / f'unit_{unit}/robot_set/SHEETS'
        plate_dirs = sorted(source_dir.glob('sheet_*'))
        if unit != 404:
            plate_dirs = plate_dirs[:1]
        for plate in plate_dirs:
            lp = plate / 'layout.json'
            layout = json.loads(lp.read_text(encoding='utf-8'))
            result = Image.new('RGBA', tuple(layout['sheet']))
            for entry in layout['layout']:
                filtered, _, _ = pose(unit, entry['pose'])
                if list(filtered.size) != entry['source_canvas']:
                    raise ValueError(f'{unit}/{entry["pose"]}: source canvas mismatch')
                result.paste(filtered, tuple(entry['sheet_origin']))
            target_dir = OUT / f'unit_{unit}'
            target_dir.mkdir(exist_ok=True)
            target = target_dir / f'{plate.name}_4xbrz_rgba.png'
            result.save(target)
            sheets.append({'unit': unit, 'sheet': plate.name,
                           'source_layout': str(lp), 'layout_sha256': digest(lp),
                           'reference': str(target), 'reference_sha256': digest(target),
                           'size': list(result.size), 'usage': 'reference_only_not_HD_art'})

    layouts = {u: json.loads((PACKETS / f'unit_{u}/robot_set/SHEETS/sheet_01/layout.json')
                           .read_text(encoding='utf-8')) for u in (403, 405, 215, 380)}
    samples = [(404, 'pose_01'), (404, 'pose_02'), (404, 'pose_08'),
               (403, layouts[403]['base_pose']),
               (403, layouts[403]['layout'][2]['pose']),
               (405, layouts[405]['base_pose']),
               (405, layouts[405]['layout'][4]['pose']),
               (215, layouts[215]['base_pose']), (380, layouts[380]['base_pose'])]
    font = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 19)
    titlefont = ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf', 24)
    comparisons = []
    for start in range(0, len(samples), 3):
        group = samples[start:start + 3]
        images = [pose(*key) for key in group]
        width = max(item[1].width for item in images) + 32
        heights = [max(item[1].height, item[2].height) + 50 for item in images]
        sheet = Image.new('RGB', (width * 2 + 16, sum(heights) + 76), BACKGROUND[:3])
        draw = ImageDraw.Draw(sheet)
        draw.text((16, 14), '원본 · 단순 4배 확대', font=titlefont, fill='white')
        draw.text((width + 24, 14), 'DeSmuME 실제 4xBRZ', font=titlefont, fill='white')
        y = 76
        for (unit, name), (_, left, right), height in zip(group, images, heights):
            draw.text((16, y), f'unit {unit} / {name}', font=font, fill=(148, 208, 242))
            draw.text((width + 24, y), f'unit {unit} / {name}', font=font,
                      fill=(148, 208, 242))
            sheet.paste(left.convert('RGB'), (16, y + 34))
            sheet.paste(right.convert('RGB'), (width + 24, y + 34))
            y += height
        path = OUT / f'comparison_{start // 3:02d}.png'
        sheet.save(path)
        comparisons.append(str(path))

    provenance = {'created_kst': datetime.now(timezone(timedelta(hours=9))).isoformat(),
                  'algorithm': 'DeSmuME bundled xBRZ 1.4, scale=4, default ScalerCfg',
                  'display_mode': 'Render4xBRZ RGB; same dark background before filtering',
                  'transparent_mode': 'xbrz::scale<4, ColorFormatARGB>',
                  'source_cpp': str(ROOT / 'emulator/desmume/desmume/src/filter/xbrz.cpp'),
                  'source_cpp_sha256': digest(ROOT / 'emulator/desmume/desmume/src/filter/xbrz.cpp'),
                  'bridge': str(ROOT / 'tools/xbrz_compare_bridge.cpp'),
                  'bridge_sha256': digest(ROOT / 'tools/xbrz_compare_bridge.cpp'),
                  'dll_sha256': digest(ROOT / 'tools/xbrz_compare.dll'),
                  'pose_count': len(records), 'sheet_count': len(sheets),
                  'comparisons': comparisons, 'poses': records, 'sheets': sheets,
                  'limitations': ['Filtered references, not newly painted HD candidates.',
                                  'Dark-background RGB comparison is not a game capture.',
                                  'No emulator settings, bindings, source files or installed art changed.']}
    (OUT / 'provenance.json').write_text(json.dumps(provenance, ensure_ascii=False,
                                                  indent=2), encoding='utf-8')
    print(json.dumps({'poses': len(records), 'sheets': len(sheets),
                      'comparisons': comparisons}, ensure_ascii=False))


if __name__ == '__main__':
    main()
