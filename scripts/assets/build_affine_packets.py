"""Drawing packets for scaled/rotated (affine) robot sprites, which build_pose_packets skips.

The DS draws an affine OBJ from its normal texture through a 2x2 matrix, so the
HD part is drawn upright in texture space and the renderer applies the matrix
at run time (emulator/hd_parts.py). Here every attack start state of the unit is
replayed; per frame the affine sprites sharing one matrix form one object. Each
sprite is placed in texture space (its screen-centre offset from the first
sprite mapped through the matrix), un-transformed, so the object is one upright
picture. Objects already fully bound to HD, and effect-only objects (no palette
shared with the unit's own robot set), are skipped.

Each new object becomes a robot-set pose folder robot_set/pose_aNN/ in the same
format as the other poses (native.png, native_4x.png, contract.json with
texture-space positions and no flips, frames.json, source.json), so drawing
sheets, splitting, fitting, review and install treat it like any pose. A
screen.png (the frame as shown) is kept for reference.

  py -3.11 -X utf8 scripts/assets/build_affine_packets.py <unit> [--frames 0:1500:2] [--dry]
"""
import argparse,json,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]));sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'emulator'))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image
from scripts.assets.capture_rendered_obj_contract import capture_rendered_obj_contracts
from scripts.assets.build_object_packets import compose_canvas

TOP_H=192;MARGIN=8;S=4
STATES=ROOT/'test_current/gui/unit_review/attack_starts'
BASE=ROOT/'test_current/parts/pose_packets'


def texture_layout(group):
    """Texture-space top-left of each sprite of one affine object (first sprite at 0,0)."""
    a,b,c,d=[v/256 for v in group[0]['affine_matrix_8_8']]
    def centre(r):
        k=2 if r['affine_double'] else 1
        return r['screen_x']+r['w']*k/2,r['screen_y']+r['h']*k/2
    cx0,cy0=centre(group[0]);out=[]
    for r in group:
        cx,cy=centre(r);dx,dy=cx-cx0,cy-cy0
        tx,ty=a*dx+b*dy,c*dx+d*dy   # screen offset -> texture offset
        out.append((round(tx-r['w']/2+group[0]['w']/2),round(ty-r['h']/2+group[0]['h']/2)))
    return out


def scale_of(r):
    a,b,c,d=[v/256 for v in r['affine_matrix_8_8']]
    det=abs(a*d-b*c);return 1/math.sqrt(det) if det else 0   # screen size / texture size


