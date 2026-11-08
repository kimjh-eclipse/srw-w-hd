"""Read-only catalog of W archive textures, palettes and animation resources."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import sys,json,struct,hashlib,time
sys.path.insert(0,str(PROJECT_ROOT))
import scripts.assets.srw_graphics as g

ROOT=g.ROOT;OUT=ROOT/'test_current/rom_catalog';OUT.mkdir(exist_ok=True)
rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();offsets=g.archive(rom)
reference=(ROOT/'test_current/robot/vram_65340.bin').read_bytes()[:16384]
records=[];matches=[];started=time.time()
for i in range(len(offsets)-1):
    packed=rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]]
    compressed=packed[:4]==b'ECD\1';header=packed[16:20] if compressed else packed[:4]
    if header[:3] not in (b'IMG',b'PLT',b'PAT',b'TIM'):continue
    record=dict(id=i,kind=header[:3].decode(),packed_size=len(packed),offset=g.BASE+offsets[i])
    if header[:3] in (b'IMG',b'PLT'):
        raw=g.decompress(packed);record['size']=len(raw);record['sha256']=hashlib.sha256(raw).hexdigest()
        if header[:3]==b'IMG':
            record.update(w=struct.unpack_from('<H',raw,4)[0]*8,h=struct.unpack_from('<H',raw,6)[0]*8,bpp=8 if raw[3] else 4)
            at=raw.find(reference[:1024])
            if at>=0:matches.append(dict(id=i,offset=at,equal=raw[at:at+len(reference)]==reference))
        else:record['colors']=struct.unpack_from('<I',raw,4)[0]
    records.append(record)
    if i%500==0:(OUT/'progress.json').write_text(json.dumps(dict(last_resource=i,records=len(records),seconds=round(time.time()-started,1))))
(OUT/'catalog.json').write_text(json.dumps(dict(records=records,known_atlas_matches=matches,seconds=round(time.time()-started,1)),indent=2))
print(json.dumps(dict(records=len(records),matches=matches,seconds=round(time.time()-started,1))))
