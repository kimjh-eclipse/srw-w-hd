# 22338 후보 12개 / 겹침 판정대기 3개 — Claude 인계

## 현재 상태
원래 observed_effect_22338_new24 문제15개 중12개를 자체새RGBA로 제작했습니다. 49개 원본성분을 32개 motif(3개 생성panel)로 분리하고 원본bbox자리로등록하여 작은빨강점/가는선도빠뜨리지않았습니다. 같은source하위사각92473/92474는큰그림의공유crop을사용합니다. 원본 target밖과정상9+보류3영역은기존픽셀과동일합니다.

## 보류3 — 정상큰부모와동일그림
92462/92468/92470은정상92453의raw하위영역과실제full16palette가동일합니다. SQLite RO로부모의구운crop과작은바인딩구운결과를읽었습니다. 작은결과와부모crop은 AA끝15/37/39픽셀차이뿐이고 원본격자면적/미칠지표는각각완전히같습니다. 92468만분리성분cleanup1개기록이있으나면적지표는동일합니다. 작은불꽃입자는존재하지만도트사각형이좁은타원으로바뀌어엄격면적지표에걸렸습니다. 독립그림으로변경하면정상부모와불일치하므로새그림/완료수에서제외하고그대로보존했습니다. 실제결함/엄격지표차이판정은Claude대기입니다. normal_parent_child_native_baked.png와normal_parent_child_readonly_comparison.json참조.

## 입력·좌표·준비
새12개는actualcachedrawbytes/크기/indexhash/전체16색BGR555/RGBhash모두확인했습니다. source_candidate_palette_integrity12.json에state/frame/OAM증거가있습니다. candidatebox와spec는기존live좌표,source_box는별도입니다. normalized계약자체의좌표로NullCache prepare12를실행했고direct기존좌표준비와RGBA모두같고maxA255입니다.
원본mask/RGBstamp·alpha문턱삭제·형태학없음입니다. flatmaterial은자체생성내부RGBAcrop을사용,생성alpha253~254를255로덮지않았습니다. 다른팔레트alpha차용없습니다.

## 남은위험
원본격자IoU .887~1.0/면적.962~1.0. 큰섬광92455의얇은가시/끝AA차이가남으며작은기하성분은원본계단을다소유지해보일수있습니다. 원본연속rgba와팔레트모양을기계적으로확인했지만실제HD재생/공식audit정상판정은하지않았습니다. 겹침보류3도완료로세지않습니다.

## 인계
ready_replacement12.json과normalized_installer_contract12.json. candidate_atlas.png/native_atlas.png. 새atlas effect22338_components_repaired12로same12ID만교체하고정상9/보류3의기존atlas·ID·키는변경하지마십시오. native_prepared_pairs12.png에원본/실제메모리준비후후보쌍이있습니다. 공유code/live/DB/EXE변경없음,root설치/Claude검증대기입니다.
