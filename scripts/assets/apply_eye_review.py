"""Apply subagent eye reviews (robot_set/EYE_REVIEW.json), install, and write Codex feedback.

For each given unit with an EYE_REVIEW.json:
  - DRAWINGS_STATUS.json: poses in accept_poses -> accepted (eye override noted),
    poses in reject_poses -> rejected with the eye reason;
  - verdict "redraw": nothing installed, HOLD_REDRAW written;
  - otherwise the unit is installed (install_unit_sets.py) and marked INSTALLED;
  - every issue is appended to the current Codex handoff under one dated section.

  py -3.11 -X utf8 scripts/assets/apply_eye_review.py 23 25 27 28 29 [--handoff docs/HANDOFF_TO_CODEX_7.md]
"""
import argparse,datetime,json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

BASE=ROOT/'test_current/parts/pose_packets'


def main():
    p=argparse.ArgumentParser();p.add_argument('units',nargs='+',type=int);p.add_argument('--handoff',default='docs/HANDOFF_TO_CODEX_8.md')
    a=p.parse_args();install=[];lines=[];held=[]
    catalog={u['unit_id']:u for u in json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text(encoding='utf-8'))['units']}
    for u in a.units:
        rs=BASE/f'unit_{u}/robot_set';er=rs/'EYE_REVIEW.json'
        if not er.exists():print(u,'no EYE_REVIEW');continue
        r=json.loads(er.read_text(encoding='utf-8'));st_path=rs/'DRAWINGS_STATUS.json';st=json.loads(st_path.read_text(encoding='utf-8'))
        for k in r.get('accept_poses',[]):
            if k in st:st[k]['state']='accepted';st[k]['eye']='accepted by eye review'
        for k,why in r.get('reject_poses',{}).items():
            if k in st:st[k]['state']='rejected';st[k].setdefault('reasons',[]).append('eye: '+why)
        st_path.write_text(json.dumps(st,ensure_ascii=False,indent=1),encoding='utf-8');(rs/'EYE_REVIEW_PENDING').unlink(missing_ok=True)
        name=catalog.get(u,{}).get('name_ja','')
        if r.get('verdict')=='redraw':
            (rs/'HOLD_REDRAW').write_text('eye review: redraw\n',encoding='utf-8');held.append(u)
        else:install.append(u)
        if r.get('issues'):
            lines.append(f"- **unit {u} {name}** — 판정 `{r.get('verdict')}`, 설치 {len(r.get('accept_poses',[]))}자세"+(' (설치 안 함, 전체 다시 그리기)' if r.get('verdict')=='redraw' else ''))
            for i in r['issues']:lines.append(f"  - {i.get('where','')}: {i.get('what','')} → 고칠 것: {i.get('fix','')}")
        else:lines.append(f"- unit {u} {name} — 문제 없음, 설치")
    if install:
        out=subprocess.run([sys.executable,'-X','utf8','scripts/assets/install_unit_sets.py',*map(str,install)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace').stdout
        for line in out.splitlines():
            print(line[:220])
            parts=line.split()
            if parts and parts[0].isdigit() and 'ERROR' not in line and 'held' not in line and 'nothing' not in line:(BASE/f'unit_{parts[0]}/robot_set/INSTALLED').touch()
    if lines:
        h=ROOT/a.handoff;text=h.read_text(encoding='utf-8');stamp=datetime.datetime.now().strftime('%m/%d %H:%M')
        block=f"## {stamp} — 눈 검수 결과 (unit {', '.join(map(str,a.units))})\n\n"+'\n'.join(lines)+'\n\n'
        marker='## Claude 쪽 변경'
        text=text.replace(marker,block+marker,1) if marker in text else text+'\n'+block
        h.write_text(text,encoding='utf-8')
    print('installed',install,'held for redraw',held)


if __name__=='__main__':main()
