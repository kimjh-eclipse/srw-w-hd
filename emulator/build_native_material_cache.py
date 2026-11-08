"""Compile verified source material IDs for parts lacking index_pixels."""
import hashlib,json,sys,zlib
from collections import OrderedDict
import numpy as np
from hd_core import ROOT
sys.path.insert(0,str(ROOT))
import srw_graphics as graphics

def main():
    raw=(ROOT/'graphics/kazuma_parts_library.json').read_bytes();library=json.loads(raw)
    rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();offsets=graphics.archive(rom)
    images=OrderedDict();pieces=[];starts=[];lengths=[];position=0;verified=0
    for index,binding in enumerate(library['bindings'],1):
        starts.append(position);lengths.append(0)
        if not binding.get('dynamic_palette') or binding.get('index_pixels'):continue
        source=library['bindings'][binding.get('source_binding',index)-1]
        resource=source.get('resource')
        if resource is None:continue
        pixels=images.pop(resource,None)
        if pixels is None:
            packed=rom[graphics.BASE+offsets[resource]:graphics.BASE+offsets[resource+1]]
            try:pixels=graphics.pixels(graphics.decompress(packed))
            except (ValueError,IndexError):continue
        images[resource]=pixels
        while len(images)>8:images.popitem(last=False)
        x=source.get('source_x',source['x']);y=source.get('source_y',source['y']);w=binding['w'];h=binding['h']
        piece=np.ascontiguousarray(pixels[y:y+h,x:x+w],dtype='uint8')
        if piece.shape!=(h,w):continue
        encoded=np.where(piece,piece.astype('uint16')|0x8000,0).astype('<u2')
        if zlib.crc32(encoded.tobytes())^(w<<16)^h!=binding.get('index_hash'):continue
        pieces.append(piece.ravel());lengths[-1]=piece.size;position+=piece.size;verified+=1
    path=ROOT/'graphics/native_materials.npz'
    np.savez_compressed(path,starts=np.asarray(starts,dtype='int32'),lengths=np.asarray(lengths,dtype='int32'),pixels=np.concatenate(pieces))
    metadata=dict(library_sha256=hashlib.sha256(raw).hexdigest(),verified_bindings=verified,bytes=path.stat().st_size)
    (ROOT/'graphics/native_materials.json').write_text(json.dumps(metadata,indent=2));print(json.dumps(metadata))

if __name__=='__main__':main()
