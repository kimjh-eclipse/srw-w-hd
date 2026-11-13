# 아스테바리스 커스텀 손포 실제 미연결 2종 후보

미검증 후보·연결 준비 완료. 라이브/DB/코어 변경 없음. 공식 시각/재생 판정은 Claude 담당.

unit 190 무장 788 격리 진단메뉴에서 관측한 cached OBJ + rendered OAM 원본. source_mechanical_190_788/source_pose.state 로드 후 1회 run, 메뉴 frame 130. 계약 전체 시점과 core_path/SHA는 contract.json. 비용/기력/지형 완화 및 ROM/사용자 저장 불변은 원본 capture_meta.json. 캠페인 합법성 검증 아님.

팔레트 0 전체 24 OAM 중 실제 미연결 고유 2종. 그 외 기존 파츠 의존은 whole_pose_dependencies.json. 최신 exact RGB/indexed 연결 모두 0인 것은 source_identity_and_connection.json에서 확인. ROM 11337의 (32,64,16,16), (120,64,16,32)로 첫 원본 bytes 일치. 실제 크기는 계약이 기준이며 리소스 단독 소유 유일성은 미확정. palette 사용색 ROM 후보도 존재한다.

installation_map.json, candidate_atlas.png 768×288, native_atlas.png 192×72. 정확 4배·원본 indexSHA/크기/원본 RGB·alpha 계약 정합은 mechanical_contract_checks.json. 후보 2개 모두 빈 그림 아님/최대 alpha 16 이상(candidate_presence.json). 형태 품질 판정은 하지 않았다.

imagegen 원본 exec-c0ad8c92에서 주변 연무가 생겨 exec-121e347f-20e9-425e-9fdd-846130a95b6b로 투명 배경 재요청한 그림을 parts_generated.png에 보존. 원본 RGB/alpha 찍기나 다른 팔레트 그림 재색칠 없음. 생성 자체 알파 bbox를 원본 가시영역 bbox에 맞춘다. 얇은 청회색 연결편과 붉은 장갑의 모서리·분리면/검은 홈·지원영역이 실제와 맞는지는 Claude 판정 필요. 생성 그림에 일부 둥근 모서리/판금 세부가 추가되었을 위험도 미검증.

unit190_production_assembly.png는 기존 파츠를 원본으로 둔 제작 조립 자료이며 실제 HD 재생 증거가 아니다. 원본 OAM 좌표와 역순 우선순위로 합성했다.

Claude 재생:
```powershell
python scripts/verify/verify_runtime_path.py --state test_current/parts/borrowed_shape_rework/source_mechanical_190_788/source_pose.state --frames 120 --save-frames 0 15 30 60 --track-atlas aestivalis_custom_hand_missing --name aestivalis_custom_hand
```

달면 163/705는 이전 heavy_lunar 11종과 실제 RGB 차집합 0이라 중복 제작하지 않았다. 중장 157/682는 관측 조건을 충족하는 신규 기계 자세가 없어 보류. 전무장 완료 주장 없음.

