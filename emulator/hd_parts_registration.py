"""Register HD paint inside the original part's coordinate and silhouette contract.

The generated atlas is not edited. This is a cached runtime texture preparation
step, before the game's OAM transforms and layering are applied.
"""
import math,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter

def registration_stamp(root,meta=None):
    # The NPZ only contains the approved initial parts. New lazy atlases do
    # not invalidate it or require reading gigabytes during each startup.
    if meta is None:meta=json.loads((root/'graphics/kazuma_parts_library.json').read_text())
    flags=('auto_unit','auto_animation','auto_animation_reuse','auto_late_attack','auto_full_attack','auto_shared_attack','observed_generated','observed_reuse','disabled')
    approved=[(i,b) for i,b in enumerate(meta['bindings'],1) if not any(b.get(k) for k in flags)]
    names={b.get('atlas_id','base') for _,b in approved}
    digest=hashlib.sha256(json.dumps(approved,sort_keys=True).encode())
    paths=[Path(__file__),root/'graphics/kazuma_parts_atlas_reference.png',root/'graphics'/meta['atlas']]
    for name in sorted(names-{'base'}):
        extra=meta['atlases'][name];digest.update(json.dumps(extra,sort_keys=True).encode());paths.extend([root/'graphics'/extra['image'],root/'graphics'/extra['reference']])
    for path in paths:digest.update(path.read_bytes())
    return digest.hexdigest()

def register_part(art,native,scale=8):
    w,h=native.size
    target=np.asarray(native.getchannel('A'),dtype=float)/255
    coarse=art.getchannel('A').resize((w,h),Image.Resampling.BOX)
    initial=np.asarray(coarse,dtype=float)/255
    def score(mask):
        return float(np.minimum(target,mask).sum()/max(np.maximum(target,mask).sum(),1))
    best=(score(initial),0.,0.,1.)
    # Only small corrections are allowed; animation comes entirely from OAM.
    for zoom in (.96,1.,1.04):
        for dy in (-2.,-1.,-.5,0.,.5,1.,2.):
            for dx in (-2.,-1.,-.5,0.,.5,1.,2.):
                coeff=(1/zoom,0,w/2-(w/2+dx)/zoom,0,1/zoom,h/2-(h/2+dy)/zoom)
                mask=np.asarray(coarse.transform((w,h),Image.Transform.AFFINE,coeff,Image.Resampling.BILINEAR),dtype=float)/255
                value=score(mask)-.003*(dx*dx+dy*dy)-.03*abs(math.log(zoom))
                if value>best[0]+.002:best=(value,dx,dy,zoom)
    _,dx,dy,zoom=best;size=(w*scale,h*scale)
    art=art.resize(size,Image.Resampling.LANCZOS)
    coeff=(1/zoom,0,(w/2-(w/2+dx)/zoom)*scale,0,1/zoom,(h/2-(h/2+dy)/zoom)*scale)
    art=art.transform(size,Image.Transform.AFFINE,coeff,Image.Resampling.BICUBIC)
    pixels=np.array(art);rgb=pixels[:,:,:3].copy()
    # Shared source texels keep the attachment points in the same place even
    # when two different OBJ rectangles overlap or a part is mirrored.
    contract=native.getchannel('A').resize(size,Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(.5))
    # Pin attachment interiors while retaining the painted smooth contour
    # within one native pixel, rather than tracing every original pixel step.
    interior=np.asarray(contract.filter(ImageFilter.MinFilter(5)))
    envelope=np.asarray(contract.filter(ImageFilter.MaxFilter(17)))
    alpha=np.maximum(interior,np.minimum(pixels[:,:,3],envelope))
    wanted=alpha>0
    known=(pixels[:,:,3]>=32)|((pixels[:,:,3]>0)&(pixels[:,:,3]>=alpha))
    initial_missing=int((wanted&~known).sum())
    for _ in range(scale*2):
        missing=wanted&~known
        if not missing.any():break
        updated=known.copy()
        for sy,sx in ((0,1),(0,-1),(1,0),(-1,0)):
            neighbor=np.roll(known,(sy,sx),(0,1));color=np.roll(rgb,(sy,sx),(0,1))
            if sy==1:neighbor[0]=False
            if sy==-1:neighbor[-1]=False
            if sx==1:neighbor[:,0]=False
            if sx==-1:neighbor[:,-1]=False
            fill=missing&~updated&neighbor
            rgb[fill]=color[fill];updated[fill]=True
        if np.array_equal(known,updated):break
        known=updated
    missing=wanted&~known
    fallback=np.array(native.resize(size,Image.Resampling.BICUBIC))[:,:,:3]
    rgb[missing]=fallback[missing]
    result=Image.fromarray(np.dstack([rgb,alpha]))
    return result,dict(dx=dx,dy=dy,zoom=zoom,before_iou=round(score(initial),5),
                       registered_iou=round(best[0],5),filled_edge_pixels=initial_missing,
                       reference_fill_pixels=int(missing.sum()),contract_pixels=int(wanted.sum()))
