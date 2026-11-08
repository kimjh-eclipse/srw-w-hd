"""Read-only audit of actual attack objects, including affine/8-bit parts."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json
import numpy as np
from PIL import Image
from hd_core import Core,ROOT,HERE
from scripts.assets.audit_missing_parts import SIZES

def main():
    out=ROOT/'test_current/combat';c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'audit_saves')
    schedule=json.loads((HERE/'demo_input.json').read_text());wanted=[64980,65060,65380,65520,65700,65900];sheet=Image.new('RGB',(768,768));rows=[]
    try:
        c.load(HERE/'demo.state')
        for frame in range(64700,max(wanted)+1):
            c.buttons={e['button'] for e in schedule if e['from']<=frame<e['to']};c.run();c.audio.clear()
            if frame not in wanted:continue
            i=wanted.index(frame);sheet.paste(Image.fromarray(c.native),(i%3*256,i//3*384));objects=[]
            attrs=np.frombuffer(c.obj.raw,'<u2').reshape(128,4)
            for slot,(a,b,col,_) in enumerate(attrs):
                a,b,col=map(int,(a,b,col))
                if (not a&256 and a&512) or a>>14==3 or (a>>10)&3>=2:continue
                w,h=SIZES[a>>14][b>>14];x=b&511;y=a&255
                if x>=256:x-=512
                if y>=192:y-=256
                extent=2 if a&256 and a&512 else 1
                if x>=256 or x+w*extent<=0 or y>=192 or y+h*extent<=0:continue
                objects.append(dict(slot=slot,a=a,b=b,c=col,w=w,h=h,x=x,y=y,eight=bool(a&8192),affine=bool(a&256),binding=int(c.parts[slot,0])))
            rows.append(dict(frame=frame,objects=objects,bg_parts=int(np.count_nonzero(c.bgparts[:,0]))))
        sheet.save(out/'current_battle_native.png');(out/'current_battle_objects.json').write_text(json.dumps(rows,indent=2));print(json.dumps([dict(frame=r['frame'],eight=sum(o['eight'] for o in r['objects']),unmatched=sum(not o['binding'] for o in r['objects']),bg_parts=r['bg_parts']) for r in rows]))
    finally:c.close()

if __name__=='__main__':main()
