
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import time,json
import numpy as np
from PIL import Image,ImageDraw
from hd_core import Core,ROOT
from frame_compositor import ReadyParts

def main():
    out=ROOT/'test_current/formation';out.mkdir(exist_ok=True)
    target=np.asarray(Image.open('C:/Users/OXP2/AppData/Local/Temp/codex-clipboard-ccbf2fb7-c1f3-42f1-8e3f-167b482426ff.png').convert('RGB').resize((256,192),Image.Resampling.BOX)).astype('int16');mask=np.ones((192,256),bool);mask[160:]=False;mask[80:156,15:106]=False
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True,user_dir=out/'boot_saves');best=999;shots=[]
    try:
        for f in range(12000):
            phase=f%160;core.buttons={3} if 0<=phase<3 and f>=320 else ({8,11} if 80<=phase<140 and f>=400 else set());core.run();core.audio.clear()
            if f%10:continue
            score=float(np.abs(core.native[:192].astype('int16')-target)[mask].mean())
            if score<best:
                best=score;Image.fromarray(core.native).save(out/'best_native.png');core.save(out/'current.state');(out/'capture_progress.json').write_text(json.dumps(dict(frame=f,score=score)))
            if f%160==0:Image.fromarray(core.native).resize((256,384)).save(out/f'boot_{f}.png');shots.append(f)
            if score<19:
                core.set_hd(True);core.set_ready_parts(ReadyParts());core.run();core.save(out/'formation.state');Image.fromarray(core.native).save(out/'formation_native.png');print('FOUND',f,score,flush=True);break
        else:print('closest',best,flush=True)
    finally:core.close()
    contact=Image.new('RGB',(1536,384*((len(shots)+5)//6)),'#333333');d=ImageDraw.Draw(contact)
    for n,f in enumerate(shots):contact.paste(Image.open(out/f'boot_{f}.png'),((n%6)*256,(n//6)*384));d.text(((n%6)*256,(n//6)*384+190),str(f),fill='yellow')
    contact.save(out/'boot_contact.png')

if __name__=='__main__':main()
