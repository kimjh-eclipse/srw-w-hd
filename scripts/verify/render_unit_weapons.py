"""HD-only render of one unit across its weapons (production renderer), one row per weapon.

  py -3.11 -X utf8 scripts/verify/render_unit_weapons.py --unit 2 --frames 120,240,360,480
writes test_current/parts/pose_packets/unit_<U>/robot_set/HD_WEAPONS.png
"""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]));sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'emulator'))
from scripts._bootstrap import ROOT
from scripts.verify.render_units_check import render_one,CACHE,ROM
from PIL import Image,ImageDraw


def main():
    p=argparse.ArgumentParser();p.add_argument('--unit',type=int,required=True);p.add_argument('--frames',default='120,240,360,480')
    a=p.parse_args();frames=[int(x) for x in a.frames.split(',')]
    from attack_start import build_in_child
    unit=next(x for x in json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text(encoding='utf-8'))['units'] if x['unit_id']==a.unit)
    tmp=ROOT/'test_current/parts/pose_packets/_render_tmp';tmp.mkdir(exist_ok=True);rows=[]
    for wid in unit['weapon_ids']:
        s=CACHE/f'unit_{a.unit}_weapon_{wid}.state'
        if not s.exists() and not build_in_child(ROOT,ROM,a.unit,wid,s).get('ok'):print('weapon',wid,'no start');continue
        render_one(s,frames,tmp/f'u{a.unit}w{wid}')
        ims=[Image.open(tmp/f'u{a.unit}w{wid}_{f}.png').convert('RGB').resize((448,336)) for f in frames if (tmp/f'u{a.unit}w{wid}_{f}.png').exists()]
        row=Image.new('RGB',(len(frames)*452,336),(20,20,24))
        for k,im in enumerate(ims):row.paste(im,(k*452,0))
        ImageDraw.Draw(row).text((6,6),f'weapon {wid}',fill=(255,255,0));rows.append(row);print('weapon',wid,'rendered',len(ims),flush=True)
    sheet=Image.new('RGB',(rows[0].width,sum(r.height+6 for r in rows)),(0,0,0));y=0
    for r in rows:sheet.paste(r,(0,y));y+=r.height+6
    out=ROOT/f'test_current/parts/pose_packets/unit_{a.unit}/robot_set/HD_WEAPONS.png';sheet.save(out);print(out)


if __name__=='__main__':main()
