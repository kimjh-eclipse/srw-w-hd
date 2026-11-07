"""Exact face lookup; cold HD preparation never blocks the game frame."""
import json,zlib,weakref,sys,sqlite3
from contextlib import closing
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parent.parent
@lru_cache(maxsize=1)
def _catalog(stamp):
    return tuple(json.loads((ROOT/'graphics/portraits/library.json').read_text())['portraits'])
@lru_cache(maxsize=1)
def _reference_library(stamp):
    with np.load(ROOT/'graphics/portraits/native_reference.npz') as archive:
        paths=archive['paths'];rgba=archive['rgba']
    area=Image.new('L',(56,48));ImageDraw.Draw(area).polygon([(4,1),(48,1),(52,5),(52,47),(4,47)],fill=255);area=np.asarray(area)>0
    table={}
    for path,original in zip(paths,rgba):
        mask=(original[:,:,3]>0)&area;expected=(original[:,:,:3]>>3)[mask]
        mask.flags.writeable=False;expected.flags.writeable=False;table[str(path)]=(mask,expected)
    return table
def _background_priority():
    if sys.platform=='win32':
        import ctypes as C
        api=C.windll.kernel32;api.GetCurrentThread.restype=C.c_void_p;api.SetThreadPriority.argtypes=[C.c_void_p,C.c_int]
        api.SetThreadPriority(api.GetCurrentThread(),-1)
def _prepare_art_from_source(item):
    x,y,w,h=item['rectangle']
    with Image.open(ROOT/'graphics'/item['path']) as source:
        art=source.convert('RGBA').resize((round(w*1440/256),round(h*1080/192)),Image.Resampling.LANCZOS)
    mask=Image.new('L',(w,h));ImageDraw.Draw(mask).polygon([(4,1),(48,1),(52,5),(52,47),(4,47)],fill=255)
    if item.get('portrait_mask'):
        with Image.open(ROOT/'graphics'/item['portrait_mask']) as original:
            mask=ImageChops.multiply(mask,original.convert('RGBA').getchannel('A'))
    art.putalpha(ImageChops.multiply(art.getchannel('A'),mask.resize(art.size,Image.Resampling.BICUBIC)))
    return art
def _asset_stamp(item):
    parts=['portrait-registration-1']
    for key in ('path','portrait_mask'):
        if not item.get(key):continue
        source=(ROOT/'graphics'/item[key]).stat();parts.extend((str(source.st_mtime_ns),str(source.st_size)))
    return ':'.join(parts)
def _prepare_art(item):
    cache=ROOT/'graphics/portraits/prepared.sqlite'
    if cache.exists():
        try:
            with closing(sqlite3.connect('file:'+cache.as_posix()+'?mode=ro',uri=True,timeout=.05)) as database:
                row=database.execute('SELECT stamp,w,h,pixels FROM art WHERE path=?',(item['path'],)).fetchone()
            if row is not None and row[0]==_asset_stamp(item):return Image.frombytes('RGBA',(row[1],row[2]),zlib.decompress(row[3]))
        except (OSError,ValueError,sqlite3.Error,zlib.error):pass
    return _prepare_art_from_source(item)
