"""All attack poses of one unit: build every weapon's start state (attack_start),
capture poses per weapon (build_pose_packets) and objects (build_object_packets).

  py -3.11 -X utf8 scripts/assets/capture_unit_poses.py --unit 2 [--frames 0:1800:1]
Output: test_current/parts/pose_packets/unit_<U>/weapon_<W>/...
"""
import argparse,json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]));sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'emulator'))
from scripts._bootstrap import ROOT

CACHE=ROOT/'test_current/gui/unit_review/attack_starts'


def main():
    p=argparse.ArgumentParser();p.add_argument('--unit',type=int,required=True);p.add_argument('--frames',default='0:1800:1')
    a=p.parse_args()
    catalog=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text(encoding='utf-8'))
    unit=next(u for u in catalog['units'] if u['unit_id']==a.unit)
    rom=ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds';base=ROOT/f'test_current/parts/pose_packets/unit_{a.unit}'
    from attack_start import build_in_child
    status={}
    for wid in unit['weapon_ids']:
        state=CACHE/f'unit_{a.unit}_weapon_{wid}.state'
        if not state.exists():
            result=build_in_child(ROOT,rom,a.unit,wid,state)
            if not (result.get('ok') and state.exists()):status[wid]='no start: '+str(result.get('reason'));print(wid,status[wid]);continue
        out=base/f'weapon_{wid}'
        r=subprocess.run([sys.executable,'-X','utf8','scripts/assets/build_pose_packets.py','--state',str(state),'--out',str(out),'--frames',a.frames],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
        if r.returncode:status[wid]='pose capture failed: '+r.stderr.strip().splitlines()[-1];print(wid,status[wid]);continue
        r=subprocess.run([sys.executable,'-X','utf8','scripts/assets/build_object_packets.py',str(out)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
        status[wid]=r.stdout.strip().splitlines()[0] if r.returncode==0 else 'objects failed: '+r.stderr.strip().splitlines()[-1]
        print(wid,status[wid],flush=True)
    base.mkdir(parents=True,exist_ok=True);(base/'STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=1),encoding='utf-8')


if __name__=='__main__':main()
