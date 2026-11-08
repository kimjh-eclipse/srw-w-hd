"""Exercise named units through the game's actual native forecast renderer.

Only an isolated core's RAM is changed. Player RAM, saves and the ROM are never
written. This verifies forecast poses, not attacks or campaign availability.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import argparse,ctypes as C,json,time,hashlib,base64,zlib
import numpy as np
from PIL import Image,ImageDraw
from hd_core import Core
from hd_renderer import HDRenderer

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--units',default='all');args=parser.parse_args()
    roster=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text());units=roster['units']
    selected=set(map(int,args.units.split(','))) if args.units!='all' else None
    units=[u for u in units if u['primary_image'] is not None and (selected is None or u['unit_id'] in selected)]
    out=ROOT/'test_current/parts/named_forecasts';out.mkdir(exist_ok=True)
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=ROOT/'test_current/combat/roster_saves')
    r=HDRenderer(async_parts=False);r.set_resolution(768);rows=[];cards=[];start=time.perf_counter()
    def step(buttons,frames):
        c.buttons=set(buttons)
        for _ in range(frames):c.run();c.audio.clear()
        c.buttons=set()
    try:
        for u in units:
            uid=u['unit_id'];c.load(ROOT/'test_current/combat/sandrock_weapons.state');step([],15)
            c.api.retro_get_memory_data.restype=C.c_void_p;ram=c.api.retro_get_memory_data(2);unit=ram+0x1f0dbc+3*64
            for off in [6,10]:C.c_int16.from_address(unit+off).value=uid
            C.c_uint32.from_address(unit).value=max(1,u['hp']);C.c_uint16.from_address(unit+4).value=u['en']
            step([0],5);step([],35)
            # The normal game's B handler redraws the forecast from its new
            # unit record; the HD compositor receives real OAM and VRAM.
            kw=dict(paused=True,parts=c.parts,obj=c.obj.raw,owners=c.owners,bgpriors=c.bgpriors,
                    bgparts=c.bgparts,part_palettes=c.part_palettes,backgrounds=c.backgrounds,
                    bg_layout=c.bg_layout,unknown=c.unknown_snapshot(),
                    sub_parts=(c.sub_parts,c.sub_owners,c.sub_oam.raw,c.sub_palettes,c.sub_ids,c.sub_priorities))
            image=r.render_top(c.native,c.ids,c.hd,**kw)
            oam=np.frombuffer(c.obj.raw,dtype='<u2').reshape(128,4);visible=[];missing=[];seen=[]
            vram=C.create_string_buffer(131072);c.api.retro_srw_copy_vram(0x06400000,vram,131072)
            raw=np.frombuffer(vram.raw,dtype='uint8')
            dims=[[(8,8),(16,16),(32,32),(64,64)],[(16,8),(32,8),(32,16),(64,32)],[(8,16),(8,32),(16,32),(32,64)]]
            for i,(a,b,t,_) in enumerate(oam):
                if (a&0x300)==0x200 or a>>14==3:continue
                x=int(b&511);y=int(a&255)
                # Forecast figures use OBJ palette 6. Palette 9 is the large
                # hit-rate display and palette 13 is the ON/OFF control.
                if not (166<=x<256 and 88<=y<166 and t>>12==6):continue
                # The native menu retains enabled but completely transparent
                # OBJ slots. They are not unconverted robot fragments.
                w,h=dims[a>>14][b>>14];base=int(t&1023)*32
                packed=np.concatenate([raw[base+yy*1024+xx*32:base+yy*1024+xx*32+32]
                                       for yy in range(h//8) for xx in range(w//8)])
                if not packed.any():continue
                bid=int(c.parts[i,0]);visible.append(i)
                if bid:seen.append(bid)
                else:missing.append(i)
            record=dict(unit_id=uid,name_ja=u['name_ja'],name_ko=u['name_ko'],primary_image=u['primary_image'],
                        real_native_forecast=True,attack_replay=False,visible_unit_objects=len(visible),
                        bound_unit_objects=len(seen),unbound_unit_objects=missing,
                        observed_bindings=sorted(set(seen)),prepare_errors=dict(r.parts_renderer.prepare_errors),
                        hd_sha256=hashlib.sha256(np.asarray(image).tobytes()).hexdigest())
            rows.append(record)
            snapshot=c.unknown_snapshot();unknown=[]
            if snapshot is not None:
                descriptors,pixels,palettes=snapshot
                for i in missing:
                    key,w,h,*_=map(int,descriptors[i])
                    if not key:continue
                    unknown.append(dict(object=i,index_hash=key,w=w,h=h,
                        hash=int(descriptors[i,6]),palette=palettes[i].tolist(),
                        indices=base64.b64encode(zlib.compress(pixels[i,:w*h].tobytes())).decode('ascii')))
            record['unknown_parts']=unknown
            card=image.resize((384,288));ImageDraw.Draw(card).text((4,4),f'Unit {uid} / IMG {u["primary_image"]}',fill='yellow');cards.append(card)
            if missing or not seen or r.parts_renderer.prepare_errors:
                image.save(out/f'unit_{uid}_hd.png');Image.fromarray(c.native).save(out/f'unit_{uid}_native.png')
            if len(cards)==20 or u is units[-1]:
                page=(len(rows)-1)//20;sheet=Image.new('RGB',(384*5,288*4))
                for i,card in enumerate(cards):sheet.paste(card,(i%5*384,i//5*288))
                sheet.save(out/f'contact_{page:02}.png');cards=[]
            report=dict(scope='Actual native forecast poses only; not all attacks/cutins',checked=len(rows),seconds=round(time.perf_counter()-start,1),
                        units_with_unbound_objects=[x['unit_id'] for x in rows if x['unbound_unit_objects']],rows=rows)
            (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
            print(uid,u['name_ko'],'objects',len(seen),'missing',len(missing),flush=True)
    finally:c.close();r.parts_renderer.close()

if __name__=='__main__':main()
