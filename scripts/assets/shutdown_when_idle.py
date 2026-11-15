"""At a given time, wait until no library writer runs, commit, then shut the PC down.

Library writers: install_pending_art / install_unit_sets / apply_eye_review /
bake_parts / build_tile_library. Waits up to --grace minutes for them to end.

  py -3.11 -X utf8 scripts/assets/shutdown_when_idle.py --at "2026-11-16 09:32"
"""
import argparse,datetime,subprocess,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

WRITERS=('install_pending_art','install_unit_sets','apply_eye_review','bake_parts','build_tile_library','install_great_mazinger_pose','record_completed_art_batch')


def writers_running():
    out=subprocess.run(['powershell','-NoProfile','-Command',"Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | ForEach-Object { $_.CommandLine }"],capture_output=True,text=True,encoding='utf-8',errors='replace').stdout
    return [w for w in WRITERS if w in out]


def main():
    p=argparse.ArgumentParser();p.add_argument('--at',required=True);p.add_argument('--grace',type=int,default=40)
    a=p.parse_args();at=datetime.datetime.strptime(a.at,'%Y-%m-%d %H:%M')
    while datetime.datetime.now()<at:time.sleep(30)
    print('time reached',flush=True)
    deadline=time.time()+a.grace*60
    while writers_running() and time.time()<deadline:print('waiting for',writers_running(),flush=True);time.sleep(30)
    subprocess.run(['powershell','-NoProfile','-Command',"Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { $_.CommandLine -match 'ingest|process_pose|fit_pose|review_pose|sheet_side|pose_sheets|split_unified' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"])
    subprocess.run(['git','add','graphics/kazuma_parts_library.json','graphics/atlas_digests.json','graphics/parts_registered.sqlite','docs/ART_INSTALL_DONE.json','docs/PENDING_ART_INSTALL_QUEUE.json','emulator/hd_parts.py','scripts/assets','scripts/verify','docs/HANDOFF_TO_CODEX_8.md'],cwd=ROOT)
    subprocess.run(['git','add','graphics/rework_*'],cwd=ROOT,capture_output=True)
    subprocess.run(['git','commit','-q','-m','Robot redraw installs up to the scheduled shutdown'],cwd=ROOT)
    print('shutting down',flush=True)
    subprocess.run(['shutdown','/s','/t','60','/c','SRW W HD: scheduled shutdown after the work session'])


if __name__=='__main__':main()
