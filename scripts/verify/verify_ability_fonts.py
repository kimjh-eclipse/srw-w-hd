"""Check the actual production pipeline against native ability screenshots/state."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json
from pathlib import Path
import numpy as np
from PIL import Image
from hd_core import Core,ROOT
from hd_renderer import HDRenderer

def main():
    out=ROOT/'test_current/font';renderer=HDRenderer(async_parts=False)
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True)
    report={'production_pipeline':True,'scenes':{}}
    label_calls=[];original=renderer.ui_labels.compose
    def tracked(target,native):
        count=original(target,native)
        if count:label_calls.append(list(renderer.ui_labels.last_matches))
        return count
    renderer.ui_labels.compose=tracked
    try:
        core.load(ROOT/'test_current/parts/result.state',refresh_code=True);core.run()
        assert len(core.bg_layout)==4,'Actual BG register metadata required'
        for name,native in [('result_state',core.native.copy()),('scene_1',np.asarray(Image.open(out/'scene_1.png').convert('RGB')).copy())]:
            label_calls.clear()
            image=renderer.render(native,core.ids,core.hd,robot=core.robot,obj=core.obj.raw,
                parts=core.parts,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,
                part_palettes=core.part_palettes,backgrounds=core.backgrounds,unknown=getattr(core,'unknown',None),bg_layout=core.bg_layout)
            assert not renderer.text_renderer.battle_scan,(name,'Ability incorrectly uses battle ROI')
            matches=renderer.text_renderer.last_matches
            assert len(matches)==79,(name,len(matches))
            def line(y,left=0,right=256):return ''.join(ch for x,yy,ch in sorted(matches) if yy==y and left<=x<right)
            expected=[(0,0,256,'카즈마·아디건'),(16,64,88,'레벨'),(16,104,112,'5'),(32,96,120,'102'),
                (16,128,184,'원공1/1'),(32,128,184,'원방1/1'),(16,192,248,'요청0/0'),
                (48,0,256,'정신'),(64,0,256,'상태'),(80,0,256,'발호크'),
                (96,0,256,'5000/5000'),(112,0,96,'170/170'),(160,0,64,'지형')]
            for y,left,right,text in expected:assert line(y,left,right)==text,(name,y,line(y,left,right),text)
            assert label_calls and [text for x,y,text in label_calls[0]]==['HP','EN','PARTS']
            image.save(out/f'ui_ability_{name}_production.png')
            report['scenes'][name]=dict(battle_roi=False,glyphs=len(matches),labels=label_calls[0],native_top_crc=__import__('zlib').crc32(native[:192].tobytes()),bg_layout=core.bg_layout)
    finally:core.close()
    (out/'ui_ability_production_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
