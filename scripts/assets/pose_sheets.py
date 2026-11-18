"""Split a robot set into drawing sheets of at most N poses, each with the base pose.

A generator gives one picture of limited size; with many poses on one sheet
each pose gets few pixels. Sheets keep each at about 4 drawn px per native px.
Every sheet also carries the unit's base pose (the pose seen in the most
frames, i.e. its standing pose), so all sheets share one reference and stay
in one style.

  build <set> [--per 8]
      -> <set>/SHEETS/sheet_NN/native_sheet_4x.png, guide_labels.png, layout.json,
         plus <set>/SHEETS/INDEX.json and DRAWING_RULES.md
         layout.json: {"sheet":[W,H],"base_pose":"pose_KK",
                       "layout":[{"pose":"pose_00","sheet_origin":[x,y],"source_canvas":[w,h]}]}
  split <set>
      -> cuts every SHEETS/sheet_NN/candidate_sheet.png into pose_NN/candidate.png
         (base pose from the first sheet that has a drawing; older candidate.png
         kept as candidate_vN.png). A drawing smaller than the sheet is scaled up
         first (aspect within 1%).

  py -3.11 -X utf8 scripts/assets/pose_sheets.py build test_current/parts/pose_packets/unit_5/robot_set
"""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw

GAP=48

RULES="""# 기체 시트 그리기 규칙 (Claude 작성)

- 이 기체의 자세를 여러 장(`sheet_01`, `sheet_02` …)으로 나눴습니다. 한 장에 기본 자세 포함 최대 9자세(3×3)라 자세마다 충분한 해상도를 받습니다.
- **모든 장에 같은 기본 자세(`base_pose`, 장마다 첫 칸)가 들어 있습니다.** 이 기본 자세를 기준으로 모든 장을 같은 화풍·같은 디테일·같은 색으로 그려 주세요. 같은 부품은 모든 자세·모든 장에서 같은 모양입니다.
- 장마다 `native_sheet_4x.png` 와 같은 크기(또는 같은 비율로 줄인 크기)의 `candidate_sheet.png` 한 장. 원본 위에 같은 자리·같은 크기로 덧그리듯, 자세 사이 여백과 실루엣 밖은 알파 0, 원본 색 그대로(재색칠 금지), 글자 넣지 않기.
- 생성 원본은 같은 폴더 `generated_sheet.png`. 자르기·정합·분할·설치·게임 확인은 Claude.
"""


def frames_of(pose):
    f=json.loads((pose/'frames.json').read_text())
    return len(f['frames']) if isinstance(f,dict) else len(f)


def build(root,per,affine_only=False):
    poses=sorted(d for d in root.glob('pose_*') if d.is_dir())
    normal=[p for p in poses if not p.name.startswith('pose_a')]
    base=max(normal or poses,key=frames_of)
    if affine_only:   # scaled/rotated objects: their own sheets, with the unit's base pose for style
        rest=[p for p in poses if p.name.startswith('pose_a')];prefix='sheet_a'
    else:rest=[p for p in normal if p!=base];prefix='sheet_'
    groups=[rest[i:i+per-1] for i in range(0,len(rest),per-1)] or [[]]
    out=root/'SHEETS';out.mkdir(exist_ok=True);index=[]
    for n,group in enumerate(groups,1):
        items=[base]+group;ims=[(p.name,Image.open(p/'native_4x.png').convert('RGBA')) for p in items]
        cols=min(3,len(ims));rows=[ims[i:i+cols] for i in range(0,len(ims),cols)]
        colw=[max((r[c][1].width for r in rows if c<len(r)),default=0) for c in range(cols)];rowh=[max(im.height for _,im in r) for r in rows]
        W=sum(colw)+GAP*(cols+1);H=sum(rowh)+GAP*(len(rows)+1)
        sheet=Image.new('RGBA',(W,H));guide=Image.new('RGBA',(W,H));d=ImageDraw.Draw(guide);layout=[];y=GAP
        for r,row in enumerate(rows):
            x=GAP
            for c,(name,im) in enumerate(row):
                sheet.alpha_composite(im,(x,y));layout.append(dict(pose=name,sheet_origin=[x,y],source_canvas=[im.width,im.height]))
                d.rectangle((x-2,y-2,x+im.width+1,y+im.height+1),outline=(255,200,0,255));d.text((x,y-14),name+(' (base)' if name==base.name else ''),fill=(255,200,0,255))
                x+=colw[c]+GAP
            y+=rowh[r]+GAP
        folder=out/f'{prefix}{n:02d}';folder.mkdir(exist_ok=True)
        sheet.save(folder/'native_sheet_4x.png');guide.save(folder/'guide_labels.png')
        (folder/'layout.json').write_text(json.dumps(dict(sheet=[W,H],base_pose=base.name,layout=layout),indent=1),encoding='utf-8')
        index.append(dict(sheet=folder.name,poses=len(items),size=[W,H]))
    if affine_only:
        (out/'INDEX_AFFINE.json').write_text(json.dumps(dict(base_pose=base.name,per_sheet=per,sheets=index,note='scaled/rotated objects drawn upright; the game applies the scale/rotation'),indent=1),encoding='utf-8');return
    (out/'INDEX.json').write_text(json.dumps(dict(base_pose=base.name,per_sheet=per,sheets=index),indent=1),encoding='utf-8');(out/'DRAWING_RULES.md').write_text(RULES,encoding='utf-8')
    print(root.parent.name,'poses',len(poses),'base',base.name,'sheets',len(index),[s['size'] for s in index])


