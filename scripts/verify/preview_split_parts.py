"""Re-assemble split HD parts into other poses to see how the pieces join.

For each pose of a set, every sprite is drawn from <split>/parts/<hash>.png
where that part has drawn pixels, otherwise from the native sprite (nearest
4x, marked in the stats). Output preview_<pose>.png (native 4x | assembled)
for the poses that reuse the most split parts.

  py -3.11 -X utf8 scripts/verify/preview_split_parts.py <set dir> <split dir name> [--top 6]
"""
import argparse,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts.assets.build_pose_packets import sprite_pixels
S=4


def main():
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('split');p.add_argument('--top',type=int,default=6)
    a=p.parse_args();parts=a.root/a.split/'parts'
    have={int(f.stem) for f in parts.glob('*.png')}
    scored=[]
    for pose in sorted(d for d in a.root.glob('pose_*') if d.is_dir()):
        rows=json.loads((pose/'contract.json').read_text(encoding='utf-8'))
        scored.append((sum(1 for r in rows if r['hash'] in have),pose,rows))
    scored.sort(key=lambda t:-t[0]);out=[]
    for n,pose,rows in scored[:a.top]:
        W,H=Image.open(pose/'native.png').size;canvas=Image.new('RGBA',(W*S,H*S))
        for r in sorted(rows,key=lambda r:(r['priority'],r['oam']),reverse=True):
            idx=sprite_pixels(r);pal=np.array(r['original_palette_rgb'],dtype='uint8')
            nat=Image.fromarray(np.dstack([pal[idx],np.where(idx>0,255,0).astype('uint8')])).resize((r['w']*S,r['h']*S),Image.Resampling.NEAREST)
            art=nat
            if r['hash'] in have:
                hd=Image.open(parts/f"{r['hash']}.png").convert('RGBA')
                if r['flip_x']:hd=hd.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                if r['flip_y']:hd=hd.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                art=nat.copy();ha=np.asarray(hd)[:,:,3]>0;base=np.asarray(art).copy();base[ha]=np.asarray(hd)[ha];art=Image.fromarray(base)
            canvas.alpha_composite(art,(r['screen_x']*S,r['screen_y']*S))
        sheet=Image.new('RGBA',(W*S*2+8,H*S),(60,62,72,255))
        sheet.alpha_composite(Image.open(pose/'native_4x.png').convert('RGBA'),(0,0));sheet.alpha_composite(canvas,(W*S+8,0))
        sheet.save(a.root/a.split/f'preview_{pose.name}.png');out.append((pose.name,n,len(rows)))
    print('previews',out)


if __name__=='__main__':main()
