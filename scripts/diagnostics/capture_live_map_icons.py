
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import sys,json
import numpy as np
from PIL import Image
from hd_core import Core,ROOT
from hd_map_icons import MapIconRenderer

def main():
    out=ROOT/'test_current/map_icons';c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True,user_dir=out/'saves');r=MapIconRenderer();rows=[]
    try:
        c.load(ROOT/'test_current/font/menu_step_5.state')
        for f in range(501):
            c.buttons={8,11} if f%70<40 else set();c.run();c.audio.clear()
            if f%100==0:
                Image.fromarray(c.native).save(out/f'live_{f}.png');matches=r.recognize(c.native[192:]);rows.append(dict(frame=f,matches=matches));print(f,len(matches),matches,flush=True)
        c.save(out/'enemy_and_ally.state')
        # Cancel selection, then pan the actual tactical camera to expose the
        # enemy ships above the first viewport. These are native game inputs.
        for direction,button in [('cancel',0),('up',4),('right',7),('down',5),('left',6)]:
            for tick in range(160 if direction!='cancel' else 20):
                c.buttons={button};c.run();c.audio.clear()
                if tick%40==39:
                    name=f'pan_{direction}_{tick}';Image.fromarray(c.native).save(out/(name+'.png'));matches=r.recognize(c.native[192:]);rows.append(dict(scene=name,matches=matches));print(name,len(matches),matches,flush=True)
                    if direction=='up' and tick==119:c.save(out/'all_enemies_visible.state')
    finally:c.close()
    (out/'live_matches.json').write_text(json.dumps(rows,indent=2))

if __name__=='__main__':main()
