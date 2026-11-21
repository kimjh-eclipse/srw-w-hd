"""Connect Codex's Creuset helmet cut-in (11/18 RAWs) - unit 77 weapon 329, frames ~208-290.

BG1 IMG22864 (Creuset, masked face) -> cut-in id 19: picture replaced (the 11/09 one had no mask),
  map window signature replaced by the live measurement. The ROM map is 30 tiles wide; the game
  lays it out again in VRAM, so the ROM-derived window (272207096) never matched. Live, at the
  GPU.cpp image_origin rule (probe at base 128, window origin 128, 512 entries): 1393323117.
BG2 IMG26391 (blue scan-line backdrop) -> new cut-in, layer 2, battle_effect_bg, whole 256x256
  plane, probe 1936081678 at base 640, window 4033636805 (origin 640, 512 entries).
Pictures are planes at 3.75x (960 per 256), as the other cut-ins. Codex RAW pixels are only
scaled (silhouette bbox fit) and the interior alpha 252/253 set to 255.

  py -3.11 -X utf8 scripts/assets/install_creuset_cutin.py
"""
import json,shutil,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
REQ=ROOT/'test_current/parts/cutin_requests/creuset_helmet'


def main():
    out=ROOT/'graphics/pilot_cutins/creuset_mask';out.mkdir(parents=True,exist_ok=True)
    shutil.copy2(REQ/'candidate_22864_plane.png',out/'creuset_mask_bg1_22864_hd.png')
    bg=Image.open(REQ/'codex_generated_20261118/RAW_26391_20261118.png').convert('RGBA').resize((960,960),Image.Resampling.LANCZOS)
    a=np.asarray(bg).copy();a[...,3]=255;Image.fromarray(a).save(out/'scanline_bg2_26391_hd.png')
    path=ROOT/'graphics/cutins_library.json';lib=json.loads(path.read_text(encoding='utf-8'))
    shutil.copy2(path,ROOT/'test_current/parts/pending_install/cutins_library.before_creuset_20261121.json')
    rel=lambda p:str(p.relative_to(ROOT/'graphics')).replace('\\','/')
    for c in lib['cutins']:
        if c['id']==19:
            c['image']=c['paint_image']=rel(out/'creuset_mask_bg1_22864_hd.png')
            c['map_window_signature']=1393323117;c['map_window_entries']=512
            c['note']='Creuset masked face (BG1); Codex drawing 11/18 fitted by silhouette; map window measured live 11/21 (ROM map is 30 tiles wide)'
    lib['cutins']=[c for c in lib['cutins'] if c.get('name')!='creuset_scanline_bg_26391']
    lib['cutins'].append(dict(id=max(c['id'] for c in lib['cutins'])+1,name='creuset_scanline_bg_26391',resource=26391,layer=2,layers=[2],native_size=[256,256],
        image=rel(out/'scanline_bg2_26391_hd.png'),paint_image=rel(out/'scanline_bg2_26391_hd.png'),signatures=[1936081678],signature_mode='image_origin',
        map_window_signature=4033636805,map_window_entries=512,repeat_native_plane=True,presentation_role='battle_effect_bg',
        note='Creuset cut-in blue scan-line backdrop (BG2); Codex drawing 11/18; probe and window measured live at unit 77 weapon 329 frame 240'))
    path.write_text(json.dumps(lib,ensure_ascii=False,indent=1),encoding='utf-8')
    print('id 19 replaced; backdrop id',lib['cutins'][-1]['id'])


if __name__=='__main__':main()
