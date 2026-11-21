# Codex 이미지 생성 재개 — 2026-11-18 22:15 KST 이후

실제 builtin imagegen 성공으로 이전 한도 해제 확인. 전체 완료 아님. 재색칠/코드 리사이즈/알파 마스킹 없이 RAW 원본을 보존한다.

## 즉시 전달: 마징카이저 몸체 23021

- RAW: `test_current/parts/cutin_requests/mazinkaiser_fire_blaster/codex_prepared_20261118/generated_23021.png`
- SHA256: `03cc67da5593422505be639672bc4deae210426dbedda5ee42d168f3d44fcc8a`
- 실제 1672×941, 요청 1024×576. 크기 불일치로 candidate_23021.png 자동 발행하지 않음. RAW 그대로 Claude에게 정렬/분할 검토 요청.
- 참조/프롬프트/시도 이력: 같은 폴더 `request_23021.json`. 이전 20:05 quota 실패는 과거 이력이며 이번 실제 생성은 성공.
- 검증: 원본 큰 왼쪽 여백, 두 주먹/어깨/팔 연결, 은색 얼굴과 뿔, 빨강 V 가슴과 빨간 보석, 아래쪽 크롭. 청록 V 광원은 별도 런타임이므로 몸체에 넣지 않았음. 외곽 A0와 원본 내부 불투명 검정은 구분해 확인할 것. 캔버스/픽셀 위치/디자인 일치 및 게임 적용은 아직 통과로 표시하지 않음.
- 알파 실제 범위0..255. A>0 bbox [49,39,1626,941]로 보이는 본체보다 넓은 미세 알파 잔재 가능성도 Claude 확인 필요. 자동 마스킹/삭제하지 않았음. 24557 배경은 전체A255 확인.

## 병렬 진행

### 추가 RAW: 히페리온124 B 5자세

- `test_current/parts/pose_packets/unit_124/robot_set/qa_source_pale_pods_b_20261118/generated.png` (1028×1529), SHA `2e91dc8f1b51d255bc3934938b6e15e45bf7d83c9813edd2ad2106da3b207f34`.
- 16/22,24/26,28/EMPTY 순서. pale pod 외면과 원본 green eyes/red crest 새 그림. 상세 손발/팔 연결·크기·A0 검증은 local HANDOFF_GENERATED_20261118.md대로.

### 추가 RAW: 델피니움172 2자세

- `test_current/parts/pose_packets/unit_172/robot_set/codex_prepared_redraw_20261118/generated.png` (1737×906), SHA `f83e676115e70d3234d1259d72fc6813545106466e7e0e19320dbf43408158f0`.
- LEFT01 / RIGHT00. source852×444의 비율/해상도 gate 통과. 아래 hook 길이, 상단 block/tubes, 내부 구멍·접합과 registration은 local HANDOFF_GENERATED_20261118.md대로 Claude 확인.

### 추가 RAW: 마징카이저 배경24557

- `test_current/parts/cutin_requests/mazinkaiser_fire_blaster/codex_prepared_20261118/generated_24557.png`
- SHA256 `204ee25f8465cde1fe01953e16a1a1c5051ec4429ef09551ac55f50c11791b47`, 실제1774×887 / 요청1024×512. 원본 비율2:1 유지, 크기만 달라 RAW로 인계. 재크기/마스크 하지 않음.
- 원본 olive/yellow-green 가로 흐름의 smooth redraw. Claude 확인: LEFT로 스크롤 시 좌우 반복 이음새, 원본 어두운 상단과 밝은 하단 범위, 전체 불투명. 본체와 합치지 않은 BG2 독립 레이어.
- 컷인 담당 22864/26391/23591도 실제 생성 성공. 해당 작업 local handoff가 원본 경로/출력크기/QA를 기록한다. 전체5개 컷인 레이어 RAW가 생성됐지만 정렬·설치·게임 검증 완료는 아님.

- 컷인: 22864 source_only / 26391 / 23591, root는 24557 배경.
- 로봇: 214 sheet02/03, 247 magenta plate01~03. 이미 납품한 214 sheet01/24706·13 제외.
- 신규 금색: unit334 weapon1360 obj000, frames234/236 원본 발견. own gold 원본으로 생성, 기존 보라/빨강 HD 재색칠 금지. affine 설치 매핑은 Claude 확인 필요.
- affine 중앙44판은 재확인 당시 원본·layout·contract 일치. builder 진행 중이므로 실제 생성 전 재검사 필수. unit131 빈 target을 새로 그리지 않음.
- unit1 critical body, unit130 및 unit213/40 새 정확한 조합 packet은 아직 미발견. 기존 다른 팔레트로 대체하지 않음.

각 작업 담당은 RAW가 나올 때마다 자체 local handoff/맵을 저장하고 후속 작업을 계속한다. 컷인별 레이어 분리 유지. ROM/렌더러/설치 변경은 Claude 담당.

## 재개 작업의 결과 인덱스

