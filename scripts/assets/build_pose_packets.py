"""Whole-pose drawing packets from live battle frames.

Plays an attack start state (emulator/attack_start.py cache), captures every
rendered OBJ (all sprites, with or without HD: capture_rendered_obj_contract)
each frame, groups frames with the same sprite layout into poses and writes,
per pose, under <out>/pose_NNN/:

  native.png      the pose as the game composes it (OBJ only, 256x192, alpha 0 elsewhere)
  native_4x.png   same, nearest 4x - the canvas the drawing must match exactly
  labels.png      per pixel, which sprite is in front (colour = sprite), for review
  contract.json   one row per sprite: screen box, flips, priority, hash/index hash,
                  palette, index pixels, binding id (0 = no HD yet), visible share
  frames.json     the frames that show this pose

Codex draws candidate.png (1024x768, the pose at 4x over native_4x.png,
alpha 0 outside the pose). split_pose_drawing() then cuts each sprite back out
(un-flipped to texture orientation) so every part gets its HD from one
consistent picture.

  py -3.11 -X utf8 scripts/assets/build_pose_packets.py --state <file> --out <dir> [--frames 0:1500:5]
"""
import argparse,base64,json,sys,zlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]));sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'emulator'))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image
from scripts.assets.capture_rendered_obj_contract import capture_rendered_obj_contracts

TOP_H=192


def sprite_pixels(r):
    idx=np.frombuffer(zlib.decompress(base64.b64decode(r['index_pixels'])),dtype='uint8').reshape(r['h'],r['w'])
    if r['flip_x']:idx=idx[:,::-1]
    if r['flip_y']:idx=idx[::-1]
    return idx


def compose(rows):
    """Front-to-back as the DS draws OBJ: lower priority value in front, then lower OAM index."""
    rgba=np.zeros((TOP_H,256,4),'uint8');label=np.full((TOP_H,256),-1,'int16')
    order=sorted(range(len(rows)),key=lambda k:(rows[k]['priority'],rows[k]['oam']))
    for k in order:
        r=rows[k];idx=sprite_pixels(r);pal=np.array(r['original_palette_rgb'],dtype='uint8')
        x,y,w,h=r['screen_x'],r['screen_y'],r['w'],r['h']
        x0,y0=max(0,x),max(0,y);x1,y1=min(256,x+w),min(TOP_H,y+h)
        if x1<=x0 or y1<=y0:continue
        sub=idx[y0-y:y1-y,x0-x:x1-x];free=(label[y0:y1,x0:x1]<0)&(sub>0)
        label[y0:y1,x0:x1][free]=k
        rgba[y0:y1,x0:x1][free]=np.concatenate([pal[sub[free]],np.full((int(free.sum()),1),255,'uint8')],1)
    return rgba,label


def main():
    p=argparse.ArgumentParser();p.add_argument('--state',required=True,type=Path);p.add_argument('--out',required=True,type=Path)
    p.add_argument('--frames',default='0:1500:5');p.add_argument('--min-sprites',type=int,default=3)
    a=p.parse_args();lo,hi,step=map(int,a.frames.split(':'))
    from hd_core import Core
    a.out.mkdir(parents=True,exist_ok=True)
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=a.out/'isolated_saves')
    core.load(a.state)
    poses={};skipped_affine=0
    for f in range(hi):
        if not core.run():continue
        core.audio.clear()
        if f<lo or (f-lo)%step:continue
        rows=[r for r in capture_rendered_obj_contracts(core,state=a.state.name,frame=f) if r['screen_y']<TOP_H]
        affine=[r for r in rows if r['affine']];skipped_affine+=len(affine)
        rows=[r for r in rows if not r['affine']]
        if len(rows)<a.min_sprites:continue
        key=tuple(sorted((r['hash'],r['screen_x'],r['screen_y'],r['flip_x'],r['flip_y']) for r in rows))
        if key in poses:poses[key]['frames'].append(f);continue
        poses[key]=dict(rows=rows,frames=[f])
    core.close()
    index=[]
    for n,(key,pose) in enumerate(sorted(poses.items(),key=lambda kv:kv[1]['frames'][0])):
        folder=a.out/f'pose_{n:03d}';folder.mkdir(exist_ok=True)
        rows=pose['rows'];rgba,label=compose(rows)
        Image.fromarray(rgba).save(folder/'native.png');Image.fromarray(rgba).resize((1024,768),Image.Resampling.NEAREST).save(folder/'native_4x.png')
        colours=np.random.default_rng(1).integers(40,255,(len(rows)+1,3)).astype('uint8');lab=np.zeros((TOP_H,256,3),'uint8');lab[label>=0]=colours[label[label>=0]]
        Image.fromarray(lab).save(folder/'labels.png')
        contract=[]
        for k,r in enumerate(rows):
            opaque=int((sprite_pixels(r)>0).sum());visible=int((label==k).sum())
            contract.append({key:r[key] for key in ('oam','screen_x','screen_y','w','h','flip_x','flip_y','priority','palette_bank','hash','index_hash','material',
                'binding_id','index_pixels','palette_15bit','original_palette_rgb','eight_bit')}|dict(opaque=opaque,visible=visible,visible_share=round(visible/max(opaque,1),3)))
        (folder/'contract.json').write_text(json.dumps(contract,ensure_ascii=False),encoding='utf-8')
        (folder/'frames.json').write_text(json.dumps(pose['frames']),encoding='utf-8')
        hidden=[c for c in contract if c['visible_share']<.98]
        index.append(dict(pose=folder.name,frames=len(pose['frames']),first=pose['frames'][0],sprites=len(rows),
            with_hd=sum(1 for c in contract if c['binding_id']),partly_hidden=len(hidden),fully_hidden=sum(1 for c in contract if c['visible']==0)))
    parts={}
    for i,(key,pose) in enumerate(sorted(poses.items(),key=lambda kv:kv[1]['frames'][0])):
        for r in pose['rows']:parts.setdefault(r['hash'],[]).append(i)
    summary=dict(state=str(a.state),frames=a.frames,poses=len(index),unique_sprites=len(parts),affine_skipped=skipped_affine,poses_list=index)
    (a.out/'INDEX.json').write_text(json.dumps(summary,ensure_ascii=False,indent=1),encoding='utf-8')
    print('poses',len(index),'unique sprites',len(parts),'affine skipped',skipped_affine)
    for e in index[:60]:print(e)


if __name__=='__main__':main()
