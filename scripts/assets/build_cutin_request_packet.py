"""Drawing-request packet for a cut-in shown on the top screen (Trowa mask precedent).

Captures one frame of an attack-start state with the plain core and writes
test_current/parts/cutin_requests/<name>/:
  live_native.png / live_native_4x.png   the whole top screen as shown (256x192, 4x nearest)
  layer_bg<N>.png / layer_obj.png         each layer alone (same frame, 1x)  + _4x copies
  owner_map.png                            which layer owns each screen pixel (colour key in contract)
  current_hd.png                           what the production renderer shows now (768 wide)
  live_bg<N>_map.bin / _tiles.bin          raw VRAM of the cut-in BG layers
  rendered_obj.json                        OBJ contracts of the frame (scripts/assets/capture_rendered_obj_contract.py)
  contract.json                            layers, matched ROM IMG/PLT/SCR ids, HD status, what to draw

The ROM IMG ids are found by matching the live BG character tiles against every
IMG resource in the given id range (tile-bytes identity, no pixel guessing).

  py -3.11 -X utf8 scripts/assets/build_cutin_request_packet.py --name x --state S --frame 300 [--frames 300,340]
"""
import argparse,ctypes as C,hashlib,json,pickle,struct,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
sys.path.insert(0,str(ROOT/'emulator'))
from scripts.assets import srw_graphics as g

ROM=ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds'
OUTROOT=ROOT/'test_current/parts/cutin_requests'
INDEX=OUTROOT/'_img_tile_index.pkl'
OWNER_COLOURS={0:(255,64,64),1:(64,200,64),2:(64,96,255),3:(255,200,0),4:(255,0,255),5:(40,40,40)}


def img_tile_index(lo,hi):
    """{sha1(tile bytes): {resource,...}} for 4bpp and 8bpp IMG resources lo..hi (cached)."""
    if INDEX.exists():
        data=pickle.loads(INDEX.read_bytes())
        if data['range']==[lo,hi]:return data
    rom=ROM.read_bytes();off=g.archive(rom);idx4={};idx8={};meta={}
    for r in range(lo,min(hi,len(off)-1)):
        raw=rom[g.BASE+off[r]:g.BASE+off[r+1]]
        if len(raw)<8:continue
        try:data=g.decompress(raw)
        except Exception:continue
        if data[:3]!=b'IMG':continue
        wt,ht=struct.unpack_from('<HH',data,4);bpp=8 if data[3] else 4;size=32 if bpp==4 else 64;body=data[8:8+wt*ht*size]
        meta[r]=dict(tiles_w=wt,tiles_h=ht,bpp=bpp)
        target=idx4 if bpp==4 else idx8
        for k in range(0,len(body),size):
            t=body[k:k+size]
            if t.count(0)==size:continue
            target.setdefault(hashlib.sha1(t).digest()[:10],set()).add(r)
    data=dict(range=[lo,hi],idx4=idx4,idx8=idx8,meta=meta)
    INDEX.parent.mkdir(parents=True,exist_ok=True);INDEX.write_bytes(pickle.dumps(data));return data


def match_tiles(index,tiles,bpp):
    size=32 if bpp==4 else 64;table=index['idx4' if bpp==4 else 'idx8'];hits={};total=0
    for k in range(0,len(tiles),size):
        t=tiles[k:k+size]
        if len(t)<size or t.count(0)==size:continue
        total+=1
        for r in table.get(hashlib.sha1(t).digest()[:10],()):hits[r]=hits.get(r,0)+1
    rows=sorted(hits.items(),key=lambda kv:-kv[1])
    return total,[dict(image=r,matched_tiles=n,image_tiles=index['meta'][r]['tiles_w']*index['meta'][r]['tiles_h']) for r,n in rows[:6]]


def rom_resource(i,_cache={}):
    if 'rom' not in _cache:_cache['rom']=ROM.read_bytes();_cache['off']=g.archive(_cache['rom'])
    rom,off=_cache['rom'],_cache['off'];return g.decompress(rom[g.BASE+off[i]:g.BASE+off[i+1]])


