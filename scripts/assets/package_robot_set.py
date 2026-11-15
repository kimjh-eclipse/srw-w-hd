"""Package a split robot set for install_pending_art.py.

Input: <set>/split_fit/parts/<hash>.png (4x, texture orientation, from
split_object_drawings.py) and the pose contracts (one row per sprite hash).
Each part's pixels that no pose showed (hidden in every frame) are filled by
growing the part's own drawn pixels; alpha stays 0 outside the native sprite.
No colour from another palette or picture is used.

Two packets go to <set>/install/:
  replace/  sprites whose exact RGB key already has HD (binding hash == sprite hash):
            nested contract with replace_binding, prior spec SHA recorded
  new/      sprites without their own RGB-keyed HD (unbound, or shown through an
            index/recolour match): new parts under their real RGB key
Both are added to docs/PENDING_ART_INSTALL_QUEUE.json (ready_candidates).

  py -3.11 -X utf8 scripts/assets/package_robot_set.py <set dir> [--split split_fit]
"""
import argparse,base64,hashlib,json,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets.fit_pose_drawing import grow_fill
from scripts.assets.install_pending_art import spec_hash

S=4


def pack(items,width=256):
    x=y=rowh=0;out=[]
    for it in sorted(items,key=lambda it:-it['h']):
        w,h=it['w'],it['h']
        if x+w>width:x=0;y+=rowh;rowh=0
        out.append((it,x,y));x+=w;rowh=max(rowh,h)
    return out,y+rowh


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def write_packet(folder,placed,H,make_row,entry_extra):
    folder.mkdir(parents=True,exist_ok=True)
    native=np.zeros((H,256,4),'uint8');cand=Image.new('RGBA',(256*S,H*S));rows=[]
    for it,x,y in placed:
        idx=it['idx'];pal=np.array(it['row']['original_palette_rgb'],dtype='uint8')
        native[y:y+it['h'],x:x+it['w'],:3]=pal[idx];native[y:y+it['h'],x:x+it['w'],3]=np.where(idx>0,255,0)
        cand.alpha_composite(it['art'],(x*S,y*S));rows.append(make_row(it,[x,y,it['w'],it['h']]))
    Image.fromarray(native).save(folder/'native_atlas.png');cand.save(folder/'candidate_atlas.png');cand.save(folder/'generated.png')
    (folder/'contract.json').write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8')
    entry=dict(source=str(folder.relative_to(ROOT)).replace('\\','/'),contract='contract.json',drawing='candidate_atlas.png',native='native_atlas.png',generated='generated.png',
        file_sha256={k:sha(folder/v) for k,v in (('contract','contract.json'),('drawing','candidate_atlas.png'),('native','native_atlas.png'),('generated','generated.png'))},**entry_extra(rows))
    (folder/'queue_entry.json').write_text(json.dumps(entry,ensure_ascii=False,indent=1),encoding='utf-8')
    return entry


