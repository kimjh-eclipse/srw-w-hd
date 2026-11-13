"""Compare untagged OBJ decisions with classification off/on in isolated cores."""
import argparse,json,queue,subprocess,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

def capture(mode,out,ready_mode,fixtures,frames_per_fixture):
    from hd_core import Core
    count=len(json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text(encoding='utf-8'))['bindings'])
    values=np.arange(1,count+1,dtype='uint32')
    if ready_mode=='baked':
        from hd_parts import PartsRenderer
        renderer=PartsRenderer(async_prepare=True)
        try:values=renderer.ready_bindings().copy()
        finally:renderer.close()
    class AllReady:
        ready_generation=0
        dynamic_bindings=queue.SimpleQueue()
        def ready_bindings(self):return values
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/f'decision_saves_{mode}')
    try:
        if mode=='off':c.api.retro_srw_register_effect_parts(None,0)
        frames=[]
        for fixture in fixtures:
            c.load(ROOT/fixture);c.ready_generation=None;c.set_ready_parts(AllReady())
            for _ in range(frames_per_fixture):c.run();c.audio.clear();frames.append(c.parts.copy())
        np.savez_compressed(out/f'decisions_{mode}.npz',parts=np.stack(frames),effects=c.effect_part_ids,ready_count=len(values))
    finally:c.close()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--capture',choices=('off','on'));parser.add_argument('--ready-mode',choices=('baked','all'),default='baked');parser.add_argument('--sweep',action='store_true');parser.add_argument('--frames',type=int,default=300);args=parser.parse_args()
    out=ROOT/'test_current/parts/effect_guard_review'
    fixtures=['test_current/combat/duo_cutin_full.state']
    if args.sweep:
        out=out/'unit_sweep'
        rows=json.loads((ROOT/'test_current/combat/runtime_path/coverage_all/report.json').read_text(encoding='utf-8'))['rows']
        fixtures=list(dict.fromkeys(row['state'] for row in rows if (ROOT/row['state']).exists()))
    out.mkdir(exist_ok=True)
    if args.capture:capture(args.capture,out,args.ready_mode,fixtures,args.frames);return
    for mode in ('off','on'):
        command=[sys.executable,'-X','utf8',__file__,'--capture',mode,'--ready-mode',args.ready_mode,'--frames',str(args.frames)]
        if args.sweep:command.append('--sweep')
        subprocess.run(command,check=True)
    with np.load(out/'decisions_off.npz') as d:a=d['parts'];effects=d['effects']
    with np.load(out/'decisions_on.npz') as d:b=d['parts']
    changed=((a[:,:,7]^b[:,:,7])&0x80000000)!=0
    valid=(a[:,:,0]>0)&(a[:,:,0]==b[:,:,0]);untagged=~np.isin(a[:,:,0],effects)
    locations=np.argwhere(changed&valid&untagged)
    report=dict(ready_mode=args.ready_mode,fixtures=len(fixtures),frames_per_fixture=args.frames,tagged_decisions_changed=int((changed&valid&~untagged).sum()),untagged_guard_decisions_changed=len(locations),frames_changed=len(set(int(x[0]) for x in locations)),examples=[dict(state=fixtures[int(f)//args.frames],frame=int(f)%args.frames,oam=int(s),binding=int(a[f,s,0]),old_held=bool(a[f,s,7]&0x80000000),new_held=bool(b[f,s,7]&0x80000000)) for f,s in locations[:30]])
    (out/'unit_decision_comparison.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
