
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT, tool_path

import os,sys,json,subprocess,time
from pathlib import Path
ROOT=PROJECT_ROOT;OUT=ROOT/'test_current/parts'

def main():
    os.environ['SRWW_CORE_PATH']=str(ROOT/'test_current/core/desmume_libretro.dll')
    tests=['verify_native_texture_cache.py','profile_native_runtime.py','verify_frame_compositor.py','verify_worker_pipeline.py','verify_dynamic_parts.py','verify_observed_hd.py','record_hd_status.py'];results=[]
    for name in tests:
        print('START',name,flush=True);start=time.perf_counter()
        with (OUT/(Path(name).stem+'.log')).open('w',encoding='utf8') as log:code=subprocess.run([sys.executable,'-X','utf8',str(tool_path(name))],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT).returncode
        row=dict(script=name,exit_code=code,seconds=round(time.perf_counter()-start,2));results.append(row);(OUT/'runtime_checks.json').write_text(json.dumps(results,indent=2));print(row,flush=True)
        if code:raise RuntimeError(name+' failed')
    print('COMPLETE',flush=True)

if __name__=='__main__':main()
