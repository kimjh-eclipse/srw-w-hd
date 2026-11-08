"""Audit every PAT record, including shared palettes and affine records.

Read-only research inventory. It never silently counts an unparsed animation
as covered and does not overwrite any approved atlas or its packing positions.
"""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import sys,json,struct,collections
sys.path.insert(0,str(PROJECT_ROOT))
import scripts.assets.srw_graphics as g
ROOT=g.ROOT;OUT=ROOT/'test_current/rom_catalog'
rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
records=json.loads((OUT/'catalog.json').read_text())['records'];byid={r['id']:r for r in records}
def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])

def poses(data):
    n=struct.unpack_from('<I',data,4)[0]
    assert n<=10000 and 8+n*4<=len(data)
    offsets=list(struct.unpack_from(f'<{n}I',data,8));result=[]
    for index,at in enumerate(offsets):
        count=struct.unpack_from('<H',data,at)[0];cursor=at+2;parts=[]
        for _ in range(count):
            flags=struct.unpack_from('<H',data,cursor)[0];cursor+=2
            x=y=0
            if flags&0x2000:x,y=struct.unpack_from('<hh',data,cursor);cursor+=4
            tile=struct.unpack_from('<H',data,cursor)[0];cursor+=2
            extra=[]
            if flags&0x4000:extra.extend(struct.unpack_from('<hh',data,cursor));cursor+=4
            if flags&0x8000:extra.append(struct.unpack_from('<h',data,cursor)[0]);cursor+=2
            assert (flags>>6)&3<3
            parts.append(dict(flags=flags,x=x,y=y,tile=tile&0xfff,palette_bank=tile>>12,w=8<<(flags&3),h=8<<((flags>>2)&3),extra=extra))
        end=min([p for p in offsets if p>at]+[len(data)])
        assert cursor<=end and end-cursor<=3,(index,hex(at),count,cursor,end)
        result.append(parts)
    return result

results=[];errors=[];last_palette=None;images=[];pending=[];after_timing=False
for record in records:
    kind=record['kind'];i=record['id']
    if kind=='TIM':after_timing=True;continue
    if after_timing:images=[];pending=[];after_timing=False
    if kind=='PLT':last_palette=i
    if kind=='IMG':
        if pending:images=[];pending=[]
        images.append(i)
    if kind!='PAT':continue
    pending.append(i)
    # Consecutive PATs correspond to the preceding consecutive IMG run;
    # one IMG may also have several pose tables.
    source=images[min(len(pending)-1,len(images)-1)] if images else None
    try:
        parsed=poses(resource(i));parts=[p for pose in parsed for p in pose]
        results.append(dict(pattern=i,image=source,image_group=images.copy(),palette=last_palette,poses=len(parsed),records=len(parts),affine=sum(bool(p['extra']) for p in parts),palette_banks=sorted({p['palette_bank'] for p in parts}),max_tile=max((p['tile'] for p in parts),default=0),parts=parts))
    except (AssertionError,ValueError,struct.error) as error:errors.append(dict(pattern=i,image=source,palette=last_palette,error=str(error)))
summary=dict(patterns=len(results)+len(errors),parsed=len(results),errors=errors,records=sum(p['records'] for p in results),affine=sum(p['affine'] for p in results),sources=len({p['image'] for p in results}))
(OUT/'animation_audit.json').write_text(json.dumps(dict(summary=summary,patterns=results),indent=2));print(json.dumps(summary)[:12000])
if __name__=='__main__':pass
