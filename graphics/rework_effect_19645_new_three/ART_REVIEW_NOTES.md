# IMG19645 실제 관측 추가 슬래시 3개 / Claude 인계

## 설치 후보
candidate_19645_three.png: native96×32의4배384×128 RGBA. new_candidate_contract.json3개만설치. atlas observed_effect_19645_three_slashes/exactRGB/static/effect=True/resourceNone.
1.612676352 source19645(208,32,32,32),atlas(0,0,32,32)
2.1614621463 source19645(224,16,16,16),atlas(32,0,16,16)
3.1172039251 source19645(176,32,32,32),atlas(64,0,32,32)

## 실제 계약과 기존 보존
capture_19645_22378_next.py가공통capture_rendered_obj_contracts를사용했다. unit4135개,unit19/299/333 각1개총8보유fixture의각180frame을제작원본수집했다. 캐시index/palette와renderedOAM, boundhash/attrs일치를확인하고source19645/22378 사각형rawindex배열과대조했다. VRAM/obj_debug픽셀읽기없음. sourceROM주소역추적이아니므로resourceNone.
19645관측10개중기존7개는w/h+indexbytes+사용paletteRGB7/7동일로보존. 기존그림품질판정/재교체없음.22378은이번fixture범위에서관측없었으며누락없음이라고판정하지않는다.

observed_contract.json10개및new_candidate_contract.json3개각각실제palette_15bit/RGB,index_pixels,source좌표,OAMattrs/engine/좌표/변형,state/firstframe포함. source팔레트와현재팔레트는해당실제캐시값으로같고다른effect그림을재색칠하지않았다.
612676352/1172039251은비투명색2개([238,255,246],[205,222,238])뿐인가느다란slash. 색수가적다고제외하지않고수집/제작했다.1614621463은슬롯7~10의연한청회색~라벤더다.

## 새 그림
reference_new_three.png를imagegen built-in으로새로생성. generated_slashes_three.png를자체alpha threshold/minmax정리후4배축소. 그림을코드로다시칠하거나nativeRGB/alpha를찍지않았다. 첫두crop은같은길고얇은신규그림을연속좌표에서분할하고,세번째는반대방향큰흰slash다. 내부절단선윤곽추가없음.

남은차이: source의계단은매끈한대각선으로바뀌고왼쪽끝/위쪽라벤더끝이원본보다가늘어졌을수있다. 생성저농도fringe를정리했으나가는선손실/과채도색점/흰핵폭은공식판정하지않았다. 오른쪽큰slash의미묘한곡률/좌표차이가원본과맞는지Claude확인필요. 생산원본계약확인과그림생성만했으며품질/재생합격을의미하지않는다.

## Claude 확인
state:test_current/combat/named_attacks/unit_333/diagnostic_preview/mechanical_cutin_168.state
+34:612676352와1614621463; +46:1172039251. 정확OAM/coords는계약참조. 기존7개보존과신규3개HD등장,가는선두께/현팔레트색/절단접합,앞뒤와UI/준비후held·소실확인.
공식audit/독립QA/후보HD재생없음. liveart/library/DB/core/EXE/설정변경없음. root등록·굽기후Claude검증대기.
