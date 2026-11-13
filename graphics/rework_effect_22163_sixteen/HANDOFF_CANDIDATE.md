# IMG22163 실제 관측16개 신규 연속 효과 후보

## 인수 결과

- 후보 `candidate_22163_sixteen.png`:512×512 RGBA. 4배, 위512×256은실제팔레트0, 아래는실제팔레트1.
- `candidate_contract.json`:16개RGB전용등록계약. resource=None,dynamic_palette=False,effect_part=True. x/y는합친후보좌표,source_x/source_y는원본IMG좌표. source_atlas_y는각팔레트아틀라스원래y.
- `native_22163_sixteen.png`:128×128 native비교배치.
- `native_candidate_comparison.png`:왼실제원본/오른신규후보.

라이브그림·library·구운DB·코어·EXE·사용자창에손대지않았다.설치/굽기/최종HD재생은미실행.

## 관측 계약

fixture: test_current/combat/named_attacks/unit_299/mechanical_cutin_141.state

실제Core unknown_snapshot에서16고유RGB변형을수집했다. 전체180프레임합계3776회관측,첫등장+54/55/56. 실제팔레트2종이며한색은중간청색/옅은청록핵,다른색은옅은청록/흰핵이다. PLT추정없음.

observed_contract.json에실제15bit팔레트,RGB hash,index hash,압축raw index,OAM index/attr0,1,2,fixture,frame이있다. oam_descriptor[3:6]이세원시OAM속성이다. obj_raw한바이트값은계약으로쓰지않는다.

16개모두raw index배열이ROM IMG22163의해당crop과완전일치했다. 단실제ROM주소를코어에서추적하지않았으므로리소스alias가능성은남으며resource=None+실제RGB hash로등록한다.

순수원본장면 unit299_pure_native_54/55/56.png를별도Core hd=False로저장했다.

범위: 원본IMG192×64중실제보인x64..192의연속128×64구간을두실제팔레트로각각그렸다. 누락목록24개중이fixture에실제로등장한16개전부다. IMG전체모든다른자세/팔레트완료를뜻하지않는다.

## 새 그림 방식

imagegen스킬built-in사용.팔레트0과1을각각독립호출해새그림을만들었다. 기존그림재색칠로두번째팔레트를채우지않았다.

연속128×64효과아틀라스전체를먼저그린뒤4배512×256로등록했다. 내부32texel단위절단면마다따로테두리를그리지않았다. prepare_continuous.py는생성alpha를기준으로미세반투명찌꺼기를정리하고전체캔버스를리사이즈했다. 원본alpha stamping/원본RGB복사/슬롯강제색칠없음.

원출력: generated_palette0.png,generated_palette1.png. 각실제원본참조는reference_palette0.png,reference_palette1.png.

프롬프트공통: 모든스파이크/틈/색영역위치고정,연속효과를한번에그림,내부32texel절단선윤곽금지,검은테두리/추가분기/새폭발/입자추가금지,실제투명. 팔레트0은중청색바깥과옅은cyan핵(흰색대체금지),팔레트1은옅은cyan바깥과흰핵을명시. 원본계단선만부드러운애니메이션곡선으로교체.

## 후보 검사

- audit_candidates.py: 공식audit_all_parts.analyse를후보메모리stub에적용.16개flags0,키색flags0.
- IoU최소0.747,최대0.968. colour_bad최대0.179,대부분0.1미만.
- audit_palette.py: 공식material_map/palette_alignment에실제2palette/index계약적용.16개misplaced0/wrong_colour_share0/slots_never_native없음.
- candidate_quality.json/candidate_palette_alignment.json에세부값.
- 임계값및공식검사모듈변경없음.

시각비교에서는두팔레트의흰핵/청색핵구별이유지되고,주변빈영역에초록키색이나새입자증식이보이지않는다. 얇은전기선의커브가원본보다둥글고왼쪽burst내부작은홈의모양도차이가있다. 원본의선폭과완전동일하다는뜻은아니다.

## 다음

16개를RGB전용으로일괄설치→exact16굽기→같은unit299 fixture180프레임,순수원본+54/55/56 대조→16전체실제HD/준비후held/vanish/UI전면검사필요. 효과태그는기체용10%guard에서제외하되미준비원본fallback은유지해야한다.
