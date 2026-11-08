"""Independent exact rolling-row-bit scanner experiment; no production edits."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,time,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
from hd_fonts import FontRenderer,ROOT
from native_font_scan import NativeFontScanner

class RowBitScanner:
    def __init__(self):self.tables={};self.key_refs={}
    @staticmethod
    def rowbits(mask,width):
        cols=mask.shape[1]-width+1
        rows=np.zeros((mask.shape[0],cols),dtype=np.uint16)
        for bit in range(width):rows|=mask[:,bit:bit+cols].astype(np.uint16)<<(width-1-bit)
        return rows
    def scan(self,mask,height,width,keys,characters,minimum=1,maximum=144):
        if mask.shape[0]<height or mask.shape[1]<width:return []
        identity=(height,width,id(keys))
        if identity not in self.tables:
            self.key_refs[id(keys)]=keys
            weights=np.array([pow(65599,i,1<<64) for i in range(height)],dtype=np.uint64)
            patterns=np.unpackbits(keys.view(np.uint8).reshape(len(keys),-1),axis=1)[:,:height*width].reshape(-1,height,width).astype(bool)
            rowvalues=(patterns.astype(np.uint16)*(1<<np.arange(width-1,-1,-1,dtype=np.uint16))).sum(2).astype(np.uint64)
            hashes=(rowvalues*weights).sum(1,dtype=np.uint64)
            order=np.argsort(hashes);bloom=np.zeros(65536,dtype=bool);bloom[(hashes&65535).astype(np.intp)]=True
            self.tables[identity]=(weights,patterns,hashes[order],order,patterns.sum((1,2)),bloom)
        weights,patterns,table,order,counts,bloom=self.tables[identity]
        rows=self.rowbits(mask,width).astype(np.uint64);out_h=mask.shape[0]-height+1
        hashes=np.zeros((out_h,rows.shape[1]),dtype=np.uint64)
        scratch=np.empty_like(hashes)
        for i in range(height):
            np.multiply(rows[i:i+out_h],weights[i],out=scratch);np.add(hashes,scratch,out=hashes)
        ys,xs=np.where(bloom[(hashes&65535).astype(np.intp)])
        values=hashes[ys,xs];lo=np.searchsorted(table,values)
        valid=lo<len(table);valid[valid]&=table[lo[valid]]==values[valid]
        result=[]
        for y,x,slot_start in zip(ys[valid],xs[valid],lo[valid]):
            end=np.searchsorted(table,hashes[y,x],side='right')
            for slot in range(slot_start,end):
                i=order[slot]
                if minimum<=counts[i]<=maximum and np.array_equal(mask[y:y+height,x:x+width],patterns[i]):
                    result.append((int(x),int(y),characters[i],width,height,mask[y:y+height,x:x+width].copy()))
        return result

def signature(found):
    return [(x,y,ch,w,h,np.packbits(ink).tobytes()) for x,y,ch,w,h,ink in found]

def main():
    font=FontRenderer();scanner=RowBitScanner();native_scanner=NativeFontScanner();cases=[]
    for n in (0,1,3,4):
        source=np.asarray(Image.open(ROOT/f'test_current/font/scene_{n}.png').convert('RGB'))
        for screen in (0,1):
            p=source[screen*192:(screen+1)*192];low=p.min(2);high=p.max(2)
            for threshold in (80,232):cases.append((f'scene{n}_{screen}_{threshold}',(low>=threshold)&(high.astype('int16')-low<32)))
    rng=np.random.default_rng(16)
    cases += [('blank',np.zeros((192,256),bool)),('solid',np.ones((192,256),bool))]
    cases += [(f'random{n}',rng.random((192,256))<p) for n,p in enumerate((.01,.1,.5,.9))]
    tables=[(12,12,font.keys,font.characters,5,100),(12,8,font.narrow_keys,font.narrow_characters,1,80),(8,8,font.compact_keys,font.compact_characters,5,60)]
    timings={'original':[],'row_bits':[],'native_c':[]};native_timings={k:[] for k in timings};total=0
    for name,mask in cases:
        for args in tables:
            original=getattr(FontRenderer,'_scan_numpy',FontRenderer._scan)
            old=original(mask,*args);new=scanner.scan(mask,*args)
            assert signature(old)==signature(new),(name,args[:2],len(old),len(new))
            assert signature(old)==signature(native_scanner.scan(mask,*args)),('C native',name,args[:2])
            total+=len(old)
            for mode,fn in [('original',original),('row_bits',scanner.scan),('native_c',native_scanner.scan)]:
                samples=[]
                for _ in range(3):
                    start=time.perf_counter();fn(mask,*args);samples.append((time.perf_counter()-start)*1000)
                timings[mode].append(float(np.median(samples)))
                if name.startswith('scene'):native_timings[mode].append(float(np.median(samples)))
    # Every registered glyph is tested at an arbitrary non-grid alignment.
    glyphs=0
    for h,w,keys,chars,minimum,maximum in tables:
        patterns=np.unpackbits(keys.view(np.uint8).reshape(len(keys),-1),axis=1)[:,:h*w].reshape(-1,h,w).astype(bool)
        for start in range(0,len(keys),160):
            batch=patterns[start:start+160];mask=np.zeros((192,256),bool)
            for i,p in enumerate(batch):
                y=1+(i//16)*(h+2);x=3+(i%16)*(w+2);mask[y:y+h,x:x+w]=p
            expected=signature(original(mask,h,w,keys,chars,minimum,maximum))
            assert expected==signature(scanner.scan(mask,h,w,keys,chars,minimum,maximum))
            assert expected==signature(native_scanner.scan(mask,h,w,keys,chars,minimum,maximum))
            glyphs+=len(batch)
    # Exercise the production wrapper's graceful NumPy fallback as well.
    import hd_fonts
    old_scanner=getattr(hd_fonts._native_scanners,'instance',None)
    class BrokenScanner:
        closed=False
        def scan(self,*args):raise RuntimeError('simulated scanner failure')
        def close(self):self.closed=True
    broken=BrokenScanner();hd_fonts._native_scanners.instance=broken
    try:
        h,w,keys,chars,minimum,maximum=tables[0];mask=cases[0][1]
        assert signature(FontRenderer._scan(mask,h,w,keys,chars,minimum,maximum))==signature(original(mask,h,w,keys,chars,minimum,maximum))
        assert broken.closed and hd_fonts._native_scanners.instance is False
    finally:hd_fonts._native_scanners.instance=old_scanner
    report={'exact_order_ink_and_char_equivalence_cases':len(cases)*3,'native_match_count':total,'registered_glyphs_equivalent':glyphs,
        'scan_mean_ms':{k:round(float(np.mean(v)),3) for k,v in timings.items()},
        'speedup':round(float(np.mean(timings['original'])/np.mean(timings['row_bits'])),2),
        'native_only_scan_mean_ms':{k:round(float(np.mean(v)),3) for k,v in native_timings.items()},
        'native_only_speedup':round(float(np.mean(native_timings['original'])/np.mean(native_timings['row_bits'])),2),
        'native_c_speedup':round(float(np.mean(timings['original'])/np.mean(timings['native_c'])),2),
        'native_c_real_screen_speedup':round(float(np.mean(native_timings['original'])/np.mean(native_timings['native_c'])),2),
        'production_numpy_fallback_verified':True,
        'allocation':'row uint16 plane and uint64 hash plane; no N x glyph-area copy. Exact bitmap verification after hash lookup.'}
    path=ROOT/'test_current/font/ui_scan_bits_benchmark.json';path.write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))

if __name__=='__main__':main()
