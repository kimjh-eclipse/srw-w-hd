"""Copy whole-image tile-source sheets (handed over as `whole_img_tile_source`) into
graphics/tile_sources/ and list them for build_tile_library.py. Verifies the
recorded drawing SHA and that the sheet is 4x the ROM image.

usage: register_tile_sources.py PACKET.json [PACKET.json ...]
"""
import hashlib,json,shutil,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from PIL import Image
from scripts.assets import srw_graphics as g


def main():
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    dst=ROOT/'graphics/tile_sources';dst.mkdir(exist_ok=True);index=dst/'sheets.json'
    data=json.loads(index.read_text(encoding='utf-8')) if index.exists() else dict(sheets=[])
    for arg in sys.argv[1:]:
        packet_path=(ROOT/arg).resolve() if not Path(arg).is_absolute() else Path(arg);packet=json.loads(packet_path.read_text(encoding='utf-8'));folder=packet_path.parent
        drawing=folder/packet['drawing'];assert hashlib.sha256(drawing.read_bytes()).hexdigest()==packet['file_sha256']['drawing'],('drawing changed',arg)
        row=json.loads((folder/packet['contract']).read_text(encoding='utf-8'))[0];resource=row['resource']
        native=g.pixels(g.decompress(rom[g.BASE+offsets[resource]:g.BASE+offsets[resource+1]]))
        size=Image.open(drawing).size;assert size==(native.shape[1]*4,native.shape[0]*4),(resource,size,native.shape)
        name=f'img{resource}_hd.png';shutil.copy2(drawing,dst/name)
        data['sheets']=[s for s in data['sheets'] if s['resource']!=resource]
        data['sheets'].append(dict(resource=resource,image=name,native_size=[int(native.shape[1]),int(native.shape[0])],palette_rgb=row['actual_palette_rgb'],source=str(packet_path.relative_to(ROOT)).replace('\\','/')))
        print('registered',resource,size)
    index.write_text(json.dumps(data,ensure_ascii=False,indent=1),encoding='utf-8')


if __name__=='__main__':main()
