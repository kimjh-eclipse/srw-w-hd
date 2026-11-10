"""Register assembled compact pilot planes after checking layout and alpha.

Registration is not a gameplay/all-poses certificate. Native images remain
references only; a missing or rejected drawing never becomes a replacement.
"""
import argparse,hashlib,json,struct,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g
from scripts.assets.install_pilot_cutins import fnv

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    folder=ROOT/'graphics/compact_pilot_cutins'
    library_path=ROOT/'graphics/cutins_library.json';library=json.loads(library_path.read_text())
    existing={row.get('resource'):row for row in library['cutins']}
    signatures={v:row['id'] for row in library['cutins'] for v in row['signatures']}
    next_id=max(row['id'] for row in library['cutins'])+1
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    def read(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    accepted=[];pending=[]
    generation={row['resource']:row for row in json.loads((folder/'generation.json').read_text())['items']}
    for item in json.loads((folder/'plan.json').read_text())['items']:
        resource=item['resource'];source=folder/item['output']
        if not source.exists():pending.append(dict(resource=resource,reason='not_painted'));continue
        proof=generation.get(resource,{})
        reference_digest=hashlib.sha256((folder/item['reference']).read_bytes()).hexdigest()
        if proof.get('reference_sha256')!=reference_digest or not proof.get('visual_style_reviewed'):
            pending.append(dict(resource=resource,reason='reference_changed_or_unreviewed'));continue
        with Image.open(source) as image:art=image.convert('RGBA').resize((768,384),Image.Resampling.LANCZOS)
        with Image.open(folder/f'cutin_{resource}_native.png') as image:reference=np.asarray(image.getchannel('A'))>64
        alpha=np.asarray(art.getchannel('A').resize((256,128),Image.Resampling.BOX))>64
        iou=float((alpha&reference).sum()/max(1,(alpha|reference).sum()))
        if iou<.82:pending.append(dict(resource=resource,reason='layout_or_alpha_mismatch',alpha_iou=iou));continue
        pixels=np.array(art);pixels[pixels[:,:,3]==0]=0;art=Image.fromarray(pixels)
        data=read(resource);assert data[:4]==b'IMG\0' and struct.unpack_from('<H',data,4)[0]==32
        sample=data[8+1024:8+3072];assert len(sample)==2048
        signature=fnv(sample);mapdata=read(item['map'])
        map_signature=fnv(b''.join(struct.pack('<H',v&0xfff) for v in struct.unpack_from('<16H',mapdata,8)))
        map_window=fnv(b''.join(struct.pack('<H',v&0xfff) for v in struct.unpack_from('<512H',mapdata,8)))
        prior=existing.get(resource);ident=prior['id'] if prior else next_id
        assert signature not in signatures or signatures[signature]==ident,('ambiguous_signature',resource)
        rel=f'compact_pilot_cutins/cutin_{resource}_hd.png'
        row=dict(id=ident,name=f'compact_pilot_bg_{resource}',resource=resource,source_map=item['map'],
            source_palettes=item['palettes'],layer=1,layers=[0,1,2,3],native_size=[256,128],
            restore_rect=[0,0,256,128],image=rel,paint_image=rel,signatures=[signature],
            map_signature=map_signature,signature_mode='image_origin',alpha_iou=iou,
            map_window_signature=map_window,map_window_entries=512,
            gameplay_verified=False,simultaneous_layers=True)
        if args.apply:
            art.save(ROOT/'graphics'/rel,optimize=True)
            if prior:prior.update(row)
            else:library['cutins'].append(row)
        signatures[signature]=ident;accepted.append(dict(resource=resource,id=ident,alpha_iou=iou))
        if not prior:next_id+=1
    if args.apply:
        temporary=library_path.with_suffix('.tmp.json');temporary.write_text(json.dumps(library,indent=2));temporary.replace(library_path)
    report=dict(scope=__doc__,accepted=accepted,pending=pending,applied=args.apply)
    (folder/('registration.json' if args.apply else 'registration_review.json')).write_text(json.dumps(report,indent=2))
    print(json.dumps(report))

if __name__=='__main__':main()
