"""Replay saved native scenes with the production simultaneous-cut-in bridge."""
import hashlib,json,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_core import Core
from hd_renderer import HDRenderer
from PIL import Image,ImageDraw

def main():
    folder=ROOT/'test_current/combat/multilayer_cutins';folder.mkdir(exist_ok=True)
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=folder/'isolated_saves')
    renderer=HDRenderer(async_parts=True,dynamic_parts=True);renderer.set_resolution(768)
    rows=[];cards=[]
    scenes=[('getter_cutin',None),('golion_cutin_full',None),('duo_cutin_full',6),
        ('duo_smile_cutin_full',None),('quatre_cutin_full',7),('bonta_cutin',0)]
    try:
        assert core.layer_cutin_bridge,'native library does not export per-layer cut-ins'
        for name,expected in scenes:
            core.load(ROOT/f'test_current/combat/{name}.state');core.run();core.audio.clear()
            if expected!=0:assert core.hd[0],(name,'missing native cut-in')
            if expected is not None:assert core.hd[0]==expected,(name,list(core.hd))
            active=[list(map(int,row)) for row in core.cutin_layers if row[0]]
            if expected!=0:assert active and int(core.hd[0]) in {row[0] for row in active},name
            else:assert core.parts[:,0].any(),(name,'missing mechanical OBJ cut-in parts')
            image=renderer.render_top(core.native,core.ids,core.hd,parts=core.parts,obj=core.obj.raw,
                owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,
                part_palettes=core.part_palettes,backgrounds=core.backgrounds,bg_layout=core.bg_layout,
                cutin_layers=core.cutin_layers)
            image.save(folder/f'{name}.png')
            card=image.resize((384,288));ImageDraw.Draw(card).text((3,3),name,fill='yellow');cards.append(card)
            rows.append(dict(scene=name,primary=int(core.hd[0]),active_layers=active))
        captures=ROOT/'test_current/combat/named_attacks/unit_297/diagnostic_preview/weapon_1213_capture'
        observed=json.loads((captures/'hd_360.json').read_text())['active_layers']
        assert {171,172}<={row[0] for row in observed if row[0]},observed
        # Exact native frame capture, not a hand-composited proof image.
        with Image.open(captures/'hd_360.png') as image:
            cards.append(image.resize((384,288)))
        rows.append(dict(scene='final_dynamic_special_360',active_layers=observed))
        contact=Image.new('RGB',(1152,288*3))
        for i,card in enumerate(cards):contact.paste(card,(i%3*384,i//3*288))
        contact.save(folder/'contact.png')
        report=dict(scope=__doc__,scenes=rows,simultaneous_layers_observed=True,
            campaign_all_poses_verified=False,player_save_modified=False)
        (folder/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
    finally:core.close();renderer.parts_renderer.close()

if __name__=='__main__':main()