def main():
    p=argparse.ArgumentParser();p.add_argument('unit',type=int);p.add_argument('--frames',default='0:1500:2');p.add_argument('--dry',action='store_true')
    a=p.parse_args();lo,hi,step=map(int,a.frames.split(':'))
    rs=BASE/f'unit_{a.unit}/robot_set'
    # palettes of the unit's own (non-affine) robot sprites: an affine object using none of them is an effect
    body=set();normal_hashes=set()
    for c in rs.glob('pose_[0-9]*/contract.json'):
        for r in json.loads(c.read_text(encoding='utf-8')):body.add(tuple(r['palette_15bit']));normal_hashes.add(r['hash'])
    from hd_core import Core
    objs={}
    # Attack starts of the weapons whose capture skipped affine sprites; rebuilt when pruned.
    from attack_start import build_in_child
    wanted=[]
    for idx in sorted(BASE.glob(f'unit_{a.unit}/weapon_*/INDEX.json')):
        d=json.loads(idx.read_text(encoding='utf-8'))
        if d.get('affine_skipped',0)>0:wanted.append(int(idx.parent.name.split('_')[1]))
    states=[]
    for w in wanted:
        st=STATES/f'unit_{a.unit}_weapon_{w}.state'
        if not st.exists():
            r=build_in_child(ROOT,ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',a.unit,w,st)
            if not r.get('ok'):print('no start',a.unit,w,r.get('reason'),flush=True);continue
        states.append(st)
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=BASE/f'unit_{a.unit}/affine_saves') if states else None   # one core per process
    for st in states:
        core.load(st);print('state',st.name,'body palettes',len(body),flush=True);seen=0
        for f in range(hi):
            if not core.run():continue
            core.audio.clear()
            if f<lo or (f-lo)%step:continue
            rows=[r for r in capture_rendered_obj_contracts(core,state=st.name,frame=f) if r['affine'] and r['screen_y']<TOP_H];seen+=len(rows)
            groups={}
            for r in rows:groups.setdefault((tuple(r['affine_matrix_8_8']),r['palette_bank']),[]).append(r)   # one object: same matrix and palette
            for g in groups.values():
                g.sort(key=lambda r:r['oam'])
                if all(r['binding_id'] for r in g):continue
                if body and not any(tuple(r['palette_15bit']) in body for r in g):continue
                # every texture already drawn in the normal poses: their HD covers the scaled view too
                if all(r['hash'] in normal_hashes for r in g):continue
                pos=texture_layout(g)
                key=tuple(sorted(r['hash'] for r in g))   # same sprites = same object at any scale
                sc=scale_of(g[0])
                o=objs.setdefault(key,dict(rows=g,pos=pos,frames=[],state=st.name,best=None))
                o['frames'].append(f)
                # layout from the frame shown closest to 1:1 (least rounding)
                if o['best'] is None or abs(math.log(max(sc,1e-3)))<abs(math.log(max(o['best'][0],1e-3))):
                    o['best']=(sc,f,None);o['rows']=g;o['pos']=pos
        print('affine sprites seen',seen,flush=True)
    if core:core.close()
    print('unit',a.unit,'affine objects',len(objs),[(len(o['rows']),len(o['frames'])) for o in objs.values()][:12],flush=True)
    if a.dry or not objs:return
    for old in rs.glob('pose_a*'):
        if not (old/'candidate.png').exists():
            for f in old.iterdir():f.unlink()
            old.rmdir()
    for n,(key,o) in enumerate(sorted(objs.items(),key=lambda kv:-len(kv[1]['frames']))):
        rows,pos=o['rows'],o['pos']
        x0=min(x for x,_ in pos);y0=min(y for _,y in pos)
        W=max(x+r['w'] for r,(x,_) in zip(rows,pos))-x0+2*MARGIN;H=max(y+r['h'] for r,(_,y) in zip(rows,pos))-y0+2*MARGIN
        crow=[]
        for r,(x,y) in zip(rows,pos):
            c=dict(r);c.update(screen_x=x-x0+MARGIN,screen_y=y-y0+MARGIN,flip_x=False,flip_y=False);crow.append(c)
        rgba,label=compose_canvas(crow,W,H)
        folder=rs/f'pose_a{n:02d}';folder.mkdir(exist_ok=True)
        Image.fromarray(rgba).save(folder/'native.png');Image.fromarray(rgba).resize((W*S,H*S),Image.Resampling.NEAREST).save(folder/'native_4x.png')
        keep=('oam','screen_x','screen_y','w','h','flip_x','flip_y','priority','palette_bank','hash','index_hash','material','binding_id','index_pixels','palette_15bit','original_palette_rgb','eight_bit')
        contract=[]
        for k,c in enumerate(crow):
            opaque=int((label==k).sum()) if False else None
            d={kk:c.get(kk) for kk in keep}
            vis=int((label==k).sum());from scripts.assets.build_pose_packets import sprite_pixels
            op=int((sprite_pixels(c)>0).sum());d.update(opaque=op,visible=vis,visible_share=round(vis/max(op,1),3),affine=True)
            contract.append(d)
        (folder/'contract.json').write_text(json.dumps(contract,ensure_ascii=False),encoding='utf-8')
        (folder/'frames.json').write_text(json.dumps(o['frames']),encoding='utf-8')
        (folder/'source.json').write_text(json.dumps(dict(affine=True,state=o['state'],reference_frame=o['best'][1],scale=round(o['best'][0],3))),encoding='utf-8')
        if o['best'][2] is not None:Image.fromarray(np.asarray(o['best'][2])).save(folder/'screen.png')
    print('written',len(objs),'affine poses to',rs)


if __name__=='__main__':main()
