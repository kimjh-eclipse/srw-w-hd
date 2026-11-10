"""Verify every named mini IMG against the production exact-tile compositor.

These are ROM texels, including observed hardware rectangles, not complete
campaign replays. Keep this distinction in the saved report.
"""
import base64,json,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from tile_compositor import TileCompositor

def main():
    library=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text())
    bindings={b['resource']:b for b in library['bindings'] if b.get('secondary_unit')}
    catalog=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text())
    expected={u['secondary_image'] for u in catalog['units'] if u.get('secondary_image') and u.get('primary_image') is not None}
    assert not expected-bindings.keys(),sorted(expected-bindings.keys())
    compositor=TileCompositor();rows=[];out=ROOT/'test_current/parts/secondary_units';out.mkdir(exist_ok=True);cards=[]
    for resource in sorted(expected):
        b=bindings[resource];h,w=b['h'],b['w'];a=np.frombuffer(zlib.decompress(base64.b64decode(b['index_pixels'])),dtype='uint8').reshape(h,w)
        q=np.rint(np.asarray(b['original_palette_rgb'],dtype='float64')*31/255).astype('uint16');palette=q[:,0]|q[:,1]<<5|q[:,2]<<10
        atlas=library['atlases'][b['atlas_id']]
        with Image.open(ROOT/'graphics'/atlas['image']) as image:
            assert max(image.size)<=960,(resource,image.size)
            paint=np.asarray(image.convert('RGBA'));assert not paint[paint[:,:,3]==0,:3].any(),resource
        art,stats=compositor.assemble(a,palette);assert art is not None,(resource,stats)
        assert stats.get('offline_registered'),(resource,'fell back to a pixel silhouette',stats)
        rows.append(dict(resource=resource,exact_tiles=stats['exact_tiles'],source_resources=sorted({compositor.source(x['source'])[0]['resource'] for x in stats['tile_groups']})))
        if len(cards)<24:
            card=Image.new('RGB',(192,160),'#283238');art.thumbnail((192,140));card.paste(art,(0,20),art);ImageDraw.Draw(card).text((3,3),f'IMG {resource}',fill='white');cards.append(card)
        if len(rows)%40==0:print('mini bindings',len(rows),'/',len(expected),flush=True)
    report=dict(scope=__doc__,expected=len(expected),verified=len(rows),all_campaign_scenes_verified=False,rows=rows)
    (out/'report.json').write_text(json.dumps(report,indent=2))
    sheet=Image.new('RGB',(192*6,160*4))
    for n,card in enumerate(cards):sheet.paste(card,(n%6*192,n//6*160))
    sheet.save(out/'contact.png');print('verified',len(rows),flush=True)

if __name__=='__main__':main()
