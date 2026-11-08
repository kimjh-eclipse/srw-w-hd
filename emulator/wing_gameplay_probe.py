"""Interactive native-game replay in an isolated save root, never player slots."""
import sys,json
from pathlib import Path
from PIL import Image
from hd_core import Core,ROOT

def main():
    out=ROOT/'test_current/combat';c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True,user_dir=out/'wing_saves')
    c.load(Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'test_current/menu_card/player_saves/games/0a5a22bd6bb25ebe/slot_1.state')
    def capture():
        Image.fromarray(c.native).resize((768,1152),Image.Resampling.NEAREST).save(out/'wing_progress.png');c.save(out/'wing_progress.state');print('CAPTURED',flush=True)
    c.run();c.audio.clear();capture()
    try:
        for line in sys.stdin:
            command=json.loads(line)
            if command.get('quit'):break
            for step in command.get('steps',[]):
                c.buttons=set(step.get('buttons',[]))
                for _ in range(step['frames']):c.run();c.audio.clear()
            c.buttons=set();capture()
    finally:c.close()

if __name__=='__main__':main()
