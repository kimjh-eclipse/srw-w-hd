"""Sheet of the partitions found by split_object_drawings.py, grouped by shape.

Sprites with the same index hash are the same part shape in different palettes
(fades, flashes, colour variants). Per shape: the cut partition of the
best-covered palette, how many palettes, coverage, and whether HD is already
connected for any of them.

  py -3.11 -X utf8 scripts/verify/partition_sheet.py <set dir> [split dir name]
"""
import json,sys
from collections import defaultdict
from pathlib import Path
from PIL import Image,ImageDraw


def main():
    root=Path(sys.argv[1]);split=root/(sys.argv[2] if len(sys.argv)>2 else 'split_selftest')
    cov={r['hash']:r for r in json.loads((split/'coverage.json').read_text(encoding='utf-8'))}
    shape={};palettes=defaultdict(set);bound=defaultdict(set)
    for c in root.glob('pose_*/contract.json'):
        for r in json.loads(c.read_text(encoding='utf-8')):
            shape[r['hash']]=r['index_hash'];palettes[r['index_hash']].add(r['hash'])
            if r['binding_id']:bound[r['index_hash']].add(r['binding_id'])
    groups=[]
    for ih,hashes in palettes.items():
        best=max(hashes,key=lambda h:cov[h]['coverage'])
        groups.append(dict(index_hash=ih,palettes=len(hashes),best=best,coverage=cov[best]['coverage'],w=cov[best]['w'],h=cov[best]['h'],with_hd=len(bound[ih])))
    groups.sort(key=lambda g:(-g['w']*g['h'],g['index_hash']))
    cell=150;cols=10;rows=(len(groups)+cols-1)//cols
    sheet=Image.new('RGBA',(cols*cell,rows*cell+30),(50,52,60,255));d=ImageDraw.Draw(sheet)
    full=sum(1 for g in groups if g['coverage']>=.999)
    d.text((6,8),f"shapes {len(groups)} (sprites {len(shape)}), fully covered {full}, mean coverage {sum(g['coverage'] for g in groups)/max(len(groups),1):.3f}",fill=(255,255,255))
    for k,g in enumerate(groups):
        im=Image.open(split/'parts'/f"{g['best']}.png");im.thumbnail((cell-8,cell-40))
        x=(k%cols)*cell;y=30+(k//cols)*cell
        sheet.alpha_composite(im,(x+4,y+4))
        d.text((x+4,y+cell-34),f"{g['w']}x{g['h']} pal {g['palettes']}",fill=(255,255,0))
        d.text((x+4,y+cell-20),f"cov {g['coverage']:.2f} hd {g['with_hd']}",fill=(120,255,120) if g['coverage']>=.999 else (255,140,120))
    sheet.save(root/'PARTITIONS_SHEET.png');(root/'PARTITIONS.json').write_text(json.dumps(groups,ensure_ascii=False,indent=1),encoding='utf-8')
    print('shapes',len(groups),'sprites',len(shape),'fully covered',full,'sheet',root/'PARTITIONS_SHEET.png')


if __name__=='__main__':main()
