"""Find retained scenes that show quarantined parts and compare the screen with and without the quarantine.

For the scenes where the most quarantined parts appear this saves
pure native | HD ignoring the quarantine | HD with the quarantine.
Reads only; writes test_current/parts/quarantine_scenes/.
"""
import argparse,json,os,queue,sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image


def native_frame(state,frame,target):
    from hd_core import Core
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,user_dir=ROOT/'test_current/parts/quarantine_scenes/isolated_saves')
    try:
        core.load(ROOT/state,refresh_code=True)
        for _ in range(frame+1):core.run();core.audio.clear()
        Image.fromarray(np.asarray(core.native)[:192]).save(target)
    finally:core.close()


def main():
    if len(sys.argv)>1 and sys.argv[1]=='--native':return native_frame(sys.argv[2],int(sys.argv[3]),sys.argv[4])
    parser=argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--frames',type=int,default=180);parser.add_argument('--every',type=int,default=15);parser.add_argument('--per-unit',type=int,default=3);parser.add_argument('--sheets',type=int,default=8)
    args=parser.parse_args();out=ROOT/'test_current/parts/quarantine_scenes';out.mkdir(parents=True,exist_ok=True)
    for old in out.glob('*.png'):old.unlink()
    from hd_core import Core
    from hd_renderer import HDRenderer
    held={int(k) for k in json.loads((ROOT/'graphics/quarantined_parts.json').read_text(encoding='utf-8'))['parts']}
    by_unit=defaultdict(list)
    for path in sorted((ROOT/'test_current/combat/named_attacks').rglob('*.state')):
        unit=next((int(p[5:]) for p in path.parts if p.startswith('unit_') and p[5:].isdigit()),None)
        if unit is not None and path.stem!='capture':by_unit[unit].append(path)
    states=[path for unit,paths in sorted(by_unit.items()) for path in paths[::max(1,len(paths)//args.per_unit)][:args.per_unit]]
    for extra in ('test_current/combat/getter_cutin.state','test_current/combat/golion_cutin.state'):
        if (ROOT/extra).exists():states.append(ROOT/extra)
    class Ready:
        ready_generation=-1
        def __init__(self):self.dynamic_bindings=queue.SimpleQueue()
        def ready_bindings(self):return self.values
    def renderer_for(flag):
        os.environ['SRWW_QUARANTINE']=flag;renderer=HDRenderer(async_parts=False,dynamic_parts=False,gpu_composition=True);renderer.set_resolution(768);parts=renderer.parts_renderer;parts.load_baked()
        ready=Ready();ready.values=np.fromiter((alias for source in parts.baked for alias in parts.ready_aliases.get(source,())),dtype='uint32');return renderer,ready
    off,ready_off=renderer_for('0');on,ready_on=renderer_for('1');hits=[]
    def play(core,state,ready,frames,render=None,wanted=()):
        core.load(state,refresh_code=True);found={}
        for frame in range(frames):
            core.set_ready_parts(ready);core.run();core.audio.clear()
            if frame in wanted:
                sub=(core.sub_parts,core.sub_owners,core.sub_oam.raw,core.sub_palettes,core.sub_ids,core.sub_priorities) if core.sub_bridge else None
                top=render.render_top(core.native,core.ids,tuple(core.hd),paused=False,parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,
                    backgrounds=core.backgrounds,unknown=None,bg_layout=core.bg_layout,sub_parts=sub,cutin_layers=core.cutin_layers,effect_foreground=core.effect_foreground,window=getattr(core,'window',None),cutin_palettes=getattr(core,'cutin_palettes',None))
                found[frame]=np.asarray(top)[:,:,:3].copy()
            elif render is None and frame%args.every==args.every-1:
                rows=np.asarray(core.parts);shown=[int(b) for b in rows[:,0] if b];bad=sorted({b for b in shown if b in held or on.parts_renderer.bindings[b-1].get('source_binding') in held})
                if bad:found[frame]=(len([b for b in shown if b in bad]),bad)
        return found
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',user_dir=out/'isolated_saves')
    try:
        for index,state in enumerate(states,1):
            found=play(core,state,ready_off,args.frames)
            for frame,(count,bad) in found.items():hits.append(dict(state=str(state.relative_to(ROOT)).replace('\\\\','/'),frame=frame,quarantined_on_screen=count,bindings=bad))
        hits.sort(key=lambda h:-h['quarantined_on_screen']);chosen=[];seen=set()
        for hit in hits:
            if hit['state'] in seen:continue
            seen.add(hit['state']);chosen.append(hit)
            if len(chosen)>=args.sheets:break
        pictures={}
        for hit in chosen:
            state=ROOT/hit['state'];frame=hit['frame']
            pictures[hit['state'],'off']=play(core,state,ready_off,frame+1,off,(frame,))[frame];pictures[hit['state'],'on']=play(core,state,ready_on,frame+1,on,(frame,))[frame]
    finally:core.close();off.parts_renderer.close();on.parts_renderer.close()
    # The core cannot be initialised twice in one process: each untouched native frame comes from a child process.
    import subprocess
    for rank,hit in enumerate(chosen):
        target=out/f'native_{rank:02d}.png'
        subprocess.run([sys.executable,'-X','utf8',__file__,'--native',hit['state'],str(hit['frame']),str(target)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,cwd=ROOT)
        left=np.asarray(Image.open(target).convert('RGB').resize((768,576),Image.Resampling.NEAREST)) if target.exists() else np.zeros((576,768,3),dtype='uint8')
        sheet=np.concatenate([left,pictures[hit['state'],'off'],pictures[hit['state'],'on']],1);hit['sheet']=f"{rank:02d}_{Path(hit['state']).parent.name}_{Path(hit['state']).stem}_f{hit['frame']:03d}.png"
        Image.fromarray(sheet).resize((1152,288)).save(out/hit['sheet'])
        if target.exists():target.unlink()
    report=dict(quarantined=len(held),states_checked=len(states),states_showing_quarantined=len({h['state'] for h in hits}),frames_with_quarantined=len(hits),top=chosen,all=hits[:400])
    (out/'report.json').write_text(json.dumps(report,indent=1,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('all','top')}))
    for hit in chosen:print(hit.get('sheet'),hit['quarantined_on_screen'],hit['bindings'][:8])


if __name__=='__main__':main()
