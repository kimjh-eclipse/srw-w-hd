"""Install a complete reviewed missing-export bank using exact native colours."""
import argparse, base64, hashlib, json, shutil, sys, zlib
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--resource', type=int, required=True)
    p.add_argument('--candidate-dir', type=Path, required=True)
    p.add_argument('--apply', action='store_true')
    args = p.parse_args()
    entry = next(e for e in json.loads((ROOT/'test_current/parts/missing_export/report.json').read_text())['images'] if e['image'] == args.resource)
    rom = (ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes()
    offsets = g.archive(rom)
    raw = lambda i: g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    indices = g.pixels(raw(args.resource))
    palettes = np.asarray(g.palette(raw(entry['palette'])), dtype=np.uint8)[:, :3]
    path = ROOT/'graphics/kazuma_parts_library.json'
    meta = json.loads(path.read_text())
    prefix = hashlib.sha256(json.dumps(meta['bindings'][:5263], sort_keys=True).encode()).hexdigest()
    folder = ROOT/'graphics/reviewed_effects'
    added, review = [], []
    for bank in sorted({r['bank'] for r in entry['missing']}):
        palette = palettes[bank*16:bank*16+16]
        h, w = indices.shape
        name = f'reviewed_effect_{args.resource}_bank{bank}'
        art_path = args.candidate_dir/f'final_candidate_bank{bank}.png'
        art = Image.open(art_path).convert('RGBA')
        assert art.size == (w*4, h*4), art.size
        native = Image.fromarray(np.dstack((palette[indices], (indices!=0).astype(np.uint8)*255)))
        for r in (r for r in entry['missing'] if r['bank'] == bank):
            x,y,rw,rh = (r[k] for k in ('x','y','w','h'))
            a = indices[y:y+rh,x:x+rw]
            ih = zlib.crc32(np.where(a,a.astype(np.uint16)|32768,0).astype('<u2').tobytes())^(rw<<16)^rh
            colors = np.rint(palette.astype(float)*31/255).astype(np.uint16)
            packed = colors[:,0]|colors[:,1]<<5|colors[:,2]<<10
            rgb = zlib.crc32(np.where(a,packed[a]|32768,0).astype('<u2').tobytes())^(rw<<16)^rh
            assert (ih,rgb) == (r['index_hash'],r['hash']), (r,ih,rgb)
            tile = art.crop((x*4,y*4,(x+rw)*4,(y+rh)*4))
            mask = np.asarray(tile.getchannel('A').resize((rw,rh),Image.Resampling.BOX))>64
            expected = a!=0
            iou = float((mask&expected).sum()/max(1,(mask|expected).sum()))
            assert iou >= .70, (r,iou)
            existing = next((i for i,b in enumerate(meta['bindings'],1) if b.get('atlas_id')==name and b.get('hash')==rgb),None)
            if existing:
                review.append(dict(binding=existing,bank=bank,alpha_iou=iou,reused=True)); continue
            assert not any(b.get('hash')==rgb and b.get('rgb_enabled',True) and not b.get('disabled') for b in meta['bindings']), ('already bound',rgb)
            meta['bindings'].append(dict(hash=rgb,rgb_enabled=True,index_hash=ih,indexed_safe=False,dynamic_palette=True,
                original_palette_rgb=palette.tolist(),index_pixels=base64.b64encode(zlib.compress(a.tobytes())).decode(),
                x=x,y=y,w=rw,h=rh,atlas_id=name,resource=args.resource,source_x=x,source_y=y,
                registered_attack_bank=True,preserve_canonical_paint=True,reviewed_effect_bank=True))
            added.append(len(meta['bindings']))
            review.append(dict(binding=len(meta['bindings']),bank=bank,alpha_iou=iou,reused=False))
        meta['atlases'][name] = dict(image=f'reviewed_effects/{args.resource}_bank{bank}_hd.png',reference=f'reviewed_effects/{args.resource}_bank{bank}_native.png',native_size=[w,h],lazy=True)
        if args.apply:
            folder.mkdir(exist_ok=True)
            art.save(folder/f'{args.resource}_bank{bank}_hd.png')
            native.save(folder/f'{args.resource}_bank{bank}_native.png')
            shutil.copy2(args.candidate_dir/f'generated_bank{bank}.png',folder/f'{args.resource}_bank{bank}_generated.png')
    assert prefix == hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True).encode()).hexdigest()
    assert len(review) == len(entry['missing'])
    if args.apply:
        temp = path.with_suffix('.tmp.json')
        temp.write_text(json.dumps(meta,indent=2),encoding='utf-8'); temp.replace(path)
    report = dict(resource=args.resource,applied=args.apply,new_bindings=added,rectangles=review,original_prefix_preserved=True)
    (args.candidate_dir/'install_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))

if __name__ == '__main__': main()
