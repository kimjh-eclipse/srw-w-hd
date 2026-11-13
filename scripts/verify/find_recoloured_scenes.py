"""Find retained battle scenes where HD parts are recoloured, and compare the two slot rules there.

A part is recoloured when the game shows it with a palette other than the
one its picture was painted for. For each state this replays some frames,
counts such parts on screen, and renders the frame twice: slots chosen by
colour alone (the earlier rule) and slots anchored to the native texels
around each pixel. Reads only; writes test_current/parts/recolour_scenes/.
"""
import argparse,json,queue,sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image


def recoloured(parts,row,palette):
    """True when sprite() will recolour this OBJ (same test as the renderer)."""
    binding=int(row[0]);spec=parts.bindings[binding-1]
    if not spec.get('dynamic_palette') or palette is None or int(row[4])==int(spec['hash']):return False
    colours=np.asarray(palette,dtype='uint32');target=np.stack([(colours&31)*255//31,((colours>>5)&31)*255//31,((colours>>10)&31)*255//31],-1)
    original=np.asarray(spec.get('original_palette_rgb',parts.source_palette))
    return len(original)==len(target) and not np.array_equal(target[1:],original[1:])


def main():
    parser=argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--frames',type=int,default=90);parser.add_argument('--every',type=int,default=30);parser.add_argument('--per-unit',type=int,default=2);parser.add_argument('--sheets',type=int,default=16)
    args=parser.parse_args();out=ROOT/'test_current/parts/recolour_scenes';out.mkdir(parents=True,exist_ok=True)
    for old in out.glob('*.png'):old.unlink()
    import hd_parts
    from hd_core import Core
    from hd_renderer import HDRenderer
    catalog=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text(encoding='utf-8'))
    names={u['unit_id']:(u.get('name_ko') or u['name_ja']) for u in catalog['units']};weapons={w['weapon_id']:(w.get('name_ko') or w['name_ja']) for w in catalog['weapons']}
    by_unit=defaultdict(list)
    for path in sorted((ROOT/'test_current/combat/named_attacks').rglob('*.state')):
        unit=next((int(p[5:]) for p in path.parts if p.startswith('unit_') and p[5:].isdigit()),None)
        if unit is not None and path.stem!='capture':by_unit[unit].append(path)
    states=[(unit,path) for unit,paths in sorted(by_unit.items()) for path in paths[::max(1,len(paths)//args.per_unit)][:args.per_unit]]
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',user_dir=out/'isolated_saves')
    renderer=HDRenderer(async_parts=False,dynamic_parts=False,gpu_composition=True);renderer.set_resolution(768);parts=renderer.parts_renderer;parts.load_baked()
    class Ready:
        ready_generation=-1
        def __init__(self):self.dynamic_bindings=queue.SimpleQueue()
        def ready_bindings(self):return self.values
    ready=Ready();ready.values=np.fromiter((alias for source in parts.baked for alias in parts.ready_aliases.get(source,())),dtype='uint32');rows=[]
    def draw(anchor):
        hd_parts.RECOLOUR_ANCHOR=anchor;parts.cache.clear();parts.material_maps.clear()
        sub=(core.sub_parts,core.sub_owners,core.sub_oam.raw,core.sub_palettes,core.sub_ids,core.sub_priorities) if core.sub_bridge else None
        top=renderer.render_top(core.native,core.ids,tuple(core.hd),paused=False,parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,
            backgrounds=core.backgrounds,unknown=None,bg_layout=core.bg_layout,sub_parts=sub,cutin_layers=core.cutin_layers,effect_foreground=core.effect_foreground,window=getattr(core,'window',None))
        return np.asarray(top)[:,:,:3].copy()
    try:
        for index,(unit,state) in enumerate(states,1):
            core.load(state,refresh_code=True)
            weapon=next((int(p.split('_')[1]) for p in state.parts if p.startswith('weapon_') and p.endswith('_capture')),None)
            for frame in range(args.frames):
                core.set_ready_parts(ready);core.run();core.audio.clear()
                if frame%args.every!=args.every-1:continue
                shown=[i for i in range(128) if core.parts[i,0] and not int(core.parts[i,7])&0x80000000]
                changed=[i for i in shown if recoloured(parts,core.parts[i],core.part_palettes[i])]
                if not changed:
                    rows.append(dict(unit=unit,name=names.get(unit),weapon=weapon,weapon_name=weapons.get(weapon),state=str(state.relative_to(ROOT)),frame=frame,hd_parts=len(shown),recoloured=0));continue
                before=draw(False);after=draw(True);delta=np.abs(before.astype('int16')-after.astype('int16')).max(2);differ=int((delta>=24).sum())
                row=dict(unit=unit,name=names.get(unit),weapon=weapon,weapon_name=weapons.get(weapon),state=str(state.relative_to(ROOT)),frame=frame,hd_parts=len(shown),recoloured=len(changed),
                    bindings=sorted({int(core.parts[i,0]) for i in changed}),atlases=sorted({parts.bindings[int(core.parts[i,0])-1].get('atlas_id','base') for i in changed}),pixels_changed_by_fix=differ)
                rows.append(row);row['_pictures']=(np.asarray(core.native)[:192].copy(),before,after)
            if index%20==0:print(index,'/',len(states),flush=True)
    finally:core.close();parts.close()
    hits=sorted((row for row in rows if row['recoloured']),key=lambda row:-row['pixels_changed_by_fix'])
    for rank,row in enumerate(hits[:args.sheets]):
        native,before,after=row['_pictures'];sheet=np.concatenate([np.asarray(Image.fromarray(native).resize((768,576),Image.Resampling.NEAREST)),before,after],1)
        row['sheet']=f"{rank:02d}_unit{row['unit']}_w{row['weapon']}_f{row['frame']:03d}.png";Image.fromarray(sheet).resize((1152,288)).save(out/row['sheet'])
    for row in rows:row.pop('_pictures',None)
    units=defaultdict(lambda:dict(frames=0,recoloured_frames=0,max_parts=0,max_changed=0))
    for row in rows:
        entry=units[row['unit']];entry['frames']+=1;entry['recoloured_frames']+=bool(row['recoloured']);entry['max_parts']=max(entry['max_parts'],row['recoloured']);entry['max_changed']=max(entry['max_changed'],row.get('pixels_changed_by_fix',0))
    report=dict(states=len(states),frames_checked=len(rows),frames_with_recoloured_parts=len(hits),units_checked=len(units),units_with_recolouring=sum(1 for e in units.values() if e['recoloured_frames']),
        by_unit=sorted(({'unit':u,'name':names.get(u),**e} for u,e in units.items() if e['recoloured_frames']),key=lambda e:-e['max_changed']),frames=hits)
    (out/'report.json').write_text(json.dumps(report,indent=1,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('by_unit','frames')},ensure_ascii=False))
    for entry in report['by_unit'][:25]:print(entry)
    for row in hits[:args.sheets]:print(row['sheet'],row['name'],row['weapon_name'],'frame',row['frame'],'recoloured',row['recoloured'],'changed px',row['pixels_changed_by_fix'],row['atlases'][:3])


if __name__=='__main__':main()
