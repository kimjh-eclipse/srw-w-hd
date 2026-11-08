"""Verify immutable ROM/approved artwork and the installed supplement contract."""
import hashlib,json,subprocess,sys,py_compile
from PIL import Image
from hd_core import ROOT

def main():
    path=ROOT/'graphics/kazuma_parts_library.json';raw=path.read_bytes();meta=json.loads(raw)
    previous=subprocess.check_output(['git','show','HEAD:graphics/kazuma_parts_library.json'],cwd=ROOT)
    if previous.startswith(b'version https://git-lfs.github.com/spec/v1'):
        previous=subprocess.run(['git','lfs','smudge'],input=previous,stdout=subprocess.PIPE,check=True,cwd=ROOT).stdout
    assert json.loads(previous)['bindings'][:5263]==meta['bindings'][:5263]
    rom_hash=hashlib.sha256((ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes()).hexdigest()
    face_hash=hashlib.sha256((ROOT/'graphics/kazuma_parts_atlas_facefix.png').read_bytes()).hexdigest()
    assert rom_hash=='0a5a22bd6bb25ebe640767e6b422b91358636e9ae1300e61d7e8ac3c5d8cd478'
    assert face_hash=='fc876ea3a755726ea8a2badfd9c44101f5a5410edf58f154625fd08cd9e897fe'
    assets=[]
    for directory in ('wing_parts','img_first'):
        for image in (ROOT/'graphics'/directory).glob('*.png'):
            with Image.open(image) as im:
                assert max(im.size)<=960,(image,im.size)
                im.verify()
            assets.append(dict(path=image.relative_to(ROOT).as_posix(),bytes=image.stat().st_size))
    stamp=hashlib.sha256(raw).hexdigest()
    for name in ('native_materials.json','material_slots.json'):assert json.loads((ROOT/'graphics'/name).read_text())['library_sha256']==stamp
    audit=json.loads((ROOT/'test_current/rom_catalog/img_first_audit.json').read_text());assert audit['unregistered_unique_parts']==0
    for script in ('hd_parts','hd_core','hd_renderer','prepare_all_unit_assets','build_tile_library','install_wing_parts','install_wing_cutins','install_wing_full_cutins','install_wing_closeup','prepare_img_first_supplement','install_img_first_supplement','verify_wing_attacks','verify_duo_map_attack'):
        py_compile.compile(str(ROOT/f'emulator/{script}.py'),doraise=True)
    sandrock=json.loads((ROOT/'test_current/combat/sandrock_weapon_verification.json').read_text());duo=json.loads((ROOT/'test_current/combat/duo_weapon_verification.json').read_text());map_attack=json.loads((ROOT/'test_current/combat/duo_map_verification.json').read_text());gpu=json.loads((ROOT/'test_current/performance/gpu_surface_verification.json').read_text())
    assert len(sandrock)==3 and len(duo)==2
    assert all(row['battle_started'] and not row['prepare_errors'] for row in sandrock+duo)
    assert set(duo[1]['cutin_ids'])=={6,8}
    assert map_attack['started'] and not map_attack['prepare_errors'] and 8 in map_attack['cutin_ids']
    assert len(gpu)==24 and max(row['max_error'] for row in gpu)<=3
    report=dict(bindings=len(meta['bindings']),approved_first_5263_unchanged=True,rom_sha256=rom_hash,approved_face_sha256=face_hash,audited_img_first_packages=audit['total'],unregistered_audited_parts=0,assets=len(assets),asset_bytes=sum(x['bytes'] for x in assets),largest_dimension=960,compiled_metadata_matches=True,actual_weapon_replays=6,gpu_screen_comparisons=len(gpu),gpu_max_channel_error=max(row['max_error'] for row in gpu),all_campaign_replayed=False)
    (ROOT/'test_current/combat/wing_installation_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
