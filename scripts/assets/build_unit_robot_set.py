"""One unit's robot drawing set across all its weapons.

Reads test_current/parts/pose_packets/unit_<U>/weapon_*/objects/obj_* and keeps
the objects that are the robot: any sprite bound to the unit's own images
(resource_start..resource_end, secondary_image). Unbound sprites in the same
object (attack-only arms, weapons) come along. Visibility is judged inside
the object (smoke or beams of other palette banks do not hide the robot).

Greedy selection over all weapons picks the fewest poses giving every robot
sprite pixel; a pose must add at least --min-gain sprite texels. The set is
copied to unit_<U>/robot_set/pose_NN/ (native.png, native_4x.png,
contract.json, source.json) with INDEX.json and DRAWING_RULES.md.

  py -3.11 -X utf8 scripts/assets/build_unit_robot_set.py --unit 2
"""
import argparse,json,shutil,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets.build_pose_packets import sprite_pixels
from scripts.assets.build_object_packets import compose_canvas

RULES="""# 그리는 규칙 (Claude 작성)

- 폴더마다 `native_4x.png`(원본 자세를 4배로 확대)를 그대로 깔고, 그 위에 **같은 자리·같은 크기로 덧그리듯** `candidate.png` 를 그립니다. 캔버스 크기는 `native_4x.png` 와 같아야 합니다.
- 원본 실루엣 밖은 **알파 0**. 팔다리·무장의 위치와 윤곽은 원본 그대로, 색은 원본 그대로(다른 팔레트 그림을 다시 칠하지 말 것).
- 겹친 부분은 화면에 보이는 대로(앞에 있는 부품이 앞). Claude 가 앞에 있는 부품의 픽셀만 그 부품으로 떼어 갑니다.
- 같은 기체의 모든 자세는 같은 화풍·같은 디테일로(같은 부품이 자세마다 다르게 그려지면 섞여 보입니다).
- 완료되면 `candidate.png` 만 두면 됩니다. 검수·분할·연결·확인은 Claude.
"""


def unit_tiles(resources):
    """All 8x8 index tiles (and their flips) of the unit's ROM images."""
    from scripts.assets import srw_graphics as g
    rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();off=g.archive(rom);out=set()
    for res in resources:
        try:a=g.pixels(g.decompress(rom[g.BASE+off[res]:g.BASE+off[res+1]]))
        except Exception:continue
        for y in range(0,a.shape[0]-7,8):
            for x in range(0,a.shape[1]-7,8):
                t=np.ascontiguousarray(a[y:y+8,x:x+8]).astype('uint8')
                for v in (t,t[:,::-1],t[::-1],t[::-1,::-1]):out.add(np.ascontiguousarray(v).tobytes())
    return out


