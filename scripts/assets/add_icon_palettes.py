"""HD mini-unit icons for every palette a shared icon is shown in.

An icon IMG (secondary_image) is shared by several units; the HD binding is keyed by the RGB of
ONE palette (e.g. Gates 6133: white). A unit showing the same icon in another palette (green
Gates) then gets no HD, or another unit's picture. Recolouring is not allowed, so each palette
gets its own picture: the unit's status screen is played, its battle parts (installed for that
palette) are assembled back to front (DS: lower OAM index in front), holes are filled from the
ROM icon upscaled by xBRZ in that same palette, and a binding keyed by that palette is added.

  py -3.11 -X utf8 scripts/assets/add_icon_palettes.py [--units 74,75] [--apply]
Writes graphics/secondary_units/unit_<res>_p<hash>_hd.png and (with --apply, under the install
lock) new secondary_unit bindings. Report: graphics/secondary_units/ICON_PALETTES.json
"""
import argparse,base64,collections,ctypes as C,json,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
sys.path.insert(0,str(ROOT/'emulator'))
from scripts.assets import srw_graphics as g


def main():
    p=argparse.ArgumentParser();p.add_argument('--units',default='');p.add_argument('--apply',action='store_true');a=p.parse_args()
    from hd_core import Core
    from hd_renderer import HDRenderer
    import hd_parts
    from native_obj_filter import _xbrz4
    cat=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text())
    by=collections.defaultdict(list)
    for u in cat['units']:
        if u.get('secondary_image'):by[u['secondary_image']].append(u)
    want=set(map(int,a.units.split(','))) if a.units else None
    units=[u for r,us in by.items() if len(us)>1 for u in us if want is None or u['unit_id'] in want]
    lib_path=ROOT/'graphics/kazuma_parts_library.json';lib=json.loads(lib_path.read_text(encoding='utf-8'))
    have=collections.defaultdict(set)
    for b in lib['bindings']:
        if b.get('secondary_unit') and not b.get('disabled'):have[b['resource']].add(b['hash'])
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    folder=ROOT/'graphics/secondary_units';rows=[];new=[]
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=ROOT/'test_current/combat/roster_saves')
    r=HDRenderer(async_parts=False);r.set_resolution(768)
    def step(buttons,n):
        c.buttons=set(buttons)
        for _ in range(n):c.run();c.audio.clear()
        c.buttons=set()
    try:
        for u in units:
            uid=u['unit_id'];res=u['secondary_image']
            ia=g.pixels(g.decompress(rom[g.BASE+offsets[res]:g.BASE+offsets[res+1]]));h,w=ia.shape
            c.load(ROOT/'test_current/combat/sandrock_weapons.state');step([],15)
            c.api.retro_get_memory_data.restype=C.c_void_p;ram=c.api.retro_get_memory_data(2);unit=ram+0x1f0dbc+3*64
            for off in (6,10):C.c_int16.from_address(unit+off).value=uid
            C.c_uint32.from_address(unit).value=max(1,u['hp']);C.c_uint16.from_address(unit+4).value=u['en']
            step([0],5);step([],35)
            attrs=np.frombuffer(c.obj.raw,dtype='<u2').reshape(128,4);canvas=Image.new('RGBA',(768,576));pal=None;n=0
            for i in sorted(range(128),key=lambda i:(-((int(attrs[i][2])>>10)&3),-i)):
                oa,ob,ot,_=attrs[i];x=int(ob&511);y=int(oa&255)
                if (oa&0x300)==0x200 or not (166<=x<256 and 88<=y<166 and ot>>12==6):continue
                if pal is None:pal=c.part_palettes[i].astype('uint32').copy()
                if not int(c.parts[i,0]):continue
                art=r.parts_renderer.sprite(c.parts[i],c.obj.raw,c.part_palettes[i])
                if art is None:continue
                canvas.alpha_composite(art,(round(x*hd_parts.SCALE),round(y*hd_parts.SCALE)));n+=1
            if pal is None:rows.append(dict(unit=uid,res=res,status='no sprite on the status screen'));continue
            colors=np.where(ia,(pal[ia]&0x7fff)|0x8000,0).astype('<u2');key=zlib.crc32(colors.tobytes())^(w<<16)^h
            if key in have[res]:rows.append(dict(unit=uid,res=res,status='palette already has HD'));continue
            rgb=np.stack([(pal&31)*255//31,((pal>>5)&31)*255//31,((pal>>10)&31)*255//31],-1).astype('uint32')
            box=canvas.getbbox();native=Image.fromarray((ia!=0).astype('uint8')*255);target=native.getbbox()
            scale=960/max(ia.shape);size=(round(w*scale),round(h*scale));dest=tuple(round(v*scale) for v in target)
            out=Image.new('RGBA',size)
            if box and n:out.alpha_composite(canvas.crop(box).resize((dest[2]-dest[0],dest[3]-dest[1]),Image.Resampling.LANCZOS),dest[:2])
            argb=np.where(ia>0,(255<<24)|(rgb[ia,0]<<16)|(rgb[ia,1]<<8)|rgb[ia,2],0).astype(np.uint32)
            up=_xbrz4(argb);up=np.dstack([(up>>16)&255,(up>>8)&255,up&255,(up>>24)&255]).astype('uint8')
            up=np.asarray(Image.fromarray(up).resize(size,Image.Resampling.LANCZOS));o=np.asarray(out).copy()
            hole=(o[...,3]<128)&(up[...,3]>128);o[hole]=up[hole];out=Image.fromarray(o)
            name=f'unit_{res}_p{key:08x}_hd.png';out.save(folder/name)
            ref=f'unit_{res}_p{key:08x}_native.png';Image.fromarray(np.dstack([rgb[ia],(ia!=0)*255]).astype('uint8')).save(folder/ref)
            have[res].add(key);rows.append(dict(unit=uid,res=res,status='new palette',hash=key,image=name,hd_parts=n,hole_px=int(hole.sum())))
            idx=np.where(ia,ia.astype('uint16')|0x8000,0).astype('<u2')
            new.append(dict(hash=key,rgb_enabled=True,index_hash=zlib.crc32(idx.tobytes())^(w<<16)^h,indexed_safe=True,dynamic_palette=True,original_palette_rgb=rgb.astype(int).tolist(),
                index_pixels=base64.b64encode(zlib.compress(ia.astype('uint8').tobytes())).decode('ascii'),x=0,y=0,w=w,h=h,atlas_id=f'secondary_unit_{res}_p{key:08x}',resource=res,source_x=0,source_y=0,secondary_unit=True,auto_unit=True,
                atlas=dict(image=f'secondary_units/{name}',reference=f'secondary_units/{ref}',native_size=[w,h],lazy=True)))
            print(rows[-1],flush=True)
    finally:c.close();r.parts_renderer.close()
    (folder/'ICON_PALETTES.json').write_text(json.dumps(rows,indent=1),encoding='utf-8')
    print('units',len(units),'new palettes',len(new))
    if a.apply and new:
        lib=json.loads(lib_path.read_text(encoding='utf-8'))
        for b in new:
            at=b.pop('atlas');lib['atlases'][b['atlas_id']]=at;lib['bindings'].append(b)
        lib_path.write_text(json.dumps(lib,ensure_ascii=False,indent=2),encoding='utf-8');print('bindings added',len(new))


if __name__=='__main__':main()
