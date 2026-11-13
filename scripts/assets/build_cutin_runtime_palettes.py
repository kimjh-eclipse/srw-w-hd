"""List cut-in pictures the game colours through the palette at run time.

A few BG pictures are stored as a neutral grey ramp; the game loads a
coloured ramp into their palette bank and animates it. Their HD pictures
are grey as well, so the player has to map brightness to the live palette.
This writes the grey ramp of every such cut-in to
graphics/cutin_runtime_palettes.json (5-bit levels of palette slots 1-15).
"""
import json,struct,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import numpy as np
from scripts.assets import srw_graphics as g


def main():
    library=json.loads((ROOT/'graphics/cutins_library.json').read_text(encoding='utf-8'))['cutins']
    rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();offsets=g.archive(rom);found={}
    for spec in library:
        resource=spec.get('source_palette')
        if resource is None:continue
        try:
            raw=g.decompress(rom[g.BASE+offsets[resource]:g.BASE+offsets[resource+1]]);count=struct.unpack_from('<I',raw,4)[0]
            values=np.frombuffer(raw[8:8+count*2],dtype='<u2')
        except Exception:continue
        if count!=16:continue
        colours=np.stack([values&31,(values>>5)&31,(values>>10)&31],-1)[1:].astype(int)
        neutral=np.all(colours.max(1)-colours.min(1)<=1);rising=np.all(np.diff(colours[:,1])>=0) and colours[-1,1]>colours[0,1]
        if neutral and rising:found[str(spec['id'])]=dict(name=spec.get('name'),palette_resource=resource,ramp=colours[:,1].tolist())
    out=ROOT/'graphics/cutin_runtime_palettes.json';out.write_text(json.dumps(found,indent=1),encoding='utf-8');print(len(found),'cut-ins',list(found))


if __name__=='__main__':main()
