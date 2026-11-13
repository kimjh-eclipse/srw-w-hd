"""Install source-contracted 4x artwork into exact RGB bindings."""
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
    r['slot']=r.get('slot',r.get('oam'))
    r['actual_palette_bgr555']=r['palette_15bit']
    r['actual_palette_rgb']=r['original_palette_rgb']
    resource=r.get('resource')
    if resource is None:resource=r.get('source_image')
    r['spec']=dict(resource=resource,source_x=r.get('source_x',r['x']),source_y=r.get('source_y',r['y']))
    return r


def validate_source_containment(contract, art, excluded_hashes):
    """Confirmed overlapping source pixels must share generated artwork."""
    checks=[]
    for i,a in enumerate(contract):
        sa=a.get('spec',{});sx,sy=sa.get('source_x'),sa.get('source_y')
        if a['hash'] in excluded_hashes or sa.get('resource') is None or sx is None or sy is None:continue
        x,y,w,h=a['atlas_box']
        for b in contract[i+1:]:
            sb=b.get('spec',{});lx,ly=sb.get('source_x'),sb.get('source_y');ax,ay,aw,ah=b['atlas_box']
            if b['hash'] in excluded_hashes or sb.get('resource')!=sa['resource'] or lx is None or ly is None:continue
            if a['actual_palette_bgr555']!=b['actual_palette_bgr555']:continue
            left,top=max(sx,lx),max(sy,ly);right,bottom=min(sx+w,lx+aw),min(sy+h,ly+ah)
            if right<=left or bottom<=top:continue
            dx,dy=left-sx,top-sy;bx,by=left-lx,top-ly;ow,oh=right-left,bottom-top
            ai=np.frombuffer(zlib.decompress(base64.b64decode(a['index_pixels'])),dtype=np.uint8).reshape(h,w)
            bi=np.frombuffer(zlib.decompress(base64.b64decode(b['index_pixels'])),dtype=np.uint8).reshape(ah,aw)
            assert np.array_equal(ai[dy:dy+oh,dx:dx+ow],bi[by:by+oh,bx:bx+ow]),('source overlap raw mismatch',a['slot'],b['slot'])
            own=np.asarray(art.crop(((x+dx)*4,(y+dy)*4,(x+dx+ow)*4,(y+dy+oh)*4)))
            shared=np.asarray(art.crop(((ax+bx)*4,(ay+by)*4,(ax+bx+ow)*4,(ay+by+oh)*4)))
            equal=bool(np.array_equal(own,shared));contained=(ow*oh==min(w*h,aw*ah))
            checks.append(dict(slot_a=a['slot'],slot_b=b['slot'],source_overlap=[left,top,ow,oh],relation='contained' if contained else 'partial_overlap',generated_rgba_equal=equal))
            assert equal,('same confirmed source region has different generated artwork',a['slot'],b['slot'])
    return checks


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true')
    parser.add_argument('--source-dir',type=Path,default=ROOT/'test_current/parts/borrowed_shape_rework')
    parser.add_argument('--contract',default='great_complete_contract.json');parser.add_argument('--drawing',default='great_candidate_atlas.png')
    parser.add_argument('--native',default='great_native_atlas.png');parser.add_argument('--generated',default='great_parts_generated.png')
    parser.add_argument('--atlas-id',default='great_mazinger_observed_pose');parser.add_argument('--graphics-dir',default='rework_great_mazinger')
    parser.add_argument('--effect',action='store_true',help='mark an explicitly reviewed visual-effect atlas for the core unit guard')
    parser.add_argument('--static-palette',action='store_true',help='exact-RGB artwork only; never recolour this observed variant')
    parser.add_argument('--defer-shape-review',action='store_true',help='record silhouette warnings for the independent reviewer instead of blocking draft installation')
    parser.add_argument('--new-only',action='store_true',help='preserve already-connected exact RGB artwork while filling missing contracts')
    args=parser.parse_args();source=args.source_dir
    for required in (args.contract,args.drawing,args.native,args.generated):
        if not (source/required).is_file():raise FileNotFoundError(f'production packet file missing: {source/required}')
    contract=[observed_contract(r) for r in json.loads((source/args.contract).read_text(encoding='utf-8'))]
    art=Image.open(source/args.drawing).convert('RGBA');native=Image.open(source/args.native).convert('RGBA')
    assert art.size==(native.width*4,native.height*4),('HD/native canvas ratio must be 4x',art.size,native.size)
    path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text(encoding='utf-8'))
    prefix=hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True).encode()).hexdigest()
    rgb_bindings={}
    for i,b in enumerate(meta['bindings']):
        if b.get('rgb_enabled',True) and not b.get('disabled'):rgb_bindings.setdefault(b['hash'],i)
    overlap_checks=validate_source_containment(contract,art,set(rgb_bindings) if args.new_only else set())
    name=args.atlas_id;rows=[]
    for r in contract:
        x,y,w,h=r['atlas_box'];a=np.frombuffer(zlib.decompress(base64.b64decode(r['index_pixels'])),dtype=np.uint8).reshape(h,w)
        ih=zlib.crc32(np.where(a,a.astype(np.uint16)|32768,0).astype('<u2').tobytes())^(w<<16)^h
        palette=np.asarray(r['actual_palette_bgr555'],dtype=np.uint16)
        rgb=zlib.crc32(np.where(a,palette[a]|32768,0).astype('<u2').tobytes())^(w<<16)^h
        assert (ih,rgb)==(r['index_hash'],r['hash'])
        reference=np.asarray(native.crop((x,y,x+w,y+h)))
        expected=a>0
        assert expected.any(),('empty original has no artwork to replace',r['slot'])
        assert np.array_equal(reference[:,:,3]>0,expected),('native reference alpha differs from source contract',r['slot'])
        if expected.any():
            source_rgb=np.asarray(r['actual_palette_rgb'],dtype=int)[a]
            assert np.max(abs(reference[:,:,:3].astype(int)-source_rgb)[expected])<=1,('native reference palette differs from source contract',r['slot'])
        if expected.any():
            assert art.crop((x*4,y*4,(x+w)*4,(y+h)*4)).getchannel('A').getextrema()[1]>=16,('empty or near-transparent artwork',r['slot'])
        got=np.asarray(art.crop((x*4,y*4,(x+w)*4,(y+h)*4)).getchannel('A').resize((w,h),Image.Resampling.BOX))>64
        iou=float((expected&got).sum()/max(1,(expected|got).sum()))
        if not args.defer_shape_review:assert iou>=.70,(r['slot'],iou)
        existing=rgb_bindings.get(rgb)
        if args.new_only and existing is not None:
            rows.append(dict(slot=r['slot'],binding=existing+1,hash=rgb,alpha_iou=iou,new_rgb=False,skipped_existing=True,shape_review_required=False))
            continue
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
                  registered_attack_bank=True,preserve_canonical_paint=True,reviewed_observed_pose=False,source_engine=r.get('engine'),
                  actual_observed=bool(r.get('actual_observed',r.get('observed_shape',True))),
                  independent_visual_verification=False,review_status='pending_claude')
        for field in ('source_candidate_matches','source_owner','source_owner_confirmed','source_owner_note','source_native_visible_area','source_native_visible','source_visibility_note','source_rendered_cache_observed'):
            if field in r:spec[field]=r[field]
        if args.effect:spec['effect_part']=True
        if existing is None:
            meta['bindings'].append(spec);binding=len(meta['bindings']);rgb_bindings[rgb]=binding-1
        else:meta['bindings'][existing]=spec;binding=existing+1
        rows.append(dict(slot=r['slot'],binding=binding,hash=rgb,alpha_iou=iou,new_rgb=existing is None,shape_review_required=iou<.70))
    assert len(rows)==len(contract) and rows
    assert prefix==hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True).encode()).hexdigest()
    if args.apply:
        folder=ROOT/'graphics'/args.graphics_dir;folder.mkdir(exist_ok=True)
        for old,new in ((args.drawing,'pose_hd.png'),(args.native,'pose_native.png'),(args.generated,'pose_generated.png')):shutil.copy2(source/old,folder/new)
        shutil.copy2(source/args.contract,folder/'pose_contract.json')
        meta['atlases'][name]=dict(image=f'{args.graphics_dir}/pose_hd.png',reference=f'{args.graphics_dir}/pose_native.png',native_size=list(native.size),lazy=True)
        temp=path.with_suffix('.tmp.json');temp.write_text(json.dumps(meta,indent=2),encoding='utf-8')
        # Windows readers can briefly hold a handle without FILE_SHARE_DELETE.
        import time
        for attempt in range(20):
            try:
                temp.replace(path)
                break
            except PermissionError:
                if attempt == 19:raise
                time.sleep(.15)
    (source/'install_report.json').write_text(json.dumps(dict(applied=args.apply,parts=rows,source_containment_checks=overlap_checks,source_containment_scope='newly-written contracts with confirmed resource, full actual palette and raw overlap; not global visual QA',original_prefix_preserved=True,shape_review_deferred=args.defer_shape_review,reference_iou_threshold=.70,shape_review_slots=[r['slot'] for r in rows if r['shape_review_required']],independent_visual_verification=False),indent=2));print(json.dumps(rows))
    if args.apply:shutil.copy2(source/'install_report.json',folder/'installation_report.json')

if __name__=='__main__':main()
