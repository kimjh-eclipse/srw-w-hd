"""Finalize the frozen asset plan and run bounded, representative checks."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT, tool_path

import sys,time,json,subprocess
from pathlib import Path
ROOT=PROJECT_ROOT
OUT=ROOT/'test_current/parts'

def main():
    plan=json.loads((ROOT/'graphics/animation_parts/full_attack_sheets.json').read_text());start=time.monotonic()
    while not (ROOT/'graphics/animation_parts/full_attack_generation_132.json').exists():
        if '--wait' not in sys.argv:raise RuntimeError('Final image-generation batch is not complete')
        if time.monotonic()-start>1200:raise TimeoutError('Image generation remains unfinished')
        time.sleep(5)
    assert all((ROOT/'graphics/animation_parts'/s['image']).exists() for s in plan['sheets'])
    scripts=['install_full_attack_parts.py','install_shared_attack_parts.py','audit_generated_bindings.py','verify_all_unit_coverage.py','build_tile_library.py','verify_compound_parts.py','verify_dynamic_parts.py','verify_async_parts.py','verify_frame_compositor.py','verify_observed_hd.py','record_hd_status.py']
    results=[]
    for name in scripts:
        print('START',name,flush=True);started=time.perf_counter()
        with (OUT/(Path(name).stem+'.log')).open('w',encoding='utf8') as log:
            result=subprocess.run([sys.executable,'-X','utf8',str(tool_path(name))],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
        item=dict(script=name,exit_code=result.returncode,seconds=round(time.perf_counter()-started,2));results.append(item)
        (OUT/'finalization.json').write_text(json.dumps(results,indent=2));print(item,flush=True)
        if result.returncode:raise RuntimeError('Check failed: '+name)
    print('COMPLETE',flush=True)

if __name__=='__main__':main()
