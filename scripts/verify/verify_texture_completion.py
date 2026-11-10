"""Completed textures must enter the cache even after their OBJ disappears."""
import json,queue,sys
from concurrent.futures import Future
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_parts import PartsRenderer

def renderer():
    r=PartsRenderer.__new__(PartsRenderer);r.dynamic_parts=True;r.unmapped_pending={};r.unmapped_misses={}
    r.bindings=[];r.prepared={};r.registration_stats={};r.runtime_requests={};r.ready_aliases={}
    r.palette_luts={};r.dynamic_bindings=queue.SimpleQueue();r.ready_generation=0
    return r

def main():
    r=renderer();done=Future();done.set_result((Image.new('RGBA',(8,8)),dict(reference_hash=123,reference_palette_rgb=[[0,0,0]]*16),None,None))
    r.unmapped_pending[(12,34)]=(done,('request',),dict(w=1,h=1));r.schedule_unknown(None)
    assert not r.unmapped_pending and 1 in r.prepared
    assert r.dynamic_bindings.get_nowait()==(12,34,1)
    failed=Future();failed.set_result((None,dict(reason='unpainted native tile'),None,None))
    r.unmapped_pending[(56,78)]=(failed,('request',),dict(w=1,h=1));r.schedule_unknown(None)
    assert not r.unmapped_pending and r.unmapped_misses[(56,78)]['reason']=='unpainted native tile'
    result=dict(completed_texture_retained_without_visible_obj=True,unpainted_result_drained_without_visible_obj=True)
    (ROOT/'test_current/parts/texture_completion.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))

if __name__=='__main__':main()
