"""Build a save state at the first frame of a unit's attack animation.

The test window used retained mid-attack states, so an attack never played
from its start. This drives the game's own menus in an isolated fixture (the
same steps as scripts/verify/verify_named_attacks.py): the Duo weapon-menu
state with the unit record swapped, the canonical pilot seated, weapon costs,
requirements and terrain ratings relaxed in RAM only, the weapon chosen in the
native list, the target and forecast confirmed. The state is saved on the
first frame the battle animation runs. Runs in a child process: the core can
be initialised only once per process.
"""
import ctypes as C,json
from pathlib import Path

WEAPON_STATS=0x80d58
A,B,UP,DOWN,LEFT,RIGHT=8,0,4,5,6,7


def forecast_visible(native):
    import numpy as np
    left=native[24:58,:128];right=native[24:58,128:]
    red=np.count_nonzero((left[:,:,0]>96)&(left[:,:,1]<72)&(left[:,:,2]<72))
    blue=np.count_nonzero((right[:,:,2]>96)&(right[:,:,0]<72))
    header=native[:24,:256];yellow=(header[:,:,0]>150)&(header[:,:,1]>120)&(header[:,:,2]<100)
    return red>40 and blue>40 and np.count_nonzero(yellow[:,:128])>5 and np.count_nonzero(yellow[:,128:])>5


def build(root,rom,uid,wid,target,morale=150,max_frames=900):
    from hd_core import Core
    root=Path(root);catalog=json.loads((root/'test_current/parts/named_unit_catalog.json').read_text(encoding='utf-8'))
    unit=next(u for u in catalog['units'] if u['unit_id']==uid);pilots={p['pilot_id']:p for p in catalog['pilots']};weapons={w['weapon_id']:w for w in catalog['weapons']}
    target=Path(target);core=Core(Path(rom),enabled=False,demo=True,user_dir=target.parent/'attack_start_saves'/target.stem)
    def step(keys,n):
        core.buttons=set(keys)
        for _ in range(n):core.run();core.audio.clear()
        core.buttons=set()
    try:
        core.load(root/'test_current/combat/duo_weapons.state');step([],15);step([B],5);step([],35)
        core.api.retro_get_memory_data.restype=C.c_void_p;ram=core.api.retro_get_memory_data(2);address=ram+0x1f0dbc+64
        for offset in (6,10):C.c_int16.from_address(address+offset).value=uid
        pilot_id=unit.get('default_pilot_id')
        if pilot_id is not None:
            template=C.string_at(ram+0x1eb250+40,40);seat_mask=0
            for seat,pid in enumerate(dict.fromkeys(unit.get('default_pilot_ids',[pilot_id]))):
                slot=pilots[pid]['roster_slot']
                if slot<0:
                    if seat:continue
                    slot=1
                record=ram+0x1eb250+slot*40
                if C.c_uint16.from_address(record).value!=pid or C.c_uint16.from_address(record+14).value==0:
                    C.memmove(record,template,40);C.c_uint16.from_address(record).value=pid
                C.c_uint16.from_address(record+12).value=morale
                C.c_int16.from_address(address+14+seat*2).value=slot;seat_mask|=1<<seat
            C.c_uint16.from_address(address+12).value=seat_mask
        else:C.c_uint16.from_address(ram+0x1eb284).value=morale
        C.c_uint32.from_address(address).value=max(1,unit['hp']);C.c_uint16.from_address(address+4).value=max(1,unit['en'])
        stat=weapons[wid]['stats_id'];weapon=ram+WEAPON_STATS-0x4000+stat*36
        for offset in (16,20):C.c_uint8.from_address(weapon+offset).value=0
        C.c_int8.from_address(weapon+21).value=-1;C.c_uint16.from_address(weapon+8).value|=8
        C.c_uint8.from_address(weapon+22).value=10;C.c_uint8.from_address(weapon+23).value=1
        for offset in range(29,33):C.c_uint8.from_address(weapon+offset).value=3
        for slot in range(8):C.c_uint8.from_address(address+38+slot).value=99
        step([A],5);step([],35)
        menu=[]
        for slot in range(32):
            value=C.c_uint32.from_address(ram+0x1e8408+slot*4).value
            if value not in unit['weapon_ids']:break
            menu.append(value)
        if wid not in menu:return dict(ok=False,reason='이 무기는 이 테스트 배치에서 메뉴에 나오지 않습니다(합체기·맵 병기 등)')
        cursor=int(C.c_uint16.from_address(ram+0x1e8592).value);distance=menu.index(wid)-cursor
        for _ in range(abs(distance)):step([DOWN if distance>0 else UP],1);step([],10)
        step([A],5);step([],40)
        for key in (RIGHT,RIGHT,UP):step([key],1);step([],10)
        step([A],5);step([],40);step([A],5);step([],40)
        if C.c_uint32.from_address(ram+0xa6f38).value==256 and forecast_visible(core.native):step([A],5);step([],40)
        confirm_until=-1
        for frame in range(max_frames):
            core.buttons={A} if frame<confirm_until else set()
            core.run();core.audio.clear()
            if C.c_uint32.from_address(ram+0xa6f38).value==128 and C.c_uint32.from_address(ram+0x1e7a10).value==0:
                core.buttons=set();core.save(target);return dict(ok=True,frame=frame)
            if frame in (120,240,360) and C.c_uint32.from_address(ram+0xa6f38).value==256 and forecast_visible(core.native):confirm_until=frame+5
        return dict(ok=False,reason='전투가 시작되지 않았습니다')
    finally:core.close()


def _child(root,rom,uid,wid,target,queue):
    try:queue.put(build(root,rom,uid,wid,target))
    except Exception as error:queue.put(dict(ok=False,reason=f'{type(error).__name__}: {error}'))


def build_in_child(root,rom,uid,wid,target,timeout=180):
    import multiprocessing as mp
    ctx=mp.get_context('spawn');queue=ctx.Queue();proc=ctx.Process(target=_child,args=(str(root),str(rom),uid,wid,str(target),queue),daemon=True)
    proc.start()
    try:return queue.get(timeout=timeout)
    except Exception:return dict(ok=False,reason='시간 초과')
    finally:proc.join(5)
