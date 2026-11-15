"""Robot drawing sets for several units, one after another.

Per unit: capture all weapons (capture_unit_poses), select the pose set
(build_unit_robot_set), round-trip split check, partition and pose sheets.
Prints one line per finished step so a monitor can follow.

  py -3.11 -X utf8 scripts/assets/run_robot_sets.py 0 1 3 4 ...
"""
import json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from PIL import Image,ImageDraw

PY=[sys.executable,'-X','utf8']


def step(args):
    r=subprocess.run(PY+args,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    lines=[l for l in r.stdout.strip().splitlines() if l.strip()]
    return r.returncode,(lines[-1] if lines else ''),(r.stderr.strip().splitlines()[-1] if r.returncode and r.stderr.strip() else '')


def pose_sheet(folder):
    idx=json.loads((folder/'INDEX.json').read_text(encoding='utf-8'));W,H=300,230;cols=5;n=len(idx['poses_list'])
    s=Image.new('RGBA',(cols*W,max(1,(n+cols-1)//cols)*H+30),(60,62,72,255));d=ImageDraw.Draw(s)
    d.text((8,8),f"unit {idx['unit']} {idx['name']}: {idx['poses']} poses / {idx['shapes']} shapes / {idx['set_share_of_visible']*100:.1f}% of visible pixels",fill=(255,255,255))
    for k,e in enumerate(idx['poses_list']):
        im=Image.open(folder/e['pose']/'native.png');im=im.resize((im.width*2,im.height*2),0);im.thumbnail((W-6,H-30))
        x=(k%cols)*W;y=30+(k//cols)*H;s.alpha_composite(im,(x+3,y+3))
        d.text((x+3,y+H-26),f"{e['pose']}  {e['source']}",fill=(255,255,0));d.text((x+3,y+H-14),f"sprites {e['sprites']}  no HD {e['without_hd']}",fill=(200,200,200))
    s.save(folder/'ROBOT_SET_SHEET.png')


def main():
    for uid in map(int,sys.argv[1:]):
        base=ROOT/f'test_current/parts/pose_packets/unit_{uid}';rs=base/'robot_set'
        if (rs/'PARTITIONS_SHEET.png').exists():print(uid,'already done',flush=True);continue
        code,last,err=step(['scripts/assets/capture_unit_poses.py','--unit',str(uid),'--frames','0:1800:2'])
        print(uid,'capture',code,last,err,flush=True)
        if code:continue
        code,last,err=step(['scripts/assets/build_unit_robot_set.py','--unit',str(uid)])
        print(uid,'set',code,last,err,flush=True)
        if code:continue
        code,last,err=step(['scripts/assets/split_object_drawings.py',str(rs),'--selftest'])
        print(uid,'split',code,last,err,flush=True)
        code,last,err=step(['scripts/verify/partition_sheet.py',str(rs)])
        print(uid,'partitions',code,last,err,flush=True)
        try:pose_sheet(rs);print(uid,'sheet ok',flush=True)
        except Exception as e:print(uid,'sheet failed',e,flush=True)
    print('ALL DONE',flush=True)


if __name__=='__main__':main()
