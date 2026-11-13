"""Visible unknowns must get a worker slot before speculative neighbors."""
import sys,json
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_parts import PartsRenderer
from hd_renderer import character_cutin
class Pending:
    def done(self):return False
class Executor:
    def __init__(self):self.calls=[]
    def submit(self,*args):self.calls.append(args);return Pending()
def main():
    p=PartsRenderer.__new__(PartsRenderer);p.dynamic_parts=True;p.async_prepare=True;p.pending={1:Pending()};p.unmapped_pending={};p.unmapped_seen=set();p.unmapped_misses={};p.executor=Executor()
    p.collect_prepared=lambda:p.pending.clear()
    rows=np.zeros((1,8),dtype='uint32');rows[0,[0,1,2,6,7]]=[123,8,8,456,789]
    pixels=np.arange(64,dtype='uint8')[None,:]%4;palettes=np.arange(16,dtype='uint16')[None,:]
    p.schedule_unknown((rows,pixels,palettes))
    assert len(p.executor.calls)==1,'Completed prefetch stranded a visible unknown'
    assert p.unmapped_on_screen
    p.pending.clear();p.prefetch_related(np.array([[99]],dtype='uint32'))
    assert len(p.executor.calls)==1,'Speculative prefetch overtook the visible unknown'
    p.schedule_unknown(None);assert not p.unmapped_on_screen
    specs=json.loads((ROOT/'graphics/cutins_library.json').read_text())['cutins']
    compact=[s for s in specs if s.get('name','').startswith('compact_pilot_bg_')]
    assert len(compact)==11 and all(character_cutin(s,s['id']) for s in compact)
    assert not character_cutin({'name':'cloud','image':'mechanical_cutins/cloud.png'},168)
    report=dict(completed_prefetch_drained=True,visible_unknown_precedes_prefetch=True,empty_frame_resets_priority=True,compact_pilots=len(compact),cloud_not_promoted=True)
    (ROOT/'test_current/parts/visible_priority.json').write_text(json.dumps(report,indent=2));print(report)
if __name__=='__main__':main()