- `test_current/parts/CODEX_IMAGE_RESUME_DELIVERY_INDEX_20261118.json`: 중앙 affine44판 및 이후 새로 준비된 자기팔레트 판들의 결과 존재/타깃/핸드오프 경로. 재집계되는 현재 인덱스. RAW 존재는 그림 구조·픽셀 정렬·설치 합격을 뜻하지 않는다.
- `test_current/parts/CUTIN_AGENT_GENERATED_INDEX_20261118.json`: 크루제22864/배경26391/무대23591.
- `test_current/parts/AFFINE_CUTIN_AGENT_GENERATED_INDEX_20261118.json`: 특수 형태/부분 파츠 affine 그룹. 수정본도 따로 기록.
- `test_current/parts/AFFINE_GENERATION_DELIVERIES_AFFINE_AGENT_20261118.json`: affine 일반군과 muzzle/lower-block 집중 수정.
- 214 sheet02/03 및247 magenta plate01~03: 각 `HANDOFF_RESUME_20261118.md` / `GENERATION_DELIVERY_20261118_RESUME.json`, 모두 실제 생성 완료·설치 검증 대기.
- root affine80/109/113/119 및 후속143/144/147/156/166/167/187/190/191/217/220~225/228/231 등: 각 중앙prepared 폴더 `DELIVERY_ROOT_20261118.json` / `HANDOFF_ROOT_20261118.md`.
- 119은 `PREFERRED_TARGETS_ROOT_20261118.json` 우선: 첫 RAW 로봇4개 + source-only 마지막 평면효과2개. 중간흐림수정본 제외, 마지막판의 도트 로봇영역 설치금지. 내부 A252~253 원본완전불투명과 차이는 별도 검증.
- 224/225도 preferred target map 우선: 첫 RAW로봇a00/a01 + source-only 교정RAW a02분리조각. 첫RAWa02의가짜검정그릴제외, 후속판의도트로봇영역설치금지.
- 222/223은unit221의 target별원본RGBA/색/크기가완전히같아RAW공유. **RAW배치는unit221이므로수신unit배치를RAW에바로씌우지말것**,localDELIVERY의 source_pose→receiver_pose맵사용.
- 50 초광폭원본의생성aspect문제는comparison제외2ship위아래source-only보조packet으로재생성하여해결방향인계. 보조RAW의원본좌표맵/localHANDOFF참조,원래wholewidecandidate그대로설치금지.
- 신규143/144/147은 중앙44 이후 추가로 source snapshot/원본 재구성·actual4xBRZ를 검증하고 각각 자기팔레트로 새 그림 생성 중. 143teal을144blue로 재색칠하지 않음.

## 23:07 현재 확대된 affine 인계 범위

- live builder 현재254판/894target. 이 중 RAW존재173판, 미생성81판(진행중 포함). 생성 저장 수량은 구조/알파/좌표/설치 통과 수량이 아니다. 최신수량·경로는 `test_current/parts/AFFINE_LIVE_REMAINING_AFTER_RESUME_20261118.json`.
- root301~330 및361~380 a01도 순차인계, a02+추가판은 별도원본스냅샷/직접관찰/actual4xBRZ 후 fresh 생성중. 동계열 다른색 HD 재색칠 없음.
- unit361 a01 검정뷰어의 초록 후광은 readonlygray 실제합성에서 사라지고 확인한 배경표본A0이다. 보이는 RGB만으로 불투명 후광으로 판정하지 말것. `READONLY_GRAY_diagnostic.jpg`는 검사전용이며 설치파일이 아니다.
- 327/329/364 a01은 RAW 비율 gate 실패이므로 그대로설치 금지. 원본레이아웃 대조/target별 정렬·구조 검증필요. RAW파일은 원형보존, 강제리사이즈/마스크/색변환 없음.
- 379 a01은 원본 둥근눈/검정동공을 명시한 새판을 전달했음. 별개 기존 pose01/02/03/08 검수사항 전체가 해결됐다고 간주하지 말고 계약별 확인.
- 원본파츠가 분리된 판은 조립상태로 상상하지 않도록 요청. 324/330/361/367/368 등 a02+의 flatWHITE실루엣/십자·색평면·분리파츠는 각각 원본 literal형태/빈틈/opaque BLACK을 확인할 것.

### 324 flat 교정 및 동일 원본 타깃 공유

- 324 sheet_a02 flat a12/a13/a15와 sheet_a03 flat a18/a19/a21은 source-only 추가 생성 후 readonlygray에서 금속 테두리/후광 없이 흰 평면과 A0틈 확인. 각 local PREFERRED_TARGETS_ROOT_20261118.json 우선: 로봇은 첫 RAW, 평면은 교정 RAW. 교정판의 도트 로봇영역 설치 금지.
- 이 flat target과 native RGBA/size가 완전히 같은 타깃은 323/361/367/368에도 있으며, 복사/재색칠 없이 같은 보존RAW를 donor layout으로 추출하여 연결 가능. 전체 proof `test_current/parts/affine_codex_prepared_20261118/IDENTICAL_FLAT_TARGET_REUSE_PROOF_ROOT_20261118.json`; 각 local preferred map이 receiver→donor pose/layout을 명시. 392는 담당 교정판/맵 유지, 이 proof는 보조 정보.
- 324 a04 source-only교정판은 a31 WHITE target이 통째로 누락되어 a31에 사용금지. a26 mint평면도 gradient 잔존으로 아직 원본flat색 검수/추가교정필요. 이 둘은 해결로 세지 않는다. 로봇영역은 첫RAW 유지.

