"""One canvas with every pose of a robot set, so the whole robot is drawn in one go.

  build  <set dir>   -> <set>/COMBINED/native_combined_4x.png (all poses' native_4x on
                        one canvas, grey gutters), layout.json (each pose's place),
                        guide_labels.png (pose names), DRAWING_RULES.md
  split  <set dir> [drawing]  -> cuts COMBINED/<drawing> (default candidate_combined.png)
                        back into pose_NN/candidate.png; an existing candidate.png is
                        kept as candidate_v1.png (or the next free vN).

  py -3.11 -X utf8 scripts/assets/combined_pose_sheet.py build test_current/parts/pose_packets/unit_2/robot_set
"""
import json,sys
from pathlib import Path
from PIL import Image,ImageDraw

GAP=48;COLS=5

RULES="""# 한 장 그리기 규칙 (Claude 작성)

- `native_combined_4x.png` 한 장에 이 기체의 모든 자세(원본 4배)가 놓여 있습니다. **이 캔버스와 같은 크기의 `candidate_combined.png` 한 장**에, 모든 자세를 같은 화풍·같은 디테일로 그려 주세요(같은 부품은 모든 자세에서 같은 모양·같은 색·같은 장식).
- 각 자세는 원본 위에 **같은 자리·같은 크기로 덧그리듯**(팔다리·무장 위치와 윤곽 그대로). 자세 사이 여백과 원본 실루엣 밖은 **알파 0**.
- 색은 원본 색 그대로. 다른 팔레트 그림을 다시 칠하지 말 것.
- 자세 이름은 `guide_labels.png`(같은 크기, 이름만 표시)를 참고. 그림에 글자를 넣지 말 것.
- 다 그리면 `COMBINED/candidate_combined.png` 만 두면 됩니다. 자세별로 자르기·정합·분할·설치·게임 확인은 Claude.
"""


def build(root):
    poses=sorted(d for d in root.glob('pose_*') if d.is_dir())
    ims=[(p.name,Image.open(p/'native_4x.png').convert('RGBA')) for p in poses]
    colw=[0]*COLS;rows=[]
    for i in range(0,len(ims),COLS):rows.append(ims[i:i+COLS])
    for row in rows:
        for c,(_,im) in enumerate(row):colw[c]=max(colw[c],im.width)
    rowh=[max(im.height for _,im in row) for row in rows]
    W=sum(colw)+GAP*(COLS+1);H=sum(rowh)+GAP*(len(rows)+1)
    sheet=Image.new('RGBA',(W,H));guide=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(guide);layout={}
    y=GAP
    for r,row in enumerate(rows):
        x=GAP
        for c,(name,im) in enumerate(row):
            sheet.alpha_composite(im,(x,y));layout[name]=[x,y,im.width,im.height]
            d.rectangle((x-2,y-2,x+im.width+1,y+im.height+1),outline=(255,200,0,255));d.text((x,y-14),name,fill=(255,200,0,255))
            x+=colw[c]+GAP
        y+=rowh[r]+GAP
    out=root/'COMBINED';out.mkdir(exist_ok=True)
    sheet.save(out/'native_combined_4x.png');guide.save(out/'guide_labels.png')
    (out/'layout.json').write_text(json.dumps(dict(canvas=[W,H],poses=layout),indent=1),encoding='utf-8');(out/'DRAWING_RULES.md').write_text(RULES,encoding='utf-8')
    print('poses',len(layout),'canvas',W,H)


def split(root,name):
    out=root/'COMBINED';layout=json.loads((out/'layout.json').read_text(encoding='utf-8'))
    art=Image.open(out/name).convert('RGBA')
    assert list(art.size)==layout['canvas'],(art.size,layout['canvas'])
    for pose,(x,y,w,h) in layout['poses'].items():
        dst=root/pose/'candidate.png'
        if dst.exists():
            n=1
            while (root/pose/f'candidate_v{n}.png').exists():n+=1
            dst.replace(root/pose/f'candidate_v{n}.png')
        art.crop((x,y,x+w,y+h)).save(dst)
    print('split',len(layout['poses']),'poses from',name)


if __name__=='__main__':
    cmd,root=sys.argv[1],Path(sys.argv[2])
    build(root) if cmd=='build' else split(root,sys.argv[3] if len(sys.argv)>3 else 'candidate_combined.png')
