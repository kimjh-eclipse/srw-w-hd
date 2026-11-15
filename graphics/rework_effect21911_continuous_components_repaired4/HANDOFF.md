# observed_effect_fresh_21911 문제4/4 후보 인계

- 대상94224~94227은 fixed current classified와 실제 live atlas observed_effect_fresh_21911이 같은 미교체항목임을 확인했습니다. 해당atlas는 총4개로 정상보존대상0개입니다. 다른atlas/바인딩은 수정하지 않았습니다.
- 최종 입력 final_flat_contract.json,native_atlas.png(96×32),candidate_atlas.png(384×128)입니다. candidate SHA256=cbaa51a45f74be911d81a103546f5d36eace8b166b457b1fe71e0ff0ada7fc9c. 파일SHA는 sha256.json입니다.
- actual_observed_contract.json은 next_confirmed_fx_source/art_fresh_21911/source_contract.json 원자료 그대로입니다. 실제 index raw와전체16색BGR555/RGB,관측state/frame/OAM/observation 목록을 유지합니다. 최종flat에도 full16pal과state/frame및source_box/atlas_box를 따로 기록했습니다. 미관측추정추가 없음.
- 실제 상태 native_weapon_source_19_67/unit19_weapon67_source.state:94224/94225/94226 +570,94227 +575입니다. 여러프레임/OAM관측별칭은 actual_observed_contract.json을 확인하세요.
- 신규 builtin image_gen으로 각 독립 source그림4개를 새로 그렸습니다. 분홍외곽/옅은분홍/흰분홍하이라이트의실제palette계열을 지켰습니다. 기존그림의 가늘어진선 대신 원본의 넓은채움·큰꺾임·고리·가지폭을 유지했습니다.
- 원본의 큰angular bends는 유지하고 micro pixelstairs는 새연속round-corner경계로 다시그렸습니다. 픽셀계단을 흐린확대그림이 아닙니다. 94224 첫계단형생성은 rejected_pixelstairs_94224.png로 보존하고 재생성했습니다.
- native 연결성분수는94224=3,94225=1,94226=4,94227=1입니다. 각생성의대응자체RGBA만crop/resize하여 작은분리성분까지원래bbox에등록했습니다(geometry_registration.json). 94224의분리파편/작은점,94226의작은점3개를 모두유지합니다. source/fullpal의직접겹침영역은없습니다.
- 원본RGB/alpha전사,생성알파문턱삭제,morphology,다른팔레트재색칠/alpha차용없음. 자체생성RGBA alpha연속값을crop/resize하며 유지합니다.
- 후보및NullCache prepare preflight4개모두 flags=[]입니다(candidate_geometry.json,prepare_geometry.json). IoU .872/.896/.853/.845,미칠최대.076,밖0입니다. 자동통과는공식QA가아닙니다.
- PartsRenderer.prepare_texture4개전부nonempty 및native index/alpha/RGB 입력일치(production_report.json)입니다. 실제최종좌표로검사했습니다.
- 수동회색RGBA비교 manual_native_before_candidate_prepare.png는왼쪽부터원본/기존live/새후보/prepare입니다. 넓은분홍채움,분리성분위치,고리/꺾임이유지됨을확인했습니다. alpha0RGB잔여를실색으로오인하지않았습니다. 원본의격자내부색배치를연속하이라이트로해석한차이는남아있습니다.
- 라이브러리/sqlite/공유코드/코어/EXE/배포/푸시/모니터/게임창미수정. 중앙설치·굽기·동일도구검사및Claude독립시각/실제게임검증대기입니다.
