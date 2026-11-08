"""Replay actual command-menu and cut-in frames through font composition."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json
import numpy as np
from PIL import Image
from hd_core import Core, ROOT
from hd_fonts import FontRenderer
from hd_renderer import HDRenderer


def main():
    out = ROOT / 'test_current/font'
    font = FontRenderer()
    native = np.asarray(Image.open(out / 'command_progress_600.png'))[192:]
    matches = font.recognize(native)
    for y, expected in ((128, '이동'), (144, '정신'), (160, '능력')):
        assert ''.join(ch for x, yy, ch in sorted(matches) if yy == y) == expected
    image = Image.fromarray(native).resize((1440, 1080), Image.Resampling.NEAREST)
    font.compose(image, native)
    image.save(out / 'command_all_fonts_hd.png')
    core = Core(ROOT / 'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',
                demo=True, user_dir=out / 'saves')
    try:
        core.load(out / 'cutin_dialogue.state')
        core.run()
        renderer = HDRenderer()
        captured = {}
        original = renderer.text_renderer.compose

        def observe(target, native, background=None, **kwargs):
            captured['background'] = background.copy() if background is not None else (target.copy() if kwargs.get('only_text') else None)
            return original(target, native, background, **kwargs)

        renderer.text_renderer.compose = observe
        image = renderer.render_top(core.native, core.ids, core.hd,
                                    parts=core.parts, obj=core.obj.raw, owners=core.owners,
                                    bgpriors=core.bgpriors, bgparts=core.bgparts,
                                    part_palettes=core.part_palettes, backgrounds=core.backgrounds)
        image.save(out / 'cutin_font_background_fixed.png')
        background = captured['background']
        assert background is not None
        background.save(out / 'cutin_font_clean_background.png')
        backdrop = core.native[150, 0].copy()
        result, clean = np.asarray(image), np.asarray(background)
        introduced = np.all(result == backdrop, axis=2) & np.any(clean != backdrop, axis=2)
        # Unrecognized native HUD remains legitimate. In recognized text areas,
        # the old hidden-cut-in backdrop must never be stamped over the HD art.
        ink = Image.fromarray(renderer.text_renderer.last_mask.astype('uint8')*255).resize(
            image.size, Image.Resampling.NEAREST)
        assert not (introduced & (np.asarray(ink) > 0)).any()
        report = dict(selected_and_unselected_commands=True, cutin=int(core.hd[0]),
                      scroll=[int(core.hd[1]), int(core.hd[2])],
                      native_backdrop=backdrop.tolist(),
                      introduced_backdrop_pixels_in_text=0, uses_clean_hd_underlay=True,
                      recognized_characters=len(renderer.text_renderer.last_matches))
        (out / 'cutin_font_background_verification.json').write_text(json.dumps(report, indent=2))
        print(json.dumps(report))
    finally:
        core.close()


if __name__ == '__main__':
    main()
