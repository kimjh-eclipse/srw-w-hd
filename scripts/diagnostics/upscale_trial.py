"""Technical trial: open-source Real-ESRGAN on native robot/effect sheets against the current HD art.

For each source image: render it in its pattern palette (index 0 transparent),
upscale x4 with two models, assemble the current HD art of that image from the
part library, and write a comparison (native nearest | current HD | model A |
model B) plus alpha checks. Writes test_current/parts/upscale_trial/. Reads only.
"""
import json,subprocess,sys
from collections import Counter
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image,ImageDraw
from scripts.assets import srw_graphics as g

EXE=ROOT/'tools/realesrgan/realesrgan-ncnn-vulkan.exe'
MODELS=('realesr-animevideov3','realesrgan-x4plus-anime')


def main():
    images=[int(a) for a in sys.argv[1:]] or [3376,3392,1164,21948,19645]
    out=ROOT/'test_current/parts/upscale_trial';out.mkdir(parents=True,exist_ok=True)
    rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();offsets=g.archive(rom)
    resource=lambda i:g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    patterns=json.loads((ROOT/'test_current/rom_catalog/animation_audit.json').read_text(encoding='utf-8'))['patterns']
    meta=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text(encoding='utf-8'))
    for image in images:
        owner=[p for p in patterns if image in (p.get('image_group') or [p['image']])]
        if not owner:print(image,'no pattern');continue
        p=owner[0];bank=Counter(q['palette_bank'] for q in p['parts']).most_common(1)[0][0]
        pal=np.frombuffer(resource(p['palette'])[8:],dtype='<u2');colours=pal[bank*16:(bank+1)*16] if len(pal)>=(bank+1)*16 else pal[:16]
        idx=g.pixels(resource(image));rgb=np.stack([(colours&31)*255//31,((colours>>5)&31)*255//31,((colours>>10)&31)*255//31],-1).astype('uint8')
        native=np.dstack([rgb[np.minimum(idx,len(rgb)-1)],np.where(idx>0,255,0).astype('uint8')])
        Image.fromarray(native).save(out/f'{image}_native.png')
        # Current HD: every library part cut from this image, pasted at its source place.
        hd=Image.new('RGBA',(idx.shape[1]*4,idx.shape[0]*4));count=0
        atlases={}
        for b in meta['bindings']:
            if b.get('resource')!=image or b.get('disabled') or not b.get('atlas_id'):continue
            a=meta['atlases'].get(b['atlas_id'])
            if not a or not (ROOT/'graphics'/a['image']).exists():continue
            if a['image'] not in atlases:atlases[a['image']]=Image.open(ROOT/'graphics'/a['image']).convert('RGBA')
            x,y,w,h=b['x'],b['y'],b['w'],b['h'];sx,sy=b.get('source_x',x),b.get('source_y',y)
            if sx is None or sy is None:continue
            crop=atlases[a['image']].crop((x*4,y*4,(x+w)*4,(y+h)*4));hd.alpha_composite(crop,(sx*4,sy*4));count+=1
        hd.save(out/f'{image}_current_hd.png')
        results=[]
        for model in MODELS:
            target=out/f'{image}_{model}.png'
            done=subprocess.run([str(EXE),'-i',str(out/f'{image}_native.png'),'-o',str(target),'-n',model,'-s','4','-t','64','-m',str(EXE.parent/'models')],capture_output=True,text=True)
            if not target.exists():print(image,model,'failed',done.stderr[-200:]);results.append(None);continue
            up=Image.open(target);results.append(up)
            a=np.asarray(up.convert('RGBA'))[:,:,3];print(image,model,'mode',up.mode,'size',up.size,'alpha kept',bool(up.mode=='RGBA' and (a<255).any()))
        print(image,'palette',p['palette'],'bank',bank,'current HD parts',count,'size',idx.shape[::-1])
        panels=[Image.fromarray(native).resize((idx.shape[1]*4,idx.shape[0]*4),Image.Resampling.NEAREST),hd]+[r.convert('RGBA') if r else Image.new('RGBA',hd.size) for r in results]
        labels=['native x4 (nearest)',f'current HD ({count} parts)']+list(MODELS)
        W,H=hd.size;sheet=Image.new('RGB',(W*len(panels),H+20),(96,96,104));d=ImageDraw.Draw(sheet)
        for k,(pnl,lab) in enumerate(zip(panels,labels)):sheet.paste(pnl,(k*W,20),pnl);d.text((k*W+4,4),lab,fill=(255,255,255))
        sheet.save(out/f'{image}_compare.png')


if __name__=='__main__':main()
