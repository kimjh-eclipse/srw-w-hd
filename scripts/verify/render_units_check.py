"""In-game HD render of installed robot sets: one attack per unit, three frames each.

Builds the attack start state when missing (emulator/attack_start.py, run in a
child process), renders the frames with the production renderer and writes
test_current/parts/pose_packets/RESULTS_<tag>.png (one row per unit).

  py -3.11 -X utf8 scripts/verify/render_units_check.py --units 7 8 15 --frames 150,260,380 --tag batch1
"""
import argparse,json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]));sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'emulator'))
from scripts._bootstrap import ROOT
from PIL import Image,ImageDraw

CACHE=ROOT/'test_current/gui/unit_review/attack_starts'
ROM=ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds'


def render_one(state,frames,out_prefix):
    code=f"""
import sys;sys.path.insert(0,r'{ROOT/'emulator'}');sys.path.insert(0,r'{ROOT}')
from pathlib import Path
from hd_core import Core
from hd_renderer import HDRenderer
core=Core(Path(r'{ROM}'),demo=True,user_dir=Path(r'{out_prefix}_saves'));core.load(Path(r'{state}'))
r=HDRenderer(async_parts=False,dynamic_parts=True);r.set_resolution(768)
frames={sorted(frames)}
for f in range(frames[-1]+1):
    core.run();core.audio.clear()
    if f in frames:
        img=r.render_top(core.native,core.ids,core.hd,paused=True,parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,backgrounds=core.backgrounds,bg_layout=core.bg_layout,unknown=core.unknown_snapshot(),cutin_layers=core.cutin_layers,sub_parts=(core.sub_parts,core.sub_owners,core.sub_oam.raw,core.sub_palettes,core.sub_ids,core.sub_priorities),effect_foreground=core.effect_foreground,window=core.window,cutin_palettes=getattr(core,'cutin_palettes',None))
        import time
        for _ in range(25):   # let asynchronously prepared art (portraits) finish, as a running game would a moment later
            p=r.portraits.pending if hasattr(r,'portraits') else {{}}
            if hasattr(r,'portraits'):r.portraits.collect_prepared()
            if not getattr(r.portraits,'pending',None):break
            time.sleep(.1)
        img=r.render_top(core.native,core.ids,core.hd,paused=True,parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,backgrounds=core.backgrounds,bg_layout=core.bg_layout,unknown=core.unknown_snapshot(),cutin_layers=core.cutin_layers,sub_parts=(core.sub_parts,core.sub_owners,core.sub_oam.raw,core.sub_palettes,core.sub_ids,core.sub_priorities),effect_foreground=core.effect_foreground,window=core.window,cutin_palettes=getattr(core,'cutin_palettes',None))
        img.save(r'{out_prefix}_'+str(f)+'.png')
"""
    subprocess.run([sys.executable,'-X','utf8','-c',code],cwd=ROOT,capture_output=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('--units',nargs='+',type=int,required=True);p.add_argument('--frames',default='150,260,380');p.add_argument('--tag',default='check')
    a=p.parse_args();frames=[int(x) for x in a.frames.split(',')]
    from attack_start import build_in_child
    catalog=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text(encoding='utf-8'))
    tmp=ROOT/'test_current/parts/pose_packets/_render_tmp';tmp.mkdir(exist_ok=True);rows=[]
    for u in a.units:
        unit=next(x for x in catalog['units'] if x['unit_id']==u);state=None
        # Strongest weapon first; fall back when its start cannot be built (combination/MAP weapons).
        for wid in reversed(unit['weapon_ids']):
            s=CACHE/f'unit_{u}_weapon_{wid}.state'
            if s.exists() or build_in_child(ROOT,ROM,u,wid,s).get('ok'):state=s;break
        if state is None:print(u,'no start for any weapon');continue
        render_one(state,frames,tmp/f'u{u}')
        ims=[Image.open(tmp/f'u{u}_{f}.png').convert('RGB').resize((512,384)) for f in frames if (tmp/f'u{u}_{f}.png').exists()]
        row=Image.new('RGB',(len(frames)*516+200,384),(20,20,24));d=ImageDraw.Draw(row);d.text((8,8),f"unit {u}",fill=(255,255,0))
        for k,im in enumerate(ims):row.paste(im,(200+k*516,0))
        rows.append(row);print(u,'rendered',len(ims),flush=True)
    if rows:
        sheet=Image.new('RGB',(rows[0].width,sum(r.height+6 for r in rows)),(0,0,0));y=0
        for r in rows:sheet.paste(r,(0,y));y+=r.height+6
        out=ROOT/f'test_current/parts/pose_packets/RESULTS_{a.tag}.png';sheet.save(out);print(out)


if __name__=='__main__':main()
