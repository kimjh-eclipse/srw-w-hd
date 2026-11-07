"""W resource archive and tiled image readers.

ECD framing reference: Kuriimu LZECD.cs (IcySon55/Kuriimu).
The sliding dictionary is reconstructed independently here for W.
"""
from pathlib import Path
import struct,bisect
from functools import lru_cache
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent
BASE=0x2cb000

def archive(rom):
    n=struct.unpack_from('<I',rom,BASE)[0]//4
    return list(struct.unpack_from(f'<{n}I',rom,BASE))

def decompress(data):
    if data[:4]!=b'ECD\x01':return data
    init,packed,size=struct.unpack_from('>III',data,4)
    out=bytearray(data[16:16+init]);ring=bytearray(1024);p=16+init
    while len(out)<size:
        flags=data[p];p+=1
        for bit in range(8):
            if flags&(1<<bit):
                value=data[p];p+=1
                ring[len(out)&1023]=value;out.append(value)
            else:
                a,b=data[p:p+2];p+=2
                pos=(a+((b>>6)<<8)+74)&1023
                for k in range((b&63)+3):
                    value=ring[(pos+k)&1023]
                    ring[len(out)&1023]=value;out.append(value)
            if len(out)>=size:break
    if len(out)!=size:raise ValueError((len(out),size))
    return bytes(out)

def pixels(data):
    assert data[:3]==b'IMG'
    wt,ht=struct.unpack_from('<HH',data,4);bpp=8 if data[3] else 4
    a=np.frombuffer(data[8:],dtype=np.uint8)
    if bpp==4:
        a=np.stack([a&15,a>>4],1).reshape(-1)
    expected=wt*ht*64
    assert len(a)>=expected,(len(a),expected)
    return a[:expected].reshape(ht,wt,8,8).transpose(0,2,1,3).reshape(ht*8,wt*8).copy()

def palette(data):
    assert data[:4]==b'PLT\0'
    count=struct.unpack_from('<I',data,4)[0]
    values=struct.unpack_from(f'<{count}H',data,8)
    return [(int(v&31)*255//31,int((v>>5)&31)*255//31,int((v>>10)&31)*255//31,255) for v in values]

@lru_cache(maxsize=128)
def compress(raw):
    """Encode W's 1 KiB LZSS dictionary, independently checked by game code."""
    init=8;body=raw[init:];stream=bytearray()
    lengths=[0]*len(body);distances=[0]*len(body)
    for p in range(len(body)):
        limit=min(66,len(body)-p);best=0;distance=0
        if limit>=3:
            begin=max(0,p-1024);end=p
            if p+132<=1024 and body[p:p+3]==b'\0\0\0':
                best=3;distance=958
                while best<limit and body[p+best]==0:best+=1
            for _ in range(64):
                at=body.rfind(body[p:p+3],begin,end)
                if at<0:break
                dist=p-at;n=3
                while n<limit and body[p+n]==body[p+n-dist]:n+=1
                if n>best:best=n;distance=dist
                if best==limit:break
                end=at
        lengths[p]=best;distances[p]=distance
    cost=[0]*(len(body)+1);steps=[1]*len(body)
    for p in range(len(body)-1,-1,-1):
        cost[p]=9+cost[p+1]
        for n in range(3,lengths[p]+1):
            value=17+cost[p+n]
            if value<cost[p]:cost[p]=value;steps[p]=n
    p=0
    while p<len(body):
        flag_at=len(stream);stream.append(0);flags=0
        for bit in range(8):
            if p>=len(body):break
            best=steps[p];distance=distances[p]
            if best>=3:
                pos=(958+p-distance)&1023
                stream.extend((pos&255,((pos>>8)<<6)|(best-3)));p+=best
            else:
                flags|=1<<bit;stream.append(body[p]);p+=1
        stream[flag_at]=flags
    out=b'ECD\1'+struct.pack('>III',init,init+len(stream),len(raw))+raw[:init]+stream
    assert decompress(out)==raw
    return out

def main():
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=archive(rom)
    ram=(ROOT/'battle_animation_trace2/ram_65340.bin').read_bytes()
    found=[];p=0x280000
    while True:
        p=ram.find(b'IMG\0',p)
        if p<0:break
        if ram[p-16:p-12]==b'ECD\1':
            signature=ram[p-16:p+64];at=rom.find(signature,BASE)
            if at>=0:
                i=bisect.bisect_right(offsets,at-BASE)-1
                found.append((hex(p+0x2000000),i))
        p+=4
    print('loaded image resources',found)
    output=ROOT/'test_current/graphics';output.mkdir(parents=True,exist_ok=True)
    candidates=[]
    for i in range(len(offsets)-1):
        d=rom[BASE+offsets[i]:BASE+offsets[i+1]]
        if d[:4]==b'ECD\1' and d[16:20]==b'IMG\0' and int.from_bytes(d[12:16],'big')>=24000:
            raw=decompress(d);a=pixels(raw)
            im=Image.fromarray((a*17).astype('uint8')).convert('RGB');im.thumbnail((192,192))
            candidates.append((i,im))
    from PIL import ImageDraw
    sheet=Image.new('RGB',(192*8,214*((len(candidates)+7)//8)),(30,30,30))
    for k,(i,im) in enumerate(candidates):
        x=k%8*192;y=k//8*214;sheet.paste(im,(x,y));ImageDraw.Draw(sheet).text((x+4,y+194),str(i),fill='white')
    sheet.save(output/'resource_sheet.png');print('candidates',len(candidates))

if __name__=='__main__':main()
