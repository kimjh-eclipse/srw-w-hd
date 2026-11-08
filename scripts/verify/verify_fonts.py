"""Check real captured dialogue/UI text, dim text, and font composition cost."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json
import time
import numpy as np
from PIL import Image
from hd_fonts import FontRenderer, ROOT


def main():
    out = ROOT / 'test_current/font'
    renderer = FontRenderer()
    report = dict(mapped_patterns=len(renderer.keys), scenes={})
    for number in (0, 1, 3, 4):
        native = np.asarray(Image.open(out / f'scene_{number}.png'))
        display = Image.new('RGB', (1440, 2160))
        records = []
        for screen in (0, 1):
            source = native[screen*192:(screen+1)*192]
            image = Image.fromarray(source).resize((1440, 1080), Image.Resampling.NEAREST)
            renderer.compose(image, source)
            records.append(renderer.last_matches)
            display.paste(image, (0, screen*1080))
        report['scenes'][str(number)] = records
        display.save(out / f'hd_scene_{number}.png')
    dialogue = report['scenes']['0'][1]
    assert ''.join(ch for x, y, ch in dialogue if y == 4) == '듀오'
    assert '이래선' in ''.join(ch for x, y, ch in dialogue if y == 20)
    assert '카즈마' in ''.join(ch for x, y, ch in dialogue if y == 132)
    ability = report['scenes']['1'][0]
    assert ''.join(ch for x, y, ch in sorted(ability) if y == 0) == '카즈마·아디건'
    def line(y, left=0, right=256):
        return ''.join(ch for x, yy, ch in sorted(ability) if yy == y and left <= x < right)
    assert line(16, 160, 184) == '1/1'
    assert line(16, 224) == '0/0'
    assert line(32, 96, 120) == '102'
    assert line(96) == '5000/5000'
    assert line(112) == '170/170'
    assert line(160, 204) == '±0%'
    with np.load(ROOT / 'graphics/fonts/hud_glyphs.npz') as source:
        strip = np.zeros((192, 256, 3), dtype='uint8')
        for index, glyph in enumerate(source['indices']):
            pixels = np.zeros((8, 8, 3), dtype='uint8')
            pixels[glyph == 15] = 255
            pixels[glyph == 14] = 164
            strip[80:88, 8+index*8:16+index*8] = pixels
        found = renderer.recognize(strip)
        assert ''.join(ch for x, y, ch in sorted(found) if y == 80) == '0123456789/?+-±'
    native = np.asarray(Image.open(out / 'scene_1.png'))[:192]
    measurements = {}
    for mode in ('changed_text', 'moving_background', 'unchanged'):
        values = []
        for n in range(20):
            source = native.copy()
            if mode == 'changed_text':
                renderer.last_native_key = renderer.last_key = renderer.overlay_key = renderer.layout_key = None
            elif mode == 'moving_background':
                source[120, 200] = [n, 3, 30]
            target = Image.fromarray(source).resize((1440, 1080), Image.Resampling.NEAREST)
            start = time.perf_counter()
            renderer.compose(target, source)
            values.append((time.perf_counter()-start)*1000)
        measurements[mode] = dict(mean_ms=round(float(np.mean(values)), 3),
                                  p95_ms=round(float(np.percentile(values, 95)), 3))
    blank = np.zeros((192, 256, 3), dtype='uint8')
    assert not renderer.recognize(blank)
    report.update(timing=measurements, real_dialogue_and_ui_labels=True,
                  dimmed_previous_speaker=True, empty_screen_unchanged=True,
                  numeric_fields_and_symbols=True, all_compact_digits_and_symbols=True,
                  coverage='Exact 12px text, 8px-wide text and 8x8 HUD numbers; other image lettering remains native.')
    (out / 'font_verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    # A compact actual dialogue before/after for review.
    source = np.asarray(Image.open(out / 'scene_0.png'))[192:384]
    before = Image.fromarray(source).resize((1440, 1080), Image.Resampling.NEAREST)
    from hd_renderer import HDRenderer
    from hd_portraits import PortraitRenderer
    actual = HDRenderer()
    actual.bottom_portraits = PortraitRenderer(async_prepare=False)
    actual.bottom_text_renderer = renderer
    flags = [0]*12
    flags[10] = 1
    after = actual.render_bottom(np.asarray(Image.open(out / 'scene_0.png')), flags)
    assert len(actual.bottom_portraits.last_matches) == 2
    after.save(out / 'dialogue_hd.png')
    comparison = Image.new('RGB', (1440, 1000))
    comparison.paste(before.crop((0, 0, 1440, 500)), (0, 0))
    comparison.paste(after.crop((0, 0, 1440, 500)), (0, 500))
    comparison.save(out / 'font_comparison.png')
    print(json.dumps(dict(timing=measurements, checks='passed'), ensure_ascii=False))


if __name__ == '__main__':
    main()
