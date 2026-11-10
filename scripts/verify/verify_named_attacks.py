"""Exercise named unit attacks through the game's normal weapon/target menus.

Only an isolated state's unit record is substituted. Canonical pilots with
an existing roster slot are selected from the verified ROM pilot table.
Never counts a menu-only run as an attack or certifies campaign legality.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import argparse,ctypes as C,json,time,hashlib,os,faulthandler,base64,zlib
from collections import Counter
import numpy as np
from PIL import Image,ImageDraw
from hd_core import Core
from hd_renderer import HDRenderer
from battle_rumble import BattleRumble
from scripts.assets.catalog_named_units import WEAPON_STATS

def native_forecast_visible(native):
    left=native[24:58,:128];right=native[24:58,128:]
    red=np.count_nonzero((left[:,:,0]>96)&(left[:,:,1]<72)&(left[:,:,2]<72))
    blue=np.count_nonzero((right[:,:,2]>96)&(right[:,:,0]<72))
    # MAP range cells can also be red/blue. Require the native yellow HP/EN
    # headings on both sides before pressing a further confirmation button.
    header=native[:24,:256]
    yellow=(header[:,:,0]>150)&(header[:,:,1]>120)&(header[:,:,2]<100)
    return red>40 and blue>40 and np.count_nonzero(yellow[:,:128])>5 and np.count_nonzero(yellow[:,128:])>5

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
    p.add_argument('--combination-fixture',action='store_true',help='Deploy canonical recipe partners in isolated native map slots')
    p.add_argument('--map-aligned-fixture',action='store_true',help='Align the isolated foe with a directional MAP firing lane')
    p.add_argument('--warm-replay',action='store_true',help='Replay each selected attack twice in the same renderer/cache')
    p.add_argument('--diagnostic-terrain',action='store_true',help='Set attack terrain ratings to A in isolated RAM, never the ROM or campaign')
    p.add_argument('--diagnostic-level',action='store_true',help='Set canonical pilots to level 99 via EXP in isolated RAM only')
    p.add_argument('--diagnostic-menu-entry',action='store_true',help='Preview a locked animation via an injected menu entry; never counts as a normal replay')
    p.add_argument('--capture-frames',help='Comma-separated battle frames for isolated VRAM/state snapshots')
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
    if a.diagnostic_menu_entry:out=out/'diagnostic_preview'
    if a.shard:
        shard,total=map(int,a.shard.split('/'));assert 0<=shard<total
        units=[u for u in units if u['unit_id']%total==shard];out=out/f'shard_{shard}'
    out.mkdir(exist_ok=True,parents=True)
    from scripts.verify.native_replay_lock import acquire_report_lock
    report_lock=acquire_report_lock(out)
    signature=hashlib.sha256(Path(__file__).read_bytes())
    for file in (Path(__file__).with_name('native_partner_fixture.py'),Path(__file__).with_name('native_replay_lock.py'),ROOT/'graphics/kazuma_parts_library.json',ROOT/'graphics/cutins_library.json',Path(os.environ.get('SRWW_CORE_PATH',str(ROOT/'emulator/desmume/desmume/src/frontend/libretro/desmume_libretro.dll')))):
        with file.open('rb') as stream:signature.update(hashlib.file_digest(stream,'sha256').digest())
    revision=signature.hexdigest()
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'isolated_saves')
    if a.native_render:core.set_hd(False)
    # Exercise the production lazy-loading/dynamic fallback, rather than
    # silently disabling unknown-texture diagnostics in synchronous mode.
    renderer=HDRenderer(async_parts=True,dynamic_parts=True);renderer.set_resolution(768)
    partner_fixture=None
    if a.combination_fixture:
        from scripts.verify.native_partner_fixture import NativePartnerFixture
        partner_fixture=NativePartnerFixture(catalog,core.rom.read_bytes())
    def step(keys,n):
        core.buttons=set(keys)
        for _ in range(n):core.run();core.audio.clear()
        core.buttons=set()
    def paint():
        if a.native_render:return Image.fromarray(core.native[:192])
        return renderer.render_top(core.native,core.ids,core.hd,paused=True,parts=core.parts,obj=core.obj.raw,
            owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,
            backgrounds=core.backgrounds,bg_layout=core.bg_layout,unknown=core.unknown_snapshot(),cutin_layers=core.cutin_layers,
            sub_parts=(core.sub_parts,core.sub_owners,core.sub_oam.raw,core.sub_palettes,core.sub_ids,core.sub_priorities))
    report_path=out/'report.json'
    capture_frames=set(map(int,a.capture_frames.split(','))) if a.capture_frames else set()
    rows=json.loads(report_path.read_text(encoding='utf-8'))['rows'] if report_path.exists() else []
    try:
        for unit in units:
            indices=list(map(int,a.weapon_indices.split(','))) if a.weapon_indices else list(range(len(unit['weapon_ids']) if a.weapons=='all' else 1))
            if a.warm_replay:indices=[wi for wi in indices for _ in range(2)]
            replay_passes=Counter()
            for wi in indices:
                replay_passes[wi]+=1
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
                    for seat,pid in enumerate(dict.fromkeys(unit.get('default_pilot_ids',[pilot_id]))):
                        slot=catalog['pilots'][pid]['roster_slot']
                        if slot<0:
                            if seat:continue
                            slot=1
                        record=ram+0x1eb250+slot*40
                        if C.c_uint16.from_address(record).value!=pid or C.c_uint16.from_address(record+14).value==0:
                            C.memmove(record,template,40);C.c_uint16.from_address(record).value=pid
                            pilot_runtime_synthesized=True
                        C.c_uint16.from_address(record+12).value=a.morale
                        if a.diagnostic_level:C.c_uint16.from_address(record+2).value=49000
                        C.c_int16.from_address(address+14+seat*2).value=slot
                        seat_mask|=1<<seat
                    C.c_uint16.from_address(address+12).value=seat_mask
                C.c_uint32.from_address(address).value=max(1,unit['hp'])
                C.c_uint16.from_address(address+4).value=max(1,unit['en'])
                if not canonical:C.c_uint16.from_address(ram+0x1eb284).value=a.morale
                if a.diagnostic_unlock:
                    stat=catalog['weapons'][wid]['stats_id'];weapon=ram+WEAPON_STATS-0x4000+stat*36
                    for offset in (16,20):C.c_uint8.from_address(weapon+offset).value=0
                    C.c_int8.from_address(weapon+21).value=-1
                    # +24/+25 select the native combination recipe/variant.
                    # Preserve them when relaxing the isolated fixture costs.
                    # The fixture has already moved. Permit post-move firing
                    # without changing its weapon/animation identity.
                    flags=C.c_uint16.from_address(weapon+8)
                    flags.value|=8
                    C.c_uint8.from_address(weapon+22).value=10
                    C.c_uint8.from_address(weapon+23).value=1
                    # Ammo counters are read as signed bytes by availability
                    # checks: 255 would mean -1, not a full magazine.
                    for slot in range(8):C.c_uint8.from_address(address+38+slot).value=99
                if a.diagnostic_terrain:
                    # Native getter 0x2020ae8 reads the four signed ratings
                    # at +29+terrain. Zero disables an otherwise valid attack
                    # against the space-only target in this isolated fixture.
                    weapon=ram+WEAPON_STATS-0x4000+catalog['weapons'][wid]['stats_id']*36
                    for offset in range(29,33):C.c_uint8.from_address(weapon+offset).value=3
                combination_fixture=partner_fixture.prepare(ram,unit,wid,a.morale,a.diagnostic_level) if partner_fixture else None
                map_target_fixture=None
                if a.map_aligned_fixture:
                    import struct
                    weapon_off=WEAPON_STATS+catalog['weapons'][wid]['stats_id']*36
                    rom=core.rom.read_bytes()
                    if struct.unpack_from('<I',rom,weapon_off+8)[0]&0x20:
                        from scripts.verify.native_partner_fixture import align_map_target
                        map_target_fixture=align_map_target(ram)
                step([8],5);step([],35) # Native A rebuilds this unit's weapon list.
                # The native menu sorts weapons and omits unavailable combination
                # entries. ROM record order is not the on-screen cursor order.
                menu_weapons=[]
                for slot in range(32):
                    value=C.c_uint32.from_address(ram+0x1e8408+slot*4).value
                    if value not in unit['weapon_ids']:break
                    menu_weapons.append(value)
                menu_position=menu_weapons.index(wid) if wid in menu_weapons else None
                menu_entry_injected=False
                if menu_position is None and a.diagnostic_menu_entry and menu_weapons:
                    C.c_uint32.from_address(ram+0x1e8408).value=wid
                    menu_weapons[0]=wid;menu_position=0;menu_entry_injected=True
                initial_cursor=int(C.c_uint16.from_address(ram+0x1e8592).value)
                if menu_position is not None:
                    assert 0<=initial_cursor<len(menu_weapons),(uid,wid,initial_cursor,menu_weapons)
                    distance=menu_position-initial_cursor
                    for _ in range(abs(distance)):step([5 if distance>0 else 4],1);step([],10)
                    assert C.c_uint16.from_address(ram+0x1e8592).value==menu_position,(uid,wid,'cursor did not reach requested weapon')
                paint().save(out/f'unit_{uid}_weapon_{wid}_menu.png')
                if menu_position is not None:
                    step([8],5);step([],40)
                    for key in ((7,7) if map_target_fixture else (7,7,4)):step([key],1);step([],10)
                    step([8],5);step([],40);step([8],5);step([],40)
                extra_forecast_confirmation=False
                if menu_position is not None and C.c_uint32.from_address(ram+0xa6f38).value==256:
                    # Some MAP/target-selection paths add a confirmation screen.
                    # Confirm the actual red/blue native forecast, never change
                    # weapon flags or call an animation directly.
                    if native_forecast_visible(core.native):
                        step([8],5);step([],40);extra_forecast_confirmation=True
                active_frames=0;started=False;seen=set();cutins=set();cards=[];rumble=BattleRumble();events=[];observed_weapon=None;unknown_seen={};unknown_examples={}
                confirm_until=-1;confirmation_count=int(extra_forecast_confirmation)
                start=time.perf_counter()
                for frame in range(a.frames):
                    core.set_ready_parts(renderer.parts_renderer);core.run();core.audio.clear()
                    active=C.c_uint32.from_address(ram+0xa6f38).value==128 and C.c_uint32.from_address(ram+0x1e7a10).value==0
                    if active and observed_weapon is None:observed_weapon=int(C.c_uint16.from_address(ram+0x1e8c74).value)
                    effect=rumble.sample(core)
                    if effect:events.append(dict(frame=frame,**effect))
                    if frame in capture_frames:
                        from scripts.diagnostics import inspect_attract_resources as capture
                        capture.OUT=out/f'weapon_{wid}_capture';capture.OUT.mkdir(parents=True,exist_ok=True)
                        capture.snapshot(core,frame)
                        core.save(capture.OUT/f'frame_{frame}.state')
                        rendered=paint();rendered.save(capture.OUT/f'hd_{frame}.png')
                        (capture.OUT/f'hd_{frame}.json').write_text(json.dumps(dict(active_layers=core.cutin_layers.tolist(),primary=list(core.hd)),indent=2))
                    if uid==413 and wid==1612 and frame in (360,480,840,960,1080,1200):
                        core.save(out/f'plasma_{frame}.state')
                    started|=active;active_frames+=int(active)
                    if started and not active and frame>180:break
                    if not started and frame>(600 if menu_position is not None else 180):break
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
                            cutins.update(int(plane[0]) for plane in core.cutin_layers if plane[0])
                            cutins.add(ident)
                        if active and frame%120==0:
                            card=image.resize((384,288));ImageDraw.Draw(card).text((3,3),f'uid {uid} weapon {wid} +{frame}',fill='yellow');cards.append(card)
                    if not started and menu_position is not None and frame in (120,240,360) and C.c_uint32.from_address(ram+0xa6f38).value==256 and native_forecast_visible(core.native):
                        confirm_until=frame+5;confirmation_count+=1
                    core.buttons={8} if frame<confirm_until else ({11,8} if active and frame%120<5 else set())
                core.buttons=set()
                deadline=time.monotonic()+5
                empty=(np.zeros((0,8),dtype='uint32'),np.zeros((0,0),dtype='uint8'),np.zeros((0,16),dtype='uint16'))
                while renderer.parts_renderer.unmapped_pending and time.monotonic()<deadline:
                    renderer.parts_renderer.schedule_unknown(empty);time.sleep(.01)
                # Keep exact native input evidence after successful HD binding.
                # Otherwise the second/warm replay overwrites the old capture
                # with only the still-unpainted effects and loses fixed cases.
                for bid in seen:
                    request=renderer.parts_renderer.runtime_requests.get(bid)
                    if request is None:continue
                    encoded,w,h,palette=request;indices=np.frombuffer(zlib.decompress(base64.b64decode(encoded)),dtype='uint8')
                    material=2166136261
                    for value in indices:material=((material^int(value))*16777619)&0xffffffff
                    index_hash=renderer.parts_renderer.bindings[bid-1]['index_hash'];identity=f'{index_hash}:{material}'
                    if identity in unknown_examples:continue
                    raw=np.zeros(8,dtype='uint32');raw[:3]=[index_hash,w,h];raw[7]=material
                    pixels=np.zeros(4096,dtype='uint8');pixels[:w*h]=indices
                    pal=np.asarray(palette,dtype='uint16');colors=np.where(indices,pal[indices]|0x8000,0).astype('<u2')
                    raw[6]=zlib.crc32(colors.tobytes())^(w<<16)^h
                    unknown_examples[identity]=(raw,pixels,pal)
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
                row['extra_forecast_confirmation']=extra_forecast_confirmation
                row['forecast_confirmation_count']=confirmation_count
                row['blocked_reason']='weapon_absent_from_native_menu' if menu_position is None else None
                row['weapon_routed_correctly']=started and observed_weapon==wid
                row['battle_completed']=started and not active
                replay_completed=row['weapon_routed_correctly'] and row['battle_completed'] and not row['errors']
                row['full_replay_verified']=replay_completed and not menu_entry_injected
                row['animation_preview_verified']=replay_completed and menu_entry_injected
                row['native_menu_entry_injected']=menu_entry_injected
                row['verification_revision']=revision
                row['cache_warm_replay_pass']=replay_passes[wi]
                # A runtime binding ID is resolved to exact source resources;
                # this is separate from a visual all-poses certification.
                import sqlite3
                with sqlite3.connect((ROOT/'graphics/parts_tile_library.sqlite').as_uri()+'?mode=ro',uri=True) as tile_db:
                    tile_resources={identifier:json.loads(description)['resource'] for identifier,description in tile_db.execute('SELECT id,description FROM sources')}
                tile_db.close()
                sources=set()
                for bid in seen:
                    spec=renderer.parts_renderer.bindings[bid-1]
                    if 'resource' in spec:sources.add(spec['resource'])
                    for group in renderer.parts_renderer.registration_stats.get(bid,{}).get('tile_groups',[]):
                        sources.add(tile_resources[group['source']])
                row['observed_source_resources']=sorted(sources)
                misses=renderer.parts_renderer.unmapped_misses
                row['new_unmapped_textures']={str(k):v for k,v in misses.items() if k not in previous_misses}
                row['unknown_native_rectangles']=unknown_seen
                row['dynamic_fallback_enabled']=renderer.parts_renderer.dynamic_parts
                row['dynamic_requests_pending']=len(renderer.parts_renderer.unmapped_pending)
                row['rumble_counts']=dict(Counter(e['reason'] for e in events if e['duration']))
                row['fixture_morale_override']=a.morale
                row['fixture_pilot_stats_synthesized']=pilot_runtime_synthesized
                row['diagnostic_requirements_override']=a.diagnostic_unlock
                row['diagnostic_terrain_ratings_override']=a.diagnostic_terrain
                row['diagnostic_level_99_override']=a.diagnostic_level
                row['combination_fixture']=combination_fixture
                row['map_target_fixture']=map_target_fixture
                rows=[r for r in rows if (r['unit_id'],r['weapon_id'])!=(uid,wid)]+[row]
                report=dict(scope=__doc__,selected_units=len(units),unit_ids=[u['unit_id'] for u in units],
                    attempted=len(rows),full_replays=sum(r.get('full_replay_verified',False) for r in rows),rows=rows)
                temporary=report_path.with_suffix('.tmp.json');temporary.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');temporary.replace(report_path)
                print(uid,wid,'battle',started,'active',active_frames,'bindings',len(seen),flush=True)
    finally:core.close();renderer.parts_renderer.close();report_lock.close()

if __name__=='__main__':main()
