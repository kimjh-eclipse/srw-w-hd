import json,time
import numpy as np
from PIL import Image
from hd_core import Core,ROOT
from hd_map_tiles import MapTilesRenderer

def main():
    out=ROOT/'test_current/map_tiles';r=MapTilesRenderer();c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'verify_saves');rows=[]
    try:
        for name in ['map_fresh','grid','menu_step_0','menu_step_1','menu_step_2','menu_step_3','menu_step_4','menu_step_5']:
            c.load(ROOT/f'test_current/font/{name}.state');c.run();native=c.native[192:];image=Image.fromarray(native).resize((1440,1080),Image.Resampling.NEAREST)
            r.compose(image,native);first=r.last_ms
            image.save(out/(name+'_hd.png'));assert r.last_matches,name
            grid=Image.fromarray(np.all(native<8,axis=2).astype('uint8')*255).resize(image.size,Image.Resampling.NEAREST)
            before=np.asarray(Image.fromarray(native).resize(image.size,Image.Resampling.NEAREST));after=np.asarray(image)
            assert not np.any(np.any(before!=after,axis=2)&(np.asarray(grid)>0)),'grid must remain native'
            times=[]
            for _ in range(20):r.compose(image,native);times.append(r.last_ms)
            rows.append(dict(state=name,matches=r.last_matches,cold_ms=round(first,3),warm_mean_ms=round(float(np.mean(times)),3)))
        (out/'verification.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows))
    finally:c.close()

if __name__=='__main__':main()
