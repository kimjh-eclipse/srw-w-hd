"""Register reviewed omitted attack fragments with bounded size and alpha checks."""
import argparse,base64,json,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g
from painted_edges import clean_alpha
from scripts.assets.install_shared_weapon_frames import components

def main():
    p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');args=p.parse_args()
    folder=ROOT/'graphics/named_attack_frames';plan=json.loads((folder/'plan.json').read_text())
    path=ROOT/'graphics/kazuma_parts_library.json';library=json.loads(path.read_text());accepted=[];rejected=[]
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    for sheet in plan['sheets']:
        generated=folder/sheet['output']
        if not generated.exists():continue
        source=Image.open(generated).convert('RGBA')
        for item in sheet['items']:
            resource=item['resource'];a=g.pixels(g.decompress(rom[g.BASE+offsets[resource]:g.BASE+offsets[resource+1]]));h,w=a.shape
            # Rows shorter than their 80px cell must not pick up a few pixels
            # of the next generated row at the rounded cell boundary.
            top=round(item['slot']*source.height/4)
            bottom=min(round((item['slot']+1)*source.height/4),top+round((h+2)*source.height/320))
            cell=source.crop((0,top,source.width,bottom))
            single=folder/f'frame_{resource}_generated.png'
            if resource==8264:
                alternate=g.pixels(g.decompress(rom[g.BASE+offsets[8265]:g.BASE+offsets[8266]]))
                assert np.array_equal(a!=0,alternate!=0)
                single=folder/'frame_8265_generated.png'
            final=folder/f'frame_{resource}_final_generated.png'
            if final.exists():single=final
            if single.exists():cell=Image.open(single).convert('RGBA')
            cell=clean_alpha(cell)
            expected=a!=0;ys,xs=np.where(expected);gy,gx=np.where(np.asarray(cell)[:,:,3]>64)
            if not len(gx):rejected.append(dict(resource=resource,reason='empty generated cell'));continue
            box=(int(gx.min()),int(gy.min()),int(gx.max()+1),int(gy.max()+1))
            target=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1))
            scale=min(8,960/max(w,h));size=(round(w*scale),round(h*scale));dest=tuple(round(v*scale) for v in target)
            art=Image.new('RGBA',size);art.paste(cell.crop(box).resize((dest[2]-dest[0],dest[3]-dest[1]),Image.Resampling.LANCZOS),dest[:2])
            mask=np.asarray(art.getchannel('A').resize((w,h),Image.Resampling.BOX))>64
            score=float((mask&expected).sum()/max(1,(mask|expected).sum()))
            if score<.82 and resource not in (8264,8265):
                # Bounded registration corrects subpixel atlas placement;
                # it does not cut the artwork to the native pixel mask.
                fragment=cell.crop(box);best=None
                for dw in (-2,-1,0,1,2):
                    for dh in (-2,-1,0,1,2):
                        tw=target[2]-target[0]+dw;th=target[3]-target[1]+dh
                        if min(tw,th)<=0:continue
                        alpha=fragment.getchannel('A').resize((tw*4,th*4),Image.Resampling.LANCZOS)
                        for dx in (-1,0,1):
                            for dy in (-1,0,1):
                                probe=Image.new('L',(w*4,h*4));probe.paste(alpha,((target[0]+dx)*4,(target[1]+dy)*4))
                                candidate=np.asarray(probe.resize((w,h),Image.Resampling.BOX))>64
                                value=float((candidate&expected).sum()/max(1,(candidate|expected).sum()))
                                if value>score and (best is None or value>best[0]):best=(value,tw,th,dx,dy)
                if best:
                    score,tw,th,dx,dy=best;art=Image.new('RGBA',size)
                    art.paste(fragment.resize((round(tw*scale),round(th*scale)),Image.Resampling.LANCZOS),(round((target[0]+dx)*scale),round((target[1]+dy)*scale)))
            if score<.82:
                source_mask=np.asarray(art.getchannel('A').resize((w,h),Image.Resampling.BOX))>64
                source_boxes=components(source_mask);target_boxes=components(expected)
                if len(source_boxes)==len(target_boxes) and len(source_boxes)>1:
                    aligned=Image.new('RGBA',size)
                    for sb,tb in zip(source_boxes,target_boxes):
                        source_box=tuple(round(v*scale) for v in sb)
                        target_box=tuple(round(v*scale) for v in tb)
                        piece=art.crop(source_box).resize((target_box[2]-target_box[0],target_box[3]-target_box[1]),Image.Resampling.LANCZOS)
                        aligned.paste(piece,target_box[:2])
                    alpha=np.asarray(aligned.getchannel('A').resize((w,h),Image.Resampling.BOX))>64
                    aligned_score=float((alpha&expected).sum()/max(1,(alpha|expected).sum()))
                    if aligned_score>score:art=aligned;score=aligned_score
            # At an 8/16px native edge, smooth contours and opaque dark
            # recesses differ by whole DS pixels. A symmetric one-pixel
            # tolerance checks location without imposing the DS alpha mask.
            mask=np.asarray(art.getchannel('A').resize((w,h),Image.Resampling.BOX))>64
            score=float((mask&expected).sum()/max(1,(mask|expected).sum()))
            expanded=np.asarray(Image.fromarray(mask.astype('uint8')*255).filter(ImageFilter.MaxFilter(3)))>0
            reference_expanded=np.asarray(Image.fromarray(expected.astype('uint8')*255).filter(ImageFilter.MaxFilter(3)))>0
            recall=float((expected&expanded).sum()/max(1,expected.sum()))
            precision=float((mask&reference_expanded).sum()/max(1,mask.sum()))
            low_alpha=np.asarray(art.getchannel('A').resize((w,h),Image.Resampling.BOX))>8
            spill=float((low_alpha&~reference_expanded).sum()/max(1,low_alpha.sum()))
            tolerance_accepted=h<=32 and score>=.65 and min(recall,precision)>=.97
            row=dict(resource=resource,alpha_iou=score,one_pixel_recall=recall,one_pixel_precision=precision,low_alpha_spill=spill,alias_tolerance_used=score<.82 and tolerance_accepted,max_dimension=max(size),actual_game_verified=False)
            if spill>.04 or (score<.82 and not tolerance_accepted):rejected.append(row);continue
            accepted.append(row)
            if not args.apply:continue
            rgba=np.array(art);rgba[rgba[:,:,3]==0]=0;art=Image.fromarray(rgba)
            image=f'named_attack_frames/frame_{resource}_hd.png';reference=f'named_attack_frames/frame_{resource}_native.png';name=f'named_attack_{resource}'
            art.save(ROOT/'graphics'/image,optimize=True)
            library['atlases'][name]=dict(image=image,reference=reference,native_size=[w,h],lazy=True)
            if any(b.get('named_attack_frame') and b.get('resource')==resource for b in library['bindings']):continue
            rgb=np.asarray(item['palette_rgb'],dtype='uint8');q=np.rint(rgb.astype('float64')*31/255).astype('uint32');pal=q[:,0]|q[:,1]<<5|q[:,2]<<10
            index=np.where(a,a.astype('uint16')|0x8000,0).astype('<u2');colors=np.where(a,pal[a]|0x8000,0).astype('<u2')
            library['bindings'].append(dict(hash=zlib.crc32(colors.tobytes())^(w<<16)^h,rgb_enabled=True,index_hash=zlib.crc32(index.tobytes())^(w<<16)^h,indexed_safe=True,dynamic_palette=True,original_palette_rgb=rgb.tolist(),index_pixels=base64.b64encode(zlib.compress(a.tobytes())).decode('ascii'),x=0,y=0,w=w,h=h,atlas_id=name,resource=resource,source_x=0,source_y=0,named_attack_frame=True,auto_shared_attack=True))
    if args.apply:
        temp=path.with_suffix('.tmp.json');temp.write_text(json.dumps(library,indent=2));temp.replace(path)
    report=dict(scope=__doc__,applied=args.apply,accepted=accepted,rejected=rejected)
    (folder/('registration.json' if args.apply else 'registration_review.json')).write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