class PortraitRenderer:
    def __init__(self,async_prepare=True):
        path=ROOT/'graphics/portraits/library.json';self.items=[];self.groups={};self.cache=OrderedDict();self.references=OrderedDict();self.last_match=None;self.last_rectangle=None;self.fastmatch=None;self.fastmatches=[];self.position_cache={};self.scan_stamp=None;self.last_matches=[];self.last_rectangles=[]
        self.pending={};self.prepare_errors={};self.executor=ThreadPoolExecutor(max_workers=1,thread_name_prefix='portrait-HD',initializer=_background_priority) if async_prepare else None
        # Collection or process shutdown owns the executor; callers need no new
        # close hook. Jobs use a module function, so they cannot retain self.
        if self.executor is not None:weakref.finalize(self,self.executor.shutdown,wait=False,cancel_futures=True)
        self.positions=(136,0,24)+tuple(y for y in range(8,145,8) if y not in (24,136))
        if not path.exists():return
        packed=ROOT/'graphics/portraits/native_reference.npz'
        self.reference_library=_reference_library(packed.stat().st_mtime_ns) if packed.exists() else {}
        for item in _catalog(path.stat().st_mtime_ns):
            self.items.append(item)
            fmt=item.get('match_format','rgb5');key=item.get('content_crc32',item['crc32'])
            self.groups.setdefault(fmt,{}).setdefault(key,[]).append(item)
            if not item.get('archive_img'):self._art(item)
    def collect_prepared(self):
        for key,future in list(self.pending.items()):
            if not future.done():continue
            del self.pending[key]
            try:self.cache[key]=future.result()
            except Exception as error:self.prepare_errors[key]=str(error)
        while len(self.cache)>32:self.cache.popitem(last=False)
    def _art(self,item):
        key=item['path'];self.collect_prepared();art=self.cache.pop(key,None)
        if art is not None:self.cache[key]=art;return art
        if self.executor is not None:
            if key not in self.pending and key not in self.prepare_errors and len(self.pending)<16:
                self.pending[key]=self.executor.submit(_prepare_art,item)
            return None
        art=_prepare_art(item);self.cache[key]=art
        while len(self.cache)>32:self.cache.popitem(last=False)
        return art
    def _matches_reference(self,item,native,x,y):
        path=item.get('portrait_mask')
        if path is None:return True
        reference=self.references.pop(path,None)
        if reference is None:reference=self.reference_library.get(path)
        if reference is None:
            with Image.open(ROOT/'graphics'/path) as source:rgba=np.asarray(source.convert('RGBA')).copy()
            area=Image.new('L',(56,48));ImageDraw.Draw(area).polygon([(4,1),(48,1),(52,5),(52,47),(4,47)],fill=255)
            mask=(rgba[:,:,3]>0)&(np.asarray(area)>0);reference=(mask,(rgba[:,:,:3]>>3)[mask])
        self.references[path]=reference
        while len(self.references)>64:self.references.popitem(last=False)
        mask,expected=reference
        return np.array_equal((native[y:y+48,x:x+56]>>3)[mask],expected)
    def _paint(self,item,top,x,y,w,h):
        art=self._art(item)
        if art is None:return False
        wanted=(round(w*top.width/256),round(h*top.height/192))
        if art.size!=wanted:
            if not hasattr(self,'scaled_art'):self.scaled_art=OrderedDict()
            key=(item['path'],wanted);scaled=self.scaled_art.pop(key,None)
            if scaled is None:scaled=art.resize(wanted,Image.Resampling.LANCZOS)
            self.scaled_art[key]=scaled
            while len(self.scaled_art)>32:self.scaled_art.popitem(last=False)
            art=scaled
        top.paste(art,(round(x*top.width/256),round(y*top.height/192)),art)
        self.last_matches.append(item['name']);self.last_rectangles.append((x,y,w,h))
        # Preserve the original single-face inspection fields for callers.
        if self.last_match is None:self.last_match=item['name'];self.last_rectangle=(x,y,w,h)
        return True
    def compose(self,top,native):
        self.last_match=None;self.last_rectangle=None;self.last_matches=[];self.last_rectangles=[]
        self.collect_prepared()
        # Cache the complete searched strip, including previously empty areas.
        # Rechecking only a found face would miss a changed or newly shown face
        # elsewhere on the same screen.
        scan_stamp=zlib.crc32(native[:192,:56].copy().tobytes())
        if scan_stamp!=self.scan_stamp:
            matches=[];occupied=[]
            for y in self.positions:
                # y0 and y24 can describe overlapping panels; an accepted face
                # owns its whole rectangle and cannot be painted a second time.
                if any(y<other+48 and other<y+48 for other in occupied):continue
                panel=native[y:y+48,:56];stamp=zlib.crc32(panel.copy().tobytes())
                cached=self.position_cache.get(y)
                if cached is not None and cached[0]==stamp:item=cached[1]
                else:
                    item=None;pixels=native[y+2:y+46,5:48]
                    for fmt,entries in self.groups.items():
                        sample=pixels>>3 if fmt=='rgb5' else pixels
                        key=zlib.crc32(sample.copy().tobytes());candidates=entries.get(key,())
                        item=next((p for p in candidates if self._matches_reference(p,native,p['rectangle'][0],y)),None)
                        if item is not None:break
                    self.position_cache[y]=(stamp,item)
                if item is None:continue
                x,_,w,h=item['rectangle'];matches.append((item,x,y,w,h,stamp));occupied.append(y)
            self.fastmatches=matches;self.fastmatch=matches[0] if matches else None;self.scan_stamp=scan_stamp
        painted=False
        for item,x,y,w,h,stamp in self.fastmatches:
            painted=self._paint(item,top,x,y,w,h) or painted
        return painted
