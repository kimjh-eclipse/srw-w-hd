"""Codex request batch for every attack BG picture shown without HD (scan_uncovered_cutins.py).

Groups consecutive IMG ids shown in the same attack (animation frames of one cut-in) and
writes test_current/parts/cutin_requests/batch_<tag>/:
  INDEX.json                         one row per group: images, layer, scene (state/frame), units/weapons,
                                     canvas size/opacity, whether an HD file with that IMG id already exists
  G<NNN>/<img>_canvas.png / _4x.png  whole layer canvas at that frame (live VRAM, index 0 transparent)
  G<NNN>/<img>_screen.png / _layer.png  what the game shows / that layer alone (256x192)
  OVERVIEW_<NN>.png                  contact sheets (game screen of one frame per group)
Flat (one or two colours) and empty layers are left out.

  py -3.11 -X utf8 scripts/assets/build_cutin_batch_request.py --tag 20261120
"""
import argparse,os,json,re,shutil,sys
from pathlib import Path
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
SCAN=ROOT/'test_current/parts/cutin_requests/_scan'


def main():
    p=argparse.ArgumentParser();p.add_argument('--tag',required=True);a=p.parse_args()
    out=ROOT/f'test_current/parts/cutin_requests/batch_{a.tag}';out.mkdir(parents=True,exist_ok=True)
    images=json.loads((SCAN/os.environ.get('CUTIN_SCAN','scan.json')).read_text(encoding='utf-8'))['images']
    groups=json.loads((SCAN/os.environ.get('CUTIN_GROUPS','groups.json')).read_text());canvas=json.loads((SCAN/'canvas'/os.environ.get('CUTIN_CANVAS_META','canvas.json')).read_text())
    hd_ids={}
    for d in ('pilot_cutins','compact_pilot_cutins','portraits'):
        for f in (ROOT/'graphics'/d).rglob('*') if (ROOT/'graphics'/d).exists() else []:
            for m in re.findall(r'(?<!\d)(2[2-9]\d{3})(?!\d)',f.name):hd_ids.setdefault(int(m),set()).add(f'{d}/{f.name}')
    rows=[]
    for n,g in enumerate(groups):
        gid=f'G{n:03d}';gd=out/gid;gd.mkdir(exist_ok=True);best=images[str(g[0])]['best'];items=[]
        for img in g:
            k=str(img);b=images[k]['best']
            for suf in ('screen','layer'):
                s=SCAN/'shots'/f'{k}_{suf}.png'
                if s.exists():shutil.copy2(s,gd/f'{k}_{suf}.png')
            c=SCAN/'canvas'/f'{k}.png'
            if c.exists():
                shutil.copy2(c,gd/f'{k}_canvas.png');im=Image.open(c);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(gd/f'{k}_canvas_4x.png')
            items.append(dict(image=img,layer=b['layer'],state=b['state'],frame=b['frame'],canvas=canvas.get(k),existing_hd_files=sorted(hd_ids.get(img,[]))))
        units=sorted({re.sub(r'@\d+$','',s) for img in g for s in images[str(img)]['scenes']})
        rows.append(dict(group=gid,images=g,layer=best['layer'],scene=f"{best['state']} +{best['frame']}",used_in=units,items=items))
    (out/'INDEX.json').write_text(json.dumps(dict(tag=a.tag,groups=rows),ensure_ascii=False,indent=1),encoding='utf-8')
    W=180;cols=8;per=48
    for s in range(0,len(rows),per):
        chunk=rows[s:s+per];sheet=Image.new('RGB',(cols*(W+4),((len(chunk)+cols-1)//cols)*(W*2//3+16)),(255,0,255));d=ImageDraw.Draw(sheet)
        for j,r in enumerate(chunk):
            k=str(r['images'][len(r['images'])//2]);x=(j%cols)*(W+4);y=(j//cols)*(W*2//3+16)
            scr=Image.open(SCAN/'shots'/f'{k}_screen.png').convert('RGB').crop((0,0,256,170)).resize((W,W*2//3))
            sheet.paste(scr,(x,y+14));d.rectangle((x,y,x+W,y+13),fill=(0,0,0));d.text((x+2,y+1),f"{r['group']} {r['images'][0]}x{len(r['images'])}",fill=(255,255,0))
        sheet.save(out/f'OVERVIEW_{s//per:02d}.png')
    print('groups',len(rows),'images',sum(len(r['images']) for r in rows),'with existing HD file',sum(1 for r in rows for i in r['items'] if i['existing_hd_files']))


if __name__=='__main__':main()
