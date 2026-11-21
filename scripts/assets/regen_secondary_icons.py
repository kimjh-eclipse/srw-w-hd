"""Redraw the HD mini-unit icon (secondary IMG) from the robot parts installed now.

connect_secondary_units.py made each icon once (11/10) by assembling the battle
parts of that day and never refreshes an icon it already registered. After a
unit's parts are reinstalled (Strike family 11/19) the icon still shows the old
assembly. This rebuilds graphics/secondary_units/unit_<res>_hd.png the same way
(live status screen, current library, silhouette check against the ROM icon)
and keeps the existing binding. Old images are kept as *_hd.before_<tag>.png.

  py -3.11 -X utf8 scripts/assets/regen_secondary_icons.py --units 11,12 [--apply] [--tag 20261119]
"""
import sys,json,ctypes as C,argparse,shutil
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g
from hd_core import Core
from hd_renderer import HDRenderer
import hd_parts


def main():
    p=argparse.ArgumentParser();p.add_argument('--units',required=True);p.add_argument('--apply',action='store_true');p.add_argument('--tag',default='regen')
    a=p.parse_args();want=set(map(int,a.units.split(',')))
    catalog=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text())
    units=[u for u in catalog['units'] if u['unit_id'] in want and u.get('secondary_image')]
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    folder=ROOT/'graphics/secondary_units';out_dir=folder/f'regen_{a.tag}';out_dir.mkdir(exist_ok=True)
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=ROOT/'test_current/combat/roster_saves')
    renderer=HDRenderer(async_parts=False);renderer.set_resolution(768);rows=[]
    def step(buttons,n):
        c.buttons=set(buttons)
        for _ in range(n):c.run();c.audio.clear()
        c.buttons=set()
    try:
        for u in units:
            uid=u['unit_id'];resource=u['secondary_image']
            img=folder/f'unit_{resource}_hd.png'
            if not img.exists():rows.append(dict(unit_id=uid,resource=resource,status='no icon registered'));continue
            ia=g.pixels(g.decompress(rom[g.BASE+offsets[resource]:g.BASE+offsets[resource+1]]))
            native=Image.fromarray((ia!=0).astype('uint8')*255);target=native.getbbox()
            c.load(ROOT/'test_current/combat/sandrock_weapons.state');step([],15)
            c.api.retro_get_memory_data.restype=C.c_void_p;ram=c.api.retro_get_memory_data(2);unit=ram+0x1f0dbc+3*64
            for off in (6,10):C.c_int16.from_address(unit+off).value=uid
            C.c_uint32.from_address(unit).value=max(1,u['hp']);C.c_uint16.from_address(unit+4).value=u['en']
            step([0],5);step([],35)
            attrs=np.frombuffer(c.obj.raw,dtype='<u2').reshape(128,4);canvas=Image.new('RGBA',(768,576));n=0;missing=0
            # DS draws the LOWER OAM index in front (same priority): paint back to front,
            # i.e. higher priority value first, then higher index first. connect_secondary_units
            # painted in index order, so the chest (slot 29) covered Strike's face (slot 28).
            order=sorted(range(128),key=lambda i:(-((int(attrs[i][2])>>10)&3),-i))
            for i in order:
                oa,ob,ot,_=attrs[i]
                x=int(ob&511);y=int(oa&255)
                if (oa&0x300)==0x200 or not (166<=x<256 and 88<=y<166 and ot>>12==6):continue
                if not int(c.parts[i,0]):missing+=1;continue
                art=renderer.parts_renderer.sprite(c.parts[i],c.obj.raw,c.part_palettes[i])
                if art is None:missing+=1;continue
                canvas.alpha_composite(art,(round(x*hd_parts.SCALE),round(y*hd_parts.SCALE)));n+=1
            box=canvas.getbbox();mask=canvas.getchannel('A').resize((256,192),Image.Resampling.BOX)
            mask=Image.fromarray((np.asarray(mask)>64).astype('uint8')*255);mb=mask.getbbox()
            if box is None or mb is None:rows.append(dict(unit_id=uid,resource=resource,status='no HD parts on screen',missing=missing));continue
            silhouette=mask.crop(mb).resize((target[2]-target[0],target[3]-target[1]),Image.Resampling.NEAREST)
            expected=np.asarray(native.crop(target))>0;opts=[]
            for flip in (False,True):
                probe=silhouette.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if flip else silhouette
                act=np.asarray(probe)>0;opts.append((float((act&expected).sum()/max(1,(act|expected).sum())),flip))
            iou,flip=max(opts)
            scale=960/max(ia.shape);size=(round(ia.shape[1]*scale),round(ia.shape[0]*scale));dest=tuple(round(v*scale) for v in target)
            paint=canvas.crop(box)
            if flip:paint=paint.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            output=Image.new('RGBA',size);output.alpha_composite(paint.resize((dest[2]-dest[0],dest[3]-dest[1]),Image.Resampling.LANCZOS),dest[:2])
            # Sprites without HD (not shown enough in any drawing) would leave holes: those
            # pixels take the ROM icon itself, upscaled by xBRZ (its own pixels, no recolour).
            ref=folder/f'unit_{resource}_native.png'
            if missing and ref.exists():
                from native_obj_filter import _xbrz4
                nr=np.asarray(Image.open(ref).convert('RGBA')).astype(np.uint32)
                argb=np.where(nr[...,3]>0,(255<<24)|(nr[...,0]<<16)|(nr[...,1]<<8)|nr[...,2],0).astype(np.uint32)
                up=_xbrz4(argb);up=np.dstack([(up>>16)&255,(up>>8)&255,up&255,(up>>24)&255]).astype('uint8')
                up=np.asarray(Image.fromarray(up).resize(size,Image.Resampling.LANCZOS))
                o=np.asarray(output).copy();hole=(o[...,3]<128)&(up[...,3]>128)
                o[hole]=up[hole];output=Image.fromarray(o)
            output.save(out_dir/f'unit_{resource}_hd.png')
            ok=iou>=.75
            row=dict(unit_id=uid,resource=resource,iou=round(iou,3),parts=n,missing_hd=missing,status='replaced' if (ok and a.apply) else ('ok' if ok else 'kept old'));rows.append(row)
            if ok and a.apply:
                bak=img.with_name(f'unit_{resource}_hd.before_{a.tag}.png')
                if not bak.exists():shutil.copy2(img,bak)
                output.save(img,optimize=True)
            print(row,flush=True)
    finally:c.close();renderer.parts_renderer.close()
    (out_dir/'report.json').write_text(json.dumps(rows,ensure_ascii=False,indent=1),encoding='utf-8')


if __name__=='__main__':main()
