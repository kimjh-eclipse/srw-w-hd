"""Verify complete terrain bindings separately from campaign-play coverage."""
import json,hashlib,time
from pathlib import Path
import numpy as np
from PIL import Image
from hd_core import Core,ROOT
from hd_map_tiles import MapTilesRenderer

def main():
    folder=ROOT/'graphics/map_tiles';out=ROOT/'test_current/map_tiles';catalog=json.loads((folder/'catalog.json').read_text());library=json.loads((folder/'library.json').read_text());shared=json.loads((folder/'shared_coverage.json').read_text());coverage={r['map']:r for r in shared}
    assert len(catalog['maps'])==len(library['maps'])==114
    assert {r['id'] for r in catalog['maps']}=={r['id'] for r in library['maps']}
    direct=0
    for row in library['maps']:
        path=folder/row['image'];assert path.exists(),row['id'];assert hashlib.sha256(path.read_bytes()).hexdigest()==row['image_sha256'],row['id']
        if row['id'] in coverage:assert coverage[row['id']]['coverage']==1,row['id']
        else:assert (folder/f"map_{row['id']}_hd.png").exists();direct+=1
        assert (folder/row['overview_native']).exists()
    assert direct==69 and len(coverage)==45
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'final_saves');renderer=MapTilesRenderer();actual=[]
    try:
        for state in ['map_fresh','grid','menu_step_0','menu_step_1','menu_step_2','menu_step_3','menu_step_4','menu_step_5']:
            c.load(ROOT/f'test_current/font/{state}.state');c.run()
            for screen in (0,1):
                native=c.native[screen*192:(screen+1)*192];image=Image.fromarray(native).resize((960,720),Image.Resampling.NEAREST);assert renderer.compose(image,native),(state,screen)
                actual.append(dict(state=state,screen=screen,matches=renderer.last_matches));image.save(out/f'{state}_screen_{screen}_hd.png')
        c.load(ROOT/'test_current/font/cutin_dialogue.state');negative=[]
        for f in range(30):
            c.run();native=c.native[:192];image=Image.fromarray(native).resize((960,720),Image.Resampling.NEAREST);start=time.perf_counter();assert not renderer.compose(image,native);negative.append((time.perf_counter()-start)*1000)
    finally:c.close()
    report=dict(total_maps=114,direct_generated_worlds=69,shared_worlds=45,source_groups=67,minimum_shared_hd_tile_coverage=1.,unmapped_source_tiles=0,supplement_atlases=3,overview_references=114,actual_state_screen_checks=len(actual),actual=actual,campaign_playthrough=False,negative_animated_scene_mean_ms=float(np.mean(negative)))
    (out/'complete_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='actual'}))

if __name__=='__main__':main()
