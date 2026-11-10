"""Build isolated native combination partners from the ROM's recipe IDs.

The recipe bytes and attack identity remain intact. Existing campaign records
and player saves are never changed. This is not campaign-legality validation.
"""
import ctypes as C,struct
from collections import defaultdict
from scripts.assets.catalog_named_units import WEAPON_STATS

class NativePartnerFixture:
    def __init__(self,catalog,rom):
        self.catalog=catalog;self.rom=rom

    @staticmethod
    def recipe_groups(ram,address):
        """Decode the loaded overlay's sentinel-delimited signed unit lists."""
        values=(C.c_int16*2048).from_address(ram+address-0x2000000)
        groups=defaultdict(list);members=None
        for index,value in enumerate(values):
            if value==-2:return dict(groups)
            if value==-1:
                members=[];groups[int(values[index+1])].append(members)
            elif index and values[index-1]==-1:continue
            else:
                assert members is not None and value>=0,'Invalid native recipe table'
                members.append(int(value))
        raise AssertionError('Unterminated native recipe table')

    @staticmethod
    def human(unit):
        slot=unit.get('default_pilot_roster_slot')
        return ('roster',slot) if slot is not None and slot>=0 else ('pilot',unit.get('default_pilot_id',unit['unit_id']))

    def prepare(self,ram,actor,wid,morale=150,high_level=False):
        off=WEAPON_STATS+self.catalog['weapons'][wid]['stats_id']*36
        if not struct.unpack_from('<I',self.rom,off+8)[0]&0x8000000:return None
        recipe=self.rom[off+24];choices=defaultdict(list)
        native_groups=self.recipe_groups(ram,0x22620d0)
        alternatives=native_groups.get(recipe,[])
        selected=next((members for members in alternatives if actor['unit_id'] in members),None)
        if selected is None:
            return dict(recipe_id=recipe,recipe_bytes_preserved=True,partners=[],
                        native_recipe_alternatives=alternatives,
                        blocked_reason='actor_variant_absent_from_native_recipe',
                        campaign_legality_verified=False)
        by_id={unit['unit_id']:unit for unit in self.catalog['units']}
        partners=[by_id[uid] for uid in selected if uid!=actor['unit_id']]
        for unit in partners:choices[self.human(unit)].append(unit)
        assert len(partners)<=5,(recipe,'Unexpected recipe size',len(partners))
        # This accessor literal belongs to the loaded native map overlay.
        table=C.c_uint32.from_address(ram+0x23bb40).value-0x2000000
        assert 0<=table<0x400000,hex(table)
        objects=[ram+table+i*0x88 for i in range(60)]
        active={C.c_int16.from_address(obj+0x28).value:(i,obj) for i,obj in enumerate(objects) if C.c_uint32.from_address(obj).value}
        assert 1 in active and 3 in active,'The isolated deployed fixture changed'
        actor_obj=active[1][1];template_obj=C.string_at(active[3][1],0x88)
        template_unit=C.string_at(ram+0x1f0dbc+3*64,64);template_pilot=C.string_at(ram+0x1eb250+40,40)
        free_objects=[active[3][0]]+[i for i,obj in enumerate(objects) if not C.c_uint32.from_address(obj).value]
        live_slots=[3]+[i for i in range(2,32) if i not in active and i!=3]
        positions=[(1,0),(0,-1),(-1,0),(0,1),(1,1)]
        placed=[]
        for unit,obj_slot,live,(dx,dy) in zip(partners,free_objects,live_slots,positions):
            obj=objects[obj_slot];C.memmove(obj,template_obj,0x88);C.c_int16.from_address(obj+0x28).value=live
            C.c_int32.from_address(obj+0x10).value=C.c_int32.from_address(actor_obj+0x10).value+dx*65536
            C.c_int32.from_address(obj+0x14).value=C.c_int32.from_address(actor_obj+0x14).value+dy*65536
            target=ram+0x1f0dbc+live*64;C.memmove(target,template_unit,64)
            for field in (6,10):C.c_int16.from_address(target+field).value=unit['unit_id']
            C.c_uint32.from_address(target).value=max(1,unit['hp']);C.c_uint16.from_address(target+4).value=max(1,unit['en'])
            for ammo in range(8):C.c_uint8.from_address(target+38+ammo).value=99
            mask=0;pilots=[]
            for seat,pid in enumerate(dict.fromkeys(unit.get('default_pilot_ids',[]))):
                slot=self.catalog['pilots'][pid]['roster_slot']
                if slot<0:continue
                record=ram+0x1eb250+slot*40;C.memmove(record,template_pilot,40)
                C.c_uint16.from_address(record).value=pid;C.c_uint16.from_address(record+12).value=morale
                # Native level is floor(EXP/500)+1, not the SP byte at +14.
                if high_level:C.c_uint16.from_address(record+2).value=49000
                C.c_int16.from_address(target+14+seat*2).value=slot;mask|=1<<seat;pilots.append(pid)
            C.c_uint16.from_address(target+12).value=mask
            for pwid in unit['weapon_ids']:
                weapon=ram+WEAPON_STATS-0x4000+self.catalog['weapons'][pwid]['stats_id']*36
                for field in (16,20):C.c_uint8.from_address(weapon+field).value=0
            placed.append(dict(unit_id=unit['unit_id'],live_unit_slot=live,map_object_slot=obj_slot,pilot_ids=pilots,offset=[dx,dy]))
        return dict(recipe_id=recipe,recipe_bytes_preserved=True,partners=placed,
                    native_recipe_members=selected,native_recipe_alternatives=alternatives,
                    candidate_variants={str(key):[u['unit_id'] for u in value] for key,value in choices.items()},
                    partner_costs_relaxed=True,campaign_legality_verified=False)

def align_map_target(ram):
    """Move the existing isolated foe onto the original MAP firing lane."""
    table=C.c_uint32.from_address(ram+0x23bb40).value-0x2000000
    assert 0<=table<0x400000
    objects=[ram+table+i*0x88 for i in range(60)]
    actor=next(obj for obj in objects if C.c_uint32.from_address(obj).value and C.c_int16.from_address(obj+0x28).value==1)
    x=C.c_int32.from_address(actor+0x10).value;y=C.c_int32.from_address(actor+0x14).value
    for i,obj in enumerate(objects):
        if not C.c_uint32.from_address(obj).value:continue
        if C.c_int32.from_address(obj+0x10).value!=x+2*65536 or C.c_int32.from_address(obj+0x14).value!=y-65536:continue
        C.c_int32.from_address(obj+0x14).value=y
        return dict(map_object_slot=i,live_unit_slot=C.c_int16.from_address(obj+0x28).value,old_offset=[2,-1],new_offset=[2,0],campaign_legality_verified=False)
    return None
