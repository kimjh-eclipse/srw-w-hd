
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json
import numpy as np
from PIL import Image,ImageDraw
from hd_core import Core,ROOT
from scripts.diagnostics.inspect_attract_resources import memory_chunk
from scripts.assets.prepare_map_tiles import decode_bg

def main():
    out=ROOT/'test_current/localized_screens';out.mkdir(exist_ok=True);c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'saves');c.load(ROOT/'test_current/font/fresh_favorite.state');sheet=Image.new('RGB',(256*8,384*5));d=ImageDraw.Draw(sheet);best=0;rows=[]
    try:
        for f in range(4000):
            c.buttons={8} if f%80<32 else set();c.run();c.audio.clear()
            if f%100==0:
                x=(f//100)%8*256;y=(f//100)//8*384;sheet.paste(Image.fromarray(c.native),(x,y));d.text((x,y),str(f),fill='red')
            a=c.native[:192];white=np.all(a[55:115,20:235]>210,axis=2).sum();blue=np.mean(a[:150,:,2])-np.mean(a[:150,:,0])
            if blue>10 and white>best and np.mean(a[:150])<60:
                best=white;Image.fromarray(a).save(out/'chapter_candidate.png');c.save(out/'chapter.state');rows.append(dict(frame=f,white=int(white),blue=float(blue)))
        sheet.save(out/'chapter_replay_contact.png');(out/'chapter_detection.json').write_text(json.dumps(rows,indent=2));print(rows[-5:])
    finally:c.close()

if __name__=='__main__':main()
