"""Exercise the secondary display's real OAM bridge with saved game states."""
import json
import numpy as np
from PIL import Image,ImageDraw
from hd_core import Core,ROOT
from hd_renderer import HDRenderer

def main():
    out=ROOT/'test_current/parts'
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'saves')
    r=HDRenderer();r.set_resolution(768);records=[];images=[]
    try:
        assert c.sub_bridge,'Secondary display bridge missing'
        for name in ('font/command_progress.state','font/command.state','parts/active.state','font/forecast_confirm.state','combat/attack_commands.state'):
            c.set_hd(False);c.load(ROOT/'test_current'/name);c.run();c.audio.clear()
            native=c.native[192:].copy()
            c.set_hd(True);c.load(ROOT/'test_current'/name);c.run();c.audio.clear()
            sub=(c.sub_parts,c.sub_owners,c.sub_oam.raw,c.sub_palettes,c.sub_ids,c.sub_priorities)
            r.sub_parts=sub
            result=r.render_bottom(c.native,c.hd)
            if hasattr(result,'to_pil'):result=result.to_pil()
            ids=np.flatnonzero(c.sub_parts[:,0]);records.append(dict(scene=name,parts=len(ids),bindings=[int(x) for x in c.sub_parts[ids,0]],pixels_changed=int(np.count_nonzero(np.any(np.asarray(result)!=np.asarray(Image.fromarray(native).resize(result.size,Image.Resampling.NEAREST)),axis=2)))))
            panel=Image.new('RGB',(768,310));panel.paste(Image.fromarray(native).resize((384,288)),(0,22));panel.paste(result.resize((384,288)),(384,22));ImageDraw.Draw(panel).text((4,4),name,fill='white');images.append(panel)
        sheet=Image.new('RGB',(768,310*len(images)))
        for i,panel in enumerate(images):sheet.paste(panel,(0,310*i))
        sheet.save(out/'sub_display_verification.png')
        assert next(v for v in records if v['scene']=='parts/active.state')['parts']>=15
        assert next(v for v in records if v['scene']=='font/forecast_confirm.state')['parts']>=25
        (out/'sub_display_verification.json').write_text(json.dumps(records,indent=2));print(json.dumps(records))
    finally:c.close();r.parts_renderer.close()

if __name__=='__main__':main()
