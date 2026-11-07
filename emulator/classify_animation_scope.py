"""Record the visual review without confusing inventory candidates with coverage."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'graphics/animation_parts'
source=json.loads((OUT/'sources.json').read_text())
ranges=[(6995,19534),(20304,20321),(20566,20620),(20957,20978),(21025,21051),(21376,21474),(21498,21621)]
excluded={7152:'pilot eye strip',7406:'pilot eye strip',13983:'Japanese text panel'}
items=[]
for item in source['items']:
    i=item['image']
    if i in excluded:kind='excluded';reason=excluded[i]
    elif any(a<=i<=b for a,b in ranges):kind='mechanical_or_attached_effect';reason='Visual review: battle mecha, weapons, mechanical cut-ins, or attached animation effects'
    elif 6098<=i<=6440:kind='map_icon';reason='Small map units; separate from top battle-screen scope'
    elif i<6995:kind='human_ui_background_or_cg';reason='Visual review: UI, pilot/story pictures, backgrounds, or gallery CG'
    else:kind='standalone_effect';reason='Visual review: attack flashes, projectiles, particles, or debris'
    items.append(dict(image=i,classification=kind,reason=reason,review_sheet=f'review_{source["items"].index(item)//48:02}.png'))
result=dict(reviewed_contact_sheets=source['pages'],candidate_images=len(items),items=items,source_associations_fully_verified=False,all_attacks_complete=False,note='These labels guide extraction. They are not evidence that every candidate part is used by a real animation. Out-of-bounds PAT references remain unresolved.')
(OUT/'scope_review.json').write_text(json.dumps(result,indent=2));print(json.dumps(dict(candidate_images=len(items),mechanical_candidates=sum(p['classification']=='mechanical_or_attached_effect' for p in items),all_attacks_complete=False)))
