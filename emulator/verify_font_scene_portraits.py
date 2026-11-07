"""Replay the actual captured dialogue frame through render_bottom."""
import json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from hd_renderer import HDRenderer
from hd_fonts import FontRenderer
from hd_portraits import PortraitRenderer,ROOT
OUT=ROOT/'test_current/portrait'
def main():
    source=ROOT/'test_current/font/scene_0.png';native=np.asarray(Image.open(source).convert('RGB'));assert native.shape==(384,256,3)
    renderer=HDRenderer.__new__(HDRenderer);renderer.bottom_portraits=PortraitRenderer(async_prepare=False);renderer.bottom_text_renderer=FontRenderer();hd=np.zeros(12,dtype='uint32');hd[10]=1
    final=renderer.render_bottom(native,hd);portraits=renderer.bottom_portraits
    assert set(portraits.last_matches)=={'kazuma','portrait_00056'},portraits.last_matches
    assert set(portraits.last_rectangles)=={(0,8,56,48),(0,136,56,48)}
    base=Image.fromarray(native[192:384]).resize((1440,1080),Image.Resampling.NEAREST)
    reference=base.copy();reference_renderer=PortraitRenderer(async_prepare=False);reference_renderer.compose(reference,native[192:384])
    before=np.asarray(base);after=np.asarray(final);reference_pixels=np.asarray(reference);faces=[]
    for name,(x,y,w,h) in zip(portraits.last_matches,portraits.last_rectangles):
        box=(round(x*5.625),round(y*5.625),round((x+w)*5.625),round((y+h)*5.625));a,b,c,d=box
        mask=portraits._art(next(p for p in portraits.items if p['name']==name)).getchannel('A');visible=np.asarray(mask)>0
        changed=int(np.any(after[b:d,a:c]!=before[b:d,a:c],axis=2).sum())
        restored=int(np.any(after[b:d,a:c]!=reference_pixels[b:d,a:c],axis=2)[visible].sum())
        assert changed>30000,(name,changed)
        assert restored==0,(name,'font renderer altered portrait',restored)
        faces.append(dict(name=name,rectangle=[x,y,w,h],changed_pixels=changed,font_changed_portrait_pixels=restored))
    final.save(OUT/'font_scene_0_bottom_hd.png');comparison=Image.new('RGB',(1440,564),'#17202a');comparison.paste(base.resize((720,540)),(0,24));comparison.paste(final.resize((720,540)),(720,24));draw=ImageDraw.Draw(comparison);draw.text((8,5),'Native captured scene',(255,255,255));draw.text((728,5),'Actual render_bottom: portraits + font',(255,255,255));comparison.save(OUT/'font_scene_0_portrait_comparison.png')
    report=dict(source=str(source),source_is_actual_native_capture=True,path='HDRenderer.render_bottom -> PortraitRenderer.compose -> FontRenderer.compose',faces=faces,all_two_faces_hd=True,portrait_module_change_needed=False,note='This replays a captured native frame through the actual composition method; it is not a new live-window screenshot.')
    (OUT/'font_scene_0_portrait_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
if __name__=='__main__':main()