def decode_resource(img,scr,plt,live_palette=None):
    """IMG+SCR+PLT straight from the ROM -> RGBA (colour index 0 transparent); SCR header word 3 = rows."""
    pix=g.pixels(rom_resource(img));wt=pix.shape[1]//8
    tiles=pix.reshape(pix.shape[0]//8,8,wt,8).transpose(0,2,1,3).reshape(-1,8,8)
    s=rom_resource(scr);n=(len(s)-8)//2;e=np.array(struct.unpack_from(f'<{n}H',s,8))
    rows=struct.unpack_from('<H',s,6)[0] or n//32;cols=n//rows
    if plt:pal=np.array(g.palette(rom_resource(plt)),dtype='uint8')
    else:   # PLT id 0: the game swaps palettes for this picture, use the live BG palette (banks from the live layer)
        v=np.asarray(live_palette,dtype=int);pal=np.stack([(v&31)*255//31,((v>>5)&31)*255//31,((v>>10)&31)*255//31,np.full_like(v,255)],1).astype('uint8')
    used=(e&0x3ff)>0
    base=int((e[used]>>12).min()) if used.any() else 0
    out=np.zeros((rows*8,cols*8,4),dtype='uint8')
    for k,v in enumerate(e):
        t=int(v)&0x3ff
        if t>=len(tiles):continue
        tile=tiles[t]
        if v&0x400:tile=tile[:,::-1]
        if v&0x800:tile=tile[::-1]
        rgba=pal[np.clip(tile.astype(int)+16*((int(v)>>12)-base),0,len(pal)-1)].copy();rgba[tile==0,3]=0
        out[(k//cols)*8:(k//cols)*8+8,(k%cols)*8:(k%cols)*8+8]=rgba
    return out


def screen_agreement(picture,layer_png,scroll,wrap,rows=128):
    """Best placement of the ROM picture on the isolated live layer (top ROWS screen rows, above the text box).
    Returns (scroll_x, scroll_y, share of opaque picture pixels with the same colour). The register
    scroll is tried first; the search covers the whole wrap because some cut-ins set scroll mid-frame."""
    live=np.asarray(Image.open(layer_png).convert('RGB')).astype(int)[:rows]
    W,H=wrap;canvas=np.zeros((H,W,4),dtype=int);h,w=picture.shape[:2];canvas[:min(h,H),:min(w,W)]=picture[:H,:W]
    def score(sx,sy):
        view=np.roll(np.roll(canvas,-sy,0),-sx,1)[:rows,:256];m=view[:,:,3]>0
        if not m.any():return 0.0
        return float((np.abs(view[:,:,:3]-live).sum(2)[m]<24).mean())
    sx,sy=scroll;best=(score(sx,sy),sx,sy)
    if best[0]<.99:
        best=max([best]+[(score(sx,y),sx,y) for y in range(H)]);best=max([best]+[(score(x,best[2]),x,best[2]) for x in range(W)])
    return best[1],best[2],round(best[0],4)


def main():
    p=argparse.ArgumentParser();p.add_argument('--name',required=True);p.add_argument('--state',required=True);p.add_argument('--frame',type=int,required=True)
    p.add_argument('--resources',default='',help='bg:IMG:SCR:PLT,... decoded from the ROM as the native drawing canvases')
    p.add_argument('--range',default='22000,29500');p.add_argument('--purpose',default='');p.add_argument('--layers',default='',help='BG layers that make the cut-in, e.g. 1,2 (default: all enabled BG)')
    a=p.parse_args();lo,hi=map(int,a.range.split(','))
    out=OUTROOT/a.name;out.mkdir(parents=True,exist_ok=True);state=ROOT/a.state
    index=img_tile_index(lo,hi)
    inventory={r['image']:r for r in json.loads((ROOT/'test_current/parts/cutin_bank/inventory.json').read_text())['images']}
    library=json.loads((ROOT/'graphics/cutins_library.json').read_text(encoding='utf-8'))['cutins']
    by_resource={}
    for c in library:
        for key in ('resource',):
            if c.get(key):by_resource.setdefault(int(c[key]),[]).append(dict(id=c['id'],name=c.get('name'),paint_image=c.get('paint_image'),gameplay_verified=c.get('gameplay_verified')))
    from hd_core import Core
    from scripts.assets.capture_rendered_obj_contract import capture_rendered_obj_contracts
    core=Core(ROM,enabled=True,demo=True,user_dir=out/'isolated_saves')
    tmp=out/'isolated_saves'/'frame.state'
    try:
        core.load(state)
        for _ in range(a.frame):core.run();core.audio.clear()
        core.save(tmp)
        core.api.retro_srw_set_main_layers.argtypes=[C.c_uint]
        def shot(mask):
            core.load(tmp);core.api.retro_srw_set_main_layers(mask);core.run();core.audio.clear()
            return np.asarray(core.native)[:192].copy()
        layers={}
        for name,mask in (('bg0',1),('bg1',2),('bg2',4),('bg3',8),('obj',16)):layers[name]=shot(mask)
        native=shot(0x1f)
        live_pal=np.zeros(256,dtype='<u2');core.api.retro_srw_copy_effect_debug(None,None,live_pal.ctypes.data,None)
        ids=np.asarray(core.ids).copy();bg_layout=[list(map(int,x)) for x in core.bg_layout];cutin_layers=core.cutin_layers.astype(int).tolist()
        backgrounds=[list(map(int,x)) for x in core.backgrounds]
        obj=capture_rendered_obj_contracts(core,state=str(state.relative_to(ROOT)).replace('\\','/'),frame=a.frame)
        live={}
        for layer in range(4):
            info=bg_layout[layer]
            if not info[7]:continue
            maps=C.create_string_buffer(info[5]*info[6]//32);core.api.retro_srw_copy_vram(info[1],maps,len(maps))
            tiles=C.create_string_buffer(65536);core.api.retro_srw_copy_vram(info[2],tiles,len(tiles))
            live[layer]=(maps.raw,tiles.raw)
        # current production picture
        from hd_renderer import HDRenderer
        core.load(tmp);core.api.retro_srw_set_main_layers(0x1f);core.run();core.audio.clear()
        r=HDRenderer(async_parts=False,dynamic_parts=True);r.set_resolution(768)
        kw=dict(paused=True,parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,backgrounds=core.backgrounds,bg_layout=core.bg_layout,unknown=core.unknown_snapshot(),cutin_layers=core.cutin_layers,sub_parts=(core.sub_parts,core.sub_owners,core.sub_oam.raw,core.sub_palettes,core.sub_ids,core.sub_priorities),effect_foreground=core.effect_foreground,window=core.window,cutin_palettes=getattr(core,'cutin_palettes',None))
        import time
        img=r.render_top(core.native,core.ids,core.hd,**kw)
        for _ in range(25):
            if hasattr(r,'portraits'):r.portraits.collect_prepared()
            if not getattr(getattr(r,'portraits',None),'pending',None):break
            time.sleep(.1)
        img=r.render_top(core.native,core.ids,core.hd,**kw);img.save(out/'current_hd.png')
    finally:
        try:core.api.retro_srw_set_main_layers(0x1f)
        except Exception:pass
        core.close()
    Image.fromarray(native).save(out/'live_native.png');Image.fromarray(native).resize((1024,768),Image.Resampling.NEAREST).save(out/'live_native_4x.png')
    for name,im in layers.items():
        if im.reshape(-1,im.shape[-1])[:, :3].max()==0:continue
        Image.fromarray(im).save(out/f'layer_{name}.png');Image.fromarray(im).resize((1024,768),Image.Resampling.NEAREST).save(out/f'layer_{name}_4x.png')
    own=np.zeros((192,256,3),dtype='uint8')
    for k,c in OWNER_COLOURS.items():own[ids[:192]==k]=c
    Image.fromarray(own).save(out/'owner_map.png')
    (out/'rendered_obj.json').write_text(json.dumps(obj,indent=1))
    use=[int(x) for x in a.layers.split(',')] if a.layers else sorted(live)
    rows=[]
    for layer in sorted(live):
        info=bg_layout[layer];maps,tiles=live[layer];bpp=8 if info[0]&0x80 else 4
        (out/f'live_bg{layer}_map.bin').write_bytes(maps);(out/f'live_bg{layer}_tiles.bin').write_bytes(tiles)
        entries=np.frombuffer(maps,dtype='<u2');size=32 if bpp==4 else 64
        used=sorted({int(e)&0x3ff for e in entries});banks=sorted({int(e)>>12 for e in entries if int(e)&0x3ff})
        total,matches=match_tiles(index,b''.join(tiles[i*size:(i+1)*size] for i in used),bpp)
        for m in matches:
            inv=inventory.get(m['image'],{});m.update(palette=inv.get('palette'),map=inv.get('map'),inventory_size=inv.get('size'),hd_library=by_resource.get(m['image'],[]))
        rows.append(dict(bg=layer,bgcnt=hex(info[0]),bpp=bpp,size=[info[5],info[6]],scroll=[info[3],info[4]],priority=info[8],cutin_layer=layer in use,
                         live_nonblank_tiles=total,map_tile_indices_used=len(used),palette_banks=banks,map_crc32=zlib.crc32(maps),rom_image_matches=matches))
    canvases=[]
    for spec in filter(None,a.resources.split(',')):
        bg,img,scr,plt=map(int,spec.split(':'));info=bg_layout[bg]
        lb=min(rows[[r['bg'] for r in rows].index(bg)]['palette_banks'] or [0])
        pic=decode_resource(img,scr,plt,live_pal[lb*16:])
        Image.fromarray(pic).save(out/f'native_{img}.png');Image.fromarray(pic).resize((pic.shape[1]*4,pic.shape[0]*4),Image.Resampling.NEAREST).save(out/f'native_{img}_4x.png')
        fx,fy,agree=screen_agreement(pic,out/f'layer_bg{bg}.png',(info[3],info[4]),(info[5],info[6]))
        canvases.append(dict(bg=bg,image=img,map=scr,palette=plt or f'live BG palette banks from {lb} (ROM PLT not the shown colours)',native_size=[pic.shape[1],pic.shape[0]],drawing_size=[pic.shape[1]*4,pic.shape[0]*4],
            register_scroll=[info[3],info[4]],matched_scroll=[fx,fy],screen_origin_at_frame=[(-fx)%info[5],(-fy)%info[6]],opaque_pixels=int((pic[:,:,3]>0).sum()),live_colour_agreement=agree,
            hd_library=by_resource.get(img,[]),native='native_%d.png'%img,native_4x='native_%d_4x.png'%img))
    contract=dict(purpose=a.purpose,source_state=str(state.relative_to(ROOT)).replace('\\','/'),frame=a.frame,
                  frame_note='all pictures are the frame after running FRAME frames from the state (isolated layers re-loaded from the same saved frame)',
                  bg_layout_fields='[bgcnt,map_vram,tile_vram,scroll_x,scroll_y,width,height,enabled,priority]',bg_layout=bg_layout,
                  owner_map_colours={str(k):v for k,v in OWNER_COLOURS.items()},owner_map_note='colour per core layer id (0-3 BG, 4 OBJ, 5 backdrop)',
                  hd_cutin_rows_live=[row for row in cutin_layers if row[0]],hd_backgrounds_live=backgrounds,layers=rows,obj_count=len(obj),drawing_canvases=canvases)
    (out/'contract.json').write_text(json.dumps(contract,ensure_ascii=False,indent=1),encoding='utf-8')
    print(json.dumps(dict(out=str(out),layers=[dict(bg=r['bg'],tiles=r['live_nonblank_tiles'],top=r['rom_image_matches'][:3]) for r in rows],cutin_live=contract['hd_cutin_rows_live'],backgrounds=backgrounds,obj=len(obj)),ensure_ascii=False,indent=1,default=str))


if __name__=='__main__':main()
