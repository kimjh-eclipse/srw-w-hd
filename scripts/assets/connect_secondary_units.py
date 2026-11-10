"""Reuse assembled painted unit parts for the separate ROM mini-unit IMG bank.

Only ROM-named counterparts with sufficient silhouette agreement are accepted.
No low-resolution alpha mask is imposed on the painted outline.
"""
import sys,json,ctypes as C,struct,zlib,base64,argparse
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
    p=argparse.ArgumentParser();p.add_argument('--units',default='all');p.add_argument('--apply',action='store_true');args=p.parse_args()
    catalog=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text())
    selected=None if args.units=='all' else set(map(int,args.units.split(',')))
    units=[u for u in catalog['units'] if u['primary_image'] is not None and u.get('secondary_image') and (selected is None or u['unit_id'] in selected)]
    folder=ROOT/'graphics/secondary_units';folder.mkdir(exist_ok=True)
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    library_path=ROOT/'graphics/kazuma_parts_library.json';library=json.loads(library_path.read_text())
    known={b.get('resource') for b in library['bindings'] if b.get('secondary_unit')};registered=set();rows=[]
    packages={p['resource']:p for p in json.loads((ROOT/'graphics/all_units/catalog.json').read_text())['packages']}
    def append_binding(resource,a,rgb,image,reference):
        h,w=a.shape;index=np.where(a,a.astype('uint16')|0x8000,0).astype('<u2')
        q=np.rint(np.asarray(rgb)*31/255).astype('uint32');pal=q[:,0]|q[:,1]<<5|q[:,2]<<10
        colors=np.where(a,pal[a]|0x8000,0).astype('<u2');name=f'secondary_unit_{resource}'
        library['atlases'][name]=dict(image=image,reference=reference,native_size=[w,h],lazy=True)
        library['bindings'].append(dict(hash=zlib.crc32(colors.tobytes())^(w<<16)^h,rgb_enabled=True,index_hash=zlib.crc32(index.tobytes())^(w<<16)^h,indexed_safe=True,dynamic_palette=True,original_palette_rgb=rgb,index_pixels=base64.b64encode(zlib.compress(a.tobytes())).decode('ascii'),x=0,y=0,w=w,h=h,atlas_id=name,resource=resource,source_x=0,source_y=0,secondary_unit=True,auto_unit=True))
    checkpoint=folder/'registration.json'
    if args.apply and checkpoint.exists():
        prior=json.loads(checkpoint.read_text())
        if prior.get('applied'):
            for row in prior['rows']:
                if row['status']!='accepted' or row['resource'] in known:continue
                resource=row['resource'];image=f'secondary_units/unit_{resource}_hd.png';reference=f'secondary_units/unit_{resource}_native.png'
                with Image.open(ROOT/'graphics'/image) as art:art.verify()
                a=g.pixels(g.decompress(rom[g.BASE+offsets[resource]:g.BASE+offsets[resource+1]]))
                rgba=np.asarray(Image.open(ROOT/'graphics'/reference).convert('RGBA'));rgb=np.zeros((16,3),dtype='uint8')
                for index in np.unique(a):
                    if index:rgb[index]=rgba[a==index][0,:3]
                append_binding(resource,a,rgb.tolist(),image,reference);registered.add(resource);rows.append(row)
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=ROOT/'test_current/combat/roster_saves')
    renderer=HDRenderer(async_parts=False);renderer.set_resolution(768)
    def step(buttons,n):
        c.buttons=set(buttons)
        for _ in range(n):c.run();c.audio.clear()
        c.buttons=set()
    try:
        for u in units:
            uid=u['unit_id'];resource=u['secondary_image']
            if resource in registered or resource in known:continue
            a=g.pixels(g.decompress(rom[g.BASE+offsets[resource]:g.BASE+offsets[resource+1]]))
            native=Image.fromarray((a!=0).astype('uint8')*255);target=native.getbbox()
            if target is None:continue
            gallery=ROOT/f'graphics/all_units/unit_{u["primary_image"]}_hd_pose.png'
            if gallery.exists() and u['primary_image'] in packages:
                canvas=Image.open(gallery).convert('RGBA');slots=[]
                rgb=np.asarray(packages[u['primary_image']]['palette_rgb'],dtype='uint32')[:16];q=np.rint(rgb*31/255).astype('uint32');palette=(q[:,0]|q[:,1]<<5|q[:,2]<<10).astype('uint16')
                bindings=[i for i,b in enumerate(library['bindings'],1) if b.get('resource')==u['primary_image'] and not b.get('source_binding')]
            else:
                c.load(ROOT/'test_current/combat/sandrock_weapons.state');step([],15)
                c.api.retro_get_memory_data.restype=C.c_void_p;ram=c.api.retro_get_memory_data(2);unit=ram+0x1f0dbc+3*64
                for off in (6,10):C.c_int16.from_address(unit+off).value=uid
                C.c_uint32.from_address(unit).value=max(1,u['hp']);C.c_uint16.from_address(unit+4).value=u['en']
                step([0],5);step([],35)
                attrs=np.frombuffer(c.obj.raw,dtype='<u2').reshape(128,4);canvas=Image.new('RGBA',(768,576));slots=[];palette=None;bindings=[]
                for i,(oa,ob,ot,_) in enumerate(attrs):
                    x=int(ob&511);y=int(oa&255)
                    if (oa&0x300)==0x200 or not (166<=x<256 and 88<=y<166 and ot>>12==6):continue
                    bid=int(c.parts[i,0])
                    if not bid:continue
                    art=renderer.parts_renderer.sprite(c.parts[i],c.obj.raw,c.part_palettes[i])
                    if art is None:continue
                    canvas.alpha_composite(art,(round(x*hd_parts.SCALE),round(y*hd_parts.SCALE)))
                    slots.append(i);bindings.append(bid);palette=c.part_palettes[i].copy()
            # Native OBJ pixels/ownership may already be omitted by the core
            # once an HD binding is ready. Compare the actual assembled paint
            # silhouette to the distinct mini IMG, not an erased owner plane.
            box=canvas.getbbox();mask=canvas.getchannel('A').resize((256,192),Image.Resampling.BOX)
            mask=Image.fromarray((np.asarray(mask)>64).astype('uint8')*255);mb=mask.getbbox()
            if box is None or mb is None:
                rows.append(dict(unit_id=uid,resource=resource,status='no_primary_pose',slots=slots,paint_box=box,native_box=mb,active_bindings=int(np.count_nonzero(c.parts[:,0]))))
                Image.fromarray(c.native).save(folder/'current_native.png')
                continue
            silhouette=mask.crop(mb).resize((target[2]-target[0],target[3]-target[1]),Image.Resampling.NEAREST)
            expected=np.asarray(native.crop(target))>0
            options=[]
            for flip in (False,True):
                probe=silhouette.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if flip else silhouette
                actual=np.asarray(probe)>0;iou=float((actual&expected).sum()/max(1,(actual|expected).sum()));options.append((iou,flip))
            iou,flip=max(options);row=dict(unit_id=uid,name_ja=u['name_ja'],resource=resource,primary_resource=u['primary_image'],silhouette_iou=iou,flip_x=flip,source_bindings=bindings,status='accepted' if iou>=.82 else 'pose_mismatch',gameplay_verified=False)
            rows.append(row)
            if iou>=.82:
                scale=960/max(a.shape);size=(round(a.shape[1]*scale),round(a.shape[0]*scale));dest=tuple(round(v*scale) for v in target)
                paint=canvas.crop(box)
                if flip:paint=paint.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                output=Image.new('RGBA',size);output.alpha_composite(paint.resize((dest[2]-dest[0],dest[3]-dest[1]),Image.Resampling.LANCZOS),dest[:2])
                name=f'secondary_unit_{resource}';image=f'secondary_units/unit_{resource}_hd.png';reference=f'secondary_units/unit_{resource}_native.png'
                pal=np.asarray(palette,dtype='uint32');rgb=np.stack([(pal&31)*255//31,((pal>>5)&31)*255//31,((pal>>10)&31)*255//31],-1).astype('uint8')
                if args.apply:
                    output.save(ROOT/'graphics'/image,optimize=True);Image.fromarray(np.dstack([rgb[a],(a!=0).astype('uint8')*255])).save(ROOT/'graphics'/reference)
                    append_binding(resource,a,rgb.tolist(),image,reference)
                registered.add(resource)
            if len(rows)%25==0:print('examined',len(rows),'connected',len(registered),flush=True)
            (folder/'registration.json').write_text(json.dumps(dict(applied=args.apply,checked=len(rows),accepted=len(registered),rows=rows),ensure_ascii=False,indent=2),encoding='utf-8')
    finally:c.close();renderer.parts_renderer.close()
    (folder/'registration.json').write_text(json.dumps(dict(applied=args.apply,checked=len(rows),accepted=len(registered),rows=rows),ensure_ascii=False,indent=2),encoding='utf-8')
    if args.apply:
        temporary=library_path.with_suffix('.tmp.json');temporary.write_text(json.dumps(library,indent=2));temporary.replace(library_path)
    print('checked',len(rows),'accepted',len(registered),'applied',args.apply,flush=True)

if __name__=='__main__':main()
