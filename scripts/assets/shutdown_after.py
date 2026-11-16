"""At a given time: stop queued work safely, let the running install step finish, commit, shut down.

1. stop queue scripts (apply_queue / revert / flat-tile shells), apply_eye_review and
   install_unit_sets parents, the ingest loop and pose processing, and render jobs;
2. wait (up to --grace minutes) for a running install_pending_art / cache build to end;
3. remove the queue lock, commit the library and records, shut the PC down in 60 s.

  py -3.11 -X utf8 scripts/assets/shutdown_after.py --at "2026-11-16 23:59"
"""
import argparse,datetime,subprocess,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

PS=['powershell','-NoProfile','-Command']


def kill(pattern,names="'python.exe','sh.exe','bash.exe','py.exe'"):
    subprocess.run(PS+[f"Get-CimInstance Win32_Process | Where-Object {{ @({names}) -contains $_.Name -and $_.CommandLine -match '{pattern}' }} | ForEach-Object {{ Stop-Process -Id $_.ProcessId -Force }}"],capture_output=True)


def running(pattern):
    out=subprocess.run(PS+[f"Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object {{ $_.CommandLine -match '{pattern}' }} | Measure-Object | Select -Expand Count"],capture_output=True,text=True).stdout.strip()
    return out not in ('','0')


def main():
    p=argparse.ArgumentParser();p.add_argument('--at',required=True);p.add_argument('--grace',type=int,default=15)
    a=p.parse_args();at=datetime.datetime.strptime(a.at,'%Y-%m-%d %H:%M')
    while datetime.datetime.now()<at:time.sleep(20)
    print('time reached',flush=True)
    kill('apply_queue|revert_queue|disable_flat_queue|apply_when_free')
    kill('apply_eye_review|install_unit_sets|ingest_loop|ingest_drawings|process_pose|fit_pose|review_pose|sheet_side|render_units|render_unit_weapons|pose_sheets|split_')
    end=time.time()+a.grace*60
    while running('install_pending_art|build_tile_library|build_material_slot|build_native_material|revert_unit|disable_flat') and time.time()<end:time.sleep(15)
    (ROOT/'test_current/parts/pose_packets/.install_lock').exists() and (ROOT/'test_current/parts/pose_packets/.install_lock').rmdir()
    subprocess.run(['git','add','graphics/kazuma_parts_library.json','graphics/atlas_digests.json','graphics/parts_registered.sqlite','docs/ART_INSTALL_DONE.json','docs/PENDING_ART_INSTALL_QUEUE.json','docs/HANDOFF_TO_CODEX_9.md','scripts/assets','scripts/verify'],cwd=ROOT)
    subprocess.run('git add graphics/rework_*',shell=True,cwd=ROOT,capture_output=True)
    subprocess.run(['git','commit','-q','-m','Robot redraw installs up to the 11/16 night shutdown'],cwd=ROOT)
    print('shutting down',flush=True)
    subprocess.run(['shutdown','/s','/t','60','/c','SRW W HD: scheduled shutdown'])


if __name__=='__main__':main()