### 23:22 flat 누락 보완과 별도 좌표 맵

- 324 a31 WHITE 누락은 `unit_324/sheet_a04/flat_pose_a31_only/RAW_imagegen.png` 추가 단독 생성으로 보완. 회색합성에서 순백평면+구멍/분리하단조각 확인. supplement_layout.json + request receiver_mapping으로 native원위치 연결. generated code편집 없음.
- 원본 동일RGBA+크기 proof가 성립하는368 a04 target에도 이 단독RAW를 공유하도록 local preferred map을 갱신. Donor layout은 wholea04가 아니라 단독 supplement_layout임에 주의.
- 324 a26 mint 단독RAW도 추가생성했으나 색평면 안 gradient가 잔존. 이 부분은 flat색 일치 해결로 세지 않으며 원형RAW와 local검수메모를 인계. 강제색치환/마스킹하지 않음.
- 327/329/364 비율 실패판은 comparison을 제외하고 원본4배 target만 세로로 배열한 보조판 생성중. 원본 그림픽셀은 변경하지 않고 source배치만 바꾼것. 원본/보조좌표 맵을 request에 동봉. 기존wide판을그대로설치하지말것.

### 기존 반려 재대조와 다음 그림

- affine 신판만으로 기존 pose_NN 반려가 모두 해결됐다고 세지 않는다. 담당이 EYE_REVIEW와 이후RAW/계약/override를 대조 중.
- unit375 기존 qa_2345_repair_20261117은 pose16을 포함한 후속RAW가 이미 있으므로 검수대기. 반려04/12 speedline은별도 `qa_speedlines_04_12_20261118` 원본+actual4xBRZ 준비/직접view 후 생성중. base00comparison, targets04/12. 원본 줄 길이·두께·색·빈틈을 줄이지 않도록명시.
- 38011은 palette0/runtime_original_preserved_no_hd_recolour 명시된 색변형정책제외로 신규그림불필요. 38008/12 최신 얼굴·하체·별무늬반려와19별무늬는원본직접검토/새그림진행.

### unit362 기존15필수반려 새그림

- 기존candidate mtime만달라졌으나 SHA가candidate_v1과동일해 후속교정으로계산하면안됨. `test_current/parts/native_redraw_20261118/unit_362/sheet_01~03/`에 원본NN4재구성검증+actual4xBRZ+공통style 참조로 새그림 진행.
- targets: 01판00..07,02판09만,03판17/20/21/22/23/24. 비교14와 나머지기존accept는교체대상아님.
- 필수QA: 25%과대배율/칸끝 잘림 해결 여부, gun/손끝/노란봉끝/등짐/발끝 원본여백, 초록 낫궤적/3속도선이 금속다발·삼지창이 되지 않고 외곽선없는반투명원본범위로 남는지. 4xBRZ가합쳐놓은부분을실물부품으로해석하지않을것. RAW저장수량과QA완료분리.

### 새 RAW 즉시인계

- 327/329/364 보조판 모두 실제생성·저장, 비율/최소해상도 gate 통과. 각 parent `PREFERRED_SUPPLEMENT_ROOT_20261118.json` 우선(본체구조/정렬 합격아님). comparison없는 native target원크기 세로배치, 보조layout→원래target 위치맵 사용.
- unit37504/12 새판 `pose_packets/unit_375/robot_set/qa_speedlines_04_12_20261118/RAW_imagegen.png`, SHA e2b65ed870495c74bf3ddc63ca8b835a4a9df3195900b4bc5a352bcbb18eabee,930×1691. 원본704×1280비율유지/해상도gate통과, base00 TOP /04 MIDDLE /12 BOTTOM. native 줄 끝·빈틈/실제알파/원본색·발모양/팔·방패소유/정렬 독립검수. 후보·설치없음.

### 23:36 반려 재작화 RAW 실시간 수령

- root 새 납품 색인 `test_current/parts/NATIVE_ROOT_REDRAW_DELIVERY_INDEX_20261118.json`을 추가. 기존 rejected candidate는 보존하고 새 RAW만 sibling으로 저장. 사전검사 실패 원인은 기존candidate존재였으며 입력/참조/계약 SHA변경은 없었음. 실패3건은 실제생성호출0회.
- 362 sheet01 RAW 저장 SHA902a54b683805eabe7889a91eb9b49e13dde162c6a2bd5e48941320b0f6520cb,1345×1170, alpha0..255. READONLY_GRAY_raw.jpg는 검수전용 실제알파 회색합성. 검정뷰의 초록노이즈는 회색에서 사라짐. 궤적은 검은외곽선 없는 연녹색으로 보이나 원본범위/투명도/정렬 및 팔·발·봉 접합은 Claude독립검수 필요. 비교14는교체대상아님.
- native223 누락8자세와225 기존필수반려5자세(00/06/09/11/15) 원본 및 actual4xBRZ 직접비교후3판 새그림중. 22500 흰속도선,06 검은motionstate,09/11/15 흰어깨·팔·등짝 색복원이 핵심. 다른accept/comparison은교체금지.
- 담당 새납품:118/121/123/244는 NORMAL_REJECT_CUTIN_AGENT_GENERATED_INDEX_20261118.json,36525/36708/39220·25·27은 normal_redraw_remaining_20261118/ 각 HANDOFF참조. 원본분할·설치·게임확인 아직미완료이며 RAW수를통과수로세지않음.

