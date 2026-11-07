import json
import numpy as np
from PIL import Image
from hd_core import Core,ROOT

def main():
    out=ROOT/'test_current/parts/unknown';out.mkdir(exist_ok=True)
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'save_data');entries=[]
    try:
        for name in ('target','battle_13110','battle_13620','battle_14850'):
            core.load(ROOT/f'test_current/attract/{name}.state')
            for frame in range(90):
                core.run();core.audio.clear();snapshot=core.unknown_snapshot()
                if snapshot is None:continue
                rows,pixels,palettes=snapshot
                for i in np.flatnonzero(rows[:,0]):
                    key,w,h,a,b,c,_,fnv=map(int,rows[i]);idx=pixels[i,:w*h].reshape(h,w);pal=palettes[i].astype('uint32');colors=np.stack([(pal&31)*255//31,((pal>>5)&31)*255//31,((pal>>10)&31)*255//31],-1)
                    filename=f'{key}_{fnv}.png';np.savez_compressed(out/f'{key}_{fnv}.npz',indices=idx,palette=palettes[i]);Image.fromarray(np.dstack([colors[idx].astype('uint8'),(idx!=0).astype('uint8')*255])).save(out/filename)
                    entries.append(dict(scene=name,visible_pixels=int(np.count_nonzero((core.owners==i)&(core.ids==4))),owner_pixels=int(np.count_nonzero(core.owners==i)),identity=[key,fnv],w=w,h=h,x=(b&511) if b&511<256 else (b&511)-512,y=(a&255) if a&255<192 else (a&255)-256,a=a,b=b,c=c,image=filename))
        (out/'inventory.json').write_text(json.dumps(entries,indent=2));print(json.dumps(entries))
    finally:core.close()

if __name__=='__main__':main()