def main():
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--split',default='split_fit')
    a=p.parse_args();root=a.root if a.root.is_absolute() else ROOT/a.root
    parts=root/a.split/'parts'
    lib=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text(encoding='utf-8'))['bindings']
    rows={}
    for c in sorted(root.glob('pose_*/contract.json')):
        for r in json.loads(c.read_text(encoding='utf-8')):rows.setdefault(r['hash'],r)
    items=[];new=[];replace=[];skipped=[]
    # The library as it is now: a sprite key may have been connected by another
    # unit's pose set since this set was captured (units share parts).
    active={}
    for i,b in enumerate(lib,1):
        if b.get('rgb_enabled',True) and not b.get('disabled'):active.setdefault(b['hash'],i)
    done=json.loads((ROOT/'docs/ART_INSTALL_DONE.json').read_text(encoding='utf-8')).get('installed',[])
    # Atlases redrawn by OTHER units' pose sets; this unit's own earlier set is replaced.
    me=root.parent.name+'/'
    redrawn={d.get('atlas') for d in done if 'pose_packets' in str(d.get('source','')) and me not in str(d.get('source','')).replace(chr(92),'/')}
    for f in parts.glob('*.png'):
        h=int(f.stem);r=rows[h]
        idx=np.frombuffer(zlib.decompress(base64.b64decode(r['index_pixels'])),dtype='uint8').reshape(r['h'],r['w'])
        want=np.kron(idx>0,np.ones((S,S),bool))
        art=np.asarray(Image.open(f).convert('RGBA'))
        if not (art[:,:,3]>127).any():continue
        filled=grow_fill(art,want);filled[~want,3]=0
        it=dict(row=r,w=r['w'],h=r['h'],idx=idx,art=Image.fromarray(filled),drawn=float((art[:,:,3]>127)[want].mean()))
        b=active.get(h)
        if b and lib[b-1].get('atlas_id') in redrawn:skipped.append(h);continue   # already redrawn by another unit's set: keep that one
        if b:it['row']=dict(r,binding_id=b);replace.append(it)
        else:new.append(it)
    # Replacements whose library sources overlap in the same image (same palette)
    # must show identical pixels there. The better-drawn part wins; the other
    # takes those pixels (same set of drawings, same palette - not a recolour).
    replace.sort(key=lambda it:-it['drawn']);unified=0
    for i,it in enumerate(replace):
        b=lib[it['row']['binding_id']-1];arr=np.asarray(it['art']).copy()
        for prev in replace[:i]:
            pb=lib[prev['row']['binding_id']-1]
            if pb.get('resource') is None or pb.get('resource')!=b.get('resource') or prev['row']['palette_15bit']!=it['row']['palette_15bit']:continue
            if None in (b.get('source_x'),b.get('source_y'),pb.get('source_x'),pb.get('source_y')):continue
            left,top=max(b['source_x'],pb['source_x']),max(b['source_y'],pb['source_y'])
            right,bottom=min(b['source_x']+b['w'],pb['source_x']+pb['w']),min(b['source_y']+b['h'],pb['source_y']+pb['h'])
            if right<=left or bottom<=top:continue
            src=np.asarray(prev['art'])
            sx,sy=(left-pb['source_x'])*S,(top-pb['source_y'])*S;dx,dy=(left-b['source_x'])*S,(top-b['source_y'])*S;w,h=(right-left)*S,(bottom-top)*S
            arr[dy:dy+h,dx:dx+w]=src[sy:sy+h,sx:sx+w];unified+=1
        it['art']=Image.fromarray(arr)
    print('shared source regions unified',unified)
    out=root/'install';out.mkdir(parents=True,exist_ok=True);summary={}
    if replace:
        placed,H=pack(replace)
        def rrow(it,box):
            r=it['row'];return dict(atlas_box=box,replace_binding=r['binding_id'],source_contract=dict(hash=r['hash'],index_hash=r['index_hash'],
                index_pixels=r['index_pixels'],palette_15bit=r['palette_15bit'],original_palette_rgb=r['original_palette_rgb'],w=r['w'],h=r['h']))
        def rentry(rows_):
            ids=[x['replace_binding'] for x in rows_]
            return dict(bindings=ids,nested=True,prior_binding_spec_sha256={str(i):sorted(spec_hash(lib[i-1]))[0] for i in ids},
                note=f'whole-pose redraw split by Claude ({root.relative_to(ROOT).as_posix()}): replacement of existing RGB-keyed HD')
        summary['replace']=write_packet(out/f'{root.parent.name}_replace',placed,H,rrow,rentry)
    if new:
        placed,H=pack(new)
        def nrow(it,box):
            r=it['row'];pal=r['palette_15bit']
            return dict(hash=r['hash'],index_hash=r['index_hash'],atlas_box=box,index_pixels=r['index_pixels'],actual_palette_bgr555=pal,
                actual_palette_rgb=r['original_palette_rgb'],w=r['w'],h=r['h'],render_mode='static',effect_part=False,actual_observed=True,
                source_owner=f'unit pose set {root.relative_to(ROOT).as_posix()}',resource=None,source_x=None,source_y=None)
        def nentry(rows_):
            return dict(bindings=[],new_source_keys=[dict(hash=x['hash'],index_hash=x['index_hash']) for x in rows_],
                note=f'whole-pose redraw split by Claude ({root.relative_to(ROOT).as_posix()}): own RGB key, no recolour')
        summary['new']=write_packet(out/f'{root.parent.name}_new',placed,H,nrow,nentry)
    print('replace',len(replace),'new',len(new),'kept from other units',len(skipped),'mean drawn share',round(float(np.mean([i['drawn'] for i in replace+new])),3))
    (out/'SUMMARY.json').write_text(json.dumps({k:dict(source=v['source'],parts=len(v.get('bindings') or v.get('new_source_keys'))) for k,v in summary.items()},ensure_ascii=False,indent=1),encoding='utf-8')


if __name__=='__main__':main()
