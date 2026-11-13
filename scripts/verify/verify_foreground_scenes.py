"""Replay retained real attack states through common GPU foreground composition.

This is fixture regression coverage, not proof of every campaign animation.
"""
import json,sys,time,os
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_core import Core
from hd_renderer import HDRenderer


def main():
    out=ROOT/'test_current/combat/foreground/regression';out.mkdir(parents=True,exist_ok=True)
    fixtures=[]
    base=ROOT/'test_current/combat/named_attacks'
    for uid in (139,145,155,214,226,227,249,261,297,299,375,390,413,417):
        candidates=sorted((base/f'unit_{uid}').rglob('*.state'))
        candidates=[p for p in candidates if p.stem!='capture']
        if uid==413:candidates=[p for p in candidates if p.stem in ('frame_360','frame_600','frame_1080','frame_1560')]
        fixtures.extend((uid,p) for p in candidates[:5])
    fixtures.extend((-1,ROOT/'test_current/combat'/name) for name in ('getter_cutin.state','golion_cutin.state'))
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'isolated_saves')
    renderer=HDRenderer(gpu_composition=True);renderer.set_resolution(768);rows=[]
    sheet=Image.new('RGB',(4*256,((len(fixtures)+3)//4)*208),(25,30,35));draw=ImageDraw.Draw(sheet)
    try:
        for n,(uid,state) in enumerate(fixtures):
            if not state.exists():continue
            core.load(state);core.run();core.audio.clear()
            kw=dict(paused=True,parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,backgrounds=core.backgrounds,bg_layout=core.bg_layout,cutin_layers=core.cutin_layers)
            start=time.perf_counter()
            image=renderer.render_top(core.native,core.ids,core.hd,effect_foreground=core.effect_foreground,**kw)
            pixels=np.asarray(image);elapsed=(time.perf_counter()-start)*1000
            assert pixels.shape==(576,768,3) and pixels.dtype==np.uint8
            name=f'{uid}_{n}';image.save(out/f'{name}.png')
            x=n%4*256;y=n//4*208;sheet.paste(Image.fromarray(pixels).resize((256,192)),(x,y+16));draw.text((x,y),f'{uid} {state.stem}',fill='white')
            count=0 if core.effect_foreground is None else int(np.count_nonzero(core.effect_foreground))
            rows.append(dict(unit=uid,state=state.relative_to(ROOT).as_posix(),cutins=[int(p[0]) for p in core.cutin_layers if p[0]],foreground_pixels=count,composition_ms=round(elapsed,2)))
            print(uid,state.stem,count,flush=True)
        sheet.save(out/'contact.png')
        report=dict(scope=__doc__,scenes=len(rows),units=len({r['unit'] for r in rows if r['unit']>=0}),gpu=renderer.gpu_composition,all_campaign_scenes_verified=False,rows=rows)
        (out/'report.json').write_text(json.dumps(report,indent=2));print('Verified',len(rows),'retained attack states')
    finally:core.close();renderer.parts_renderer.close()


if __name__=='__main__':main()