### 23:41 원본 반려 28자세 새 RAW 6판 수령

- native root362 15자세3판 +223 8자세1판 +225 5자세2판 모두 RAW 수령. RAW 경로/크기/알파/SHA/대상 목록은 NATIVE_ROOT_REDRAW_DELIVERY_INDEX_20261118.json. gate는 최소해상도/비율검사만이며 구조나 게임합격을 뜻하지 않음.
- 225 sheet01은 00/06만 사용, sheet02는09/11/15만 사용. accepted/comparison 영역은 새RAW에 있어도 교체금지. 00 흰속도선이 여전히 금속베벨처럼 읽히는지,06검은속도선 끝/밀도는 별도검수. 362 sheet02는09만 사용. source 밖 알파0로 생긴 검정뷰 노이즈는 실제alpha 회색합성으로 구별할것.
- affine live254판 중252 RAW 있음(23:37 inventory); 미생성386a01/a02는 기존 콘텐츠 제한 중단 항목이며 재시도/우회없음. 이 카운트는 원본native 기존반려180자세/설치완료와 별개임.
- root 추가담당29104/15/17 보라날개 해칭과29508/11·29607/10 연속펀치 잔상. source 원본4배와actual4xBRZ을 target만 새배열(최대4칸) 준비. 타기체 색칠/원본도트복붙 없이 새작화중. 295/296은 자체원본RGBA 동일 여부를 입증한 뒤에만 같은 그림사용 검토.

### 23:44 연속펀치 잔상 새작화

- 29508/11은 sheet_selected/RAW_imagegen.png 수령(SHA e5f5910b9a930c36eab8601eb88c3ef73d8933e6f315f8735289fd7a10a58cda). main주먹과 겹친 연속잔상을 함께 새로그림. 원본의 좁은 범위·끝밀도/투명도 및 자세별 높이 Claude검수필요.
- 29607/10은 29508/11과 nativeRGBA+크기+좌표 모두 완전동일 proof로 RAW를 byte그대로 공유(새호출0,색변환0). unit296/sheet_selected/IDENTICAL_SOURCE_PROOF.json 및 HANDOFF_ROOT_20261118.md에295 donor pose/좌표→296 pose map. RAW_reused_identical_295.png 사용, 다른palette그림의재색칠아님.

- 29104/15/17 새RAW 저장 SHA56bab0b259ebedb04b0762c63cfee68481a371c312243008a975330da002aca9,1569×1003. native_redraw_20261118/unit_291/sheet_selected/RAW_imagegen.png. READONLY_GRAY_raw.jpg에서 날개선 사이 알파빈틈과 깔끔한 주황본체 확인. 원본도트해칭 복붙없음. 줄의 정확한 개수/밀도·기울기·원래범위/원본크기와 포즈별관절·발은 Claude검수. 위치맵은 새 sheet_selected/layout_snapshot.json이며 옛 SHEETS/sheet_01~03 좌표와 다르므로 혼용금지.

### 추가 원본 구조/효과 반려 진행

- root 30000/30505·09/30901·08/32500·07/32620 원본 target만 2~3칸 새배열, 실제4xBRZ+공통STYLE 참조 확인후 새생성 중. 각각 source native/contractSHA와 새로운 layout_snapshot을동봉.
- 300 앞쪽파란소용돌이,325회색넓은궤적,326초승달은 반투명선만 그려 정합에서 원본도트로 채워지던 것이 반려원인. 새지시는 원본 opaque줄 내부 A255 + source구멍 A0, 넓이·범위 보존. 강제alpha칠/원본덧붙이기 없이 새로그림.
- 305 짧은팔속도선은 금속갈퀴로해석금지.309는target마다 촉수눈 정확히6개(좌3우3), 가슴앞/오른어깨 위 마지막눈과 좌하 붉은손이 핵심. 모두 새RAW수령후 별도검수필요.

### 23:48 새 RAW 검수 메모

- 300/305/309/325/326 5판 모두 RAW 저장 및 NATIVE_ROOT_REDRAW_DELIVERY_INDEX_20261118.json 수록.309 두target에 눈6개와좌하붉은손 보이는것 확인.300 실제알파 회색합성에서 소용돌이 stripe/빈틈확인, 정확한 source색/폭/coverage는 별도검수.
- 305 첫RAW는 속도선을 다시 둥근금속봉/갈퀴처럼 그려 원인미해결. 사용승인금지. source-only native+actualBRZ 2참조로 외곽선/베벨/하이라이트 없는 평면속도선 추가교정중. 첫RAW도 삭제/덮어쓰기없이보존.325/326 넓은궤적이 원본보다 단단한blade처럼 읽힐수있어 투명도·원래band폭/색/구멍을 독립검수할것.
- NATIVE_REDRAW_CAMPAIGN_PROGRESS_20261118.json은 23:28 필수180자세 대상으로 각담당 신규RAW 유무만 합산.23:46 시점122자세에RAW/58자세RAW미수령이며, 후속교정·정합·설치·게임완료를 뜻하지않음. 원본 누락하반신26614는 source검증 대기 별도.

