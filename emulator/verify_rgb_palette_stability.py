"""An exact RGB texture identity must survive palette slot reassignment."""
import json
import numpy as np
from hd_parts import PartsRenderer,ROOT

r=PartsRenderer();index=next(i for i,b in enumerate(r.bindings,1) if b.get('dynamic_palette') and b.get('hash') and b.get('rgb_enabled',True));b=r.bindings[index-1]
colors=np.asarray(b['original_palette_rgb'],dtype='uint32');five=(colors*31+127)//255;palette=(five[:,0]|five[:,1]<<5|five[:,2]<<10).astype('uint16')
row=np.array([index,0,0,0,b['hash'],0,0,0],dtype='uint32')
normal=np.array(r.sprite(row,bytes(1024),palette));r.cache.clear()
reordered=np.array(r.sprite(row,bytes(1024),palette[::-1].copy()))
assert np.array_equal(normal,reordered),'An unchanged RGB texture was recolored by unrelated palette slots'
row[4]=0;black=np.array(r.sprite(row,bytes(1024),np.zeros(16,dtype='uint16')))
assert np.array_equal(normal[:,:,3],black[:,:,3]) and not black[:,:,:3][black[:,:,3]>0].any()
report=dict(exact_rgb_ignores_slot_reassignment=True,indexed_color_change_still_applies=True,alpha_preserved=True)
(ROOT/'test_current/parts/rgb_palette_stability.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
