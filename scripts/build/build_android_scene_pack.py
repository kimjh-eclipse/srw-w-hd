"""Android HD pack for cut-ins and battle backgrounds (android_pack/scene.pack).

Pictures are prepared exactly as the PC player prepares them for a 1024x768 top screen (SCALE 4):
  cut-ins   cutin_assets.CutinAssets: (W, round(W*h/w)) LANCZOS, clean_alpha for paint_image, cropped
            to its painted bbox; id 1 = graphics/kazuma_cutin_hd.png at 1024x768.
  battle BG hd_battle_backgrounds.prepare_texture: native_size x 4 LANCZOS with the art_owner
            palette transfer (the hardware canvas is applied at run time by the period).

  header  b'SRWHDSC1'
  u32 ncut;  ncut x (u32 id, u32 flags[bit0 pilot, bit1 repeat_native_plane, bit2 restore_rect, bits 8-23 family = image folder], i32 bx, by, u32 w, h, i32 restore l,t,r,b, u64 off, u32 len)
  u32 nreg;  nreg x 5 u32  register_cutins rows
  u32 nmap;  nmap x 2 u32  register_cutin_maps rows
  u32 nwin;  nwin x 3 u32  register_cutin_map_windows rows
  u32 nbg;   nbg x (u32 layers mask, u16 native w, h, u64 off, u32 len)   (len 0 = no art), index order
  u16 references[nbg][256][256]   runtime_index/references.npy
  blobs (lossless WebP RGBA, exact)

  py -3.11 -X utf8 scripts/build/build_android_scene_pack.py
"""
import io,json,struct,sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]));sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'emulator'))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image

W=1024;G=ROOT/'graphics';OUT=ROOT/'android_pack'


def find(rel):
    p=G/rel
    if p.exists():return p
    q=p.with_suffix('.webp')
    return q if q.exists() else None


def webp(im):
    b=io.BytesIO();im.save(b,'WEBP',lossless=True,exact=True,method=4);return b.getvalue()


def cutin_job(row):
    from painted_edges import clean_alpha
    if row is None:
        art=Image.open(G/'kazuma_cutin_hd.png').convert('RGBA').resize((W,W*3//4),Image.Resampling.LANCZOS)
    else:
        w,h=row.get('native_size',[256,192]);path=find(row.get('paint_image',row['image']))
        with Image.open(path) as s:art=s.convert('RGBA').resize((W,round(W*h/w)),Image.Resampling.LANCZOS)
        if row.get('paint_image'):art=clean_alpha(art)
    box=art.getbbox() or (0,0,1,1)
    return box,art.size,webp(art.crop(box))


def bg_job(args):
    from hd_battle_backgrounds import prepare_texture
    item,owner=args
    w,h=item['native_size']
    art=prepare_texture(item,owner,(W,W*3//4),(w,h))      # canvas == art size here
    return webp(art)


def main():
    lib=json.loads((G/'cutins_library.json').read_text())['cutins']
    from hd_renderer import character_cutin
    cutins=[(1,None)]+[(c['id'],c) for c in lib if find(c['image']) and find(c.get('paint_image',c['image']))]
    reg=[];maps=[];wins=[]
    for c in lib:
        if not find(c['image']):continue
        mode={'image_origin':256,'origin_8192':512,'row_padded':768}.get(c.get('signature_mode'),0)
        for s in c['signatures']:
            for layer in c.get('layers',[c['layer']]):reg.append((s,c['id'],layer|mode,*c['native_size']))
        if 'map_signature' in c:maps.append((c['id'],c['map_signature']))
        if c.get('map_window_entries'):wins.append((c['id'],c['map_window_signature'],c['map_window_entries']))
    F=G/'battle_backgrounds';cat=json.loads((F/'catalog.json').read_text(encoding='utf-8'))['resources']
    meta=json.loads((F/'runtime_index/index.json').read_text());refs=np.load(F/'runtime_index/references.npy')
    by=[{r['name']:r for r in cat}][0]
    bgs=[]
    for i,name in enumerate(meta['names']):
        item=by.get(name);ok=item is not None and find(item['image']) is not None
        bgs.append((item if ok else None,by.get(item.get('art_owner')) if ok else None,sum(1<<l for l in meta['layers'][i])))
    with ProcessPoolExecutor(8) as ex:
        cut=list(ex.map(cutin_job,[c for _,c in cutins],chunksize=4))
        print('cutins',len(cut),flush=True)
        bgb=list(ex.map(bg_job,[(it,ow) for it,ow,_ in bgs if it is not None],chunksize=4))
        print('battle backgrounds',len(bgb),flush=True)
    head=bytearray(b'SRWHDSC1')
    blobs=[]
    n_cut=len(cutins);n_bg=len(bgs)
    size=8+4+n_cut*52+4+len(reg)*20+4+len(maps)*8+4+len(wins)*12+4+n_bg*20+refs.nbytes
    pos=size;cut_rows=[];families={}
    for (cid,c),(box,full,blob) in zip(cutins,cut):
        rr=(c or {}).get('restore_rect') or [0,0,0,0]
        flags=(1 if character_cutin(c or {},cid) else 0)|(2 if c and c.get('repeat_native_plane') else 0)|(4 if (c or {}).get('restore_rect') else 0)
        folder=str(Path((c or {}).get('image','kazuma')).parent);fam=families.setdefault(folder,len(families)+1);flags|=(fam&0xffff)<<8   # same folder = one animated sequence, preloaded together
        cut_rows.append(struct.pack('<IIiiIIiiiiQI',cid,flags,box[0],box[1],full[0],full[1],*rr,pos,len(blob)));blobs.append(blob);pos+=len(blob)
    bg_rows=[];k=0
    for item,owner,mask in bgs:
        if item is None:bg_rows.append(struct.pack('<IHHQI',mask,0,0,0,0));continue
        blob=bgb[k];k+=1;w,h=item['native_size']
        bg_rows.append(struct.pack('<IHHQI',mask,w,h,pos,len(blob)));blobs.append(blob);pos+=len(blob)
    with open(OUT/'scene.pack','wb') as f:
        f.write(head+struct.pack('<I',n_cut));[f.write(r) for r in cut_rows]
        f.write(struct.pack('<I',len(reg)));[f.write(struct.pack('<5I',*r)) for r in reg]
        f.write(struct.pack('<I',len(maps)));[f.write(struct.pack('<2I',*r)) for r in maps]
        f.write(struct.pack('<I',len(wins)));[f.write(struct.pack('<3I',*r)) for r in wins]
        f.write(struct.pack('<I',n_bg));[f.write(r) for r in bg_rows]
        f.write(refs.astype('<u2').tobytes())
        assert f.tell()==size,(f.tell(),size)
        for b in blobs:f.write(b)
    print('scene.pack',round(pos/1e6),'MB, cutins',n_cut,'reg rows',len(reg),'maps',len(maps),'windows',len(wins),'bg',n_bg,'with art',k)


if __name__=='__main__':main()
