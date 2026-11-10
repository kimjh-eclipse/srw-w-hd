"""Register reviewed shared punch frames without modifying the source ROM."""
import argparse,base64,json,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g

def components(mask):
    from collections import deque
    todo=set(map(tuple,np.argwhere(mask)));boxes=[]
    while todo:
        start=todo.pop();queue=deque([start]);pixels=[start]
        while queue:
            y,x=queue.popleft()
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    point=(y+dy,x+dx)
                    if point in todo:todo.remove(point);queue.append(point);pixels.append(point)
        if len(pixels)>=8:
            ys,xs=zip(*pixels);boxes.append((min(xs),min(ys),max(xs)+1,max(ys)+1))
    return sorted(boxes)

def main():
    p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');args=p.parse_args()
    folder=ROOT/'graphics/shared_weapon_frames';plan=json.loads((folder/'plan.json').read_text())
    path=ROOT/'graphics/kazuma_parts_library.json';library=json.loads(path.read_text())
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom);checked=[];rejected=[]
    for sheet in plan['sheets']:
        source=Image.open(folder/sheet['output']).convert('RGBA')
        for item in sheet['items']:
            resource=item['resource'];slot=item['slot'];a=g.pixels(g.decompress(rom[g.BASE+offsets[resource]:g.BASE+offsets[resource+1]]));h,w=a.shape
            single=folder/f'frame_{resource}_generated.png'
            # These two IMG records differ only in palette indices. Their
            # alpha silhouettes are byte-for-byte equal (checked below).
            if resource==20730:
                other=g.pixels(g.decompress(rom[g.BASE+offsets[20718]:g.BASE+offsets[20719]]))
                assert np.array_equal(a!=0,other!=0)
                single=folder/'frame_20718_generated.png'
            cell=Image.open(single).convert('RGBA') if single.exists() else source.crop((round(slot%2*source.width/2),round(slot//2*source.height/5),round((slot%2+1)*source.width/2),round((slot//2+1)*source.height/5)))
            native=Image.new('L',(80,80));native.paste(Image.fromarray((a!=0).astype('uint8')*255),(0,0))
            ys,xs=np.where(np.asarray(cell)[:,:,3]>64);ry,rx=np.where(np.asarray(native)>0)
            if not len(rx):
                checked.append(dict(resource=resource,empty_native_frame=True));continue
            if not len(xs):
                rejected.append(dict(resource=resource,reason='missing generated cell'));continue
            box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1));target=(int(rx.min()),int(ry.min()),int(rx.max()+1),int(ry.max()+1))
            scale=12;dest=tuple(v*scale for v in target);art=Image.new('RGBA',(960,960));art.paste(cell.crop(box).resize((dest[2]-dest[0],dest[3]-dest[1]),Image.Resampling.LANCZOS),dest[:2])
            alpha=np.asarray(art.getchannel('A').resize((80,80),Image.Resampling.BOX))>64;expected=np.asarray(native)>0
            iou=float((alpha&expected).sum()/max(1,(alpha|expected).sum()))
            if iou<.82 and resource in (20718,20730):
                small=np.asarray(cell.getchannel('A').resize((80,80),Image.Resampling.BOX))>64
                src_boxes=components(small);dst_boxes=components(expected)
                if len(src_boxes)==len(dst_boxes)==3:
                    aligned=Image.new('RGBA',(960,960))
                    for sb,db in zip(src_boxes,dst_boxes):
                        source_box=tuple(round(v*cell.width/80) for v in sb);target_box=tuple(v*12 for v in db)
                        piece=cell.crop(source_box).resize((target_box[2]-target_box[0],target_box[3]-target_box[1]),Image.Resampling.LANCZOS)
                        aligned.paste(piece,target_box[:2])
                    mask=np.asarray(aligned.getchannel('A').resize((80,80),Image.Resampling.BOX))>64
                    score=float((mask&expected).sum()/max(1,(mask|expected).sum()))
                    if score>iou:art=aligned;iou=score
                if iou<.82:
                    for dw in (-12,0,12):
                        for dh in (-12,0,12):
                            tile=cell.crop(box).resize((dest[2]-dest[0]+dw,dest[3]-dest[1]+dh),Image.Resampling.LANCZOS)
                            for dy in (-6,0,6):
                                for dx in (-6,0,6):
                                    aligned=Image.new('RGBA',(960,960));aligned.paste(tile,(dest[0]-dw//2+dx,dest[1]-dh//2+dy))
                                    mask=np.asarray(aligned.getchannel('A').resize((80,80),Image.Resampling.BOX))>64
                                    score=float((mask&expected).sum()/max(1,(mask|expected).sum()))
                                    if score>iou:art=aligned;iou=score
            record=dict(resource=resource,canvas=sheet['name'],alpha_iou=iou,gameplay_verified=False)
            if iou<.82:rejected.append(record);continue
            checked.append(record)
            if not args.apply:continue
            art=art.crop((0,0,w*scale,h*scale));rgba=np.array(art);rgba[rgba[:,:,3]==0]=0;art=Image.fromarray(rgba)
            image=f'shared_weapon_frames/frame_{resource}_hd.png';reference=f'shared_weapon_frames/frame_{resource}_native.png';name=f'shared_weapon_frame_{resource}'
            art.save(ROOT/'graphics'/image,optimize=True);rgb=np.asarray(item['palette_rgb'],dtype='uint8');rgba=np.dstack([rgb[a],(a!=0).astype('uint8')*255]);rgba[a==0]=0;Image.fromarray(rgba).save(ROOT/'graphics'/reference)
            library['atlases'][name]=dict(image=image,reference=reference,native_size=[w,h],lazy=True)
            if not any(b.get('shared_weapon_frame') and b.get('resource')==resource for b in library['bindings']):
                index=np.where(a,a.astype('uint16')|0x8000,0).astype('<u2');q=np.rint(rgb.astype('float64')*31/255).astype('uint32');pal=q[:,0]|q[:,1]<<5|q[:,2]<<10;colors=np.where(a,pal[a]|0x8000,0).astype('<u2')
                library['bindings'].append(dict(hash=zlib.crc32(colors.tobytes())^(w<<16)^h,rgb_enabled=True,index_hash=zlib.crc32(index.tobytes())^(w<<16)^h,indexed_safe=True,dynamic_palette=True,original_palette_rgb=rgb.tolist(),index_pixels=base64.b64encode(zlib.compress(a.tobytes())).decode('ascii'),x=0,y=0,w=w,h=h,atlas_id=name,resource=resource,source_x=0,source_y=0,shared_weapon_frame=True,auto_shared_attack=True))
    if args.apply:
        temp=path.with_suffix('.tmp.json');temp.write_text(json.dumps(library,indent=2));temp.replace(path)
    report=dict(applied=args.apply,checked=checked,rejected=rejected);(folder/'registration.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