BAD_TAGS=('reject','held','hold','before','draft','failed','wrong','previous')


HELD_POSES={}   # drawing folder (lower-case path) -> poses its STYLE_VERSION holds


def packet_folders(sheets_dir):
    """Codex repair packets that mix poses of several sheets sit beside the
    sheets (SHEETS/QA_<date>/packet_NN/ with their own layout.json)."""
    out=[]
    if not sheets_dir.is_dir():return out
    for d in sorted(sheets_dir.iterdir()):
        if d.is_dir() and not d.name.startswith('sheet_') and not any(t in d.name.lower() for t in BAD_TAGS):
            out+=[d]+sorted(x for x in d.rglob('*') if x.is_dir() and not any(t in x.name.lower() for t in BAD_TAGS))
    # Single-pose repairs delivered in the robot set itself (qa_partial_pose_NN_<date>/).
    for d in sorted(sheets_dir.parent.glob('qa_*')):
        if d.is_dir() and not any(t in d.name.lower() for t in BAD_TAGS):
            out+=[d]+sorted(x for x in d.rglob('*') if x.is_dir() and not any(t in x.name.lower() for t in BAD_TAGS))
    # Any folder a PREFERRED*.json names (e.g. shared_<unit>_<date>/poseNN/).
    rs=sheets_dir.parent.resolve()
    for _,c,_l in preferred_entries(sheets_dir.parent):
        try:c.parent.resolve().relative_to(rs)
        except ValueError:continue
        if c.parent not in out:out.append(c.parent)
    return out


def preferred_entries(rs):
    """(pose, drawing, layout) Codex named in PREFERRED*.json, oldest file first:
    pose_mapping {pose:{candidate_path,layout_path}} or {candidate, layout, targets}."""
    out=[]
    # Correction files override delivery files; within each kind the newer wins.
    for f in sorted(rs.glob('PREFERRED*.json'),key=lambda f:('CORRECTION' in f.name.upper(),f.stat().st_mtime)):
        try:d=json.loads(f.read_text(encoding='utf-8'))
        except Exception:continue
        # Any other object naming a drawing and its layout (top level or nested,
        # e.g. {"new_motion_plate": {candidate_path, layout_path}}): its targets,
        # or every pose of that layout.
        def walk(o,top=False):
            if isinstance(o,dict):
                c=o.get('candidate_path') or o.get('candidate');l=o.get('layout_path') or o.get('layout')
                if isinstance(c,str) and c.endswith('.png') and not isinstance(l,str) and o.get('targets'):
                    l=str(Path(c).parent/'layout.json')   # a correction naming only the drawing: its folder's layout
                if isinstance(c,str) and isinstance(l,str) and c.endswith('.png') and l.endswith('.json'):
                    poses=o.get('targets');explicit=bool(poses)
                    if not poses:
                        try:poses=[e['pose'] for e in json.loads(Path(l).read_text(encoding='utf-8')).get('layout',[])]
                        except Exception:poses=[]
                    for pose in poses:out.append((pose,Path(c),Path(l),explicit))
                # paired keys: "<name>_candidate" + "<name>_layout"
                for k,v in o.items():
                    if k.endswith('_candidate') and isinstance(v,str) and isinstance(o.get(k[:-10]+'_layout'),str):
                        walk({'candidate_path':v,'layout_path':o[k[:-10]+'_layout']})
                for k,v in o.items():
                    if k!='pose_mapping':walk(v)
            elif isinstance(o,list):
                for v in o:walk(v)
        mark=len(out);walk(d)
        # A pose that several plates of one file carry (the shared base pose)
        # names no single drawing: leave it to the newest-drawing rule.
        # Explicit "targets" entries are kept in file order (a later plate
        # supersedes an earlier one); layout-derived ones only when unambiguous.
        seen={}
        for pose,c,_l,ex in out[mark:]:
            if not ex:seen.setdefault(pose,set()).add(str(c).lower())
        out[mark:]=[e[:3] for e in out[mark:] if e[3] or len(seen[e[0]])==1]
        # pose_mapping is the most specific: it wins over plates named in the same file.
        for pose,m in (d.get('pose_mapping') or {}).items():
            if isinstance(m,dict) and m.get('candidate_path'):out.append((pose,Path(m['candidate_path']),Path(str(m.get('layout_path','')))))
    return [e for e in out if e[1].exists()]


