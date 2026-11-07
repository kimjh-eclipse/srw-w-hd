"""Verify emulator telemetry and locate the source voice in the captured mix."""
from pathlib import Path
import hashlib,json,struct,sys,wave
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'reference_bgm'))
import strm_codec

def main():
    folder=ROOT/(sys.argv[1] if len(sys.argv)>1 else 'kazuma_cold_final')
    marker=json.loads((folder/'voice_trigger.json').read_text())
    symbols=json.loads((ROOT/'voice_probe_symbols.json').read_text())
    ram=(folder/'main_ram.bin').read_bytes()
    telemetry={k:struct.unpack_from('<I',ram,a-0x2000000)[0] for k,a in symbols.items()}
    assert telemetry['voice_match_count']==1
    assert telemetry['playing']==0
    assert telemetry['stream_underruns']==0
    blob=(ROOT/'voice_engine/hero_streams/0.strm').read_bytes()
    reference=np.concatenate([np.array(strm_codec.decode_adpcm_block(blob[p:p+196],384)) for p in range(104,len(blob),196)])/32768
    # DS timer 759 plays at ~22078 Hz; account for that hardware rate.
    rate=16756991/759
    reference=np.interp(np.arange(int(len(reference)*22050/rate))*rate/22050,np.arange(len(reference)),reference)
    with wave.open(str(folder/'emulator_audio.wav'),'rb') as w:
        sr=w.getframerate();audio=np.frombuffer(w.readframes(w.getnframes()),'<i2').reshape(-1,2).astype(float)/32768
    start=max(0,int((marker['seconds_from_run_start']-.5)*sr))
    end=min(len(audio),int((marker['seconds_from_run_start']+4.7)*sr))
    mix=audio[start:end].mean(1)[::2]
    n=1<<(len(mix)+len(reference)-1).bit_length()
    correlation=np.fft.irfft(np.fft.rfft(mix,n)*np.conj(np.fft.rfft(reference,n)),n)[:len(mix)-len(reference)+1]
    c=np.r_[0,np.cumsum(mix*mix)];energy=c[len(reference):]-c[:-len(reference)]
    scores=correlation/np.sqrt(np.maximum(energy,1e-30)*np.dot(reference,reference))
    peak=int(np.argmax(scores));score=float(scores[peak])
    assert score>.3, f'Voice not confidently located in audio: {score}'
    with wave.open(str(ROOT/'Kazuma_voice_preview.wav'),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr)
        w.writeframes(np.clip(audio[start:end]*32768,-32768,32767).astype('<i2').tobytes())
    source=ROOT/'baseline/SRWW_Korean_1.0.8.nds'
    assert hashlib.sha256(source.read_bytes()).hexdigest()=='0a5a22bd6bb25ebe640767e6b422b91358636e9ae1300e61d7e8ac3c5d8cd478'
    report=dict(telemetry=telemetry,trigger=marker,audio_reference_correlation=score,
                voice_start_in_preview_seconds=peak/22050,
                verification=('DeSmuME libretro; cold boot through new game and the original opening'
                              if 'cold' in folder.name else 'DeSmuME libretro; resumed scene, interpreter mode'),
                hardware_verified=False,all_dialogue_voiced=False)
    (ROOT/'verification_result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
