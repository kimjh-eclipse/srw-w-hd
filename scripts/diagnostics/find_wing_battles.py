"""Locate requested pilots in the game's unmodified attract sequence."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,time
from PIL import Image,ImageDraw
from hd_core import Core,ROOT
from hd_fonts import FontRenderer

def main():
    out=ROOT/'test_current/combat';c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True,user_dir=out/'wing_saves')
    font=FontRenderer();font.set_battle_scan(True);c.set_frameskip(7);events=[];panels=[];saved=set();start=time.perf_counter();last_sample=-24;last_panel=-600
    try:
        c.load(out/'eid.state')
        for offset in range(90001):
            if not c.run():c.audio.clear();continue
            c.audio.clear()
            if offset-last_sample>=24:
                last_sample=offset
                text=''.join(ch for x,y,ch in sorted(font.recognize(c.native[:192]),key=lambda t:(t[1],t[0])) if y>=116)
                if not events or text!=events[-1]['text']:events.append(dict(offset=offset,text=text))
                for name,needle in (('duo','듀오'),('quatre','카토르')):
                    if needle in text and name not in saved:
                        c.save(out/(name+'_attract.state'));Image.fromarray(c.native).save(out/(name+'_attract_native.png'));saved.add(name)
                        print('found',name,offset,flush=True)
            if offset-last_panel>=600:
                last_panel=offset
                panel=Image.fromarray(c.native[:192]).resize((256,192));ImageDraw.Draw(panel).text((2,2),str(offset+18450),fill='yellow');panels.append(panel)
                (out/'wing_search_progress.json').write_text(json.dumps(dict(offset=offset,found=sorted(saved),seconds=time.perf_counter()-start)))
            if offset>30000 and len(saved)==2:break
    finally:c.close()
    sheet=Image.new('RGB',(256*8,212*((len(panels)+7)//8)))
    for i,panel in enumerate(panels):sheet.paste(panel,(i%8*256,i//8*212))
    sheet.save(out/'wing_attract_search.png');(out/'wing_attract_search.json').write_text(json.dumps(dict(found=sorted(saved),events=events),ensure_ascii=False,indent=2));print(sorted(saved))

if __name__=='__main__':main()
