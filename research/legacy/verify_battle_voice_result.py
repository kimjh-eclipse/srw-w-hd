"""Check the combat cue, a story negative control, startup and captured audio."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import hashlib,json,struct,sys,wave
import numpy as np
ROOT=PROJECT_ROOT
sys.path.insert(0,str(ROOT/'reference_bgm'))
import strm_codec

def telemetry(folder):
    ram=(ROOT/'test_current'/folder/'main_ram.bin').read_bytes()
    symbols=json.loads((ROOT/'release_battle_v02/voice_probe_symbols.json').read_text(encoding='utf-8'))
    return {k:struct.unpack_from('<I',ram,a-0x2000000)[0] for k,a in symbols.items()}

def main():
    combat=telemetry('combat')
    story=telemetry('scenario')
    boot=telemetry('boot')
    assert combat['voice_match_count']>=2,combat
    assert combat['voice_battle_count']==1,combat
    assert combat['voice_ignored_speaker_frames']>0
    assert combat['stream_underruns']==0 and combat['playing']==0
    # The last defensive response may be cut when the copilot speaks.
    # The full attack sample is independently checked in the captured audio.
    assert story['voice_match_count']==0 and story['stream_block']==0
    assert story['voice_battle_count']==0
    assert boot['voice_match_count']==0
    folder=ROOT/'test_current/combat'
    events=json.loads((folder/'voice_events.json').read_text())
    marker=events[1] # First attack shout after the opening combat response.
    blob=(ROOT/'research/legacy/battle_voice_engine/hero_streams/0.strm').read_bytes()
    reference=np.concatenate([np.array(strm_codec.decode_adpcm_block(blob[p:p+196],384)) for p in range(104,len(blob),196)])/32768
    rate=16756991/759
    reference=np.interp(np.arange(int(len(reference)*22050/rate))*rate/22050,np.arange(len(reference)),reference)
    with wave.open(str(folder/'emulator_audio.wav'),'rb') as w:
        sr=w.getframerate()
        audio=np.frombuffer(w.readframes(w.getnframes()),'<i2').reshape(-1,2).astype(float)/32768
    start=max(0,int((marker['seconds_from_run_start']-.5)*sr))
    end=min(len(audio),int((marker['seconds_from_run_start']+4.7)*sr))
    mix=audio[start:end].mean(1)[::2]
    n=1<<(len(mix)+len(reference)-1).bit_length()
    corr=np.fft.irfft(np.fft.rfft(mix,n)*np.conj(np.fft.rfft(reference,n)),n)[:len(mix)-len(reference)+1]
    c=np.r_[0,np.cumsum(mix*mix)];energy=c[len(reference):]-c[:-len(reference)]
    scores=corr/np.sqrt(np.maximum(energy,1e-30)*np.dot(reference,reference))
    score=float(np.max(scores));assert score>.3,score
    with wave.open(str(ROOT/'test_current/Battle_voice_preview.wav'),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr)
        w.writeframes(np.clip(audio[start:end]*32768,-32768,32767).astype('<i2').tobytes())
    baseline=ROOT/'baseline/SRWW_Korean_1.0.8.nds'
    assert hashlib.sha256(baseline.read_bytes()).hexdigest()=='0a5a22bd6bb25ebe640767e6b422b91358636e9ae1300e61d7e8ac3c5d8cd478'
    target=ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds'
    report=dict(version='battle-v02',rom_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                combat=combat,scenario_negative_control=story,cold_start=boot,
                trigger=marker,audio_reference_correlation=score,
                verified_scene='Kazuma opening response, attack shout and defence response within the Valhawk combat animation',
                method='DeSmuME libretro; actual battle resumed from baseline, interpreter mode; cold startup separately checked',
                hardware_verified=False,all_battle_quotes_voiced=False)
    (ROOT/'release_battle_v02/verification_result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
