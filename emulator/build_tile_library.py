"""Index exact ROM/observed 8x8 materials from existing AI-painted atlases."""
import sys,json,zlib,sqlite3,hashlib,time
from pathlib import Path
from functools import lru_cache
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import srw_graphics as g
ROOT=g.ROOT;OUT=ROOT/'graphics';TARGET=OUT/'parts_tile_library.sqlite'

def main():
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    @lru_cache(maxsize=256)
    def pixels(i):return g.pixels(g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]]))
    meta=json.loads((OUT/'kazuma_parts_library.json').read_text());sources=[];seen=set()
    def add(name,resource,image,native_size,x,y,a,pal,priority):
        if not (OUT/image).exists() or a.max()>15:return
        identity=(image,x,y,a.shape)
        if identity in seen:return
        seen.add(identity);sources.append(dict(name=name,resource=resource,image=image,native_size=native_size,x=x,y=y,w=a.shape[1],h=a.shape[0],palette=pal,priority=priority,indices=a))
    raw_path=ROOT/'test_current/robot/vram_65340.bin'
    if raw_path.exists():
        raw=np.frombuffer(raw_path.read_bytes()[:16384],dtype='uint8');a=np.stack([raw&15,raw>>4],-1).reshape(16,32,8,8).transpose(0,2,1,3).reshape(128,256)
        add('approved_base',-1,meta['atlas'],[256,128],0,0,a,meta['source_palette_rgb'],5)
    obs=OUT/'observed_parts/sheets.json'
    if obs.exists():
        for sheet in json.loads(obs.read_text())['sheets']:
            for s in sheet['segments']:
                r=s['source'];a=np.load(ROOT/f"test_current/attract/observed_parts/{r['hash']:08x}.npy")
                add(sheet['name'],-1,f"observed_parts/{sheet['name']}_hd.png",sheet['native_size'],s['x'],s['y'],a,r['palette_rgb'],4)
    effects=OUT/'observed_parts/effects/manifest.json'
    if effects.exists() and (effects.parent/'hd.png').exists():
        manifest=json.loads(effects.read_text())
        for item in manifest['items']:
            raw=np.load(effects.parent/item['native']);a=raw['indices']
            add('observed_effect',-1,'observed_parts/effects/hd.png',manifest['native_size'],item['x'],item['y'],a,item['palette_rgb'],4)
    packages={p['resource']:p for p in json.loads((OUT/'all_units/catalog.json').read_text())['packages']}
    for sheet in json.loads((OUT/'all_units/batches.json').read_text())['batches']:
        if not sheet.get('required'):continue
        for s in sheet['segments']:
            i=s['resource']
            if i==7406:continue
            add('all_'+sheet['name'],i,'all_units/'+sheet['image'],sheet['native_size'],0,s['batch_y'],pixels(i),packages[i]['palette_rgb'],3)
    for plan_name,priority in [('basic_extra_sheets.json',2),('late_attack_sheets.json',2),('full_attack_sheets.json',2),('shared_attack_sheets.json',1)]:
        path=OUT/'animation_parts'/plan_name
        if not path.exists():continue
        for sheet in json.loads(path.read_text())['sheets']:
            image='animation_parts/'+sheet['image']
            if not (OUT/image).exists():continue
            for s in sheet.get('segments',sheet.get('parts',[])):
                i=s.get('resource',s.get('image'));a=pixels(i)
                if 'atlas_x' in s:a=a[s['y']:s['y']+s['h'],s['x']:s['x']+s['w']];x,y=s['atlas_x'],s['atlas_y']
                else:x,y=s['x'],s['y']
                add(sheet['name'],i,image,sheet['native_size'],x,y,a,s['palette_rgb'],priority)
    sources.sort(key=lambda s:-s['priority']);temporary=TARGET.with_suffix('.tmp.sqlite')
    if temporary.exists():temporary.unlink()
    db=sqlite3.connect(temporary);db.execute('PRAGMA journal_mode=OFF');db.execute('PRAGMA synchronous=OFF')
    db.executescript('CREATE TABLE sources(id INTEGER PRIMARY KEY,description TEXT,indices BLOB);CREATE TABLE tiles(key INTEGER,source INTEGER,x INTEGER,y INTEGER,pixels BLOB);CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT);')
    count=0;stamp=hashlib.sha256();started=time.perf_counter()
    for identifier,s in enumerate(sources,1):
        a=s.pop('indices');description=json.dumps(s);stat=(OUT/s['image']).stat();stamp.update(description.encode());stamp.update(str((stat.st_mtime_ns,stat.st_size)).encode())
        db.execute('INSERT INTO sources VALUES(?,?,?)',(identifier,description,zlib.compress(a.tobytes(),1)));rows=[]
        for y in range(0,s['h']-7,8):
            for x in range(0,s['w']-7,8):
                tile=a[y:y+8,x:x+8]
                if not tile.any():continue
                raw=tile.tobytes();rows.append((zlib.crc32(raw),identifier,x,y,raw))
        db.executemany('INSERT INTO tiles VALUES(?,?,?,?,?)',rows);count+=len(rows)
        if identifier%200==0:print(identifier,len(sources),count,flush=True)
    db.execute('CREATE INDEX tile_keys ON tiles(key)')
    for key,value in dict(stamp=stamp.hexdigest(),sources=len(sources),tiles=count).items():db.execute('INSERT INTO metadata VALUES(?,?)',(key,str(value)))
    db.commit();db.close();temporary.replace(TARGET)
    report=dict(sources=len(sources),tiles=count,seconds=round(time.perf_counter()-started,2),all_source_sheets_generated=not any(not (OUT/'animation_parts'/s['image']).exists() for s in json.loads((OUT/'animation_parts/full_attack_sheets.json').read_text())['sheets']))
    (ROOT/'test_current/parts/tile_library.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
