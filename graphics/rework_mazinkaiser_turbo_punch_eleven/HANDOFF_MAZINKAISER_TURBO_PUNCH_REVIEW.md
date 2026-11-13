# 마징카이저 터보 스매셔 펀치 11종 제작 인계

미검증 후보다. 공식 시각 판정/실제 HD 재생 검사는 Claude 담당이며 수행하지 않았다. 라이브/DB/코어/공유 runtime 수정 없음.

- unit295 / weapon1192 정상 네이티브 메뉴의 공격 진입 +330에서 별도 source_pose.state를 만들고 다음1프레임 actual cachedOBJ+rendered OAM을 추출했다. 전체26 OAM 중 binding0 16 OAM은 고유11종이고10 OAM은 기존 의존이다. 전체자세에 쓰이는 새 고유11종 모두 제작했다.
- source_mechanical_295_1192/source_pose.state +0이 원본 상태 기준이다. source_selection_trace.json/capture_meta.json과 전체 cached 계약을 함께 참조한다. 게임 ROM/사용자 세이브를 변경하지 않았다.
- 현재 exact0/indexed0/core0이며 source_identity_and_connection.json에 실제 팔레트2644 bank0의 사용색 일치와 연결 상태를 기록했다. source IMG14749의9종, IMG14723의2종(크기가 다른 같은영역)이다. ROM 첫 일치 witness이며 유일 소유 주장 아님.
- candidate_atlas.png/native_atlas.png/installation_map.json 설치 입력. 후보 SHA256 eb21d7e17918b06cc713c55388b6b7964c92b08a31524fde9a6d3dcdb3744ac6.4배 그림이며 mechanical_contract_checks.json에서 원본 index SHA/실제 팔레트 RGB/크기/후보 존재를 확인했다.
- 머리는32×32+16×32 실제 인접 사각형. 오른쪽16은 반전 표시이며 실제 source는 큰32의 좌측16과 동일하다. 한 번 생성한 큰셀 좌측16을 공유했고 별도 오른쪽 머리로 해석하지 않았다. 작은 연결편16×16 또한16×32의 같은 원본 상단16과 bytes/사용팔레트가 같으므로 생성 HD를 공유했다. shared_native_region_proof.json과 joined_head_provenance.json 참조.
- native_pose_production.png/candidate_pose_production.png는 original priority/OAM 역순/반전을 적용한 제작 조립이다. 새11 외 기존 의존은 원본으로 조립했으므로 실제 HD 전체 게임 결과가 아니다.
- parts_generated.png는 내장 imagegen 생성 출처다. 실제 옅은 보라 장갑/노란 눈 띠/붉은 면/하늘색 이마 패널 유지가 목적이다. 작은 허리/골반 조각을 머리로 자동 완성하지 않도록 전체 원본 문맥을 참조했다. 내부 절단 경계를 덮는 검은 cap/원본 alpha/RGB stamping은 사용하지 않았다.
- Claude 확인 요청: 두 연결편0/1의 떨어진 지지영역, 머리 뿔/눈색과 환기구2 사이 연결, 가슴6과 허리7/골반8/손9/발10 사이 경계, 무장 진행 단계/다른 OAM 등장 시 crop 지지 보존. 생성그림 형태와 색 배치가 정확하다는 공식 판정은 아직 없다.
