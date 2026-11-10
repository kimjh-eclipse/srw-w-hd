"""Check new attack atlases and their recorded native hardware rectangles."""
import base64,json,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g
from tile_compositor import TileCompositor

def main():
    folder=ROOT/'graphics/named_attack_frames';registration=json.loads((folder/'registration.json').read_text())
    assert registration['applied'],'Run the installer first'
    accepted={r['resource'] for r in registration['accepted']};plan=json.loads((folder/'plan.json').read_text())
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom);c=TileCompositor();rows=[];cards=[]
    for sheet in plan['sheets']:
        for item in sheet['items']:
            resource=item['resource']
            if resource not in accepted:continue
            a=g.pixels(g.decompress(rom[g.BASE+offsets[resource]:g.BASE+offsets[resource+1]]))
            q=np.rint(np.asarray(item['palette_rgb'],dtype='float64')*31/255).astype('uint16');pal=q[:,0]|q[:,1]<<5|q[:,2]<<10
            art,stats=c.assemble(a,pal);assert art is not None,(resource,stats)
            sources=sorted({c.source(group['source'])[0]['resource'] for group in stats['tile_groups']})
            rows.append(dict(resource=resource,exact_tiles=stats['exact_tiles'],source_resources=sources))
            im=Image.open(folder/f'frame_{resource}_hd.png').convert('RGBA');assert max(im.size)<=960
            rgba=np.asarray(im);assert not rgba[rgba[:,:,3]==0,:3].any()
            im.thumbnail((460,115));card=Image.new('RGB',(480,140),'#263340');card.paste(im,(0,20),im);ImageDraw.Draw(card).text((4,2),f'IMG {resource}, exact native tiles {stats["exact_tiles"]}',fill='white');cards.append(card)
    observed=[]
    library=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text())
    for binding in library['bindings']:
        if not binding.get('observed_native_rectangle'):continue
        w,h=binding['w'],binding['h'];a=np.frombuffer(zlib.decompress(base64.b64decode(binding['index_pixels'])),dtype='uint8').reshape(h,w)
        q=np.rint(np.asarray(binding['original_palette_rgb'],dtype='float64')*31/255).astype('uint16');palette=q[:,0]|q[:,1]<<5|q[:,2]<<10
        art,stats=c.assemble(a,palette);assert art is not None,(binding['atlas_id'],stats)
        observed.append(dict(resource=binding['resource'],index_hash=binding['index_hash'],exact_tiles=stats['exact_tiles']))
    old=json.loads((ROOT/'test_current/parts/observed_attack_gaps/report.json').read_text());captures=[];opened={}
    try:
        for record in old['unmatched_rectangles']:
            if not any(candidate['resource'] in accepted for candidate in record['candidates']):continue
            path=ROOT/record.get('capture',f'test_current/combat/named_attacks/unit_{record["unit_id"]}/unit_{record["unit_id"]}_weapon_{record["weapon_id"]}_unknown.npz')
            if not path.exists():continue
            if path not in opened:opened[path]=np.load(path)
            data=opened[path]
            for raw,pixels,palette in zip(data['rows'],data['pixels'],data['palettes']):
                if (int(raw[0]),int(raw[7]))!=(record['index_hash'],record['material_hash']):continue
                w,h=map(int,raw[1:3]);art,stats=c.assemble(pixels[:w*h].reshape(h,w),palette)
                captures.append(dict(unit_id=record['unit_id'],weapon_id=record['weapon_id'],index_hash=record['index_hash'],assembled=art is not None,stats=stats));break
    finally:
        for data in opened.values():data.close()
    result=dict(scope=__doc__,registered_resources=len(rows),rows=rows,observed_rectangles_registered=observed,recorded_rectangles=len(captures),recorded_rectangles_assembled=sum(r['assembled'] for r in captures),captures=captures,all_gameplay_frames_verified=False)
    (folder/'coverage.json').write_text(json.dumps(result,indent=2))
    out=ROOT/'test_current/parts/named_attack_frames';out.mkdir(exist_ok=True)
    contact=Image.new('RGB',(960,140*((len(cards)+1)//2)),'#263340')
    for i,card in enumerate(cards):contact.paste(card,(i%2*480,i//2*140))
    contact.save(out/'contact.png');print(json.dumps({k:v for k,v in result.items() if k not in ('rows','captures')}))

if __name__=='__main__':main()
