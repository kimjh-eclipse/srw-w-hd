"""Reassemble unknown hardware rectangles from exact, coherent painted tiles."""
import json,zlib,sqlite3,base64,hashlib
from pathlib import Path
from collections import OrderedDict,Counter
import numpy as np
from PIL import Image
from palette_materials import material_indices
from hd_parts_registration import register_part
from tile_group_paint import complete_origins,paint_group
from asset_paths import asset_root
ROOT=asset_root(Path(__file__).resolve().parent.parent)

class TileCompositor:
    def __init__(self):
        path=ROOT/'graphics/parts_tile_library.sqlite'
        self.db=sqlite3.connect(path.as_uri()+'?mode=ro',uri=True)
        self.stamp=self.db.execute("SELECT value FROM metadata WHERE key='stamp'").fetchone()[0]
        self.stamp+=hashlib.sha256(Path(__file__).read_bytes()+Path(__file__).with_name('tile_group_paint.py').read_bytes()).hexdigest()
        self.sources=OrderedDict();self.images=OrderedDict();self.candidates=OrderedDict();self.luts={}

    def source(self,identifier):
        result=self.sources.pop(identifier,None)
        if result is None:
            text,blob=self.db.execute('SELECT description,indices FROM sources WHERE id=?',(identifier,)).fetchone();s=json.loads(text)
            if len(s['palette'])<16:s['palette']+= [s['palette'][-1]]*(16-len(s['palette']))
            a=np.frombuffer(zlib.decompress(blob),dtype='uint8').reshape(s['h'],s['w']);result=s,a
        self.sources[identifier]=result
        while len(self.sources)>64:self.sources.popitem(last=False)
        return result

    def image(self,name):
        image=self.images.pop(name,None)
        if image is None:
            with Image.open(ROOT/'graphics'/name) as opened:image=opened.convert('RGBA')
        self.images[name]=image
        while len(self.images)>4:self.images.popitem(last=False)
        return image

    def find(self,raw):
        result=self.candidates.pop(raw,None)
        if result is None:
            result=[(s,x,y) for s,x,y,p in self.db.execute('SELECT source,x,y,pixels FROM tiles WHERE key=? LIMIT 256',(zlib.crc32(raw),)) if p==raw]
        self.candidates[raw]=result
        while len(self.candidates)>4096:self.candidates.popitem(last=False)
        return result

    def recolor(self,art,tile,source_palette,target_palette):
        source=np.asarray(source_palette,dtype='float32')[:16];target=np.asarray(target_palette,dtype='float32');used=np.unique(tile[tile!=0])
        if not len(used) or np.array_equal(source[used],target[used]):return art
        pixels=np.array(art);rgb=pixels[:,:,:3].astype('float32')
        if len(np.unique(target[used],axis=0))==1:
            pixels[:,:,:3]=target[used[0]].astype('uint8');return Image.fromarray(pixels)
        key=source.tobytes()
        if key not in self.luts:
            c=np.arange(32768,dtype='uint32');colors=np.stack([(c&31)*255/31,((c>>5)&31)*255/31,((c>>10)&31)*255/31],-1).astype('float32')
            self.luts[key]=(np.argmin(((colors[:,None,:]-source[None,1:,:])**2).sum(-1),axis=1)+1).astype('uint8')
        q=np.rint(rgb*31/255).astype('uint32');indices=self.luts[key][q[:,:,0]|q[:,:,1]<<5|q[:,:,2]<<10]
        encoded=base64.b64encode(zlib.compress(tile.tobytes())).decode('ascii');indices=material_indices(encoded,tile.shape[1],tile.shape[0],art.size,indices,source)
        src=source@np.array([.2126,.7152,.0722]);dst=target@np.array([.2126,.7152,.0722]);gain=dst[used].sum()/max(1,src[used].sum());detail=np.minimum((dst+1)/(src+1),gain*1.5).clip(0,2)
        pixels[:,:,:3]=np.clip(np.rint(target[indices]+(rgb-source[indices])*detail[indices,None]),0,255).astype('uint8')
        return Image.fromarray(pixels)

    def assemble(self,indices,palette):
        h,w=indices.shape;target=np.asarray(palette,dtype='uint32');target_rgb=np.stack([(target&31)*255//31,((target>>5)&31)*255//31,((target>>10)&31)*255//31],-1)
        tiles=[];votes=Counter();missing=[]
        for y in range(0,h,8):
            for x in range(0,w,8):
                tile=indices[y:y+8,x:x+8]
                if not tile.any():continue
                raw=tile.tobytes();candidates=self.find(raw);complexity=len(np.unique(tile));tiles.append((x,y,tile))
                if not candidates:missing.append(zlib.crc32(raw));continue
                for source,sx,sy in candidates:votes[(source,sx-x,sy-y)]+=max(1,complexity-1)**2
        if missing:return None,dict(reason='unpainted native tile',missing_tiles=sorted(set(missing)))
        uncovered=set(range(len(tiles)));origins=complete_origins(tiles,votes,self.find)
        canvas=Image.new('RGBA',(w*8,h*8));groups=[]
        while uncovered and len(groups)<16:
            best=None
            for (identifier,ox,oy),vote in origins:
                s,a=self.source(identifier);matches=[]
                for n in uncovered:
                    x,y,tile=tiles[n];sx,sy=ox+x,oy+y
                    if 0<=sx<=s['w']-8 and 0<=sy<=s['h']-8 and np.array_equal(a[sy:sy+8,sx:sx+8],tile):matches.append(n)
                score=sum(np.count_nonzero(tiles[n][2]) for n in matches)
                if score and (best is None or (score,s['priority'],vote)>best[0]):best=((score,s['priority'],vote),identifier,ox,oy,matches)
            if best is None:break
            _,identifier,ox,oy,matches=best;s,a=self.source(identifier)
            paint_group(self,canvas,s,a,self.image(s['image']),indices,target_rgb,ox,oy,matches,tiles)
            uncovered.difference_update(matches);groups.append(dict(source=identifier,tiles=len(matches)))
        if uncovered:return None,dict(reason='incomplete coherent assembly',uncovered=len(uncovered))
        native=Image.fromarray(np.dstack([target_rgb[indices].astype('uint8'),(indices!=0).astype('uint8')*255]))
        if all(self.source(group['source'])[0].get('preserve_contour') for group in groups):
            from painted_edges import clean_alpha
            art=clean_alpha(canvas);stats=dict(dx=0,dy=0,zoom=1,offline_registered=True,reference_fill_pixels=0,filled_edge_pixels=0)
        else:art,stats=register_part(canvas,native)
        stats['tile_groups']=groups;stats['exact_tiles']=len(tiles)
        return art,stats