### 11/19 아침 재개

- 305 source-only 교정 RAW_imagegen_234725.png(SHA fc29124611abb2f7a5c7b1b0420913bb168acc1aa9fca2add8bde8eb8264104a)를 실제알파 회색에서 확인. 둥근금속봉·검정외곽 대신 가는 뾰족한 연보라평면선으로 변함. PREFERRED_TARGETS_ROOT_20261119.json으로 첫RAW 제외; 정확한 원본폭/줄수/정렬과 본체스타일 검수는별도.
- 신규 469/471/473/475/479/481 및482~489 원본 반려분 작업 재개. 46907은 원본RGBA가검정A255실루엣뿐이며 TO9가 명시요청한 그원본자체에서만 새로그림(HD재색칠금지). 기존22별도runtime증거 항목과혼동금지.
- 원본만세로배열한 469/471/475/484는 새 layout_snapshot 사용. 원본기체크기를변경하지않고 칸배치만바꿈. 모든생성RAW는 바이트그대로보존, 수신후정합/분할/설치/게임확인은Claude담당.

### 11/19 07:21 새 RAW 실시간 인계

- 469/471/473/475/479/481 6판 수령. 각 native_redraw_20261118/unit_N/sheet_selected/RAW_imagegen.png 및 DELIVERY_ROOT_20261118.json/HANDOFF_ROOT_20261118.md 사용. 471발끝/475구름상단은 새RAW 캔버스 안쪽에 들어옴(원본여백·각parts정렬은Claude검수). 473연기는 원본짙은slate회색+mint로, 481큰베기궤적도 새판에포함. 실제alpha 회색검수사진은 READONLY_GRAY_raw.jpg, 설치이미지가아님.
- 469은 검정뷰에서는 비어보이나 실제alpha 회색에서 하단검정실루엣 보임. 상단comparison은생성되지않았으므로사용금지. interiorA252~253이 있어 native A255와차이있음; 임계alpha칠/원본픽셀복붙없이 RAW보존, Claude원본silhouette coverage/opacity검수. 내부눈/몸체그림추가금지.
- NATIVE_REDRAW_CAMPAIGN_PROGRESS_20261118.json 현재159/180 RAW있음,21 RAW미수령. 이 숫자는검수합격/설치완료아님. 미수령 중22는고유runtime_original증거로정책제외기록중.

### Native high finish: 391~451 fresh RAW 8 plates /11 targets
Builtin image_gen only, transparenttrue. Native/actual4xBRZ/style refs directly viewed. RAW bytes unchanged; no candidate/queue/library/ROM edits. Exact splitting/alignment/install/game remains Claude QA.391/393 source-only vertical repack uses new layout_snapshot.json, not oldSHEETS layout.
- 391 pose_08 RAW C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_391\sheet_selected\RAW_imagegen.png; SHA256 886737c9d6a70d536129572380ea2bd218971f17f95f88b007f66d792d65436c; [1224, 1285]; alpha0..255; aspect/resolution gate pass ONLY. QA: feet complete with bottom margin; verify exact source trail extent and tilted feet height.
- 393 pose_04 RAW C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_393\sheet_selected\RAW_imagegen.png; SHA256 4bb8ecde2cf56c7156417252d466abe1d38a7019fdaad9b4fffde6a1d81898ab; [1169, 1346]; alpha0..255; aspect/resolution gate pass ONLY. QA: sparkle dome retained; verify exact sparkle count/positions and density, no inferred source fill.
- 394 pose_00,pose_14 RAW C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_394\sheet_selected\RAW_imagegen.png; SHA256 d6cbe6d9fd9b7fddf86c818ccc3e796467b18b1e48d032a09f400838b689710d; [1230, 1278]; alpha0..255; aspect/resolution gate pass ONLY. QA: broad opaque red-orange/pink/violet crescent retained; verify original arc width/endpoints and cape/arm ownership.
- 399 pose_10 RAW C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_399\sheet_selected\RAW_imagegen.png; SHA256 f100879c23208e20917cc6da90ad57c8ffd8884534fa92505a790127aff27387; [1836, 856]; alpha0..255; aspect/resolution gate pass ONLY. QA: crossed/braced stacked forearms now visible; verify exact arm and fist ownership/source pose.
- 409 pose_07,pose_09 RAW C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_409\sheet_selected\RAW_imagegen.png; SHA256 2e67d969e18f9eee8d2a307c6ff3df42e8f2460295903a72e877d0c1f1b5221c; [1631, 964]; alpha0..255; aspect/resolution gate pass ONLY. QA: 07 nested V gap arch and09 full horizontal speedlines present; gray source hue/stripe widths and opacity need exact check, no metallic blade reinterpretation.
- 424 pose_05 RAW C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_424\sheet_selected\RAW_imagegen.png; SHA256 cbbaedd1883386d11fb402c080987b23050ab6d914ae791a15915b2a7e1dbbd0; [1758, 895]; alpha0..255; aspect/resolution gate pass ONLY. QA: top blades and bottom detached fragment complete; verify all intentional source partial cut edges and detached patterned fragments, no invented anatomy.
- 427 pose_01 RAW C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_427\sheet_selected\RAW_imagegen.png; SHA256 ade87051c690c2fc1f7b0d59ea441d122604d5a5638dba36a0491aeab3a5422c; [1758, 895]; alpha0..255; aspect/resolution gate pass ONLY. QA: opaque dull slateblue/dark overlapping silhouettes retained; verify density,original area/holes and absence of pale cyan/translucent expansion.
- 451 pose_00,pose_06 RAW C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_451\sheet_selected\RAW_imagegen.png; SHA256 43619c465217a56f07087264efd40560145bf5aa709695c24666b483809aa7b7; [1425, 1104]; alpha0..255; aspect/resolution gate pass ONLY. QA: broad white/lavender afterimage area requested; exact source FX fill,width,color,holes and target body ownership need Claude check.
-41610 duplicate generation avoided: existing TARGETED_10_13_SOURCE_ONLY source and RAW gray diagnostics directly viewed, corrected silhouette has raised LEFT arm and transparent V gap matching source direction.13joined finger wedge visible; exact shape and source registration remain Claude QA. Use existing corrective delivery map, not rejected wholeplate10/13.
- Full delivery index: test_current/parts/NATIVE_REJECT_HIGH_FINISH_DELIVERY_INDEX_20261118.json. Each local HANDOFF_ROOT/DELIVERY_ROOT includes target/comparison/map/SHA.393yellow noise on black view disappears in actualalpha gray composition; READONLY_GRAY_raw.jpg diagnostics are not installation assets.

