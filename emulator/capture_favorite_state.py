import numpy as np,json
from PIL import Image,ImageDraw
from hd_core import Core,ROOT
from frame_compositor import ReadyParts
import inspect_attract_resources as inspector

def main():
    out=ROOT/'test_current/formation';inspector.OUT=out
    target=np.asarray(Image.open('C:/Users/OXP2/AppData/Local/Temp/codex-clipboard-ccbf2fb7-c1f3-42f1-8e3f-167b482426ff.png').convert('RGB').resize((256,192),Image.Resampling.BOX)).astype('int16');mask=np.ones((192,256),bool);mask[160:]=False;mask[80:156,15:106]=False
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'boot_saves');core.set_ready_parts(ReadyParts());core.load(out/'current.state');best=999;canvas=Image.new('RGB',(1024,768));d=ImageDraw.Draw(canvas)
    try:
        for choice in range(16):
            if choice:
                core.buttons={7}
                for _ in range(2):core.run();core.audio.clear()
            core.buttons=set()
            for _ in range(24):core.run();core.audio.clear()
            score=float(np.abs(core.native[:192].astype('int16')-target)[mask].mean());print(choice,score,flush=True)
            canvas.paste(Image.fromarray(core.native[:192]),((choice%4)*256,(choice//4)*192));d.text(((choice%4)*256,(choice//4)*192+150),str(choice),fill='yellow')
            if score<best:best=score;core.save(out/'formation.state');Image.fromarray(core.native).save(out/'formation_native.png')
        core.load(out/'formation.state');core.run();inspector.snapshot(core,0);canvas.save(out/'selection_contact.png');print('best',best)
    finally:core.close()

if __name__=='__main__':main()
