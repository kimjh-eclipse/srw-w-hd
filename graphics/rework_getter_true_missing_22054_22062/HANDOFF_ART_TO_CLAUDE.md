# 실제 미연결 4종: 겟타 도끼 불꽃·섬광

## 상태/범위
새그림4종 후보 및 실제 연결 입력만 준비했습니다. 원본 렌더캐시의 binding_id가4종모두0이고, 제작선정시 라이브 exactRGB/index_hash 연결이모두0개였습니다. 기존 연결그림을 재색칠하는 재작업이 아니라 실제 빈 연결을 채우는 후보입니다. QA·독립 시각 판정·HD 실제 재생 검증은 하지 않았습니다.

## 누락 보고서와 구분
missing_export/report.json(11,358종)의 images 목록에 IMG22054/22062가 없어 이4종을 그 수치에서 빼지 않습니다. 실제관측·원본 source 바이트 확정 미연결로 별도 집계합니다. missing_classification.json에 구분과 근거를 적었습니다.

## 최종 설치 입력
- candidate_atlas.png:576×128(1배144×32의4배), native_atlas.png:144×32.
- install_contract.json:실제해시/indices/palette/sourceIMG좌표/배치/반전 및 source캐시계약.
- rendered_source_contracts.json:공통 capture_rendered_obj_contracts helper의 실제 원본,동시출현2 OAM씩도보존.
- generated.png:새 image_gen 원본.
- geometry_registration.json:각 생성조각의 위치/크기를 원본 전체bbox로 기하정렬한수치. 원본 RGB/alpha는결과에찍지않았습니다.
- whole_native_context_78/82/84/137.png:HD를끄고얻은원본제작문맥. HD QA 비교가아닙니다.
- mechanical_input_check.json:source index바이트/hash/파일크기/코어경로 및SHA.

## 실제 역할
78/82/84:도끼를 머리위로 들 때 좌우 도끼 끝에 붙는 불꽃3단계(매단계 동일그림2 OAM). 137:도끼를 모을 때 퍼지는 섬광의 대각선 쐐기조각(동일그림2 OAM). 대규모폭발/기체얼굴로추정해그리지않았습니다.
22062세단계는원본실루엣과색을각각보며새로한시트에그렸고22054섬광도같은시트에독립구역배치. 다른기체그림/기존그림리컬러/원본확대/도트알파스탬프 없음. static/effect, 실제RGB팔레트별연결후보입니다.

## Claude fixture/위험
- test_current/combat/getter_cutin.state +78,+82,+84,+137 (load후 offset+1회 run).
- 불꽃 내부 빈곳과 단계3의 분리파편이 원본대로 남는지,도끼기점접합과선폭/색/alpha확인.
- 생성기가 팽창시킨 불꽃 끝과 내부흰코어폭,주황테두리가 원본과다를수있습니다. 기하정렬은bbox뿐이므로각세부형태까지정확하다고보증하지않습니다.
- 기체/도끼/컷인/UI순서와기존effect22053주변조각과연결도확인해야합니다.
- 이4개외 전체 IMG22054/22062 및전체공격완료를주장하지않습니다.
- live/library/DB/코어/공유코드수정없음.

| cell | IMG/sourcebox | frame | actualRGB | indexhash |
|---|---|---:|---:|---:|
| 0 | 22062 [8, 0, 32, 32] | 78 | 1614514546 | 2585560911 |
| 1 | 22062 [40, 0, 32, 32] | 82 | 1419942958 | 1902849397 |
| 2 | 22062 [72, 0, 32, 32] | 84 | 460687392 | 734960892 |
| 3 | 22054 [16, 0, 32, 32] | 137 | 2102771217 | 1540739205 |
