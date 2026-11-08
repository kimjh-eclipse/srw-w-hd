"""Conservative color rejection: every eligible UV match survives this filter."""
import hashlib
from pathlib import Path
import numpy as np

def possible_colors(references,folder):
    signature=hashlib.sha256(references.tobytes()).hexdigest()
    cache=Path(folder)/'possible_colors.npz'
    if cache.exists():
        try:
            with np.load(cache,allow_pickle=False) as archive:
                if str(archive['signature'])==signature:return archive['colors']
        except (ValueError,OSError,KeyError):pass
    result=np.zeros((len(references),32768),dtype='bool')
    for index,reference in enumerate(references):
        valid=reference[(reference&32768)!=0]&32767
        values=np.unique(valid).astype('int32');r=values&31;g=(values>>5)&31;b=(values>>10)&31
        for dr in (-1,0,1):
            for dg in (-1,0,1):
                for db in (-1,0,1):
                    rr=r+dr;gg=g+dg;bb=b+db;inside=(rr>=0)&(rr<=31)&(gg>=0)&(gg<=31)&(bb>=0)&(bb<=31)
                    result[index,rr[inside]|gg[inside]<<5|bb[inside]<<10]=True
    temporary=cache.with_suffix('.tmp.npz')
    try:
        np.savez_compressed(temporary,signature=np.array(signature),colors=result);temporary.replace(cache)
    except OSError:pass
    return result
