"""Both screens of a state at a frame: pure native beside HD, for menu, forecast and HUD checks.

usage: compare_both_screens.py OUT_NAME FRAME STATE [STATE ...]
Writes test_current/gui/both_screens/<OUT_NAME>/<state>.png (native top+bottom | HD top+bottom)
and prints how much of each screen differs strongly from the native picture.
The native frame comes from a child process: the core cannot be started twice in one.
"""
import json,queue,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image
ROM=ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds'


def native_frame(state,frame,target,saves):
    from hd_core import Core
    core=Core(ROM,enabled=False,user_dir=saves)
    try:
        core.load(ROOT/state,refresh_code=True)
        for _ in range(frame+1):core.run();core.audio.clear()
        Image.fromarray(np.asarray(core.native)[:384]).save(target)
    finally:core.close()


def main():
    if sys.argv[1]=='--native':return native_frame(sys.argv[2],int(sys.argv[3]),sys.argv[4],sys.argv[5])
    name,frame,states=sys.argv[1],int(sys.argv[2]),sys.argv[3:];out=ROOT/'test_current/gui/both_screens'/name;out.mkdir(parents=True,exist_ok=True)
    from hd_core import Core
    from hd_renderer import HDRenderer
    core=Core(ROM,user_dir=out/'isolated_saves');renderer=HDRenderer(async_parts=True,dynamic_parts=core.dynamic_bridge,gpu_composition=True);renderer.set_resolution(768);parts=renderer.parts_renderer
    class Ready:
        ready_generation=-1;values=[]
        def __init__(self):self.dynamic_bindings=queue.SimpleQueue()
        def ready_bindings(self):return self.values
    rows=[]
    try:
        for state in states:
            ready=Ready();core.load(ROOT/state,refresh_code=True);top=bottom=None
            for index in range(frame+1):
                if ready.ready_generation!=parts.ready_generation:ready.ready_generation=parts.ready_generation;ready.values=parts.ready_bindings()
                while True:
                    try:ready.dynamic_bindings.put(parts.dynamic_bindings.get_nowait())
                    except queue.Empty:break
                core.set_ready_parts(ready);core.run();core.audio.clear()
                sub=(core.sub_parts,core.sub_owners,core.sub_oam.raw,core.sub_palettes,core.sub_ids,core.sub_priorities) if core.sub_bridge else None
                top=renderer.render_top(core.native,core.ids,tuple(core.hd),paused=False,parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,
                    backgrounds=core.backgrounds,unknown=core.unknown_snapshot(),bg_layout=core.bg_layout,sub_parts=sub,cutin_layers=core.cutin_layers,effect_foreground=core.effect_foreground,window=getattr(core,'window',None),cutin_palettes=getattr(core,'cutin_palettes',None))
                bottom=renderer.render_bottom(core.native,tuple(core.hd))
            hd=np.concatenate([np.asarray(top)[:,:,:3],np.asarray(bottom)[:,:,:3]],0);label=Path(state).parent.name+'_'+Path(state).stem;target=out/f'{label}_native.png'
            subprocess.run([sys.executable,'-X','utf8',__file__,'--native',state,str(frame),str(target),str(out/'native_saves')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,cwd=ROOT)
            if not target.exists():rows.append(dict(state=state,error='no native frame'));continue
            native=np.asarray(Image.open(target).convert('RGB').resize((768,1152),Image.Resampling.NEAREST));target.unlink()
            delta=np.abs(hd.astype('int16')-native.astype('int16')).max(2);strong=delta>=96
            sub_stats=dict(parts.last_stats) if getattr(parts,'last_stats',None) else {}
            rows.append(dict(state=state,frame=frame,top_strong_share=round(float(strong[:576].mean()),4),bottom_strong_share=round(float(strong[576:].mean()),4),last_compose=sub_stats))
            Image.fromarray(np.concatenate([native,hd],1)).save(out/f'{label}.png')
    finally:core.close();parts.close()
    (out/'report.json').write_text(json.dumps(rows,indent=1),encoding='utf-8')
    for row in rows:print(row)


if __name__=='__main__':main()
