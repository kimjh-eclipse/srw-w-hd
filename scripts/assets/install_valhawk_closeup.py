"""Register the separately uploaded Valhawk attack close-up using IMG/SCR identity."""
import json,sys,struct
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g
from scripts.assets.install_pilot_cutins import fnv
from painted_edges import clean_alpha


def main():
    folder=ROOT/'graphics/mechanical_cutins';source=folder/'valhawk_24394_generated.png'
    native=Image.open(ROOT/'test_current/parts/cutin_bank/bg_24394_native.png').convert('RGBA')
    art=clean_alpha(Image.open(source).convert('RGBA'))
    # The generator returns the 256x168 picture extent. Restore its unused
    # 256x256 atlas rows explicitly, preserving the original raster offset.
    art=art.resize((960,630),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(960,960));canvas.alpha_composite(art,(0,0))
    reference=Image.new('RGBA',(256,256));reference.alpha_composite(native,(0,0))
    expected=np.asarray(reference)[:,:,3]>64
    actual=np.asarray(canvas.resize((256,256),Image.Resampling.BOX))[:,:,3]>64
    iou=float((expected&actual).sum()/max(1,(expected|actual).sum()))
    assert iou>.80,iou
    output=folder/'cutin_24394_hd.png';canvas.save(output,optimize=True)
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    def resource(index):return g.decompress(rom[g.BASE+offsets[index]:g.BASE+offsets[index+1]])
    data=resource(24394);scr=resource(24395)
    signature=fnv(data[8+1024:8+3072])
    entries=struct.unpack_from('<512H',scr,8)
    map_signature=fnv(b''.join(struct.pack('<H',v&0xfff) for v in entries[:16]))
    full_signature=fnv(b''.join(struct.pack('<H',v&0xfff) for v in entries))
    path=ROOT/'graphics/cutins_library.json';library=json.loads(path.read_text())
    prior=next((r for r in library['cutins'] if r.get('resource')==24394),None)
    ident=prior['id'] if prior else max(r['id'] for r in library['cutins'])+1
    row=dict(id=ident,name='valhawk_attack_closeup',resource=24394,source_map=24395,source_palette=24393,
        layer=2,layers=[0,1,2,3],native_size=[256,256],image='mechanical_cutins/cutin_24394_hd.png',
        paint_image='mechanical_cutins/cutin_24394_hd.png',signatures=[signature],signature_mode='image_origin',
        map_signature=map_signature,map_window_signature=full_signature,map_window_entries=512,
        alpha_iou=iou,gameplay_verified=False,normal_campaign_verified=False)
    if prior:prior.update(row)
    else:library['cutins'].append(row)
    path.write_text(json.dumps(library,indent=2));print(row)


if __name__=='__main__':main()
