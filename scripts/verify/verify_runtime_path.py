"""Replay retained attack states through the path the player actually runs.

Unlike the paused single-frame fixtures, this keeps the game running and uses
asynchronous texture preparation, runtime tile assembly and the delayed
ready-part handshake of the real player. It reports outcomes, not whether a
picture was produced:

* vanished  - the core hid a native part and no HD picture replaced it
* loading   - a known part is still shown natively while its HD art loads
              (the first frames after a state load are excluded: the core
              has not yet received any ready set)
* held      - a part whose art is ready, shown natively because its unit is
              only partly painted (the 10% rule in the core)
* unbound   - a native OBJ on screen has no HD art connected at all
* rescued   - a vanish that the renderer prevented by preparing art in place

A scene is never reported as verified. FAIL and INCOMPLETE are objective;
REVIEW means only that no defect this tool can measure was found, so the saved
native/HD pair still has to be looked at.
"""
import argparse,json,shutil,sys,time,queue
from collections import deque
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_core import Core
from hd_renderer import HDRenderer

DEFAULT_UNITS=(139,145,155,214,226,227,249,261,297,299,375,390,413,417)


class Ready:
    """The ready set as the emulation process sees it, some frames late."""
    def __init__(self):self.ready_generation=-1;self.values=[];self.dynamic_bindings=queue.SimpleQueue()
    def ready_bindings(self):return self.values


def picture(image):
    image=image.to_pil() if hasattr(image,'to_pil') else image
    return image.convert('RGB')


