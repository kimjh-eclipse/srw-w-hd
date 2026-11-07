"""Prepare observed game parts once, so first-time animation doesn't stall."""
import json,zlib,time
import numpy as np
from hd_parts import PartsRenderer,ROOT
from hd_parts_registration import registration_stamp

r=PartsRenderer();lookup={part['hash']:i for i,part in enumerate(r.bindings,1) if part.get('rgb_enabled',True)};used=set()
used.update(i for i,b in enumerate(r.bindings,1) if b.get('atlas_id') and not any(b.get(k) for k in ('auto_unit','auto_animation','auto_animation_reuse','auto_late_attack','auto_full_attack','auto_shared_attack','observed_generated','observed_reuse','disabled')))
native=np.array(r.native_atlas);rgb=native[:,:,:3].astype('uint32');five=(rgb*31+127)//255
colors=(five[:,:,0]|(five[:,:,1]<<5)|(five[:,:,2]<<10)|0x8000).astype('<u2');colors[native[:,:,3]==0]=0
for path in (ROOT/'test_current/robot').glob('obj_*.json'):
    obj=json.loads(path.read_text())
    for entry in obj.get('entries',[]):
        if entry['c']>>12 or entry['a']&8192:continue
        tile=entry['c']&1023;x=tile%32*8;y=tile//32*8;w,h=entry['w'],entry['h']
        if x+w>256 or y+h>128:continue
        key=zlib.crc32(colors[y:y+h,x:x+w].copy().tobytes())^(w<<16)^h
        if key in lookup:used.add(lookup[key])
for path in (ROOT/'test_current/parts').glob('data_*.npz'):
    with np.load(path) as data:used.update(int(v) for v in data['parts'][:,0] if v)
started=time.perf_counter()
for binding in sorted(used):r.sprite(np.array([binding,0,0,0,0,0,0,0],dtype='uint32'),bytes(1024))
arrays={f'part_{key}':np.array(value) for key,value in r.prepared.items()}
arrays['stamp']=np.array(registration_stamp(ROOT));arrays['statistics']=np.array(json.dumps(r.registration_stats))
meta_path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(meta_path.read_text())
target=ROOT/'graphics'/meta.get('registration_cache','kazuma_parts_registration.npz')
temporary=target.with_suffix('.tmp.npz');np.savez_compressed(temporary,**arrays)
try:temporary.replace(target)
except PermissionError:
    # A legacy running preview may still hold the old lazy NumPy ZIP open.
    target=ROOT/'graphics/kazuma_parts_registration_current.npz'
    meta['registration_cache']=target.name;meta_path.write_text(json.dumps(meta,indent=2))
    arrays['stamp']=np.array(registration_stamp(ROOT))
    np.savez_compressed(temporary,**arrays);temporary.replace(target)
print(json.dumps(dict(prepared_parts=len(used),seconds=round(time.perf_counter()-started,2))))

