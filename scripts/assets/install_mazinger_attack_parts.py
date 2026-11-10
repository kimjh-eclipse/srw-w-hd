"""Connect reviewed FDS atlases by exact ROM indices, without moving OAM pivots."""
import argparse,base64,collections,hashlib,json,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g
from painted_edges import clean_alpha
from scripts.assets.install_shared_weapon_frames import components


def key(a):
    h,w=a.shape
    encoded=np.where(a,a.astype('uint16')|0x8000,0).astype('<u2')
    return zlib.crc32(encoded.tobytes())^(w<<16)^h


def joined_wing(folder):
    """Use the painted ink outline, not the old DS staircase, to remove bloom."""
    image=Image.open(folder/'getter_joined_wing_generated.png').convert('RGBA');pixels=np.array(image)
    ink=(pixels[:,:,:3].max(2)<38)&(pixels[:,:,3]>128)
    barrier=Image.fromarray(ink.astype('uint8')*255).copy();ImageDraw.floodfill(barrier,(0,0),128)
    mask=Image.fromarray((np.asarray(barrier)!=128).astype('uint8')*255).filter(ImageFilter.GaussianBlur(.4))
    pixels[:,:,3]=np.minimum(np.asarray(mask),pixels[:,:,3]);pixels[pixels[:,:,3]==0]=0
    result=Image.fromarray(pixels)
    target=np.asarray(Image.open(folder/'getter_joined_wing_reference.png').getchannel('A').resize((96,64),Image.Resampling.BOX))>64
    actual=np.asarray(result.getchannel('A').resize((96,64),Image.Resampling.BOX))>64
    score=float((actual&target).sum()/max(1,(actual|target).sum()))
    assert score>=.82,('Joined wing differs from original attachment geometry',score)
    return result.resize((288,192),Image.Resampling.LANCZOS),score


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    folder=ROOT/'graphics/mazinger_attack_parts';plan=json.loads((folder/'plan.json').read_text())
    path=ROOT/'graphics/kazuma_parts_library.json';library=json.loads(path.read_text());protected=json.dumps(library['bindings'][:5263],sort_keys=True)
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    report=dict(applied=args.apply,accepted=[],rejected=[],unmatched=[])
    for item in plan['items']:
        r=item['resource'];source=folder/item['output']
        if not source.exists():report['rejected'].append(dict(resource=r,reason='missing generated art'));continue
        a=g.pixels(g.decompress(rom[g.BASE+offsets[r]:g.BASE+offsets[r+1]]));h,w=a.shape
        canvas=clean_alpha(Image.open(source).convert('RGBA')).resize((768,480),Image.Resampling.LANCZOS)
        art=canvas.crop((0,0,w*3,h*3));wing_score=None
        if r==14886 and (folder/'getter_joined_wing_generated.png').exists():
            wing,wing_score=joined_wing(folder)
            # Native OAM: root at (129,45), tip at (193,44). Both
            # rectangles come from ONE painting, then mirror together.
            art.paste(wing.crop((0,3,192,99)),(192*3,0))
            art.paste(wing.crop((192,0,288,24)),(0,48*3))
        reference=Image.open(folder/f'bank_{r}_native.png').convert('RGBA')
        expected=a!=0;mask=np.asarray(art.getchannel('A').resize((w,h),Image.Resampling.BOX))>64
        iou=float((mask&expected).sum()/max(1,(mask|expected).sum()))
        adjustments=[]
        if iou<.82:
            painted=components(mask);native=components(expected)
            # Only correct a measured one-pixel atlas-layout drift. Rounded
            # painted surfaces keep their own alpha; no native mask is baked.
            if len(painted)==len(native) and all(max(abs(int(s)-int(t)) for s,t in zip(sb,tb))<=2 for sb,tb in zip(painted,native)):
                candidate=Image.new('RGBA',art.size);sx=art.width/w;sy=art.height/h
                for sb,tb in zip(painted,native):
                    box=tuple(round(v*(sx if i%2==0 else sy)) for i,v in enumerate(sb))
                    dest=tuple(round(v*(sx if i%2==0 else sy)) for i,v in enumerate(tb))
                    piece=art.crop(box).resize((dest[2]-dest[0],dest[3]-dest[1]),Image.Resampling.LANCZOS)
                    candidate.paste(piece,dest[:2]);adjustments.append(dict(source=list(map(int,sb)),target=list(map(int,tb))))
                q=np.asarray(candidate.getchannel('A').resize((w,h),Image.Resampling.BOX))>64
                value=float((q&expected).sum()/max(1,(q|expected).sum()))
                if value>iou:art=candidate;mask=q;iou=value
                else:adjustments=[]
        envelope=np.asarray(Image.fromarray(expected.astype('uint8')*255).filter(ImageFilter.MaxFilter(3)))>0
        precision=float((mask&envelope).sum()/max(1,mask.sum()))
        painted_envelope=np.asarray(Image.fromarray(mask.astype('uint8')*255).filter(ImageFilter.MaxFilter(3)))>0
        recall=float((expected&painted_envelope).sum()/max(1,expected.sum()))
        # The requested rounded 14510 armor differs from the DS staircase,
        # while remaining within a single source pixel of the original pose.
        rounded_tolerance=r==14510 and iou>=.78 and recall>=.99 and precision>=.97
        if (iou<.80 and not rounded_tolerance) or precision<.97:
            report['rejected'].append(dict(resource=r,reason='atlas geometry differs',alpha_iou=iou,one_pixel_precision=precision));continue
        selected=[(i,b) for i,b in enumerate(library['bindings'],1) if i>5263 and b.get('resource')==r]
        dimensions={(b['w'],b['h']) for _,b in selected};lookup={};padded=np.pad(a,((0,64),(0,64)))
        for bw,bh in dimensions:
            for y in range(0,h,8):
                for x in range(0,w,8):
                    part=padded[y:y+bh,x:x+bw]
                    if part.shape==(bh,bw) and part.any():lookup.setdefault((bw,bh,key(part)),[]).append((x,y))
        updates=[]
        for bid,b in selected:
            matches=lookup.get((b['w'],b['h'],b['index_hash']),[])
            if not matches:report['unmatched'].append(dict(resource=r,binding=bid));continue
            # Repeated identical tiles are interchangeable only if their
            # entire native rectangle matches, never by a partial tile guess.
            preferred=(b.get('source_x'),b.get('source_y'));x,y=preferred if preferred in matches else matches[0]
            bh,bw=b['h'],b['w'];indices=padded[y:y+bh,x:x+bw]
            palette_votes=collections.Counter()
            for ty in range(y,min(y+bh,h),8):
                for tx in range(x,min(x+bw,w),8):
                    pal=item['cell_palettes'].get(f'{tx},{ty}')
                    if pal:palette_votes[tuple(pal)]+=int(np.count_nonzero(a[ty:ty+8,tx:tx+8]))
            pal=np.asarray(palette_votes.most_common(1)[0][0] if palette_votes else item['palette_native'],dtype='uint32')
            rgb=np.stack([(pal&31)*255//31,((pal>>5)&31)*255//31,((pal>>10)&31)*255//31],-1).tolist()
            colors=np.where(indices,pal[indices]|0x8000,0).astype('<u2')
            updates.append((b,dict(atlas_id=f'mazinger_bank_{r}',x=x,y=y,source_x=x,source_y=y,
                hash=zlib.crc32(colors.tobytes())^(bw<<16)^bh,rgb_enabled=True,indexed_safe=True,
                dynamic_palette=True,original_palette_rgb=rgb,palette_source_rgb=rgb,
                index_pixels=base64.b64encode(zlib.compress(indices.tobytes())).decode('ascii'),
                registered_attack_bank=True,preserve_canonical_paint=True)))
        record=dict(resource=r,alpha_iou=iou,one_pixel_precision=precision,bindings=len(updates),
            one_pixel_recall=recall,rounded_tolerance=rounded_tolerance,joined_wing_iou=wing_score,component_adjustments=adjustments,
            generated_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),actual_game_verified=False)
        report['accepted'].append(record)
        if not args.apply:continue
        pixels=np.array(art);pixels[pixels[:,:,3]==0]=0
        Image.fromarray(pixels).save(folder/f'bank_{r}_hd.png',optimize=True)
        library['atlases'][f'mazinger_bank_{r}']=dict(image=f'mazinger_attack_parts/bank_{r}_hd.png',
            reference=f'mazinger_attack_parts/bank_{r}_native.png',native_size=[w,h],lazy=True)
        for b,changes in updates:b.update(changes)
    assert protected==json.dumps(library['bindings'][:5263],sort_keys=True)
    if args.apply:
        temporary=path.with_suffix('.tmp.json');temporary.write_text(json.dumps(library,indent=2));temporary.replace(path)
    (folder/('registration.json' if args.apply else 'registration_review.json')).write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
