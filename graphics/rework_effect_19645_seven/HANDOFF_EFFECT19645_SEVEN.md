# 실제 관측 효과19645 7개 신규 그림 후보

## 인수 파일

- `candidate_19645_seven.png`: 512×256 RGBA, 4배. 4열×2행의32texel셀7개, 마지막셀비어있음.
- `candidate_19645_contract.json`: 등록용7개. x/y는후보아틀라스좌표,source_x/source_y는원본19645좌표. actual RGB hash+index_pixels+actual original_palette_rgb 포함. effect_part=True, dynamic_palette=False, resource=None 권장(같은index의팔레트변형을각각새로제작한RGB전용연결).
- `native_19645_seven.png`: 128×64 실제Core색 기준 네이티브 배치.
- `native_candidate_comparison.png`: 왼쪽실제색원본,오른쪽새후보.

라이브 그림/라이브러리/DB/공유코드/기본DLL/사용자테스트창에 손대지 않았다. 설치·굽기·실제 후보재생은 메인 담당.

## 선정과 실제 계약

missing_export가추천한21798/20498/22163/21948/19645를Core에서조사했다. 보유fixture 재현은22163이16실제RGB변형,19645가7개여서 작은완결관측묶음19645선택. 19645전체40개누락을모두그린것은아니고,이fixture에서실제로등장한7개전부를그렸다.

보유실제fixture:
`test_current/combat/named_attacks/unit_333/diagnostic_preview/mechanical_cutin_168.state`

실제Core snapshot의index_pixels/16색15bit palette/RGBhash/OAM index/attr0,1,2를기록했다. `effect_19645_contract.json`의oam_descriptor[3:6]이원시OAM세속성이다. obj_raw한바이트문자열은OAM계약으로쓰지않는다.

- +28: 노랑불꽃파편2개, 흰핵/분홍외곽충격광2개
- +32: 노랑외곽/진홍내부충격광2개(같은모양다른실제팔레트)
- +46: 흰색→라벤더가는궤적1개
- 180프레임관측의7고유 RGB/hash가모두반영됨.
- PLT19644로색을추정하지않았다. 실제 snapshot.palette에서만RGB를만들었다.
- `source_provenance.json`:7개 raw index배열이ROM IMG19645각crop과완전일치,ROM sha포함. ROM실주소추적은안했으므로동일tile alias가능성은남음. 등록은resource=None+실제RGB hash로제한.
- `unit333_pure_native_28/32/46.png`:별도Core hd=False 순수원본장면.

## 제작

imagegen스킬의built-in툴사용. 7개를2×4참조패널로모아한번에신규제작했으며팔레트가다른충격광은색보정으로재사용하지않고각패널을각각그리게했다. 원출력 `effect_19645_seven_generated.png`.

핵심프롬프트: 같은7패널/7실루엣/실제색영역유지,흰핵·노랑·분홍·진홍각위치고정,절단면외곽선없음,알파투명,새폭발추가금지,라벤더궤적은분기없는가느다란선. 전체프롬프트는툴기록에있음.

prepare_seven.py는생성그림자체알파로조각을잘라원본bbox에등록했다.파편은원본위치계약에맞는별도생성조각을선택했다.원본RGB복사/알파마스크찍기/코드색칠메우기없음.

## 검사

`audit_seven.py`는공식audit_all_parts.analyse를등록전후보에메모리stub로연결해실행(구운DB읽기검증은아님).

- 7개품질flags0,키색flags0.
- IoU각각1.000,1.000,0.931,0.857,0.860,0.914,0.754.
- colour_bad0~0.069.
- `audit_seven_palette.py`:실제palette+index contract로공식material_map/palette_alignment검사.7개misplaced0,wrong_colour_share0,slots_never_native없음.
- 각RGB변형별새그림이므로실행시dynamic recolour를켜서다른팔레트빈칸에재활용하지않을것.

눈으로원본/후보비교: 흰/진홍/노랑핵영역위치는유지됨,절단면에검은외곽선추가없음.원본각진파편이약간둥근보석처럼표현되며아주작은부품의원본색차이를완전히동일하게유지하지는않음.얇은라벤더궤적은원본보다매끈함.점수통과를화질완전승인으로해석하지말것.

## 다음 단계

메인이7개RGB전용으로일괄등록→정확7개재굽기→unit333동일fixture재생.통째로원본유지guard가이효과를기체로묶지않도록effect_part=True확인.이child는후보제작·계약·검사까지완료했으며실제HD재생을확인했다고보고하지않는다.
