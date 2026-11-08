"""Inspect W's add02 dialogue/codebook pairs, preserving binary offsets.

Format reference: https://github.com/snake759494/NDS-SRW-K
This is an exploratory reader; unknown dictionary codes remain explicit.
"""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import struct,json
ROOT=PROJECT_ROOT
def u32(b,o):return struct.unpack_from('<I',b,o)[0]
hangul=[]
for lead in range(0xb0,0xc9):
 for trail in range(0xa1,0xff):
  try:c=bytes([lead,trail]).decode('euc-kr')
  except UnicodeDecodeError:continue
  if len(c)==1 and 0xac00<=ord(c)<=0xd7a3:hangul.append(c)
slots=[]
for lead in range(0x88,0x99):
 for trail in range(0x40,0xfd):
  code=lead*256+trail
  if code>=0x889f and trail!=0x7f:slots.append(code)
mapping=dict(zip(slots,hangul))
def char(code):
 if code in mapping:return mapping[code]
 return code.to_bytes(2,'big').decode('cp932','replace')
def decode(block,cb,chunk):
 t=cb[0x11];start=u32(cb,0x14);idiom=u32(cb,0x18)
 p=u32(block,0);end=u32(block,p-4)
 result=[]
 while p<min(end,len(block)):
  node=p;c1=struct.unpack_from('<H',block,p)[0];c2=0;p+=2;name=''
  v=c1
  for m in (0xa000,0x8000,0x3000,0x2000,0x1000):v%=m
  if False:
   stop=block.index(0,p);name=''.join(char(int.from_bytes(block[a:a+2],'big')) for a in range(p,stop-1,2));p=stop+1
  lines=[]
  while p<end:
   length=block[p];p+=1;stop=p+(length&127);line=''
   while p<stop:
    b=block[p];p+=1
    if b>=t:
     b2=block[p];p+=1;value=(b<<8)|b2;idx=t+(b-t)*256+b2
    else:value=b;idx=b
    if value>=idiom:line+=f'<DICT:{value:04X}>'
    else:line+=char(int.from_bytes(cb[start+idx*2:start+idx*2+2],'big'))
   lines.append(line)
   if length>128:break
  result.append(dict(chunk=chunk,offset=node,code1=c1,code2=c2,name=name,lines=lines,raw=block[node:p].hex()))
 return result
def main():
 d=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();base=0x30b7000;size=2719653
 n=u32(d,base)//4;offs=list(struct.unpack_from(f'<{n}I',d,base))+[size]
 rows=[];errors=[]
 for i in range(n-2):
  cb=d[base+offs[i+1]:base+offs[i+2]]
  if len(cb)<0x30 or cb[0x11] not in (0xfa,0xfb,0xfc,0xfd):continue
  block=d[base+offs[i]:base+offs[i+1]]
  try:rows+=decode(block,cb,i)
  except Exception as e:errors.append((i,str(e)))
 out=ROOT/'research/legacy/analysis';out.mkdir(exist_ok=True)
 (out/'dialogue.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 (out/'dialogue.txt').write_text('\n'.join(f"{r['chunk']}:{r['offset']:04x} {r['code1']:04x}/{r['code2']:04x} {r['name']} {' / '.join(r['lines'])}" for r in rows),encoding='utf-8')
 print('decoded',len(rows),'errors',errors[:15]);print(json.dumps(rows[:4],ensure_ascii=False,indent=2))
if __name__=='__main__':main()
