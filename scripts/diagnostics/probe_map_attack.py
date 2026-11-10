"""Record native phase transitions for a MAP weapon in an isolated fixture."""
import argparse,ctypes as C,json,sys
from pathlib import Path
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_core import Core
from scripts.verify import verify_named_attacks as replay

OUT=ROOT/'test_current/combat/map_probe'

class ProbeCore(Core):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs);self.trace=[];self.tick=0;self.last_phase=None
        self.api.retro_get_memory_data.restype=C.c_void_p;self.ram=self.api.retro_get_memory_data(2)
    def run(self):
        result=super().run();self.tick+=1
        phase=(C.c_uint32.from_address(self.ram+0xa6f38).value,C.c_uint32.from_address(self.ram+0x1e7a10).value)
        if phase!=self.last_phase:
            self.last_phase=phase;self.trace.append(dict(tick=self.tick,phase=phase))
            Image.fromarray(self.native).save(OUT/f'phase_{len(self.trace)-1:02}.png')
        if self.tick<=600 and self.tick%45==0:Image.fromarray(self.native).save(OUT/f'step_{self.tick}.png')
        return result
    def close(self):
        Image.fromarray(self.native).save(OUT/'final.png');self.save(OUT/'final.state')
        (OUT/'phases.json').write_text(json.dumps(self.trace,indent=2));super().close()

def main():
    p=argparse.ArgumentParser();p.add_argument('--unit',type=int,default=2);p.add_argument('--weapon-index',type=int,default=2);args=p.parse_args()
    OUT.mkdir(exist_ok=True);replay.Core=ProbeCore
    sys.argv=[sys.argv[0],'--units',str(args.unit),'--weapon-indices',str(args.weapon_index),'--unit-output','--diagnostic-unlock','--frames','4000','--native-render']
    replay.main()

if __name__=='__main__':main()
