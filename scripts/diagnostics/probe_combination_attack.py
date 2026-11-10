"""Use an existing friendly map slot as a canonical combination partner.

No combination weapon flag or animation pointer is overridden. This isolated
fixture tests native partner discovery; it does not certify campaign legality.
"""
import argparse,ctypes as C,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_core import Core
from scripts.verify import verify_named_attacks as replay

def main():
    p=argparse.ArgumentParser();p.add_argument('--unit',type=int,default=294);p.add_argument('--partner',type=int,default=298);p.add_argument('--weapon-index',type=int,default=5);a=p.parse_args()
    catalog=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text());partner=catalog['units'][a.partner]
    class PartnerCore(Core):
        def load(self,*args,**kwargs):
            super().load(*args,**kwargs);self.api.retro_get_memory_data.restype=C.c_void_p;ram=self.api.retro_get_memory_data(2)
            unit=ram+0x1f0dbc+3*64;pilot=partner['default_pilot_id'];slot=partner['default_pilot_roster_slot']
            if slot<0:slot=0
            template=C.string_at(ram+0x1eb250+40,40);C.memmove(ram+0x1eb250+slot*40,template,40)
            C.c_uint16.from_address(ram+0x1eb250+slot*40).value=pilot
            C.c_uint16.from_address(ram+0x1eb250+slot*40+12).value=150
            C.c_uint16.from_address(ram+0x1eb250+slot*40+14).value=99
            for off in (6,10):C.c_int16.from_address(unit+off).value=a.partner
            C.c_uint32.from_address(unit).value=partner['hp'];C.c_uint16.from_address(unit+4).value=partner['en']
            C.c_uint16.from_address(unit+12).value=1;C.c_int16.from_address(unit+14).value=slot
            for ammo in range(8):C.c_uint8.from_address(unit+38+ammo).value=99
            # Native map records are 0x88 bytes. Their +0x28 field names a
            # live unit, and +0x10/+0x14 hold 16.16 map coordinates.
            table=C.c_uint32.from_address(ram+0x23bb40).value-0x2000000
            actor=target=None
            for index in range(60):
                obj=ram+table+index*0x88
                if not C.c_uint32.from_address(obj).value:continue
                live=C.c_int16.from_address(obj+0x28).value
                if live==1:actor=obj
                if live==3:target=obj
            assert actor is not None and target is not None,'Native deployed fixture slots missing'
            C.c_int32.from_address(target+0x10).value=C.c_int32.from_address(actor+0x10).value+65536
            C.c_int32.from_address(target+0x14).value=C.c_int32.from_address(actor+0x14).value
            self.fixture_combination_partners=[dict(live_unit_slot=3,unit_id=a.partner,pilot_id=pilot,adjacent=True)]
    replay.Core=PartnerCore
    sys.argv=[sys.argv[0],'--units',str(a.unit),'--weapon-indices',str(a.weapon_index),'--unit-output','--diagnostic-unlock','--frames','6000']
    replay.main()
    path=ROOT/f'test_current/combat/named_attacks/unit_{a.unit}/report.json';report=json.loads(path.read_text(encoding='utf-8'));wid=catalog['units'][a.unit]['weapon_ids'][a.weapon_index]
    for row in report['rows']:
        if row['weapon_id']==wid:
            row['fixture_combination_partners']=[dict(live_unit_slot=3,unit_id=a.partner,pilot_id=partner['default_pilot_id'],adjacent=True)]
            row['partner_fixture_script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':main()
