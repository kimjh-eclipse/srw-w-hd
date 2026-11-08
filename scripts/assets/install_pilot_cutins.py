"""Validate and register completed pilot canvases, keeping incomplete work pending.

Does not equate registration with actual attack replay verification.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g
import argparse, hashlib, json, struct
import numpy as np
from PIL import Image


def fnv(data):
    value = 2166136261
    for byte in data:
        value = ((value ^ byte) * 16777619) & 0xffffffff
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    folder = ROOT/'graphics/pilot_cutins'
    plan = json.loads((folder/'plan.json').read_text())
    library_path = ROOT/'graphics/cutins_library.json'
    library = json.loads(library_path.read_text())
    old = library['cutins']
    registered = {row.get('resource'): row for row in old}
    signatures = {}
    for row in old:
        for signature in row['signatures']:
            signatures[signature] = row['id']
    rom = (ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes()
    offsets = g.archive(rom)
    def resource(index):
        return g.decompress(rom[g.BASE+offsets[index]:g.BASE+offsets[index+1]])
    checked, pending, added, rejected = [], [], [], []
    next_id = max(row['id'] for row in old)+1
    for pair in plan['pairs']:
        target = folder/pair['output']
        if not target.exists():
            pending.extend(item['image'] for item in pair['items'])
            continue
        with Image.open(target) as source:
            assert source.mode == 'RGBA', (target, source.mode)
            assert abs(source.height/source.width-2) < .02, target
            paint = source.copy()
        native = Image.open(folder/(pair['name']+'_native.png')).convert('RGBA')
        for item in pair['items']:
            index = item['image']; slot = item['slot']
            crop = paint.crop((0, round(slot*paint.height/2), paint.width, round((slot+1)*paint.height/2)))
            crop = crop.resize((960,960), Image.Resampling.LANCZOS)
            reference = np.asarray(native)[slot*256:(slot+1)*256,:,3] > 64
            width,height = item['size']
            # A few source pictures contain a deliberately opaque black bed.
            # Transparency generation can mistake this for unused atlas space.
            # Restore that solid rectangular bed without imposing a pixel mask
            # on nonrectangular painted contours.
            if reference[:height,:width].all():
                bed = Image.new('RGBA',(960,960))
                bed.paste((0,0,0,255),(0,0,round(width*960/256),round(height*960/256)))
                bed.alpha_composite(crop);crop=bed
            # The original cut-in is a deliberately cropped rectangle. Never
            # let model-generated matte dust fill its unused atlas rows.
            rgba = np.array(crop)
            rgba[round(height*960/256):] = 0
            rgba[:,round(width*960/256):] = 0
            rgba[rgba[:,:,3] == 0] = 0
            crop = Image.fromarray(rgba)
            alpha = np.asarray(crop.resize((256,256),Image.Resampling.BOX))[:,:,3] > 64
            iou = float((alpha&reference).sum()/max(1,(alpha|reference).sum()))
            if iou <= .82:
                rejected.append(dict(resource=index,canvas=pair['name'],alpha_iou=iou))
                continue
            data = resource(index); mapdata = resource(item['map'])
            assert data[:4] == b'IMG\0', (index, data[:4])
            tile_width,tile_height=struct.unpack_from('<HH',data,4)
            padded=tile_width!=32
            uploaded=data[8:]
            if padded:
                uploaded=b''.join(uploaded[y*tile_width*32:(y+1)*tile_width*32]+bytes((32-tile_width)*32) for y in range(tile_height))
            # Several eye strips start their SCR with the final blank tile.
            # Sampling relative to that tile reads beyond the uploaded IMG.
            # Use the explicit image-origin mode instead of hashing stale VRAM.
            sample_offset=8192 if index in (24859,24862) else 1024
            prior = registered.get(index)
            ident = prior['id'] if prior else next_id
            if prior and prior.get('signature_mode')=='origin_8192':sample_offset=8192
            sample_size=512 if padded else 2048
            sample = uploaded[sample_offset:sample_offset+sample_size]
            assert len(sample) == sample_size, index
            signature = fnv(sample)
            if signature in signatures and signatures[signature]!=ident:
                sample_offset=8192
                sample=uploaded[sample_offset:sample_offset+sample_size]
                assert len(sample)==sample_size,index
                signature=fnv(sample)
            assert signature not in signatures or signatures[signature] == ident, ('signature collision',index,signature)
            record = dict(resource=index,signature=signature,alpha_iou=iou,
                          canvas=pair['name'],gameplay_verified=False)
            checked.append(record)
            if prior:
                signatures[signature]=ident
                if args.apply:
                    crop.save(ROOT/'graphics'/prior.get('paint_image',prior['image']),optimize=True)
                    prior['alpha_iou']=iou
                    prior['signatures']=[signature]
                    prior['signature_mode']='row_padded' if padded else ('origin_8192' if sample_offset==8192 else 'image_origin')
                continue
            rel = f'pilot_cutins/cutin_{index}_hd.png'
            row = dict(id=ident,name=f'pilot_bg_{index}',resource=index,
                       layer=1,layers=[0,1,2,3],native_size=[256,256],
                       image=rel,paint_image=rel,signatures=[signature],
                       alpha_iou=iou,source_map=item['map'],source_palette=item['palette'],
                       generation_canvas=pair['name'],signature_mode='row_padded' if padded else ('origin_8192' if sample_offset==8192 else 'image_origin'),gameplay_verified=False)
            if args.apply:
                crop.save(ROOT/'graphics'/rel,optimize=True)
            added.append(row); signatures[signature]=ident;next_id+=1
    if args.apply:
        library['cutins'].extend(added)
        temporary = library_path.with_suffix('.tmp.json')
        temporary.write_text(json.dumps(library,indent=2));temporary.replace(library_path)
    report = dict(scope='Registration and alpha validation only; gameplay replay still required',
                  applied=args.apply,checked=checked,added=[r['resource'] for r in added],
                  pending=pending,rejected=rejected,library_count=len(old)+len(added) if not args.apply else len(library['cutins']))
    (folder/'registration_report.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(dict(checked=len(checked),added=len(added),pending=len(pending),rejected=rejected,applied=args.apply)))


if __name__ == '__main__':
    main()
