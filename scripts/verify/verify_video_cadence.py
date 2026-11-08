"""Skipped video keeps the last complete RGB/metadata pair and full audio ticks."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,zlib,sys
import numpy as np
from hd_core import Core,ROOT
from frame_compositor import ReadyParts

def main():
    baseline='--baseline' in sys.argv;records=[];out=ROOT/'test_current/parts';expected=[] if baseline else json.loads((out/'video_cadence_reference.json').read_text());core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'cadence_saves',frameskip=0 if baseline else 1);ready=ReadyParts();core.set_ready_parts(ready);record=0;fresh=skipped=audio=skipped_audio=0
    try:
        for name in ('target','battle_13110','battle_13620','battle_14850','cutin_2','target'):
            core.load(ROOT/f'test_current/attract/{name}.state');previous=None
            for frame in range(90):
                changed=core.run();size=len(core.audio);audio+=size;core.audio.clear()
                digest=zlib.crc32(core.native.tobytes())
                # BG pixels have no OBJ owner; inactive OBJ palette rows are
                # intentionally not cleared by the native renderer. Neither is
                # consumed by the HD compositor. Compare only defined fields.
                for array in (core.parts,core.bgparts,core.ids,np.where(core.ids==4,core.owners,0).astype('uint8'),np.where(core.parts[:,0,None]>0,core.part_palettes,0).astype('uint16')):digest=zlib.crc32(array.tobytes(),digest)
                if changed:
                    fresh+=1
                    if not baseline:assert expected[record]==[name,frame,digest],(expected[record],[name,frame,digest])
                    previous=digest
                else:
                    skipped+=1;skipped_audio+=size
                    if previous is not None:assert digest==previous,'incomplete skipped-frame metadata leaked'
                records.append([name,frame,digest]);record+=1
        if baseline:
            (out/'video_cadence_reference.json').write_text(json.dumps(records));print('saved semantic video reference',len(records));return
        assert fresh==270 and skipped==270,(fresh,skipped)
        assert audio>540*600*4 and skipped_audio>0,(audio,skipped_audio)
        report=dict(emulated_frames=record,complete_video_frames=fresh,skipped_video_frames=skipped,video_and_visible_metadata_match_full_rate_reference=True,background_owner_bytes_ignored=True,inactive_object_palette_rows_ignored=True,audio_bytes=audio,audio_on_skipped_video_bytes=skipped_audio);(out/'video_cadence_verification.json').write_text(json.dumps(report,indent=2));print(report)
    finally:core.close()

if __name__=='__main__':main()
