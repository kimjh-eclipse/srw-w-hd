"""Apply the requested intermediate FMP armor style to menu and fallback art."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from painted_edges import clean_alpha


def main():
    folder=ROOT/'graphics/menu_units';source=folder/'config_fmp_generated.png'
    original=Image.open(folder/'favorite_4_display.png').convert('RGBA');generated=clean_alpha(Image.open(source).convert('RGBA'))
    def bounds(image):return Image.fromarray((np.asarray(image.getchannel('A'))>64).astype('uint8')*255).getbbox()
    box=bounds(original);crop=generated.crop(bounds(generated));art=Image.new('RGBA',original.size)
    art.paste(crop.resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS),box[:2]);rgba=np.array(art);rgba[rgba[:,:,3]==0]=0;art=Image.fromarray(rgba)
    reference=Image.open(folder/'favorite_runtime_native.png').convert('RGBA').crop((384,0,512,112))
    mask=np.asarray(art.getchannel('A').resize((128,112),Image.Resampling.BOX))>64;expected=np.asarray(reference.getchannel('A'))>0
    score=float((mask&expected).sum()/max(1,(mask|expected).sum()));assert score>=.80,score
    art.save(folder/'favorite_4_display.png',optimize=True)
    whole=Image.open(folder/'favorite_runtime_hd.png').convert('RGBA');sx=whole.width/512;sy=whole.height/224
    rect=(round(384*sx),0,round(512*sx),round(112*sy));whole.paste(art.resize((rect[2]-rect[0],rect[3]),Image.Resampling.LANCZOS),rect[:2]);whole.save(folder/'favorite_runtime_hd.png',optimize=True)
    layout=json.loads((folder/'favorite_runtime.json').read_text());group=next(x for x in layout['groups'] if x['bank']==4)
    library=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text());bindings={b['hash']:b for b in library['bindings'] if b.get('atlas_id')=='favorite_menu'}
    atlas=Image.open(folder/'favorite_parts_hd.png').convert('RGBA');ax=atlas.width/512;ay=atlas.height/256
    for part in group['parts']:
        b=bindings[part['hash']];x,y,w,h=part['sheet_x']-384,part['sheet_y'],part['w'],part['h']
        crop=art.crop((round(x*art.width/128),round(y*art.height/112),round((x+w)*art.width/128),round((y+h)*art.height/112)))
        if part['b']&4096:crop=crop.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if part['b']&8192:crop=crop.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        dest=(round(b['x']*ax),round(b['y']*ay),round((b['x']+w)*ax),round((b['y']+h)*ay))
        atlas.paste(crop.resize((dest[2]-dest[0],dest[3]-dest[1]),Image.Resampling.LANCZOS),dest[:2])
    atlas.save(folder/'favorite_parts_hd.png',optimize=True)
    report=dict(style='Intermediate mechanical volume; reduced inflated armor',alpha_iou=score,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),fallback_parts=len(group['parts']))
    (folder/'fmp_style_registration.json').write_text(json.dumps(report,indent=2));print(report)


if __name__=='__main__':main()
