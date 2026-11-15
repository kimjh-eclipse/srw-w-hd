# 12281 형상교정2개 그림/계약 인계

## 범위와역할

- 대상94157/94162는원본/현재live의시각대조에서실제형태결함을확인했습니다. 정상부모와직접겹치는동일child는없습니다. atlas총46개중정상44개자체RGBA/metadata를byte비교보존했습니다(preserved_normal44_metadata.json).
- 역할변경을반영하여Codex는새그림/원천/좌표계약만작성했습니다. **PartsRenderer.prepare_texture,전체/공식검사도구,설치,연결,굽기는실행하지않았습니다.** 중앙library/DB/materialcache/manifest수정없음. Claude가준비·연결·굽기·검증을진행해야합니다.

## 최종그림/원본계약

- 파일 final_flat_contract.json,native_atlas.png(256×224),candidate_atlas.png(1024×896)입니다. 후보SHA256=6fead30716cf5c465944a5b2df49432999f40d5e76743de72632d4c0bede5e9f. sha256.json에계약/원본/생성SHA를고정했습니다.
- actual_observed_contract.json은native_weapon_source_250_1026/fx_production/art_12281/source_contract.json 원자료그대로입니다. raw index/full16 BGR555/RGB/state/frame/OAM을보존합니다. 94157=unit250_weapon1026_source.state+525,94162=같은state+540입니다. 미관측추정없음.
- source_candidate_matches는IMG12281에서각각[232,64]/[64,0]이며기존owner_confirmed=true입니다. legacy resource=None는임의수정하지않고그대로둡니다. finalflat에source_image_candidate=12281과source_candidate_matches,별도source_box/atlas_box를유지했습니다.
- 실제사용색은index1 #CDFFF6 한색이며index0만투명입니다. 두그림은전체불투명단색타일이아닌형상이지만,새색·질감의HD이득으로계수하지않고**형태교정2개**로명시합니다.

## 새그림내용

- 94157:기존그림의원본없는상단가로줄을제거한새단일민트대각띠입니다. 아래왼쪽~위오른쪽의원래위치와폭을유지하며새연속직선경계로생성했습니다. hairline/추가ray/흰core/외부glow를요청하지않았습니다.
- 94162:기존큰V형꺾임을대신해왼위좁은끝에서오른쪽넓은절단끝으로이어지는단순연속쐐기를새로생성했습니다. 첫생성은pixelstairs가남아 rejected_94162_pixelstairs.png로보존하고채택하지않았습니다.
- 생성원천 generated_94157.png,generated_94162.png는builtin image_gen입니다. own_rgba_ID.png는생성자체bbox crop/resize로원래bbox에등록한그림입니다(own_geometry_registration.json). 원본RGB/mask/alpha전사,재색칠/알파문턱삭제/morphology없음.
- manual_native_before_new_art.png는왼쪽부터원본/기존live/새후보의회색RGBA합성입니다. source각도/끝모양/새연속경계를수동대조했습니다. alpha0RGB잔여를실색으로오인하지않았습니다.

## 남은위험/검증대기

- 단색실루엣의새이미지생성이므로원본픽셀계단을연속직선으로해석한차이가있습니다. 94157채워진두께와94162끝폭은Claude의실제4배좌표검증이필요합니다. 생성재질의미세민트명암은원본단색과차이가있을수있으나자동재색칠로덮지않았습니다.
- 사전geometry/prepare/동일도구전수검사/게임재생을하지않았습니다. 자동통과나공식QA완료주장없음. 연결·굽기·검증은Claude전담입니다.