### native low finish RAW / sensor and effect corrections
- C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_99\sheet_selected\RAW_imagegen.png | SHA256 3d135af26c9945d4cc8ce0419e334c4849d0506d23321e32cb2a1810436528aa | [1247, 1261] | targets pose_06,pose_07; Claude geometry/alpha/registration review pending.
- C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_278\sheet_selected\RAW_imagegen.png | SHA256 5a792d8e794a75ecfe6693c4af3fb73e7706f951bb810949e30c1011ba543c13 | [1625, 968] | targets pose_09; Claude geometry/alpha/registration review pending.
- C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_279\sheet_selected\RAW_imagegen.png | SHA256 87686f461b453615b76ef059041cc7916cd280763ca54289391bf7b8b5595afc | [1131, 1391] | targets pose_00,pose_07,pose_08,pose_10; Claude geometry/alpha/registration review pending.
- C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_279\sheet_selected\qa_flat_white_sourceonly\RAW_imagegen.png | SHA256 649b6f7b8cde2072cf37674ff9ce4ad0abe00e7d40c2bd5190ee64c0f7269a56 | [1897, 829] | targets pose_07,pose_08; Claude geometry/alpha/registration review pending.
- C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_71\sheet_selected\RAW_imagegen.png | SHA256 9569be219bb8b93d04ddac6f60cf2860600332741f489ac825d27694e28b7f4f | [1873, 840] | targets pose_06; Claude geometry/alpha/registration review pending.
- C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_119\sheet_selected\RAW_imagegen.png | SHA256 0135838801fc1424d5ea954c8f7eb1c3ed101aacb3aa29befa31087dbf9740a0 | [1610, 977] | targets pose_09; Claude geometry/alpha/registration review pending.
- C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_119\sheet_selected\qa_white_streak_sourceonly\RAW_imagegen.png | SHA256 373d9318bfc560a75064f2043ac7a067237fa97db6cca3661ccea975366df7eb | [1187, 1325] | targets pose_09; Claude geometry/alpha/registration review pending.
- 71 fresh RIGHT06 2x3 six pink sensors confirmed.119 prefer qa_white_streak_sourceonly;27907/08 prefer qa_flat_white_sourceonly. Each parent PREFERRED_TARGETS_ROOT_20261118.json supplies NEW source layout, do not mix old SHEETS coordinates. First RAW retained; no install/ROM/candidate change. Actualalpha graydiagnostics show clean flashwhite holes and outlinefree streaks; not installation assets.
- 22 pose02 source 146x86 has3344 opaque pixels ALL RGB0; INDEX/VARIANT_STATE proof SHAs revalidated. Runtime original policy preserved, zero new calls; RUNTIME_POLICY_REAUDIT_20261119.json.

### Native middle finish 신규 RAW 17자세 / 9판

Builtin image_gen transparenttrue only. Every source/native4x equality and reference/contract SHA checked; direct input view before calls. Existing rejected candidates, ROM/library/queue untouched. First slot comparison only, never install. Layout authority is each new layout_snapshot.json; 372 correction shares original sheet_selected layout.

