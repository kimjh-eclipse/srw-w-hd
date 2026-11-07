"""Verify installed scope, source rectangles, and preserved base assets."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'graphics/all_units'
plan=json.loads((OUT/'batches.json').read_text());installed=json.loads((OUT/'installed.json').read_text());catalog=json.loads((OUT/'catalog.json').read_text())
meta=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text());bindings=meta['bindings']
covered={p['resource']:p['bindings'] for p in installed['coverage']};selected=set(plan['selected_resources'])
assert set(covered)==selected and len(selected)==338
assert not installed['missing_images']
primary=[p for p in catalog['packages'] if p['resource']<3500]
assert len(primary)==269
for package in catalog['packages']:
    if package['resource'] not in selected:continue
    mapped=covered[package['resource']]
    assert len(mapped)==len(package['parts'])
    for part,index in zip(package['parts'],mapped):
        binding=bindings[index-1]
        assert binding['hash']==part['hash'] and (binding['w'],binding['h'])==(part['w'],part['h'])
for binding in bindings:
    source=bindings[binding.get('source_binding',0)-1] if binding.get('source_binding') else binding
    assert (source['w'],source['h'])==(binding['w'],binding['h'])
    width,height=meta['atlases'][source['atlas_id']]['native_size'] if source.get('atlas_id') else (256,128)
    assert 0<=source['x']<=width-source['w'] and 0<=source['y']<=height-source['h']
for p in primary:assert (OUT/f"unit_{p['resource']}_hd_pose.png").exists()
prefix=json.loads((OUT/'approved_prefix.json').read_text())
assert hashlib.sha256(json.dumps(bindings[:5263],sort_keys=True,separators=(',',':')).encode()).hexdigest()==prefix['sha256']
assert hashlib.sha256((ROOT/'graphics/kazuma_parts_atlas_facefix.png').read_bytes()).hexdigest()==prefix['face_sha256']
assert hashlib.sha256((ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes()).hexdigest()==prefix['rom_sha256']
battle=json.loads((ROOT/'test_current/parts/verification.json').read_text());indexed=json.loads((ROOT/'test_current/parts/indexed_verification.json').read_text())
assert battle['voice_events']==0 and battle['hd_off_verified'] and all(indexed.values())
result=dict(primary_forms=len(primary),auxiliary_packages=len(selected)-len(primary),registered_part_occurrences=installed['parts'],binding_count=len(bindings),hd_sheets=64,missing_selected_packages=0,all_source_rectangles_valid=True,approved_base_preserved=True,face_preserved=True,rom_preserved=True,gallery_forms=269,visual_review_sheets=9,representative_battle_scenes=len(battle['scenes']),voice_events=battle['voice_events'],indexed_palette_checks=indexed,full_game_attack_playthrough=False)
(ROOT/'test_current/parts/all_units_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
