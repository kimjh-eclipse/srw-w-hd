# IMG21657 붉은색 2 실제 변형 / 신규16개 그림

## 설치
candidate_red_pair.png768×512 RGBA(native192×128,4배). **red_new_candidate_contract.json16개만등록.** red_candidate_contract.json25개는전체문맥이고기존9는red_keep_existing_contract.json으로유지. atlas observed_effect_21657_red_pair / resourceNone / exactRGB/static/effectTrue.
위64native행은white-core/red-edge,아래는red-core/white-edge. 각각실제원본참조로별도imagegen생성(generated_red_0/1.png). 노란그림을재색칠한것이아니다.

## 제작 입력/팔레트
같은capture_21657_22419.py 공통cachedOBJ/renderedOAM계약에서실제안정붉은2팔레트25개를선정. 실제sourceindex배열과일치. rawindex/sourcecoords/현재palette_15bit 및RGB/OAMattrs/변환/engine/좌표/state/frame포함. actual신규16개는전부core row0/unbound였다. 기존indexed연결된OAM을새미연결로세지않았다.
원본참조palette와현재실제palette는각각candidate행original_palette_rgb/palette_15bit에같은관측값으로기록. 위slot1~6은white,[255,205,205],[255,156,156],[255,98,106],[255,49,57],[255,0,8],아래는역순. 등록은독립그림이며다른effect이미지재색칠없음.

## 기존9개 보존
red_existing_overlap_proof.json:9/9 w/h+원본indexbytes+실제사용targetpalette색일치. 구형alias는원참조의고유source팔레트로index복원. **alias의original_palette_rgb는그림원색, palette_rgb는현재target색**이므로target색대조는palette_rgb우선으로했다(실제hd_parts.py target_palette분기와같음). 두값을증거에따로기록. 원본palette만보고색이안맞는기체로오판해재교체하지않았다. 그림품질판정은하지않고기존9유지.

## 새 그림의 범위/제한
fullsheet를연속제작하고등록crop을원래좌표에서잘라공유. 생성자체낮은alpha주변찌꺼기만정리후4배축소. nativeRGBfill/nativealpha찍기/다른색그림재색칠안함.
전체시트의particle구역은생성본에서구슬같아졌지만**신규16개crop에는x80..112,y0..32 particle구역이없다.** 그부위기존계약9개는유지하며이번생성시트particle를설치하지않는다. 전체25를새시트로덮어쓰지말것. 오른쪽bottom176,32fill도신규16범위밖이다.

남은미검증: slash가원본보다뾰족점/내부띠가늘고곡률·폭이달라졌다. red강한색은실제팔레트정상색이나일부아주작은분홍/자홍generated점은프린지일수있다. source에서다른파츠에이어지는crop끝의얇은윤곽선/밝기이음새,원본과새그림크기가맞는지는Claude판정필수. 생성했다는것을실재생합격으로표시하지않는다.

## Claude 실제 장면 큐
- test_current/combat/named_attacks/unit_214/mechanical_cutin_168.state: +37, +39, +41, +43, +45, +47, +48
- test_current/combat/named_attacks/unit_280/mechanical_cutin_168.state: +110, +111

정확OAM/좌표/변환/첫관측은JSON우선. 신규16HD등장·기존9보존·두붉은색배열·sourcecrop연결/앞뒤/UI/준비후held·소실을확인할것. 21657의시간연속fade계약전체를이번16으로해소했다고세지말것.

liveart/library/DB/core/EXE/플레이어설정변경없음. 공식audit/독립QA/후보HD재생없음. root등록·굽기후Claude확인대기.