- unit327 sheet_selected pose_03,pose_15 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_327\sheet_selected\RAW_imagegen_071531.png`, SHA f7f09c8493ea5ba2e480ba0b9c7d08ce0addbd691eaf8d0aa43a8d9b97957d2e, [1351, 1164], alpha[0, 255], resolution/aspect gate True. Lavender trails flatness/count/extent, raised-hand ownership, opaque material and alpha holes need Claude QA.

- unit332 sheet_selected pose_01 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_332\sheet_selected\RAW_imagegen.png`, SHA ab353a274e9a881b32f6d40b0ac2b09eb20f1a79f681446c07e601d293378dd2, [2143, 734], alpha[0, 255], resolution/aspect gate True. Horizontal right speedlines are fuller gray graphic streaks; check no comb/metal bevel, source gaps/extent and fist scale.

- unit336 sheet_selected pose_10,pose_11 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_336\sheet_selected\RAW_imagegen.png`, SHA 9eed8532e805dbc2ed0ad1184b3c0ea7a636777a643cc87e364dec79bd4f71be, [1132, 1390], alpha[0, 255], resolution/aspect gate True. Full overhead sword visible; small generated shadow speckles under platform MUST be assessed against source alpha0; head/platform proportions need QA.

- unit338 sheet_selected pose_07 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_338\sheet_selected\RAW_imagegen.png`, SHA 00c4370adcd877828540e4ea9c7d9347f10d01a420a9e8ceb842d58d2e353e2a, [1983, 793], alpha[0, 255], resolution/aspect gate True. TO_CODEX_9 lines1961/3103 explicitly requests silhouette position/proportion redraw. Native RGB entirely0, alpha bbox(8,9,98,84),109x92; all contract palette15bit0. Right target stays black: alpha bbox/scale and pure-black material need Claude QA. Left comparison never install.

- unit345 sheet_selected pose_04,pose_06 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_345\sheet_selected\RAW_imagegen.png`, SHA bb0860047268514539e1989de934e6fe75333b2f438522737988213e3d87b42f, [1312, 1199], alpha[0, 255], resolution/aspect gate True. Dense pale smoke now occludes front hull. Check target04/06 exact smoke coverage/holes; generated smoke is smoother/larger curls and must not expose hidden chassis.

- unit359 sheet_selected pose_09 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_359\sheet_selected\RAW_imagegen.png`, SHA bb1114b4bf7885bef2ce26d243bdfd460389fb869343223f08a3c633f3215513, [2155, 730], alpha[0, 255], resolution/aspect gate True. Curved gold side afterimages freshly drawn. Check no blade interpretation, source width/endpoint density/alpha gaps and original olive palette.

- unit371 sheet_selected pose_15 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_371\sheet_selected\RAW_imagegen.png`, SHA f1c9a733a462ea79c05fcca80f5aac71cf403b22cd2375dce61deb545dcc29de, [1911, 823], alpha[0, 255], resolution/aspect gate True. Orange crossing and horizontal speedlines freshly drawn. Check no blade interpretation and exact source trailing density/extent.

- unit372 sheet_selected pose_01,pose_02,pose_09,pose_15,pose_22,pose_25,pose_27 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_372\sheet_selected\RAW_imagegen.png`, SHA 78ba221d7743b602874fa870bacab7479e0045ad2faa4ddf227d0292e300ad6c, [891, 1766], alpha[0, 255], resolution/aspect gate True. First RAW remains blade-like. Source-only correction changes them toward thinner graphic hatching but some physical blade reading may remain. NO acceptance asserted. Claude must inspect all7 against source especially01 arcs,02 below-platform speedlines and22 chest traces.

