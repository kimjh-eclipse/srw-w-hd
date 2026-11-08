"""Validate independent HD parts in battle, contact, result and ability screens."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from hd_core import Core,ROOT,HERE
from hd_renderer import HDRenderer
import json,ctypes as C
import numpy as np
from PIL import Image

def verify():
    out=ROOT/'test_current/parts';out.mkdir(exist_ok=True)
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True);core.load(HERE/'demo.state',refresh_code=True)
    renderer=HDRenderer();events=json.loads((HERE/'demo_input.json').read_text());report=[];scenes={}
    weapon_manifest=ROOT/'graphics/kazuma_weapon_parts_manifest.json'
    expected_weapons={part['hash'] for part in json.loads(weapon_manifest.read_text())['parts']} if weapon_manifest.exists() else set()
    weapon_seen={};unit_seen={}
    library=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text())['bindings']
    wanted={65040:'idle',65220:'windup',65340:'cutin',65390:'weapon_turn',65400:'weapon_raise',65520:'shoot',65674:'enemy_hit_flash',65680:'enemy_hit',65840:'motion_pose',65880:'contact',66400:'enemy_attack',66580:'enemy_transform',67000:'after_attack',67080:'fade',68000:'result',68900:'ability_no_top_robot'}
    for f in range(64700,68901):
        core.buttons={e['button'] for e in events if e['from']<=f<e['to']}
        if f>=68500 and f%120<3:core.buttons.add(8)
        core.run();core.audio.clear();count=int((core.parts[:,0]>0).sum());bgcount=int((core.bgparts[:,0]>0).sum())
        for row in core.parts:
            if row[0]:
                spec=library[int(row[0])-1]
                if spec.get('unit'):unit_seen.setdefault(spec['unit'],set()).add(spec.get('source_binding',int(row[0])))
            if row[0] and int(row[4]) in expected_weapons:
                key=str(int(row[4]));entry=weapon_seen.setdefault(key,dict(first=f,last=f,frames=0))
                entry['last']=f;entry['frames']+=1
        if count or bgcount:report.append([f,count,bgcount])
        if f in wanted:
            image=renderer.render(core.native,core.ids,core.hd,robot=core.robot,obj=core.obj.raw,parts=core.parts,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes)
            native=Image.fromarray(core.native[:192]).resize((1440,1080),Image.Resampling.NEAREST)
            changed=int(np.any(np.array(image)[:,:1440]!=np.array(native),axis=2).sum())
            unit_counts={unit:sum(bool(row[0]) and library[int(row[0])-1].get('unit')==unit for row in core.parts) for unit in unit_seen}
            scenes[wanted[f]]=dict(frame=f,obj_parts=count,bg_tiles=bgcount,changed_pixels=changed,unit_parts=unit_counts)
            image.save(out/f'{wanted[f]}.png')
            if f in [65040,65220,65390,65400,65520,65674,65680,65840,65880,66400,66580,67080,68000]:image.save(ROOT/f'graphics/kazuma_parts_{wanted[f]}.png')
            if f==65400 and expected_weapons:
                assert {4259027044,1821243665}.issubset(set(map(int,core.parts[:,4]))),'upright rifle pieces did not match'
            if f==68000:core.save(out/'result.state')
            if f==68900:
                # This menu puts its robot on the lower physical display. Do
                # not draw that engine's robot over the upper stats text.
                assert count+bgcount==0 and changed==0,(f,'wrong display received HD parts')
            else:
                assert count+bgcount>0,(f,'no part textures matched')
                assert changed>500,(f,'matched parts did not render')
    core.api.retro_get_memory_data.argtypes=[C.c_uint];core.api.retro_get_memory_data.restype=C.c_void_p
    ram=core.api.retro_get_memory_data(2);symbols=json.loads((ROOT/'release_battle_v02/voice_probe_symbols.json').read_text(encoding='utf-8'))
    if core.clean_korean:
        # An old preview state contains the retired payload. Its entry hook
        # must be restored to the clean ROM before advancing any frames.
        rom=core.rom.read_bytes();arm=int.from_bytes(rom[0x20:0x24],'little')
        assert C.string_at(ram+0xee50,8)==rom[arm+0xee50:arm+0xee58]
        voices=0
    else:
        voices=C.c_uint32.from_address(ram+symbols['voice_match_count']-0x2000000).value;assert voices>=2,voices
    core.load(out/'result.state');core.set_hd(False);core.run()
    assert not np.any(core.parts[:,0]) and not np.any(core.bgparts[:,0])
    assert expected_weapons==set(map(int,weapon_seen)),('unseen weapon fragments',expected_weapons-set(map(int,weapon_seen)))
    for unit in {b['unit'] for b in library if 'unit' in b}:
        expected={i for i,b in enumerate(library,1) if b.get('unit')==unit and not b.get('source_binding')}
        assert expected==unit_seen.get(unit,set()),(unit,'unit parts not observed',expected-unit_seen.get(unit,set()))
    if any('palette_source_rgb' in b for b in library):
        assert len(renderer.parts_renderer.palette_luts)>1,'enemy palette recoloring was not exercised'
    result=dict(renderer='individual content-addressed OBJ/BG parts; no whole-pose artwork',scenes=scenes,unit_parts_seen={k:len(v) for k,v in unit_seen.items()},palette_sources_prepared=len(renderer.parts_renderer.palette_luts),weapon_parts_seen=weapon_seen,voice_events=voices,hd_off_verified=True,frames_with_parts=len(report))
    (out/'verification.json').write_text(json.dumps(result,indent=2));core.close();print(json.dumps(result))

if __name__=='__main__':verify()
