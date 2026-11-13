"""Install the complete 17-part pose from observed RGB/index/palette contracts."""
import argparse,base64,hashlib,json,shutil,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

def observed_contract(row):
    """Accept the rendered-cache producer schema without altering its pixels."""
    if 'atlas_box' in row:return row
    r=dict(row)
    r['atlas_box']=[r[k] for k in ('x','y','w','h')]
    r['slot']=r.get('slot',r.get('oam',0))
    r['actual_palette_bgr555']=r['palette_15bit']
    r['actual_palette_rgb']=r['original_palette_rgb']
    r['spec']=dict(resource=r.get('resource'),source_x=r.get('source_x',r['x']),source_y=r.get('source_y',r['y']))
    return r

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true')
    parser.add_argument('--source-dir',type=Path,default=ROOT/'test_current/parts/borrowed_shape_rework')
    parser.add_argument('--contract',default='great_complete_contract.json');parser.add_argument('--drawing',default='great_candidate_atlas.png')
    parser.add_argument('--native',default='great_native_atlas.png');parser.add_argument('--generated',default='great_parts_generated.png')
    parser.add_argument('--atlas-id',default='great_mazinger_observed_pose');parser.add_argument('--graphics-dir',default='rework_great_mazinger')
    parser.add_argument('--effect',action='store_true',help='mark an explicitly reviewed visual-effect atlas for the core unit guard')
    parser.add_argument('--static-palette',action='store_true',help='exact-RGB artwork only; never recolour this observed variant')
    parser.add_argument('--defer-shape-review',action='store_true',help='record silhouette warnings for the independent reviewer instead of blocking draft installation')
    args=parser.parse_args();source=args.source_dir
    contract=[observed_contract(r) for r in json.loads((source/args.contract).read_text())]
    art=Image.open(source/args.drawing).convert('RGBA');native=Image.open(source/args.native).convert('RGBA')
    assert art.size==(native.width*4,native.height*4),('HD/native canvas ratio must be 4x',art.size,native.size)
    path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text())
    prefix=hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True).encode()).hexdigest()
    name=args.atlas_id;rows=[]
    for r in contract:
        x,y,w,h=r['atlas_box'];a=np.frombuffer(zlib.decompress(base64.b64decode(r['index_pixels'])),dtype=np.uint8).reshape(h,w)
        ih=zlib.crc32(np.where(a,a.astype(np.uint16)|32768,0).astype('<u2').tobytes())^(w<<16)^h
        palette=np.asarray(r['actual_palette_bgr555'],dtype=np.uint16)
        rgb=zlib.crc32(np.where(a,palette[a]|32768,0).astype('<u2').tobytes())^(w<<16)^h
        assert (ih,rgb)==(r['index_hash'],r['hash'])
        reference=np.asarray(native.crop((x,y,x+w,y+h)))
        expected=a>0
        assert np.array_equal(reference[:,:,3]>0,expected),('native reference alpha differs from source contract',r['slot'])
        if expected.any():
            source_rgb=np.asarray(r['actual_palette_rgb'],dtype=int)[a]
            assert np.max(abs(reference[:,:,:3].astype(int)-source_rgb)[expected])<=1,('native reference palette differs from source contract',r['slot'])
        if expected.any():
            assert art.crop((x*4,y*4,(x+w)*4,(y+h)*4)).getchannel('A').getextrema()[1]>=16,('empty or near-transparent artwork',r['slot'])
        got=np.asarray(art.crop((x*4,y*4,(x+w)*4,(y+h)*4)).getchannel('A').resize((w,h),Image.Resampling.BOX))>64
        iou=float((expected&got).sum()/max(1,(expected|got).sum()))
        if not args.defer_shape_review:assert iou>=.70,(r['slot'],iou)
        existing=next((j for j,b in enumerate(meta['bindings']) if b['hash']==rgb and b.get('rgb_enabled',True) and not b.get('disabled')),None)
        # Existing indexed contracts retain their fallback art, so unrelated
        # palette variants do not silently switch to this exact-RGB painting.
        if existing is not None:
            assert existing>=5263
            old=meta['bindings'][existing]
            if old.get('indexed_safe',True) and old.get('dynamic_palette'):
                proxy=dict(old,rgb_enabled=False,indexed_fallback_for=existing+1)
                meta['bindings'].append(proxy)
        old=r['spec']
        spec=dict(hash=rgb,index_hash=ih,rgb_enabled=True,indexed_safe=False,dynamic_palette=not args.static_palette,
                  original_palette_rgb=r['actual_palette_rgb'],index_pixels=r['index_pixels'],x=x,y=y,w=w,h=h,atlas_id=name,
                  resource=old.get('resource'),source_x=old.get('source_x',old.get('x',x)),source_y=old.get('source_y',old.get('y',y)),
                  registered_attack_bank=True,preserve_canonical_paint=True,reviewed_observed_pose=False,
                  actual_observed=bool(r.get('actual_observed',True)),
                  independent_visual_verification=False,review_status='pending_claude')
        if args.effect:spec['effect_part']=True
        if existing is None:meta['bindings'].append(spec);binding=len(meta['bindings'])
        else:meta['bindings'][existing]=spec;binding=existing+1
        rows.append(dict(slot=r['slot'],binding=binding,hash=rgb,alpha_iou=iou,new_rgb=existing is None,shape_review_required=iou<.70))
    assert len(rows)==len(contract) and rows
    assert prefix==hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True).encode()).hexdigest()
    if args.apply:
        folder=ROOT/'graphics'/args.graphics_dir;folder.mkdir(exist_ok=True)
        for old,new in ((args.drawing,'pose_hd.png'),(args.native,'pose_native.png'),(args.generated,'pose_generated.png')):shutil.copy2(source/old,folder/new)
        shutil.copy2(source/args.contract,folder/'pose_contract.json')
        meta['atlases'][name]=dict(image=f'{args.graphics_dir}/pose_hd.png',reference=f'{args.graphics_dir}/pose_native.png',native_size=list(native.size),lazy=True)
        temp=path.with_suffix('.tmp.json');temp.write_text(json.dumps(meta,indent=2),encoding='utf-8');temp.replace(path)
    (source/'install_report.json').write_text(json.dumps(dict(applied=args.apply,parts=rows,original_prefix_preserved=True,shape_review_deferred=args.defer_shape_review,reference_iou_threshold=.70,shape_review_slots=[r['slot'] for r in rows if r['shape_review_required']],independent_visual_verification=False),indent=2));print(json.dumps(rows))
    if args.apply:shutil.copy2(source/'install_report.json',folder/'installation_report.json')

if __name__=='__main__':main()
