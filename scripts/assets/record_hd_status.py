"""Report verified resource coverage separately from full-game playback."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import json,hashlib
ROOT=PROJECT_ROOT

def read(name):return json.loads((ROOT/name).read_text())
def main():
    out=ROOT/'graphics/animation_parts';meta=read('graphics/kazuma_parts_library.json');plan=read('graphics/animation_parts/full_attack_sheets.json');shared=read('graphics/animation_parts/shared_attack_sheets.json')
    full_done=sum((out/s['image']).exists() for s in plan['sheets']);shared_done=sum((out/s['image']).exists() for s in shared['sheets']);portrait=read('graphics/portraits/library.json')
    approved=read('graphics/all_units/approved_prefix.json');prefix=hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    face=hashlib.sha256((ROOT/'graphics/kazuma_parts_atlas_facefix.png').read_bytes()).hexdigest();rom=hashlib.sha256((ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes()).hexdigest()
    assert prefix==approved['sha256'] and face==approved['face_sha256'] and rom==approved['rom_sha256']
    report=dict(all_mechs_complete=False,all_attacks_complete=False,full_attack_sheets_generated=full_done,full_attack_sheets_planned=len(plan['sheets']),shared_palette_sheets_generated=shared_done,shared_palette_sheets_planned=len(shared['sheets']),reviewed_mechanical_source_art_generated=full_done==len(plan['sheets']) and shared_done==len(shared['sheets']),total_bindings=len(meta['bindings']),blocked_index_collisions=len(meta.get('indexed_collision_keys',[])),portraits=len(portrait.get('portraits',portrait.get('items',[]))),background_layers=len(read('graphics/backgrounds/library.json')['backgrounds']),approved_prefix_preserved=True,approved_face_preserved=True,canonical_rom_preserved=True,voice_enabled=False,exact_dynamic_tile_assembly=True,tests={})
    for name,path in [('native_speed','test_current/parts/worker_speed.json'),('native_texture_cache','test_current/parts/native_cache_verification.json'),('video_audio_cadence','test_current/parts/video_cadence_verification.json'),('worker_lifecycle_actions','test_current/gui/worker_pipeline.json'),('cold_registration','test_current/parts/async_verification.json'),('dynamic_bridge','test_current/parts/dynamic_verification.json'),('compound_and_fade','test_current/parts/compound_verification.json'),('generated_identities','test_current/parts/generated_bindings_audit.json'),('palette_render_cache','test_current/parts/palette_render_cache_verification.json'),('portraits','test_current/portrait/catalog_verification.json'),('portrait_performance','test_current/portrait/performance_two_screens.json')]:
        report['tests'][name]=dict(path=path,result=read(path))
    report['remaining']=['All-unit weapons, transformations, destruction and special scenes have not been replayed through the whole campaign.','Background coverage currently consists of six observed layers, not every map or story CG.','Special palette effects and source mismatches retain native graphics.']
    report['counts_note']='Resources, material variants and bindings are not unique character/mecha counts or a completion percentage.'
    (out/'completion_status.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    path=ROOT/'release_battle_v02/current_features.json';features=json.loads(path.read_text());features.update(hd_all_mechs_complete=False,hd_status='../graphics/animation_parts/completion_status.json',voice_enabled=False,rom_sha256=rom);path.write_text(json.dumps(features,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='tests'}))

if __name__=='__main__':main()
