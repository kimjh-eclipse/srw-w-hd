"""Exercise named unit attacks through the game's normal weapon/target menus.

Only an isolated state's unit record is substituted. Canonical pilots with
an existing roster slot are selected from the verified ROM pilot table.
Never counts a menu-only run as an attack or certifies campaign legality.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import argparse,ctypes as C,json,time,hashlib,os,faulthandler
from collections import Counter
import numpy as np
from PIL import Image,ImageDraw
from hd_core import Core
from hd_renderer import HDRenderer
from battle_rumble import BattleRumble
from scripts.assets.catalog_named_units import WEAPON_STATS

def main():
    faulthandler.enable()
    p=argparse.ArgumentParser();p.add_argument('--units',default='0,1,2,3,4')
    p.add_argument('--weapons',choices=['first','all'],default='first')
    p.add_argument('--weapon-indices',help='Comma-separated native list positions; overrides --weapons')
    p.add_argument('--morale',type=int,default=150,help='Isolated Duo fixture morale, never a player save')
    p.add_argument('--diagnostic-unlock',action='store_true',help='Ignore costs/requirements in isolated RAM; not campaign legality')
    p.add_argument('--shard',help='Independent unit-ID partition, e.g. 0/3')
    p.add_argument('--resume',action='store_true')
    p.add_argument('--retry-failed',action='store_true',help='Retry only previously attempted cases without a verified completed replay')
    p.add_argument('--unit-output',action='store_true',help='Use a separate fixed report directory for one unit (crash-isolated supervisor)')
    p.add_argument('--native-render',action='store_true',help='Separate HD-off reference replay; never overwrites the HD report')
    p.add_argument('--frames',type=int,default=1800);a=p.parse_args()
    catalog=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text())
    mechanical_ids={r['id'] for r in json.loads((ROOT/'graphics/cutins_library.json').read_text())['cutins'] if r.get('image','').startswith('mechanical_cutins/')}
    selected=set(map(int,a.units.split(','))) if a.units!='all' else None
    units=[u for u in catalog['units'] if u['primary_image'] is not None and u['weapon_ids'] and (selected is None or u['unit_id'] in selected)]
    out=ROOT/'test_current/combat/named_attacks'
    if a.unit_output:
        assert selected is not None and len(selected)==1
        out=out/f'unit_{next(iter(selected))}'
    if a.native_render:out=out/'native_reference'
    if a.shard:
        shard,total=map(int,a.shard.split('/'));assert 0<=shard<total
        units=[u for u in units if u['unit_id']%total==shard];out=out/f'shard_{shard}'
    out.mkdir(exist_ok=True,parents=True)
    signature=hashlib.sha256(Path(__file__).read_bytes())
    for file in (ROOT/'graphics/kazuma_parts_library.json',ROOT/'graphics/cutins_library.json',Path(os.environ.get('SRWW_CORE_PATH',str(ROOT/'emulator/desmume/desmume/src/frontend/libretro/desmume_libretro.dll')))):
        with file.open('rb') as stream:signature.update(hashlib.file_digest(stream,'sha256').digest())
    revision=signature.hexdigest()
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'isolated_saves')
    if a.native_render:core.set_hd(False)
    # Exercise the production lazy-loading/dynamic fallback, rather than
    # silently disabling unknown-texture diagnostics in synchronous mode.
    renderer=HDRenderer(async_parts=True,dynamic_parts=True);renderer.set_resolution(768)
    def step(keys,n):
        core.buttons=set(keys)
        for _ in range(n):core.run();core.audio.clear()
        core.buttons=set()
    def paint():
        if a.native_render:return Image.fromarray(core.native[:192])
        return renderer.render_top(core.native,core.ids,core.hd,paused=True,parts=core.parts,obj=core.obj.raw,
            owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,
            backgrounds=core.backgrounds,bg_layout=core.bg_layout,unknown=core.unknown_snapshot(),
            sub_parts=(core.sub_parts,core.sub_owners,core.sub_oam.raw,core.sub_palettes,core.sub_ids,core.sub_priorities))
    report_path=out/'report.json'
    rows=json.loads(report_path.read_text(encoding='utf-8'))['rows'] if report_path.exists() else []
    try:
        for unit in units:
            indices=list(map(int,a.weapon_indices.split(','))) if a.weapon_indices else list(range(len(unit['weapon_ids']) if a.weapons=='all' else 1))
            for wi in indices:
                wid=unit['weapon_ids'][wi]
                if a.retry_failed and not any(r['unit_id']==unit['unit_id'] and r['weapon_id']==wid and not r.get('full_replay_verified') for r in rows):continue
                if a.resume and any(r['unit_id']==unit['unit_id'] and r['weapon_id']==wid and r.get('verification_revision')==revision and r.get('full_replay_verified') for r in rows):continue
                previous_misses=set(renderer.parts_renderer.unmapped_misses)
                uid=unit['unit_id'];core.load(ROOT/'test_current/combat/duo_weapons.state');step([],15)
                step([0],5);step([],35) # Native B: return to attack command.
                core.api.retro_get_memory_data.restype=C.c_void_p;ram=core.api.retro_get_memory_data(2)
                address=ram+0x1f0dbc+64
                for offset in (6,10):C.c_int16.from_address(address+offset).value=uid
                pilot_slot=unit.get('default_pilot_roster_slot');pilot_id=unit.get('default_pilot_id')
                canonical=pilot_id is not None
                pilot_runtime_synthesized=False
                if canonical:
                    # Unit+12 is a seat-presence mask, not a pilot index.
                    # Unit+14..24 are slots in the 40-byte live pilot table.
                    # Its first field selects the ROM's canonical pilot ID.
                    template=C.string_at(ram+0x1eb250+40,40)
                    seat_mask=0
                    for seat,pid in enumerate(unit.get('default_pilot_ids',[pilot_id])):
                        slot=catalog['pilots'][pid]['roster_slot']
                        if slot<0:
                            if seat:continue
                            slot=1
                        record=ram+0x1eb250+slot*40
                        if C.c_uint16.from_address(record).value!=pid or C.c_uint16.from_address(record+14).value==0:
                            C.memmove(record,template,40);C.c_uint16.from_address(record).value=pid
                            pilot_runtime_synthesized=True
                        C.c_uint16.from_address(record+12).value=a.morale
                        C.c_int16.from_address(address+14+seat*2).value=slot
                        seat_mask|=1<<seat
                    C.c_uint16.from_address(address+12).value=seat_mask
                C.c_uint32.from_address(address).value=max(1,unit['hp'])
                C.c_uint16.from_address(address+4).value=max(1,unit['en'])
                if not canonical:C.c_uint16.from_address(ram+0x1eb284).value=a.morale
                if a.diagnostic_unlock:
                    stat=catalog['weapons'][wid]['stats_id'];weapon=ram+WEAPON_STATS-0x4000+stat*36
                    for offset in (16,20,24):C.c_uint8.from_address(weapon+offset).value=0
                    C.c_int8.from_address(weapon+21).value=-1
                    C.c_int8.from_address(weapon+25).value=-1
                    # The fixture has already moved. Permit post-move firing
                    # without changing its weapon/animation identity.
                    flags=C.c_uint16.from_address(weapon+8)
                    flags.value|=8
                    C.c_uint8.from_address(weapon+22).value=10
                    C.c_uint8.from_address(weapon+23).value=1
                    # Ammo counters are read as signed bytes by availability
                    # checks: 255 would mean -1, not a full magazine.
                    for slot in range(8):C.c_uint8.from_address(address+38+slot).value=99
                step([8],5);step([],35) # Native A rebuilds this unit's weapon list.
                # The native menu sorts weapons and omits unavailable combination
                # entries. ROM record order is not the on-screen cursor order.
                menu_weapons=[]
                for slot in range(32):
                    value=C.c_uint32.from_address(ram+0x1e8408+slot*4).value
                    if value not in unit['weapon_ids']:break
                    menu_weapons.append(value)
                menu_position=menu_weapons.index(wid) if wid in menu_weapons else None
                initial_cursor=int(C.c_uint16.from_address(ram+0x1e8592).value)
                if menu_position is not None:
                    assert 0<=initial_cursor<len(menu_weapons),(uid,wid,initial_cursor,menu_weapons)
                    distance=menu_position-initial_cursor
                    for _ in range(abs(distance)):step([5 if distance>0 else 4],1);step([],10)
                    assert C.c_uint16.from_address(ram+0x1e8592).value==menu_position,(uid,wid,'cursor did not reach requested weapon')
                paint().save(out/f'unit_{uid}_weapon_{wid}_menu.png')
                if menu_position is not None:
                    step([8],5);step([],40)
                    for key in (7,7,4):step([key],1);step([],10)
                    step([8],5);step([],40);step([8],5);step([],40)
                active_frames=0;started=False;seen=set();cutins=set();cards=[];rumble=BattleRumble();events=[];observed_weapon=None;unknown_seen={};unknown_examples={}
                start=time.perf_counter()
                for frame in range(a.frames):
                    core.set_ready_parts(renderer.parts_renderer);core.run();core.audio.clear()
                    active=C.c_uint32.from_address(ram+0xa6f38).value==128 and C.c_uint32.from_address(ram+0x1e7a10).value==0
                    if active and observed_weapon is None:observed_weapon=int(C.c_uint16.from_address(ram+0x1e8c74).value)
                    effect=rumble.sample(core)
                    if effect:events.append(dict(frame=frame,**effect))
                    if uid==413 and wid==1612 and frame in (360,480,840,960,1080,1200):
                        core.save(out/f'plasma_{frame}.state')
                    started|=active;active_frames+=int(active)
                    if started and not active and frame>180:break
                    if not started and frame>180:break
                    if frame%12==0:
                        snapshot=core.unknown_snapshot()
                        if snapshot is not None:
                            for pos,raw in enumerate(snapshot[0]):
                                if not raw[0]:continue
                                identity=f'{int(raw[0])}:{int(raw[7])}'
                                unknown_seen[identity]=dict(width=int(raw[1]),height=int(raw[2]))
                                if identity not in unknown_examples:
                                    unknown_examples[identity]=(raw.copy(),snapshot[1][pos].copy(),snapshot[2][pos].copy())
                        image=paint();seen.update(int(v) for v in core.parts[:,0] if v)
                        if core.hd[0]:
                            ident=int(core.hd[0])
                            if ident in mechanical_ids and ident not in cutins:core.save(out/f'mechanical_cutin_{ident}.state')
                            cutins.add(ident)
                        if active and frame%120==0:
                            card=image.resize((384,288));ImageDraw.Draw(card).text((3,3),f'uid {uid} weapon {wid} +{frame}',fill='yellow');cards.append(card)
                    core.buttons={11,8} if active and frame%120<5 else set()
                core.buttons=set()
                deadline=time.monotonic()+5
                empty=(np.zeros((0,8),dtype='uint32'),np.zeros((0,0),dtype='uint8'),np.zeros((0,16),dtype='uint16'))
                while renderer.parts_renderer.unmapped_pending and time.monotonic()<deadline:
                    renderer.parts_renderer.schedule_unknown(empty);time.sleep(.01)
                if unknown_examples:
                    examples=list(unknown_examples.values())
                    np.savez_compressed(out/f'unit_{uid}_weapon_{wid}_unknown.npz',
                        rows=np.stack([x[0] for x in examples]),pixels=np.stack([x[1] for x in examples]),palettes=np.stack([x[2] for x in examples]))
                if cards:
                    sheet=Image.new('RGB',(1536,288*((len(cards)+3)//4)))
                    for n,card in enumerate(cards):sheet.paste(card,(n%4*384,n//4*288))
                    sheet.save(out/f'unit_{uid}_weapon_{wid}.png')
                row=dict(unit_id=uid,name_ja=unit['name_ja'],name_ko=unit['name_ko'],weapon_id=wid,
                    weapon_name=catalog['weapons'][wid]['name_ja'],battle_started=started,active_battle_frames=active_frames,
                    frames=frame,cutin_ids=sorted(cutins),observed_bindings=sorted(seen),
                    errors=dict(renderer.parts_renderer.prepare_errors),seconds=round(time.perf_counter()-start,2),
                    rumble_events=events,
                    canonical_pilot_selected=canonical,default_pilot_id=pilot_id,all_poses_verified=False)
                row['observed_weapon_id']=observed_weapon
                row['native_menu_weapon_ids']=menu_weapons
                row['native_menu_position']=menu_position
                row['native_menu_initial_cursor']=initial_cursor
                row['blocked_reason']='weapon_absent_from_native_menu' if menu_position is None else None
                row['weapon_routed_correctly']=started and observed_weapon==wid
                row['battle_completed']=started and not active
                row['full_replay_verified']=row['weapon_routed_correctly'] and row['battle_completed'] and not row['errors']
                row['verification_revision']=revision
                misses=renderer.parts_renderer.unmapped_misses
                row['new_unmapped_textures']={str(k):v for k,v in misses.items() if k not in previous_misses}
                row['unknown_native_rectangles']=unknown_seen
                row['dynamic_fallback_enabled']=renderer.parts_renderer.dynamic_parts
                row['dynamic_requests_pending']=len(renderer.parts_renderer.unmapped_pending)
                row['rumble_counts']=dict(Counter(e['reason'] for e in events if e['duration']))
                row['fixture_morale_override']=a.morale
                row['fixture_pilot_stats_synthesized']=pilot_runtime_synthesized
                row['diagnostic_requirements_override']=a.diagnostic_unlock
                rows=[r for r in rows if (r['unit_id'],r['weapon_id'])!=(uid,wid)]+[row]
                report=dict(scope=__doc__,selected_units=len(units),unit_ids=[u['unit_id'] for u in units],
                    attempted=len(rows),full_replays=sum(r.get('full_replay_verified',False) for r in rows),rows=rows)
                temporary=report_path.with_suffix('.tmp.json');temporary.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');temporary.replace(report_path)
                print(uid,wid,'battle',started,'active',active_frames,'bindings',len(seen),flush=True)
    finally:core.close();renderer.parts_renderer.close()

if __name__=='__main__':main()
