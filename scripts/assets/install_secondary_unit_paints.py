"""Register distinct mini-unit paintings, preserving their smooth alpha contours."""
import argparse,base64,json,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g

def main():
    p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');args=p.parse_args()
    folder=ROOT/'graphics/secondary_units';plan=json.loads((folder/'paint_plan.json').read_text())
    path=ROOT/'graphics/kazuma_parts_library.json';library=json.loads(path.read_text())
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    checked=[];rejected=[]
    for pair in plan['pairs']:
        source=Image.open(folder/pair['output']).convert('RGBA')
        for slot,item in enumerate(pair['items']):
            paint=Image.open(folder/item['output_override']).convert('RGBA') if item.get('output_override') else source
            resource=item['resource'];a=g.pixels(g.decompress(rom[g.BASE+offsets[resource]:g.BASE+offsets[resource+1]]));h,w=a.shape
            crop=paint.crop((0,round(paint.height*slot/2),paint.width,round(paint.height*(slot+1)/2)))
            ys,xs=np.where(np.asarray(crop)[:,:,3]>64);ry,rx=np.where(a!=0)
            source_box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1))
            scale=960/max(w,h);dest=tuple(round(v*scale) for v in (rx.min(),ry.min(),rx.max()+1,ry.max()+1))
            art=Image.new('RGBA',(round(w*scale),round(h*scale)))
            art.paste(crop.crop(source_box).resize((dest[2]-dest[0],dest[3]-dest[1]),Image.Resampling.LANCZOS),dest[:2])
            alpha=np.asarray(art.getchannel('A').resize((w,h),Image.Resampling.BOX))>64;native=a!=0
            iou=float((alpha&native).sum()/max(1,(alpha|native).sum()))
            # Pixel centers in the source crop and the high-resolution canvas
            # can differ by half a native pixel. Register translation only;
            # never deform or replace the painted alpha contour.
            shift=(0,0)
            if iou<.82:
                original=art
                for dy in (-round(scale/2),0,round(scale/2)):
                    for dx in (-round(scale/2),0,round(scale/2)):
                        probe=Image.new('RGBA',original.size);probe.paste(original,(dx,dy))
                        mask=np.asarray(probe.getchannel('A').resize((w,h),Image.Resampling.BOX))>64
                        score=float((mask&native).sum()/max(1,(mask|native).sum()))
                        if score>iou:iou=score;art=probe;shift=(dx,dy)
            extent=(0,0)
            if iou<.82:
                # Fit edge sample centers within one native pixel per axis.
                # This is a uniform crop registration, not a pixel-alpha mask.
                for dw in (-round(scale),0,round(scale)):
                    for dh in (-round(scale),0,round(scale)):
                        size=(dest[2]-dest[0]+dw,dest[3]-dest[1]+dh)
                        tile=crop.crop(source_box).resize(size,Image.Resampling.LANCZOS)
                        probe=Image.new('RGBA',art.size);probe.paste(tile,(dest[0]-dw//2,dest[1]-dh//2))
                        mask=np.asarray(probe.getchannel('A').resize((w,h),Image.Resampling.BOX))>64
                        score=float((mask&native).sum()/max(1,(mask|native).sum()))
                        if score>iou:iou=score;art=probe;shift=(0,0);extent=(dw,dh)
            record=dict(resource=resource,name_ja=item['name_ja'],canvas=pair['name'],alpha_iou=iou,alignment=dict(source=source_box,destination=dest),gameplay_verified=False)
            record['alignment']['translation']=shift
            record['alignment']['extent_correction']=extent
            if iou<.82:rejected.append(record);continue
            checked.append(record)
            if not args.apply:continue
            image=f'secondary_units/unit_{resource}_hd.png';reference=f'secondary_units/unit_{resource}_native.png';name=f'secondary_unit_{resource}'
            rgba=np.array(art);rgba[rgba[:,:,3]==0]=0;Image.fromarray(rgba).save(ROOT/'graphics'/image,optimize=True)
            rgb=np.asarray(item['palette_rgb'],dtype='uint8');rgba=np.dstack([rgb[a],native.astype('uint8')*255]);rgba[~native]=0;Image.fromarray(rgba).save(ROOT/'graphics'/reference)
            library['atlases'][name]=dict(image=image,reference=reference,native_size=[w,h],lazy=True)
            if not any(b.get('secondary_unit') and b.get('resource')==resource for b in library['bindings']):
                index=np.where(a,a.astype('uint16')|0x8000,0).astype('<u2');q=np.rint(rgb.astype('float64')*31/255).astype('uint32');pal=q[:,0]|q[:,1]<<5|q[:,2]<<10
                colors=np.where(a,pal[a]|0x8000,0).astype('<u2')
                library['bindings'].append(dict(hash=zlib.crc32(colors.tobytes())^(w<<16)^h,rgb_enabled=True,index_hash=zlib.crc32(index.tobytes())^(w<<16)^h,indexed_safe=True,dynamic_palette=True,original_palette_rgb=rgb.tolist(),index_pixels=base64.b64encode(zlib.compress(a.tobytes())).decode('ascii'),x=0,y=0,w=w,h=h,atlas_id=name,resource=resource,source_x=0,source_y=0,secondary_unit=True,auto_unit=True))
    if args.apply:
        temp=path.with_suffix('.tmp.json');temp.write_text(json.dumps(library,indent=2));temp.replace(path)
    (folder/'paint_registration.json').write_text(json.dumps(dict(applied=args.apply,checked=checked,rejected=rejected),ensure_ascii=False,indent=2),encoding='utf-8')
    catalog=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text())
    expected={u['secondary_image'] for u in catalog['units'] if u.get('secondary_image') and u.get('primary_image') is not None}
    registered={b['resource'] for b in library['bindings'] if b.get('secondary_unit')}
    coverage=dict(scope='ROM-named mini-unit images; binding coverage is not complete gameplay verification',expected=len(expected),registered=len(expected&registered),missing=sorted(expected-registered))
    (folder/'coverage.json').write_text(json.dumps(coverage,indent=2));print(json.dumps(dict(accepted=len(checked),rejected=rejected,coverage=coverage),ensure_ascii=False))

if __name__=='__main__':main()
