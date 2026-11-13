"""Find part textures that kept chroma-key colour inside the picture.

Every finished part texture in the baked store is compared with the colours
its native part can show. A texture with a visible amount of saturated
green (or magenta) that its native palette has no counterpart for is
reported: that colour can only have come from the generation background
that was meant to become transparent.

Reads only. Writes a report and contact sheets under
test_current/parts/green_key_review/.
"""
import argparse,io,json,sqlite3,sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image,ImageDraw


def measure(pixels,palette):
    """Counts of key-coloured pixels the native palette cannot explain."""
    r=pixels[:,:,0].astype('int16');g=pixels[:,:,1].astype('int16');b=pixels[:,:,2].astype('int16');shown=pixels[:,:,3]>=32
    green=shown&(g>=110)&(g-r>=70)&(g-b>=70)
    magenta=shown&(r>=140)&(b>=140)&(r-g>=90)&(b-g>=90)
    colours=np.asarray(palette,dtype='int16')[1:] if palette is not None and len(palette)>1 else np.zeros((0,3),dtype='int16')
    native_green=int((colours[:,1]-np.maximum(colours[:,0],colours[:,2])).max()) if len(colours) else -255
    native_magenta=int((np.minimum(colours[:,0],colours[:,2])-colours[:,1]).max()) if len(colours) else -255
    return green,magenta,int(shown.sum()),native_green,native_magenta


def main():
    parser=argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--minimum',type=int,default=8,help='key-coloured pixels (store resolution) before a part is reported')
    parser.add_argument('--sheets',type=int,default=240,help='worst parts to draw on contact sheets')
    args=parser.parse_args()
    out=ROOT/'test_current/parts/green_key_review';out.mkdir(parents=True,exist_ok=True)
    for old in out.glob('*'):
        if old.is_file():old.unlink()
    from hd_parts import PartsRenderer
    renderer=PartsRenderer(async_prepare=False);owners=defaultdict(list)
    for binding,spec in enumerate(renderer.bindings,1):
        if spec.get('source_binding') or spec.get('runtime_texture') or spec.get('disabled'):continue
        owners[renderer.texture_key(binding,spec['w'],spec['h'])].append(binding)
    db=sqlite3.connect((Path(renderer.disk_cache.path)).as_uri()+'?mode=ro',uri=True)
    rows=[];scanned=0;kept={}
    for key,blob in db.execute('SELECT key,pixels FROM textures'):
        bindings=owners.get(key)
        if not bindings:continue
        scanned+=1;pixels=np.asarray(Image.open(io.BytesIO(blob)).convert('RGBA'))
        # A texture shared by several bindings is judged against every palette it is shown with.
        palettes=[]
        for binding in bindings:
            spec=renderer.bindings[binding-1]
            for name in ('original_palette_rgb','palette_rgb','palette_source_rgb'):
                if spec.get(name) is not None:palettes.extend(spec[name][1:])
        palette=[[0,0,0]]+palettes if palettes else None
        green,magenta,shown,native_green,native_magenta=measure(pixels,palette)
        for name,mask,native in (('green',green,native_green),('magenta',magenta,native_magenta)):
            count=int(mask.sum())
            if count<args.minimum or native>=40:continue
            spec=renderer.bindings[bindings[0]-1];colour=pixels[mask][:,:3].mean(0).round().astype(int).tolist()
            rows.append(dict(colour=name,binding=bindings[0],bindings=len(bindings),resource=spec.get('resource'),atlas=spec.get('atlas_id','base'),x=spec['x'],y=spec['y'],w=spec['w'],h=spec['h'],
                key_pixels=count,shown_pixels=shown,share=round(count/max(1,shown),4),mean_rgb=colour,native_strongest=native,key=key))
            kept[key]=(pixels,mask)
    db.close();renderer.close()
    rows.sort(key=lambda row:-row['key_pixels'])
    by_resource=defaultdict(lambda:dict(parts=0,key_pixels=0,atlases=set()));by_atlas=defaultdict(lambda:dict(parts=0,key_pixels=0))
    for row in rows:
        if row['colour']!='green':continue
        entry=by_resource[row['resource']];entry['parts']+=1;entry['key_pixels']+=row['key_pixels'];entry['atlases'].add(row['atlas'])
        entry=by_atlas[row['atlas']];entry['parts']+=1;entry['key_pixels']+=row['key_pixels']
    report=dict(textures_scanned=scanned,minimum_pixels=args.minimum,
        green_parts=sum(r['colour']=='green' for r in rows),magenta_parts=sum(r['colour']=='magenta' for r in rows),
        green_by_atlas=sorted(({'atlas':k,**v} for k,v in by_atlas.items()),key=lambda e:-e['key_pixels']),
        green_by_resource=sorted(({'resource':k,'parts':v['parts'],'key_pixels':v['key_pixels'],'atlases':sorted(v['atlases'])} for k,v in by_resource.items()),key=lambda e:-e['key_pixels']),
        parts=[{k:v for k,v in row.items() if k!='key'} for row in rows])
    (out/'report.json').write_text(json.dumps(report,indent=1,ensure_ascii=False),encoding='utf-8')
    # Contact sheets: the texture, then the same texture with the reported pixels marked.
    cell=132;per_row=8;per_sheet=per_row*5;chosen=[row for row in rows if row['colour']=='green'][:args.sheets]
    for start in range(0,len(chosen),per_sheet):
        group=chosen[start:start+per_sheet];sheet=Image.new('RGB',(per_row*cell*2,((len(group)+per_row-1)//per_row)*(cell+14)),(40,40,48));draw=ImageDraw.Draw(sheet)
        for index,row in enumerate(group):
            pixels,mask=kept[row['key']];art=Image.fromarray(pixels);marked=pixels.copy();marked[mask]=(255,0,255,255);marked=Image.fromarray(marked)
            scale=min((cell-4)/art.width,(cell-4)/art.height,4);size=(max(1,round(art.width*scale)),max(1,round(art.height*scale)))
            x=(index%per_row)*cell*2;y=(index//per_row)*(cell+14)
            for offset,picture in ((0,art),(cell,marked)):
                tile=picture.resize(size,Image.Resampling.NEAREST);sheet.paste(tile,(x+offset+2,y+2),tile)
            draw.text((x+2,y+cell),f"#{row['binding']} r{row['resource']} {row['atlas']} {row['key_pixels']}px",fill=(230,230,230))
        sheet.save(out/f'green_sheet_{start//per_sheet:02d}.png')
    print(json.dumps({k:v for k,v in report.items() if k not in ('parts','green_by_resource','green_by_atlas')}))
    print('atlases',len(report['green_by_atlas']),'resources',len(report['green_by_resource']))
    for entry in report['green_by_atlas'][:25]:print(entry)


if __name__=='__main__':main()
