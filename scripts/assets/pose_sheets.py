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


def build(root,per):
    poses=sorted(d for d in root.glob('pose_*') if d.is_dir())
    base=max(poses,key=frames_of);rest=[p for p in poses if p!=base]
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
        folder=out/f'sheet_{n:02d}';folder.mkdir(exist_ok=True)
        sheet.save(folder/'native_sheet_4x.png');guide.save(folder/'guide_labels.png')
        (folder/'layout.json').write_text(json.dumps(dict(sheet=[W,H],base_pose=base.name,layout=layout),indent=1),encoding='utf-8')
        index.append(dict(sheet=folder.name,poses=len(items),size=[W,H]))
    (out/'INDEX.json').write_text(json.dumps(dict(base_pose=base.name,per_sheet=per,sheets=index),indent=1),encoding='utf-8');(out/'DRAWING_RULES.md').write_text(RULES,encoding='utf-8')
    print(root.parent.name,'poses',len(poses),'base',base.name,'sheets',len(index),[s['size'] for s in index])


BAD_TAGS=('reject','held','hold','before','draft','failed','wrong','previous')


def drawing_sources(official):
    """(drawing, layout) pairs for one sheet: the official sheet first, then
    Codex's alternate layouts (candidate_sheet_<tag>.png + layout_<tag>.json in
    the folder, or ALT*/alt*/plate subfolders), skipping held/rejected ones."""
    out=[]
    folders=[official]+sorted(d for d in official.rglob('*') if d.is_dir() and not any(t in d.name.lower() for t in BAD_TAGS))
    for folder in folders:
        sv=folder/'STYLE_VERSION.json'
        if folder!=official and sv.exists():
            try:
                d=json.loads(sv.read_text(encoding='utf-8'));st=str(d.get('review_status','')).lower()
                if d.get('do_not_install') is True or 'reject' in st or 'hold' in st:continue
            except Exception:pass
        for lay in sorted(folder.glob('layout*.json')):
            tag=lay.stem[len('layout'):]
            if any(t in tag.lower() for t in BAD_TAGS):continue
            for name in (f'candidate_sheet{tag}.png',f'generated_sheet{tag}.png','candidate_sheet.png','generated_sheet.png'):
                if (folder/name).exists():out.append((folder/name,lay));break
    return out


def split(root):
    out=root/'SHEETS';done=set();n_out=0
    for official in sorted(out.glob('sheet_*')):
        official_lay=json.loads((official/'layout.json').read_text(encoding='utf-8'))
        cuts={}
        for cand,layf in drawing_sources(official):
            lay=json.loads(layf.read_text(encoding='utf-8'));W,H=lay['sheet']
            art=Image.open(cand).convert('RGBA')
            if abs((art.width/W)/(art.height/H)-1)>=.01:print('skip (aspect)',cand,art.size,(W,H));continue
            if art.size!=(W,H):art=art.resize((W,H),Image.Resampling.LANCZOS)
            for e in lay['layout']:
                if e['pose'] in done:continue
                x,y=e['sheet_origin'];w,h=e['source_canvas'];pose=root/e['pose'];dst=pose/'candidate.png'
                if list(Image.open(pose/'native_4x.png').size)!=[w,h]:print('skip (canvas)',e['pose'],cand);continue
                if dst.exists():
                    k=1
                    while (pose/f'candidate_v{k}.png').exists():k+=1
                    dst.replace(pose/f'candidate_v{k}.png')
                    if (pose/'candidate_fit.png').exists():(pose/'candidate_fit.png').replace(pose/f'candidate_fit_v{k}.png')
                piece=art.crop((x,y,x+w,y+h));piece.save(dst);cuts[e['pose']]=piece;done.add(e['pose']);n_out+=1
        # The cut poses back in the official layout, for the eye-review sheet.
        if cuts and not (official/'candidate_sheet.png').exists():
            W,H=official_lay['sheet'];sheet=Image.new('RGBA',(W,H))
            for e in official_lay['layout']:
                if e['pose'] in cuts:sheet.alpha_composite(cuts[e['pose']],tuple(e['sheet_origin']))
            sheet.save(official/'candidate_sheet_assembled.png')
    print('poses cut',n_out)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('cmd');p.add_argument('root',type=Path);p.add_argument('--per',type=int,default=9)
    a=p.parse_args()
    build(a.root,a.per) if a.cmd=='build' else split(a.root)