def main():
    parser=argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--frames',type=int,default=180)
    parser.add_argument('--lag',type=int,default=3,help='frames between a texture becoming ready and the core learning of it')
    parser.add_argument('--per-unit',type=int,default=2)
    parser.add_argument('--units',type=int,nargs='*',default=list(DEFAULT_UNITS))
    parser.add_argument('--state',type=Path,nargs='*',default=[],help='replay only these states')
    parser.add_argument('--evict',type=int,default=0,help='drop every prepared texture at this frame, as a stage reset or cache eviction does')
    parser.add_argument('--no-rescue',action='store_true',help='measure the unguarded behaviour')
    parser.add_argument('--name',default='regression')
    parser.add_argument('--save-frames',type=int,nargs='*',default=[],help='also retain these running frame offsets for visual review')
    args=parser.parse_args()
    out=ROOT/'test_current/combat/runtime_path'/args.name
    if out.exists():shutil.rmtree(out)
    out.mkdir(parents=True)
    fixtures=[(-1,path.resolve()) for path in args.state]
    if not fixtures:
        base=ROOT/'test_current/combat/named_attacks'
        for uid in args.units:
            states=[p for p in sorted((base/f'unit_{uid}').rglob('*.state')) if p.stem!='capture']
            step=max(1,len(states)//max(1,args.per_unit))
            fixtures.extend((uid,p) for p in states[::step][:args.per_unit])
        fixtures.extend((-1,ROOT/'test_current/combat'/name) for name in ('getter_cutin.state','golion_cutin.state'))
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'isolated_saves')
    renderer=HDRenderer(async_parts=True,dynamic_parts=core.dynamic_bridge,gpu_composition=True);renderer.set_resolution(768)
    parts=renderer.parts_renderer
    if args.no_rescue:parts.rescue=lambda *_:None
    # The texture process loads the whole part catalog before its first
    # answer. Measure that once instead of charging it to the first scene.
    from texture_preparation import prepare_task
    first=next(i for i,b in enumerate(parts.bindings,1) if not b.get('source_binding') and not b.get('lazy'))
    warm=time.perf_counter();parts.executor.submit(prepare_task,first,parts.bindings[first-1]['w'],parts.bindings[first-1]['h'],0).result(timeout=300)
    worker_start=round(time.perf_counter()-warm,1);print('texture worker start',worker_start,'s',flush=True)
    rows=[];gaps={}
    try:
        for uid,state in fixtures:
            if not state.exists():continue
            core.load(state);ready=Ready();history=deque();sent=-1;advertised=set()
            frames=[];worst=None;vanish_shot=None;started=time.perf_counter();deadline=started;cutins=set()
            for frame in range(args.frames):
                if len(history)>args.lag:
                    generation,values,dynamic=history.popleft()
                    ready.ready_generation=generation
                    if values is not None:ready.values=values;advertised=set(values)
                    for item in dynamic:ready.dynamic_bindings.put(item)
                core.set_ready_parts(ready)
                core.run();core.audio.clear()
                if args.evict and frame==args.evict:parts.prepared.clear()
                unknown=core.unknown_snapshot()
                sub=(core.sub_parts,core.sub_owners,core.sub_oam.raw,core.sub_palettes,core.sub_ids,core.sub_priorities) if core.sub_bridge else None
                image=renderer.render_top(core.native,core.ids,tuple(core.hd),paused=False,parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,
                    part_palettes=core.part_palettes,backgrounds=core.backgrounds,unknown=unknown,bg_layout=core.bg_layout,sub_parts=sub,cutin_layers=core.cutin_layers,effect_foreground=core.effect_foreground)
                if frame in args.save_frames:
                    picture(image).save(out/f'{state.stem}_running_{frame}.png')
                top=parts.last_stats
                renderer.render_bottom(core.native,tuple(core.hd))
                bottom=parts.last_stats if parts.last_stats is not top else {}
                dynamic=[]
                while True:
                    try:dynamic.append(parts.dynamic_bindings.get_nowait())
                    except queue.Empty:break
                history.append((parts.ready_generation,parts.ready_bindings() if parts.ready_generation!=sent else None,dynamic));sent=parts.ready_generation
                unbound=0;unbound_count=0
                if unknown is not None:
                    main_rows=unknown[0][:128];used=main_rows[:,0]!=0
                    unbound_count=int(used.sum());unbound=int((main_rows[used,1].astype('int64')*main_rows[used,2]).sum())
                if unknown is not None:
                    # Native OBJ with no HD art: the redraw list for the artist.
                    for index in np.flatnonzero(unknown[0][:,0]):
                        entry=unknown[0][index];w,h=int(entry[1]),int(entry[2]);key=(int(entry[0]),int(entry[7]),w,h)
                        gap=gaps.get(key)
                        if gap is None:gap=gaps[key]=dict(pixels=unknown[1][index,:w*h].copy(),palette=unknown[2][index].copy(),frames=0,scenes={},screen='sub' if index>=128 else 'main')
                        gap['frames']+=1;gap['scenes'][f'{uid}/{state.stem}']=gap['scenes'].get(f'{uid}/{state.stem}',0)+1
                # A part shown natively is either still loading, or ready but
                # held back because its unit is only partly painted.
                held=loading=0
                for entry in core.parts[core.parts[:,0]>0]:
                    if int(entry[7])&0x80000000:
                        spec=parts.bindings[int(entry[0])-1];size=spec['w']*spec['h']
                        if int(entry[0]) in advertised:held+=size
                        else:loading+=size
                cutins.update(int(p[0]) for p in core.cutin_layers if p[0])
                row=dict(beam_tie_pixels=top.get('beam_tie_pixels',0),frame=frame,ms=round((time.perf_counter()-started)*1000),drawn=top['drawn_area'],waiting=top['waiting_area'],vanished=top['vanished_area'],vanished_parts=top['vanished'],
                    rescued=top['rescued']+bottom.get('rescued',0),unbound=unbound,unbound_parts=unbound_count,sub_vanished=bottom.get('vanished_area',0),sub_waiting=bottom.get('waiting_area',0),
                    pending=len(parts.pending)+len(parts.unmapped_pending),held=held,loading=loading)
                frames.append(row)
                total=row['drawn']+row['waiting']+row['unbound']
                score=(row['waiting']+row['unbound'])/total if total and row['drawn'] else 0
                if row['vanished'] or row['sub_vanished']:
                    if vanish_shot is None:vanish_shot=(frame,core.native[:192].copy(),picture(image))
                elif score and (worst is None or score>worst[0]):worst=(score,frame,core.native[:192].copy(),picture(image))
                last=(core.native[:192].copy(),image)
                deadline+=1/59.8261;delay=deadline-time.perf_counter()
                if delay>0:time.sleep(delay)
                else:deadline=time.perf_counter()
            name=f'{uid}_{state.stem}' if uid>=0 else state.stem
            def save(tag,frame,native,hd):
                sheet=Image.new('RGB',(768*2,576));sheet.paste(Image.fromarray(native).resize((768,576),Image.Resampling.NEAREST),(0,0));sheet.paste(hd.resize((768,576)),(768,0))
                path=out/f'{name}_{tag}_{frame}.png';sheet.save(path);return path.relative_to(ROOT).as_posix()
            pictures={}
            if vanish_shot:pictures['vanished']=save('vanished',*vanish_shot)
            if worst:pictures['mixed']=save('mixed',*worst[1:])
            pictures['last']=save('last',args.frames-1,last[0],picture(last[1]))
            vanished=[f for f in frames if f['vanished'] or f['sub_vanished']]
            waiting=[f for f in frames if f['waiting'] or f['sub_waiting']]
            # After loading settles, whatever is still native has no HD art.
            settled=frames[len(frames)//2:]
            hd=sum(f['drawn'] for f in settled);native=sum(f['waiting']+f['unbound'] for f in settled)
            share=hd/(hd+native) if hd+native else None
            verdict='FAIL' if vanished else 'NO_HD_PARTS' if share is None else 'INCOMPLETE' if share<.98 else 'REVIEW'
            rows.append(dict(unit=uid,state=state.relative_to(ROOT).as_posix(),verdict=verdict,frames=len(frames),cutins=sorted(cutins),
                vanished_frames=len(vanished),vanished_area_max=max((f['vanished']+f['sub_vanished'] for f in frames),default=0),rescued=sum(f['rescued'] for f in frames),
                beam_tie_frames=sum(f['beam_tie_pixels']>0 for f in frames),beam_tie_pixels=sum(f['beam_tie_pixels'] for f in frames),waiting_frames=len(waiting),
                loading_frames=sum(1 for f in frames[args.lag+2:] if f['loading']),loading_ms=max((f['ms'] for f in frames[args.lag+2:] if f['loading']),default=0),
                held_frames=sum(1 for f in frames if f['held']),
                mixed_frames=sum(1 for f in frames if f['drawn'] and (f['waiting'] or f['unbound'])),hd_area_share_settled=None if share is None else round(share,3),
                unbound_parts_max=max(f['unbound_parts'] for f in frames),hd_flips=sum(1 for x,y in zip(frames,frames[1:]) if bool(x['drawn'])!=bool(y['drawn'])),timeline=[[f['frame'],f['drawn'],f['waiting'],f['vanished'],f['unbound'],f['pending']] for f in frames[::max(1,len(frames)//30)]],render_fps=round(len(frames)/(time.perf_counter()-started),1),pictures=pictures))
            print(verdict,name,{k:rows[-1][k] for k in ('vanished_frames','rescued','loading_frames','loading_ms','held_frames','mixed_frames','hd_area_share_settled','hd_flips')},flush=True)
        ordered=sorted(gaps.items(),key=lambda item:-item[1]['frames']*item[0][2]*item[0][3]);listing=[]
        sheet=Image.new('RGB',(16*72,max(1,(min(len(ordered),640)+15)//16)*72),(40,44,52))
        for number,((index_hash,material,w,h),gap) in enumerate(ordered):
            listing.append(dict(rank=number+1,index_hash=index_hash,material=material,w=w,h=h,screen=gap['screen'],frames=gap['frames'],scenes=gap['scenes']))
            if number>=640:continue
            colors=gap['palette'].astype('uint32');rgb=np.stack([(colors&31)*255//31,((colors>>5)&31)*255//31,((colors>>10)&31)*255//31],-1).astype('uint8')
            indices=gap['pixels'].reshape(h,w);tile=rgb[indices&15];tile[indices==0]=(40,44,52)
            sheet.paste(Image.fromarray(tile),(number%16*72+4,number//16*72+4))
        sheet.save(out/'gaps.png')
        (out/'gaps.json').write_text(json.dumps(dict(note='Native OBJ seen with no HD art, largest on-screen share first. gaps.png shows the first 640 in rank order, 16 per row, at native size. BG pictures and effects drawn on BG layers are not listed here.',dynamic_assembly_failures=len(parts.unmapped_misses),prepare_errors={str(k):v for k,v in parts.prepare_errors.items()},parts=listing),indent=1,ensure_ascii=False),encoding='utf-8')
        counts={}
        for row in rows:counts[row['verdict']]=counts.get(row['verdict'],0)+1
        report=dict(scope=__doc__,texture_worker_start_seconds=worker_start,timeline_columns=['frame','hd_area','waiting_area','vanished_area','unbound_area','pending_jobs'],core=core.core_path,unit_fallback_percent=__import__('os').environ.get('SRWW_UNIT_FALLBACK_PERCENT'),options=dict(frames=args.frames,lag=args.lag,evict=args.evict,rescue=not args.no_rescue),verdicts=counts,all_campaign_scenes_verified=False,rows=rows)
        (out/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
        print('Outcome',counts,'- REVIEW scenes still need a person to look at the saved pairs')
    finally:core.close();parts.close()


if __name__=='__main__':main()
