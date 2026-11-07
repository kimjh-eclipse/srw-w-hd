"""Read-only ROM / captured VRAM resource correspondence audit."""
import sys, json, zlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from srw_graphics import archive, decompress, BASE
F=ROOT/'graphics/battle_backgrounds'
CAPTURES={'city':'8910_3','field':'7040_3','forest':'8100_3','tower':'8910_2','space':'13110_3','deck':'14850_3'}

def main():
    rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes()
    offsets=archive(rom)
    records=json.loads((ROOT/'test_current/rom_catalog/catalog.json').read_text())['records']
    targets={name:dict(np.load(ROOT/f'test_current/attract/bg_{suffix}.npz')) for name,suffix in CAPTURES.items()}
    palettes={name:t['palette'].astype('<u2').tobytes() for name,t in targets.items()}
    hits={name:[] for name in targets}
    for record in records:
        if record['kind']!='PLT':continue
        i=record['id'];raw=decompress(rom[BASE+offsets[i]:BASE+offsets[i+1]])
        payload=raw[8:]
        for name,pal in palettes.items():
            # Ignore transparent first palette entry and require a full 15-color bank.
            if len(payload)>=32 and payload[2:32] in pal:
                hits[name].append(i)
    print('palette candidates',hits,flush=True)
    candidateids=set()
    for ids in hits.values():
        for i in ids:candidateids.update(range(max(0,i-8),min(len(offsets)-1,i+25)))
    matches={name:[] for name in targets}
    tilelookup={name:set(zlib.crc32(t['tiles'][j:j+32].tobytes()) for j in range(0,len(t['tiles'])-31,32) if np.count_nonzero(t['tiles'][j:j+32])>8) for name,t in targets.items()}
    for i in sorted(candidateids):
        raw=decompress(rom[BASE+offsets[i]:BASE+offsets[i+1]])
        if raw[:3]!=b'IMG':continue
        payload=raw[8:]
        crcs=[zlib.crc32(payload[j:j+32]) for j in range(0,len(payload)-31,32)]
        for name,lookup in tilelookup.items():
            n=sum(c in lookup for c in crcs)
            if n>=8:matches[name].append(dict(resource=i,matched_tiles=n,total_tiles=len(crcs),header=raw[:8].hex()))
    print('tile matches',json.dumps(matches),flush=True)
    F.mkdir(parents=True,exist_ok=True)
    report=dict(captures=CAPTURES,palette_candidates=hits,tile_matches=matches,candidate_images_near_matched_palettes=True)
    (F/'bank_audit.json').write_text(json.dumps(report,indent=2))

if __name__=='__main__':main()
