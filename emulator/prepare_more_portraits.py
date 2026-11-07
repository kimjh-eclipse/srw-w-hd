"""Prepare portraits from verified native game captures, without changing ROM."""
import json,zlib
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'graphics/portraits'
TEST=ROOT/'test_current/portrait';TEST.mkdir(exist_ok=True)
SOURCES=[('akito','attract/frame_11160.png'),('genichiro','attract/frame_11970.png'),('heero','attract/frame_13200.png'),('alliance_soldier','attract/frame_13740.png'),('blade','attract/frame_14700.png'),('kazuma','robot/native_65160.png')]
def main():
    items=[];sheet=Image.new('RGB',(6*168,164),'#20242a');d=ImageDraw.Draw(sheet)
    for k,(name,source) in enumerate(SOURCES):
        im=Image.open(ROOT/'test_current'/source).convert('RGB').crop((0,136,56,184))
        im.save(OUT/f'{name}_native.png')
        reference=im.convert('RGBA');mask=Image.new('L',im.size)
        ImageDraw.Draw(mask).polygon([(0,0),(48,0),(56,8),(56,48),(0,48)],fill=255);reference.putalpha(mask)
        reference.resize((1008,864),Image.Resampling.NEAREST).save(OUT/f'{name}_reference.png')
        sheet.paste(im.resize((168,144),Image.Resampling.NEAREST),(k*168,0));d.text((k*168,146),name,fill='white')
        items.append(dict(name=name,source='test_current/'+source,rectangle=[0,136,56,48],native_size=[56,48],crc32=zlib.crc32(im.tobytes()),image=f'{name}_hd.png'))
    sheet.save(TEST/'additional_review.png');(OUT/'observed_extra.json').write_text(json.dumps(dict(portraits=items),indent=2))
if __name__=='__main__':main()
