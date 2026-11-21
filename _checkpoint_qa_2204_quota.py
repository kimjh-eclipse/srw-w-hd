import json, hashlib
from pathlib import Path
from datetime import datetime
R=Path('C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
now=datetime.now().isoformat()
for s in (1,2):
    f=R/f'unit_94/robot_set/SHEETS/sheet_{s:02d}'; q=f/'qa_20261116_2204'
    prompt=('Use case: style-transfer. Fresh QA correction unit94 sheet%02d. '%s+
      ('Exactly NINE original items in original three rows/three columns, commonbase first, source1312x1236. ' if s==1 else 'Exactly TWO original items in ONE ROW, commonbase LEFT and pose09 RIGHT, source856x448. ')+
      'Image1 actual DeSmuME xBRZ1.4 ARGB4x primary contour guide; Image2 unfiltered ORIGINAL final authority for geometry/palette/tiny boundaries/scale/placement; Image3 mandatory Deathscythe STYLE ONLY broad clean painted planes, smooth fluent ink, simple bold cel shadows, few highlights, vivid ORIGINAL colors. No borrowed anatomy or palette. '+
      'Source compact mechanical robot has tall dark BLUE cylindrical helmet, large vertical RED/ORANGE forehead sensor, tiny original PALECYAN eye/visor marks, long slender SILVER diagonal horn extending upper right, small segmented SILVER mechanical mask, BLUE armor with SILVER/GREY shoulders, forearms and layered legs, RED/orange soles with tiny yellow/orange toe marks. Exact source eye count and sensor color, horn length/angle, head/chest proportions, open finger/claw count and limb ownership, shoulder/hand attachment, leg bends and asymmetric foot directions. No extra eyes/horns/human face/generic fists or boots/new panels/chrome/greebles/rivets/bevels/mosaic. '+
      ('CRITICAL pose02 TOP RIGHT: preserve original bright PALECYAN illuminated/highlight areas on the arm across the torso and waist, exact original outlines, extent, pale values and tiny bright cyan divisions; these must not turn into ordinary medium/dark blue armor. Other poses retain their own exact highlights/armor palette and original gestures: topmiddle and midright leaning with hand raised, middleleft open hand right, bottommiddle raised bent arm left. ' if s==1 else
       'CRITICAL pose09 RIGHT: original forearms/hands held together across waist/chest have bright PALECYAN illuminated/highlight areas on arms and waist; retain original light pale values, exact small boundaries and source extent, not ordinary blue armor. This is localized source light/highlight and does not recolor all armor or add parts. LEFT commonbase retains its raised bent arm and down/right arm, exact original palette and pose. ')+
      'Preserve exact original full sheet positions, individual footprints and native scale, empty gaps, actual source pose-specific occlusions and tiny disconnected parts. No added effects or weapons. True alpha0 outside bodies and original gaps, no background/text/grid/borders. High resolution, original full canvas aspect. '+
      ('Later add own fresh sheet01 as Image4 DESIGN ONLY, never pose/layout/effect borrowing.' if s==2 else ''))
    refs=[{'role':role,'path':p.as_posix(),'sha256':sha(p)} for role,p in [
      ('primary_actual_4xbrz_filtered',f/'reference_4xbrz.png'),
      ('original_geometry_palette_small_parts_layout',f/'native_sheet_4x.png'),
      ('mandatory_deathscythe_style_only',R/'unit_1/robot_set/pose_00/generated.png')]]
    write(q/'generation_request_xbrz.json',dict(prompt=prompt,refs=refs,transparent_background=True,status='ready_not_called_usage_limit_reached' if s==1 else 'prepared_waiting_own_first_reference_usage_limit_reached',qa_source='docs/HANDOFF_TO_CODEX_8.md 2026-11-16 22:04 unit94',source_and_filter_viewed=True))
scope={49:[1],50:[1,2,3,4],52:[1,3],53:[1],54:[1,2],55:[3],57:[2],86:[1,2,3],90:[1,2],93:[1,2,3],94:[1,2]}
delivered=[]; pending=[]; bad=[]
for u,ss in scope.items():
 for s in ss:
    q=R/f'unit_{u}/robot_set/SHEETS/sheet_{s:02d}/qa_20261116_2204'
    st=q/'STYLE_VERSION.json'; req=q/'generation_request_xbrz.json'
    if st.exists():
        d=json.loads(st.read_text(encoding='utf-8-sig'))
        for k in ('candidate','raw','raw_immutable'):
            item=d.get(k)
            if item and sha(item['path'])!=item['sha256']: bad.append({'unit':u,'sheet':s,'kind':k})
        delivered.append(dict(unit=u,sheet=s,folder=str(q),status=d['status'],candidate=d['candidate'],pixels_per_native_pixel=d['pixels_per_native_pixel'],slot_holds=d.get('slot_holds',[])))
    else:
        d=json.loads(req.read_text(encoding='utf-8-sig'))
        for ref in d['refs']:
            if sha(ref['path'])!=ref['sha256']: bad.append({'unit':u,'sheet':s,'kind':'prepared_ref'})
        pending.append(dict(unit=u,sheet=s,request=str(req),status=d['status'],reference_count=len(d['refs']),needs_own_first_reference='waiting_own_first' in d['status']))
quota=dict(type='usage_limit_reached',reset_epoch=1794912194,reset_kst='2026-11-17T19:43:14+09:00',no_fallback=True)
state=dict(updated=now,status='incomplete_generation_quota_blocked',delivered_count=len(delivered),pending_count=len(pending),deliveries=delivered,pending=pending,hash_errors=bad,running_cells=[],quota=quota,priority='Resume remaining QA first, then284~299;276~282 root-owned;283=269 otheragent;284=277 root duplicate;275 and294 exact proof done;467 delegated do not touch')
write(R/'ROBOT_QA_2204_49_94_STATUS.json',state)
write(R/'ROBOT_XBRZ_RUNNING_CELLS.json',dict(updated=now,cells=[],all_returns_recovered=True,quota=quota,next_checkpoint='ROBOT_QA_2204_49_94_STATUS.json'))
p=R/'ROBOT_XBRZ_RESUME_FINAL_STATUS.json'; old=json.loads(p.read_text(encoding='utf-8-sig'));old.update(updated=now,status='incomplete_QA_generation_quota_blocked',qa_checkpoint=str(R/'ROBOT_QA_2204_49_94_STATUS.json'),running_cells=[],quota=quota);write(p,old)
assert len(delivered)==13 and len(pending)==9 and not bad,(len(delivered),len(pending),bad)
text='''\n\n## 2026-11-16 final quota checkpoint\n13 QA plates delivered as unreviewed RAW/candidates; 9 remain ungenerated. All candidate/generated/immutable RAW SHA values and all queued reference SHA values verified; no missing return and no running imagegen call. No original, layout, runtime or ROM modified.\n\nRemaining: 86 sheet02/03,90 sheet01/02,93 sheet01/02/03,94 sheet01/02. Every remaining plate has observed original/native and actual4xBRZ refs plus generation_request_xbrz.json on disk. 86sheet02/03 already include own fresh first design-only reference. 90sheet02,93sheet02/03,94sheet02 MUST append the corresponding NEW sheet01 design-only path/SHA before calling; their first sheet has not been generated. 90sheet01 failed HTTP429 and has NO RAW.\n\nUnit94 observed source: bright pale cyan areas are localized arm/waist highlights in pose02 (sheet01 top right) and pose09 (sheet02 right); preserve original extent and pale values, not medium-blue armor. Tiny eye marks, red/orange tall helmet sensor and silver long upper-right horn remain original. Unit93 tall crest needs simple2~3planes and pale skyblue reflection; physical green tethers must not be mistaken for alpha motion. Unit86 white/grey trails are separate translucent motion, physical shield remains solid.\n\nIMPORTANT unit50 sheet03 TOP LEFT commonbase pose06 is SLOT HOLD: original left deck gun omitted. Do not split/use this commonbase slot. Other8target poses offered only for Claude review; use/verify sheet01 commonbase separately. Every unit50 plate still needs exact tiny orange floating dot gap and bridge BLUE window QA. Nothing is declared approved or installed.\n\nBuilt-in imagegen daily quota reset reported 2026-11-17 19:43:14 KST (epoch1794912194). No API/CLI/model fallback and no additional imagegen calls. Resume using ROBOT_QA_2204_49_94_STATUS.json; running cells empty. 284~299 remains subsequent work, 467 delegated elsewhere.\n'''
with (R/'ROBOT_QA_2204_49_94_HANDOFF.md').open('a',encoding='utf-8') as f:f.write(text)
print(json.dumps(dict(delivered=len(delivered),pending=len(pending),hash_errors=bad,checkpoint=str(R/'ROBOT_QA_2204_49_94_STATUS.json')),ensure_ascii=False))
