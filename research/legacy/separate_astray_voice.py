"""Separate real recorded speech/vocals from an Astray excerpt with HDemucs."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import json,subprocess,sys,time
import numpy as np
import soundfile as sf
import torch
from torchaudio.pipelines import HDEMUCS_HIGH_MUSDB_PLUS

ROOT=PROJECT_ROOT
OUT=ROOT/'research/legacy/astray_audio/separated';OUT.mkdir(exist_ok=True)
torch.set_num_threads(4)
torch.hub.set_dir(str(ROOT/'tools/torch_cache'))
start=float(sys.argv[1]) if len(sys.argv)>1 else 0
duration=float(sys.argv[2]) if len(sys.argv)>2 else 45
tag=sys.argv[3] if len(sys.argv)>3 else 'red_frame'
source=Path(sys.argv[4]).resolve() if len(sys.argv)>4 else ROOT/'research/legacy/astray_audio/astray_source.m4a'
source_url=sys.argv[5] if len(sys.argv)>5 else 'https://www.bilibili.com/video/BV1hW411M7Tm/'
ff=ROOT.parent/'.video-tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
original=OUT/f'{tag}_original.wav'
subprocess.run([str(ff),'-y','-v','error','-ss',str(start),'-i',str(source),'-t',str(duration),'-ar','44100','-ac','2','-c:a','pcm_f32le',str(original)],check=True)
x,sr=sf.read(original,dtype='float32',always_2d=True);mix=torch.from_numpy(x.T.copy())
print('Loading source-separation model',flush=True)
bundle=HDEMUCS_HIGH_MUSDB_PLUS;model=bundle.get_model().eval()
voice_idx=model.sources.index('vocals')
length=mix.shape[-1];step=6*sr;segment=8*sr
result=torch.zeros_like(mix);weights=torch.zeros(length)
window=torch.ones(segment);fade=2*sr
window[:fade]=torch.linspace(.001,1,fade);window[-fade:]=torch.linspace(1,.001,fade)
began=time.time()
with torch.inference_mode():
 for pos in range(0,length,step):
  count=min(segment,length-pos);part=mix[:,pos:pos+count]
  if count<segment:part=torch.nn.functional.pad(part,(0,segment-count))
  reference=part.mean(0);mean=reference.mean();std=reference.std().clamp_min(1e-5)
  stems=model(((part-mean)/std)[None])[0]
  v=stems[voice_idx]*std+mean
  w=window[:count]
  if pos==0:w=w.clone();w[:fade]=1
  if pos+count==length:w=w.clone();w[-min(fade,count):]=1
  result[:,pos:pos+count]+=v[:,:count]*w
  weights[pos:pos+count]+=w
  print(f'Separated {min(pos+segment,length)/sr:.1f}/{length/sr:.1f}s ({time.time()-began:.1f}s elapsed)',flush=True)
result/=weights.clamp_min(1e-6)
peak=float(result.abs().max());gain=min(1,.98/max(peak,1e-6))
voice=OUT/f'{tag}_voice.wav';background=OUT/f'{tag}_background.wav'
sf.write(voice,(result*gain).T.numpy(),sr,subtype='PCM_16')
sf.write(background,(mix-result).T.numpy(),sr,subtype='PCM_16')
sf.write(original,x,sr,subtype='PCM_16')
report=dict(source=source_url,start_seconds=start,duration_seconds=length/sr,model='torchaudio HDEMUCS_HIGH_MUSDB_PLUS',device='CPU',source_separated=True,voice_is_synthesized=False,voice_track_may_include_singing_or_sound_effects=True,voice_file=str(voice),original_file=str(original),background_file=str(background),gain=gain)
(OUT/f'{tag}_manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('DONE',flush=True)
