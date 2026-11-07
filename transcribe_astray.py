from pathlib import Path
import sys,json,subprocess,numpy as np
from faster_whisper import WhisperModel
root=Path(__file__).resolve().parent
path=Path(sys.argv[1]) if len(sys.argv)>1 else root/'astray_audio/astray_source.m4a'
out=Path(sys.argv[2]) if len(sys.argv)>2 else root/'astray_audio/transcript.json'
model=WhisperModel(r'D:\AI\Qwen3-TTS\tools\whisper-small',device='cpu',compute_type='int8',cpu_threads=4)
ff=root.parent/'.video-tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
start=float(sys.argv[3]) if len(sys.argv)>3 else 0
duration=float(sys.argv[4]) if len(sys.argv)>4 else 150
pcm=subprocess.check_output([str(ff),'-v','error','-ss',str(start),'-i',str(path),'-t',str(duration),'-f','f32le','-ar','16000','-ac','1','pipe:1'])
segments,info=model.transcribe(np.frombuffer(pcm,dtype='<f4'),language='ja',beam_size=3,vad_filter=True)
rows=[]
for s in segments:
 row=dict(start=s.start+start,end=s.end+start,text=s.text);rows.append(row)
 print(json.dumps(row,ensure_ascii=True),flush=True)
 out.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