def main():
    p=argparse.ArgumentParser();p.add_argument('--unit',type=int,required=True);p.add_argument('--min-gain',type=int,default=48)
    a=p.parse_args()
    catalog=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text(encoding='utf-8'))
    unit=next(u for u in catalog['units'] if u['unit_id']==a.unit)
    own=set(range(unit['resource_start'],unit['resource_end']+1))|{unit.get('secondary_image')}
    lib=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text(encoding='utf-8'))['bindings']
    base=ROOT/f'test_current/parts/pose_packets/unit_{a.unit}'
    # A sprite is the robot's when its 8x8 index tiles come from the unit's own
    # ROM images (independent of what the HD library recorded as source).
    tiles=unit_tiles(sorted(x for x in own if x is not None))
    def is_robot(r):
        idx=sprite_pixels(r);n=hit=0
        for y in range(0,r['h'],8):
            for x in range(0,r['w'],8):
                t=idx[y:y+8,x:x+8]
                if not t.any():continue
                n+=1;hit+=t.tobytes() in tiles
        return n>0 and hit/n>=.8
    found=[];screen_frames={}
    for folder in sorted(base.glob('weapon_*/objects/obj_*')):
        rows=json.loads((folder/'contract.json').read_text(encoding='utf-8'))
        if not any((r['binding_id'] and lib[r['binding_id']-1].get('resource') in own) or is_robot(r) for r in rows):continue
        frames=len(json.loads((folder/'frames.json').read_text())['frames'])
        for r in rows:screen_frames[r['hash']]=screen_frames.get(r['hash'],0)+frames
        found.append((folder,rows))
    # One palette per shape: the one the game shows longest (fade/flash variants
    # of the same shape are not separate drawings).
    shape_of={};main_of={}
    for _,rows in found:
        for r in rows:shape_of[r['hash']]=r['index_hash']
    for h,ih in shape_of.items():
        if ih not in main_of or screen_frames[h]>screen_frames[main_of[ih]]:main_of[ih]=h
    main=set(main_of.values());variants={ih:sorted(h for h,s in shape_of.items() if s==ih) for ih in main_of}
    cands=[];need={}
    for folder,rows in found:
        W,H=Image.open(folder/'native.png').size;_,label=compose_canvas(rows,W,H);gain={}
        for k,r in enumerate(rows):
            if r['hash'] not in main:continue
            x,y,w,h=r['screen_x'],r['screen_y'],r['w'],r['h'];vis=label[y:y+h,x:x+w]==k;op=sprite_pixels(r)>0
            if r['flip_y']:vis=vis[::-1];op=op[::-1]
            if r['flip_x']:vis=vis[:,::-1];op=op[:,::-1]
            need.setdefault(r['hash'],op);gain[r['hash']]=gain.get(r['hash'],np.zeros_like(vis))|vis
        if gain:cands.append((folder,gain,len(rows)))
    covered={h:np.zeros_like(m) for h,m in need.items()};chosen=[]
    while True:
        best=None
        for i,(folder,gain,n) in enumerate(cands):
            if i in chosen:continue
            add=sum(int((v&~covered[h]&need[h]).sum()) for h,v in gain.items())
            if best is None or add>best[1]:best=(i,add)
        if not best or best[1]<a.min_gain:break
        chosen.append(best[0])
        for h,v in cands[best[0]][1].items():covered[h]|=v&need[h]
    ever={h:np.zeros_like(m) for h,m in need.items()}
    for _,gain,_ in cands:
        for h,v in gain.items():ever[h]|=v&need[h]
    out=base/'robot_set'
    if out.exists() and any(out.glob('pose_*/candidate*.png')):sys.exit(f'{out} holds drawings; not rebuilding (move them first)')
    if out.exists():shutil.rmtree(out)
    out.mkdir(parents=True);index=[]
    for n,i in enumerate(chosen):
        folder,gain,count=cands[i];dst=out/f'pose_{n:02d}';dst.mkdir()
        for f in ('native.png','native_4x.png','contract.json','frames.json'):shutil.copy2(folder/f,dst/f)
        (dst/'source.json').write_text(json.dumps(dict(object=str(folder.relative_to(ROOT)).replace('\\','/')),ensure_ascii=False),encoding='utf-8')
        W,H=Image.open(folder/'native.png').size
        rows=json.loads((folder/'contract.json').read_text(encoding='utf-8'))
        index.append(dict(pose=dst.name,source=folder.parent.parent.name+'/'+folder.name,sprites=count,canvas_4x=[W*4,H*4],without_hd=sum(1 for r in rows if not r['binding_id'])))
    total=sum(int(m.sum()) for m in need.values());vis=sum(int(m.sum()) for m in ever.values());got=sum(int(m.sum()) for m in covered.values())
    (out/'SHAPES.json').write_text(json.dumps(dict(main_palette={str(ih):h for ih,h in main_of.items()},variants={str(ih):v for ih,v in variants.items()}),ensure_ascii=False,indent=1),encoding='utf-8')
    summary=dict(unit=a.unit,name=unit.get('name_ja'),robot_objects_seen=len(found),shapes=len(main_of),palette_variants_skipped=len(shape_of)-len(main_of),poses=len(chosen),sprites=len(need),sprite_texels=total,
        visible_somewhere=vis,covered_by_set=got,set_share_of_visible=round(got/max(vis,1),4),never_visible=total-vis,poses_list=index)
    (out/'INDEX.json').write_text(json.dumps(summary,ensure_ascii=False,indent=1),encoding='utf-8');(out/'DRAWING_RULES.md').write_text(RULES,encoding='utf-8')
    print({k:v for k,v in summary.items() if k!='poses_list'})


if __name__=='__main__':main()