def unit_sources(rs):
    """All usable (drawing, layout) pairs of a robot set: per official sheet,
    or the repair packets alone when the unit has no sheet_NN (it was drawn
    as one unified sheet before)."""
    officials=sorted(rs.glob('SHEETS/sheet_*'))
    if officials:return [x for o in officials for x in drawing_sources(o)]
    return drawing_sources(None,rs/'SHEETS')


def drawing_sources(official,sheets_dir=None):
    """(drawing, layout) pairs for one sheet: the official sheet first, then
    Codex's alternate layouts (candidate_sheet_<tag>.png + layout_<tag>.json in
    the folder, or ALT*/alt*/plate subfolders), skipping held/rejected ones."""
    out=[]
    if official is None:folders=packet_folders(sheets_dir)
    else:
        folders=[official]+sorted(d for d in official.rglob('*') if d.is_dir() and not any(t in d.name.lower() for t in BAD_TAGS))
        folders+=packet_folders(official.parent)
    for folder in folders:
        sv=folder/'STYLE_VERSION.json'
        if sv.exists():
            try:
                d=json.loads(sv.read_text(encoding='utf-8'));st=' '.join(str(v) for k,v in d.items() if isinstance(v,str) and any(w in k.lower() for w in ('status','hold','check','install'))).lower().replace('hold_released','').replace('hold released','')
                # "partial_candidate_pose12_delivered_pose00_held": only the named poses are held.
                import re
                part=re.findall(r'pose_?(\d+)_held',st)
                if part and 'delivered' in st and d.get('do_not_install') is not True and 'reject' not in st:
                    HELD_POSES[str(folder.resolve()).lower()]={f'pose_{int(n):02d}' for n in part}
                elif d.get('do_not_install') is True or 'reject' in st or 'hold' in st or 'held' in st:continue
            except Exception:pass
        for lay in sorted(folder.glob('*layout*.json')):   # layout.json, layout_<tag>.json, shared_layout.json
            st=lay.stem
            if 'layout' not in st:continue   # Windows glob ignores case: LAYOUT_ORIGIN_*.json etc. are not layouts
            tag=st.split('layout',1)[1]
            if any(t in lay.stem.lower() for t in BAD_TAGS):continue
            try:
                if 'layout' not in json.loads(lay.read_text(encoding='utf-8')):continue   # not a pose layout (other Codex metadata)
            except Exception:continue
            for name in (f'candidate_sheet{tag}.png',f'generated_sheet{tag}.png','candidate_sheet.png','generated_sheet.png'):
                if (folder/name).exists():out.append((folder/name,lay));break
    out.sort(key=lambda s:-s[0].stat().st_mtime)   # newest drawing of a pose wins (Codex repairs come later)
    return out


