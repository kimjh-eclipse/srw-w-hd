# 본타군 격투 자세 실제 미연결2종 후보

상태: 미검증 후보·연결 준비 완료. Claude가 실제 재생·시각검증 담당. 라이브/DB/코어 변경없음.

source_mechanical_266_1101/source_pose.state 로드후1회run으로 얻은 실제 cached OBJ+rendered OAM. 원본메뉴 진입frame520에서 source를 저장했다. unit266 본타군·weapon1101 격투. 이전duo_weapons 진단 fixture에서 아군슬롯만 RAM으로설정하고 무장비용/지형/기력을완화한격리원본추출이다. ROM/사용자저장변경없음. 캠페인게임플레이합법성검증이아니다. capture_meta.json에그대로기록.

palette0 본체7OAM 중새2종/2OAM, 기존5의존 whole_pose_dependencies.json 보존. 최신 exact/indexed 연결없음(source_identity_and_connection.json). 실제캐시 팔레트와ROM사용색후보일치. 큰원본은IMG13893(200,0,32,32) bytes완전일치.4검정픽셀 슬리버는IMG8936(40,80,8,8)에 동일원본bytes가 있지만 실제 소유 이미지는 미확정이다. installation_map의 resource=None, source_candidate_matches에 첫일치 예시만 기록(전수검색 목록 아님). 캐시 exact계약은확정(rom_indices_identity.json). core_path/SHA256·실제indexSHA는contract에기록.

설치: installation_map.json + candidate_atlas.png768×288/native_atlas.png192×72로정확4배. 기계적원본RGB/alpha/indexSHA/크기확인은 mechanical_contract_checks.json, 후보빈/alpha_max<16=0은candidate_presence.json. 품질판정아님. 후보SHA `2d9b1408170afc602c3d5eb2630185cbc7807c26809cb4e5174766d5ad4a6274`.

parts_generated_initial_rejected.png의큰그림은도트확대/헤일로가남아채택하지않았다. 재생성 parts_generated.png(exec-aaf1d887)는부드러운새그림으로제작했다. 최초생성(exec-f046f6a3)의셀0 검은슬리버만사용하며, 생성물자체의검은색전경지지영역으로불필요한헤일로알파를지웠다. 원본RGB/alpha스탬프나재색칠은없다. prepare_candidate.py 재현.

원본참조 native_atlas_reference_gray.png / whole_native_bbox_context.png. 큰조각은올리브장비/몸체일부이며얼굴또는총이라고부르지않는다.4픽셀슬리버의형태·접합과큰조각위쪽내부절단면에새cap이생겼는지 Claude판정대기.

Claude재생:
```powershell
python scripts/verify/verify_runtime_path.py --state test_current/parts/borrowed_shape_rework/source_mechanical_266_1101/source_pose.state --frames 90 --save-frames 0 15 30 60 --track-atlas bonta_melee_missing --name bonta_melee
```

합체weapon1102는원본확보메뉴에서열리지않아미확보상태다. 본타군전무장완성주장없음.