- unit372 sheet_selected_sourceonly_correction pose_01,pose_02,pose_09,pose_15,pose_22,pose_25,pose_27 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_372\sheet_selected_sourceonly_correction\RAW_imagegen.png`, SHA 010ac675dc03630424d92eee3b51950aed3e1a816f3ff11bb05d71ffa2e2d7dd, [891, 1766], alpha[0, 255], resolution/aspect gate True. First RAW remains blade-like. Source-only correction changes them toward thinner graphic hatching but some physical blade reading may remain. NO acceptance asserted. Claude must inspect all7 against source especially01 arcs,02 below-platform speedlines and22 chest traces.

- Index: `test_current/parts/NATIVE_MIDDLE_FINISH_DELIVERY_INDEX_20261118.json`. Gate/RAW count is not geometry/color/alpha acceptance. Claude split/align/install/game still pending. 327 duplicate identical RAW_imagegen.png and timestamp sibling were saved byte-identical; index points timestamp sibling, no second generation.

- 담당17자세 preferred RAW→layout 정확한 대응은 	est_current/parts/NATIVE_MIDDLE_PREFERRED_RAW_LAYOUT_20261118.json. 372는 sourceonly_correction RAW + 원래 sheet_selected/layout_snapshot.json을 검수우선으로 지정(합격아님).
- 336 실제 RAW target10 platform아래 (700,500)-(1000,570) 알파0..47, A>0 8615px로 실제 저알파 그림자 존재. 검정뷰 단순 표시노이즈가 아님. 원본alpha0 외부이므로 별도 검수/교정 필요하며 사용승인 안함. 372 교정후 일부선의blade읽힘/원본밀도 차이도 미해결 QA로 남김.

### flat six/four-colour source-only final attempts
- C:\Emul\Workshop\SRW_W_HD\test_current\parts\affine_codex_prepared_20261118\unit_324\sheet_a04\qa_flat_sourceonly_20261119\RAW_imagegen.png | SHA 659ca71fe812c76d2e9ff5d7926cc0069d56e7b702af07b288ff4ee0ef0e1f0a | [1586, 992] | UNRESOLVED exact uniform flat palette: visible shade/gradient variations remain. Do not mark flat-color precision accepted. No generated recolor, quantization, masking or resizing. Source-only 1 extra call.
- C:\Emul\Workshop\SRW_W_HD\test_current\parts\affine_codex_prepared_20261118\unit_359\sheet_a01\qa_flat_sourceonly_20261119\RAW_imagegen.png | SHA dd62dd2d45ac43cf4191a9c5843afbea17d142dc38b09b9d11f4e29a2bfe806c | [1402, 1122] | UNRESOLVED exact uniform flat palette: visible shade/gradient variations remain. Do not mark flat-color precision accepted. No generated recolor, quantization, masking or resizing. Source-only 1 extra call.

### 336 떠있는 mechanical 교정 / 372 효과전용 보조 RAW

- 336 preferred 새 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_336\sheet_selected\RAW_imagegen_072744.png`, SHA afbef3a1976ba582805e359dc25cc9d3695e85b6e94749a2abf483c7b76f2bcb, [1132, 1390]. Layout `C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_336\sheet_selected\layout_snapshot.json`. 원본+actualBRZ+STYLE로 새로그림. 아래 빈영역 alpha체크 {"target10_below_saucer": {"rect": [650, 570, 1050, 650], "alpha_extrema": [0, 1], "nonzero": 2386}, "target11_below_saucer": {"rect": [80, 1310, 470, 1370], "alpha_extrema": [0, 1], "nonzero": 924}}. 기존 저알파그림자판 보존, 새판원본정합·발판·머리/팔크기 등Claude검수필요.
- 372 효과만 추가 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_372\sheet_effect_graphic_supplement\RAW_imagegen.png`, SHA e72296bb4b7e1a63e6b4af5bab277cad037ff987e61b59a46248dfad2c37de0c, [905, 1738]. Layout `C:\Emul\Workshop\SRW_W_HD\test_current\parts\native_redraw_20261118\unit_372\sheet_selected\layout_snapshot.json`. 원본pose02 아래단순주황선 직접확인후 sourceplate+source-onlydetail 입력. 금색부품은효과로빼지않음. 효과없는본체와합성한바없음. 얇은해칭선으로보이나 원본선개수/밀도·끝·빈틈/가려짐독립검수필요. 기존preferred fullsprite교정판은유지하고 이판은보조로맵에추가.
- NATIVE_MIDDLE_PREFERRED_RAW_LAYOUT_20261118.json 최신반영. 336교정+372보조총2호출, 둘다RAWbyte그대로 sibling. 후보/롬/큐/라이브러리변경없음.

- 336 알파수치주의: 새판 아래두영역 실제 alpha0..1(2386px/924px 비영), 이전47보다약해져화면에안보여도 strict alpha0완료아님. 마스킹/지우기없으며 원본외곽알파검수미해결. JSON수치가 alpha0설명보다우선.

### 11/19 07:32 원본 반려 신규RAW 연결 마무리

- 483 첫RAW는 너무pixelstyle이어서 제외. canonicalSTYLE를다시넣고 VOID가시화원본도참조한 RAW_imagegen_072723.png(SHA c49e4209b148df2b39ddd9b7598339e5d9b8159b579260f671da3f63293effcb) 우선. 실제alpha회색에서 중앙몸통/오른쪽은구멍으로남고 파편/부분팔/부분발만보임. 파편정확수/크기·원본coverage와위치는Claude검수.
- 489는483과whole원본RGBA+size+slot좌표가완전동일. IDENTICAL_SOURCE_PROOF.json 근거로 새smoothRAW 바이트그대로 복사(새호출0,재색칠0). native_redraw_20261118/unit_489/sheet_selected/RAW_reused_identical_483.png; donorlayout483, pose04comparison/pose01target 동일매핑.
- 필수180 중179자세 새RAW,22pose02는기존runtime_original_preserved_no_hd_recolour 증거검증으로별도제외. 전체검수/설치완료아님.484입자추가교정은계속중이며 첫판원형halo/두번째aspect실패 모두완료로세지않음.

### TO9 누락원본 읽기전용 재대조

상세 Claude 요청목록: docs/CLAUDE_SOURCE_PACKET_REQUEST_AUDIT_20261119.md. 바로 생성 가능한 새 원본패킷 발견0건,캡처/코드/설치/생성0. missing_valid_source_packet 실제 항목33902(weapon1377obj057,pose150frame614/616)는 기존native SHA그대로라 정상상체 재캡처 필요.1크리티컬/130·135돌진·붉은결합/130형제자세/213·40자기팔레트는 정확장면·object·조합contract 추가확인 필요.130obj072는 기존준비본이고scene확인대기 유지.26512/36402 새native없음: 다만 최신EYE는각각23:21/22:11에accept/no reject라 옛HELD와충돌.새생성보다Claude가검수candidate/RAW SHA와가림/A0창실제상태부터대조.기존affine납품은native해결증거로세지않음.
