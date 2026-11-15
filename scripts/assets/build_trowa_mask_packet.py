"""Drawing packet for Trowa's half-mask pilot cut-in (Heavyarms Kai, Full Open Attack).

The native picture is two BG layers placed side by side:
  BG1 = IMG 22817 (left half: hair, clown mask, hand)  map 22819  - no HD exists
  BG2 = IMG 22818 (right half: face)                   map 22820  - cut-in id 15
The id 15 HD was painted as a whole face and spills over the mask half, so
connecting it hides the mask. Both halves are redrawn as one picture and then
split by the native silhouettes.

Writes test_current/parts/cutin_redraw/trowa_mask/:
  live_native.png       the game's top screen at the cut-in (256x192), 4x copy too
  current_wrong_hd.png  what connecting the present id 15 art produces
  contract.json         resources, live signatures and what to deliver
"""
import ctypes as C,json,shutil,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
sys.path.insert(0,str(ROOT/'emulator'))

STATE=ROOT/'test_current/gui/unit_review/attack_starts/unit_2_weapon_12.state'
FRAME=225
OUT=ROOT/'test_current/parts/cutin_redraw/trowa_mask'


def main():
    from hd_core import Core
    OUT.mkdir(parents=True,exist_ok=True)
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True,user_dir=OUT/'isolated_saves')
    core.load(STATE)
    for _ in range(FRAME+1):core.run();core.audio.clear()
    native=np.asarray(core.native)[:192].copy()
    Image.fromarray(native).save(OUT/'live_native.png');Image.fromarray(native).resize((1024,768),Image.Resampling.NEAREST).save(OUT/'live_native_4x.png')
    owners={}  # split is done at install time from the ROM silhouettes (core layer ids also mark the HUD)
    shutil.copy2(ROOT/'graphics/pilot_cutins/cutin_22818_hd.png',OUT/'existing_hd_22818_whole_face.png')
    contract=dict(
        purpose='Trowa half-mask pilot cut-in: redraw as one picture (left half hair+clown mask+hand, right half face), keep the native split line',
        source_state=str(STATE.relative_to(ROOT)).replace('\\','/'),frame=FRAME,
        layers=[dict(bg=1,image=22817,map=22819,map_columns=17,live_probe_mode0=1058631903,cutin_id=None,hd=None),
                dict(bg=2,image=22818,map=22820,map_columns=24,live_probe_mode0=2860819202,cutin_id=15,live_map_window_384=707496858,hd='graphics/pilot_cutins/cutin_22818_hd.png (whole face, spills over the mask half - replace)')],
        deliver=dict(drawing='candidate_full.png: 1024x768 (4x of the 256x192 screen), same placement as live_native_4x.png, both halves in one picture',
            notes='Keep the vertical split, the mask (white/red clown) held by the hand on the left, the green eye on the right, the blue gradient stays native (not part of these layers). Claude splits the drawing by the native ROM silhouettes of 22817/22818 and connects both layers.'))
    (OUT/'contract.json').write_text(json.dumps(contract,ensure_ascii=False,indent=1),encoding='utf-8')
    print('packet',OUT,owners)


if __name__=='__main__':main()
