"""Bring Codex single-pose redraws (11/21 method) into a unit's robot set and check them.

Delivery: <root>/unit_<U>/single_poseNN/RAW_imagegen.png + layout_snapshot.json (canvas = the pose's
native_4x size; source_region_in_request = the canvas inside the request). Each RAW is resized to the
canvas, interior alpha >= 240 made opaque, written as pose_NN/candidate_fit.png (the old one kept as
candidate_fit_pre<tag>.png) and the pose marked accepted. Then the parts are cut by the original
part's own shape and size (split_object_drawings SRWW_FULL_PART=1) into split_fit, every pose is
assembled from those parts and compared with its own drawing (ASSEMBLY check) and with the
original. Sheet: <robot_set>/SINGLE_POSE_REVIEW.png. Nothing is installed here.

  py -3.11 -X utf8 scripts/assets/ingest_single_poses.py --root test_current/parts/redraw_requests/_codex_20261121 --unit 196 [--tag 20261121]
"""
import argparse,json,os,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
BASE=ROOT/'test_current/parts/pose_packets'


def main():
    a=argparse.ArgumentParser();a.add_argument('--root',required=True);a.add_argument('--unit',type=int,required=True);a.add_argument('--tag',default='20261121');a=a.parse_args()
    src=ROOT/a.root/f'unit_{a.unit}'
    if not src.exists() and a.unit==196:src=ROOT/a.root/'unit_196_pilot'
    rs=BASE/f'unit_{a.unit}/robot_set';st_path=rs/'DRAWINGS_STATUS.json'
    st=json.loads(st_path.read_text(encoding='utf-8')) if st_path.exists() else {}
    got=[]
    for d in sorted(src.glob('single_pose*')):
        raw=d/'RAW_imagegen.png'
        if not raw.exists():continue
        pose='pose_'+d.name.replace('single_pose','')
        L=json.loads((d/'layout_snapshot.json').read_text(encoding='utf-8'));cw,ch=L['canvas']
        f=rs/pose
        if not (f/'native_4x.png').exists() or Image.open(f/'native_4x.png').size!=(cw,ch):print('skip',pose,'canvas mismatch');continue
        im=Image.open(raw).convert('RGBA').resize((cw,ch),Image.Resampling.LANCZOS);x=np.asarray(im).copy()
        x[...,3]=np.where(x[...,3]>=240,255,x[...,3]);x[x[...,3]==0,:3]=0
        if (f/'candidate_fit.png').exists() and not (f/f'candidate_fit_pre{a.tag}.png').exists():(f/'candidate_fit.png').rename(f/f'candidate_fit_pre{a.tag}.png')
        Image.fromarray(x).save(f/'candidate_fit.png');st[pose]=dict(state='accepted',note=f'Codex single-pose redraw {a.tag}');got.append(pose)
    st_path.write_text(json.dumps(st,ensure_ascii=False,indent=1),encoding='utf-8')
    acc=[k for k,v in st.items() if v.get('state')=='accepted'];(rs/'accepted_poses.json').write_text(json.dumps(acc))
    env=dict(os.environ,SRWW_FULL_PART='1')
    subprocess.run([sys.executable,'-X','utf8','scripts/assets/split_object_drawings.py',str(rs),'--drawing','candidate_fit.png','--out',str(rs/'split_fit'),'--only',str(rs/'accepted_poses.json')],cwd=ROOT,env=env,capture_output=True)
    fnt=ImageFont.truetype('malgun.ttf',20);rows=[];score={}
    def onbg(im):
        b=Image.new('RGBA',im.size,(40,60,150,255));b.alpha_composite(im.convert('RGBA'));return b.convert('RGB')
    for p in got:
        f=rs/p;rws=json.loads((f/'contract.json').read_text(encoding='utf-8'));W,H=Image.open(f/'native.png').size;can=Image.new('RGBA',(W*4,H*4))
        for r in reversed(rws):
            q=rs/'split_fit/parts'/f"{r['hash']}.png"
            if not q.exists():continue
            im=Image.open(q).convert('RGBA')
            if r['flip_x']:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if r['flip_y']:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            can.alpha_composite(im,(r['screen_x']*4,r['screen_y']*4))
        A=np.asarray(can.resize((W,H),Image.Resampling.BOX)).astype(int);B=np.asarray(Image.open(f/'candidate_fit.png').convert('RGBA').resize((W,H),Image.Resampling.BOX)).astype(int)
        m=(np.asarray(Image.open(f/'native.png').convert('RGBA'))[...,3]>0)&(A[...,3]>200)&(B[...,3]>200)
        score[p]=round(float((np.abs(A[...,:3]-B[...,:3]).max(2)[m]>60).mean()),3) if m.any() else None
        ims=[onbg(Image.open(f/'native_4x.png')),onbg(Image.open(f/'candidate_fit.png')),onbg(can)];w,h=ims[0].size
        r=Image.new('RGB',(3*w+40,h+30),(255,255,255));d=ImageDraw.Draw(r)
        for i,im in enumerate(ims):r.paste(im,(i*(w+20),30))
        d.text((4,4),f'{p}  원본 | 코덱스 | 조립  어긋남 {score[p]}',fill=(0,0,0),font=fnt);rows.append(r)
    if rows:
        Wm=max(r.width for r in rows);o=Image.new('RGB',(Wm,sum(r.height+10 for r in rows)),(255,255,255));y=0
        for r in rows:o.paste(r,(0,y));y+=r.height+10
        o.save(rs/'SINGLE_POSE_REVIEW.png')
    (rs/'SINGLE_POSE_SCORES.json').write_text(json.dumps(score,indent=1),encoding='utf-8')
    print('unit',a.unit,'poses',len(got),'assembly mismatch',score)


if __name__=='__main__':main()