def register_by_content(art,folder,W,H):
    """A drawing output in another aspect (the generator pads to its own
    frame) is placed back on the W x H sheet by matching the drawn content's
    bounding box to the native sheet's: one uniform scale and an offset. None
    when the native sheet is missing or the two boxes do not agree in shape."""
    import numpy as np
    nat=folder/'native_sheet_4x.png'
    if not nat.exists():return None
    n=np.asarray(Image.open(nat).convert('RGBA'))[:,:,3]>20;c=np.asarray(art)[:,:,3]>20
    if n.shape!=(H,W) or not n.any() or not c.any():return None
    def box(m):
        ys,xs=np.where(m);return xs.min(),ys.min(),xs.max()+1,ys.max()+1
    nx0,ny0,nx1,ny1=box(n);cx0,cy0,cx1,cy1=box(c)
    sx=(cx1-cx0)/(nx1-nx0);sy=(cy1-cy0)/(ny1-ny0)
    if abs(sx/sy-1)>=.06:return None
    s=(sx+sy)/2
    # the native sheet frame expressed in drawing pixels
    left,top=cx0-nx0*s,cy0-ny0*s
    sheet=Image.new('RGBA',(round(W*s),round(H*s)))
    sheet.alpha_composite(art,(round(-left),round(-top))) if left<=0 and top<=0 else sheet.paste(art,(round(-left),round(-top)),art)
    return sheet


def preferred_poses(root):
    """pose -> drawing Codex named for it in PREFERRED_DELIVERY*.json
    (pose_mapping), kept only when that drawing is a usable source."""
    usable={c.resolve() for c,_ in unit_sources(root)};pref={}
    for pose,c,_l in preferred_entries(root):
        if c.resolve() in usable:pref[pose]=c.resolve()
    return pref


def split(root):
    out=root/'SHEETS';done=set();n_out=0
    pref=preferred_poses(root)   # Codex's named drawing for a pose beats a newer file elsewhere
    officials=sorted(out.glob('sheet_*')) or [None]   # None: repair packets only (no sheet_NN)
    for official in officials:
        official_lay=json.loads((official/'layout.json').read_text(encoding='utf-8')) if official else {'layout':[]}
        cuts={}
        for cand,layf in (drawing_sources(official) if official else drawing_sources(None,out)):
            lay=json.loads(layf.read_text(encoding='utf-8'));W,H=lay['sheet']
            art=Image.open(cand).convert('RGBA')
            if abs((art.width/W)/(art.height/H)-1)>=.06:
                art=register_by_content(art,layf.parent,W,H)
                if art is None:print('skip (aspect)',cand,(W,H));continue
                print('registered by content',cand)
            if art.size!=(W,H):art=art.resize((W,H),Image.Resampling.LANCZOS)
            for e in lay['layout']:
                if e['pose'] in done or not (root/e['pose']).is_dir():continue
                if e['pose'] in HELD_POSES.get(str(cand.parent.resolve()).lower(),()):continue
                if e['pose'] in pref and pref[e['pose']]!=cand.resolve():continue
                x,y=e['sheet_origin'];w,h=e['source_canvas'];pose=root/e['pose'];dst=pose/'candidate.png'
                if list(Image.open(pose/'native_4x.png').size)!=[w,h]:print('skip (canvas)',e['pose'],cand);continue
                if dst.exists():
                    k=1
                    while (pose/f'candidate_v{k}.png').exists():k+=1
                    dst.replace(pose/f'candidate_v{k}.png')
                    if (pose/'candidate_fit.png').exists():(pose/'candidate_fit.png').replace(pose/f'candidate_fit_v{k}.png')
                piece=art.crop((x,y,x+w,y+h));piece.save(dst);cuts[e['pose']]=piece;done.add(e['pose']);n_out+=1
        # Poses of this sheet that no usable (non-held) drawing covers: a
        # candidate.png left from an earlier cut came from a held drawing.
        for e in official_lay['layout']:
            if e['pose'] in done:continue
            pose=root/e['pose']
            if (pose/'candidate.png').exists():
                k=1
                while (pose/f'candidate_held_v{k}.png').exists():k+=1
                (pose/'candidate.png').replace(pose/f'candidate_held_v{k}.png')
                (pose/'candidate_fit.png').unlink(missing_ok=True);print('cleared (held source)',e['pose'])
        # The cut poses back in the official layout, for the eye-review sheet.
        if cuts and official:   # always: the review must show the drawing actually cut (newest repair), not the official sheet
            W,H=official_lay['sheet'];sheet=Image.new('RGBA',(W,H))
            for e in official_lay['layout']:
                if e['pose'] in cuts:sheet.alpha_composite(cuts[e['pose']],tuple(e['sheet_origin']))
            sheet.save(official/'candidate_sheet_assembled.png')
    print('poses cut',n_out)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('cmd');p.add_argument('root',type=Path);p.add_argument('--per',type=int,default=9);p.add_argument('--affine',action='store_true')
    a=p.parse_args()
    build(a.root,a.per,a.affine) if a.cmd=='build' else split(a.root)
