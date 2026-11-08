"""Replay animated translucent menus and reject unrelated effect-palette slots."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import base64,json,subprocess,types,zlib
from collections import OrderedDict
import numpy as np
from PIL import Image
from hd_core import Core,ROOT
from hd_fonts import FontRenderer
from hd_parts import PartsRenderer
from gpu_surface import Surface


def main():
    source=subprocess.check_output(['git','show','e75fb520:emulator/hd_fonts.py']).decode('utf8')
    old=types.ModuleType('font_before');old.__file__=str(ROOT/'emulator/hd_fonts.py');exec(compile(source,old.__file__,'exec'),old.__dict__)
    out=ROOT/'test_current/font';core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'saves');reports=[];panels=[]
    try:
        for name in ['font/forecast_confirm.state','combat/attack_weapons.state']:
            core.load(ROOT/'test_current'/name);previous=[old.FontRenderer(),old.FontRenderer()];current=[FontRenderer(),FontRenderer()]
            variants=[[set(),set()],[set(),set()]];styles=[set(),set()]
            for frame in range(120):
                core.run();core.audio.clear()
                for side in range(2):
                    native=core.native[side*192:(side+1)*192].copy()
                    for method,renderers in enumerate([previous,current]):
                        r=renderers[side];r.recognize(native);words=tuple(sorted((x,y,ch) for x,y,ch in r.last_matches if ch.isalpha() and not ch.isascii()));variants[method][side].add(words)
                    styles[side].add(tuple(sorted(current[side].menu_glyphs)))
                    if name.startswith('font/') and side==1 and frame==5:
                        for r in [previous[side],current[side]]:
                            image=Image.fromarray(native).resize((768,576),Image.Resampling.NEAREST);r.compose(image,native);panels.append(image.crop((285,270,465,465)))
            assert all(len(v)==1 for v in variants[1]),(name,[len(v) for v in variants[1]])
            assert all(len(v)==1 for v in styles),(name,'selected style changed')
            reports.append(dict(scene=name,frames=120,before_letter_variants=[len(v) for v in variants[0]],after_letter_variants=[len(v) for v in variants[1]],selected_style_variants=[len(v) for v in styles]))
    finally:core.close()
    montage=Image.new('RGB',(360,195));montage.paste(panels[0]);montage.paste(panels[1],(180,0));montage.save(out/'translucent_menu_font_comparison.png')
    r=PartsRenderer.__new__(PartsRenderer);r.material_maps=OrderedDict();r.palette_luts={}
    palette=np.zeros((16,3),dtype='float32');palette[1]=128;palette[2]=144;palette[3]=160
    native=np.ones((8,8),dtype='uint8');encoded=base64.b64encode(zlib.compress(native.tobytes())).decode()
    pixels=np.empty((24,24,4),dtype='uint8');pixels[:,:,:3]=np.linspace(128,165,24).astype('uint8')[None,:,None];pixels[:,:,3]=np.linspace(0,255,24).astype('uint8')[:,None]
    art=Image.fromarray(pixels);quantized=np.rint(pixels[:,:,:3].astype('float32')*31/255).astype('uint32');codes=quantized[:,:,0]|quantized[:,:,1]<<5|quantized[:,:,2]<<10
    before=r.get_palette_lut(palette)[codes];residual,indices=r.material_map(1,art,palette,dict(w=8,h=8,index_pixels=encoded))
    assert np.any(before!=1) and np.all(indices==1)
    target=palette.copy();target[2]=[255,0,0];target[3]=[0,255,0];colored=target[indices]+residual
    assert np.all(colored[:,:,0]==colored[:,:,1]) and np.all(colored[:,:,1]==colored[:,:,2])
    alpha_cases=0
    for opacity in (0,64,128,255):
        background=Image.new('RGB',(24,24),(35,70,105));mask=Image.fromarray((pixels[:,:,3].astype('uint16')*opacity//255).astype('uint8'))
        expected=background.copy();expected.paste(art,(0,0),mask)
        gpu=Surface((24,24));gpu.paste(background);gpu.draw(art,(0,0,24,24),mask=Image.new('L',(24,24),opacity),alpha=True)
        delta=np.abs(np.asarray(expected).astype('int16')-np.asarray(gpu).astype('int16'));assert delta.max()<=1;alpha_cases+=1
    report=dict(menu_replays=reports,unrelated_effect_palette_slots_excluded=True,old_pixels_using_unused_slots=int(np.count_nonzero(before!=1)),new_pixels_using_unused_slots=int(np.count_nonzero(indices!=1)),rgba_mask_blend_cases=alpha_cases,gpu_cpu_max_difference_at_most_one=True)
    (out/'translucent_text_and_palette_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))


if __name__=='__main__':main()
