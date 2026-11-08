"""Regress opaque black/gray glyph beds, both screens and changing selections."""
import json
import numpy as np
from PIL import Image,ImageDraw
from hd_core import Core,ROOT
from hd_fonts import FontRenderer

def main():
    out=ROOT/'test_current/font';core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True,user_dir=out/'saves');reports=[];panels=[]
    try:
        for fixture in ('font/forecast_confirm.state','combat/attack_commands.state','combat/sandrock_weapons.state'):
            core.load(ROOT/'test_current'/fixture)
            for selection in range(3):
                for _ in range(20):core.run();core.audio.clear()
                for screen in range(2):
                    source=core.native[screen*192:(screen+1)*192].copy();original=FontRenderer();original.recognize(source)
                    if not original.menu_repairs:continue
                    for bed in (0,96):
                        native=source.copy()
                        for left,top,right,bottom,sl,sr in original.menu_repairs:native[top:bottom,left:right]=bed
                        native[original.last_ink]=source[original.last_ink]
                        r=FontRenderer();r.recognize(native)
                        assert original.menu_glyphs<=r.menu_glyphs,(fixture,screen,selection,bed,'selection lost')
                        healed=r._heal_native(native);assert np.array_equal(native[~r.last_mask],healed[~r.last_mask])
                        checked=0
                        for left,top,right,bottom,sl,sr in r.menu_repairs:
                            for y in range(top,bottom):
                                samples=native[y,sl:sr].astype('int16');green=(samples[:,1]>samples[:,0]+16)&(samples[:,1]>samples[:,2]+16)
                                if green.sum()<4:continue
                                expected=np.median(samples[green],axis=0).astype('uint8');erased=r.last_mask[y,left:right]
                                assert np.all(healed[y,left:right][erased]==expected),(fixture,selection,bed,y,'opaque text bed remains')
                                checked+=int(erased.sum())
                        assert checked>0
                        # The same renderer must recover when the opaque bed
                        # disappears, without caching a stale selection patch.
                        r.compose(Image.fromarray(native).resize((768,576)),native)
                        image=Image.fromarray(source).resize((768,576),Image.Resampling.NEAREST);r.compose(image,source)
                        if bed==0:
                            panel=image.resize((384,288));ImageDraw.Draw(panel).text((2,274),f'{fixture}/{screen}/{selection}',fill='yellow');panels.append(panel)
                        reports.append(dict(fixture=fixture,screen=screen,selection=selection,bed=bed,repaired_pixels=checked))
                core.buttons={5}
                for _ in range(5):core.run();core.audio.clear()
                core.buttons=set()
        assert len(reports)>=18
        sheet=Image.new('RGB',(384*3,288*((len(panels)+2)//3)))
        for n,panel in enumerate(panels):sheet.paste(panel,(n%3*384,n//3*288))
        sheet.save(out/'selected_text_beds.png');(out/'selected_text_beds.json').write_text(json.dumps(reports,indent=2));print('passed',len(reports))
    finally:core.close()

if __name__=='__main__':main()
