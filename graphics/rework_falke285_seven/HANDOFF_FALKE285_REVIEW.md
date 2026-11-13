# 팔케 +285 후반 자세 미연결 7종 후보

상태: 미검증 후보·연결 준비 완료. Claude가 실제 재생/시각검증 담당. 라이브·DB·코어 변경 없음.

unit276 diagnostic_preview/mechanical_cutin_168.state +285 (286회 run)의 실제 캐시 OBJ와 rendered OAM 기준. 본체 palette0 전체15OAM 중 새7종7OAM을 제작했다. 앞선 falke165_missing 그림과 동일한 3OAM은 재제작하지 않고 raw index SHA/크기/사용 팔레트 완전동일을 검산해 prior_candidate_dependencies.json에 기록. 루트는 +165 후보 선설치 후 이 묶음을 설치할 수 있다. 나머지는 기존 연결 의존(whole_pose_dependencies.json).

새7종은 최신 exact/indexed 모두없음(source_identity_and_connection.json), ROM image14225/14249의 실제 bytes와 완전 일치(rom_indices_identity.json). 실제 palette15bit와 core_path/SHA는 contract.json에 보존. 원본192×144 / 후보768×576로 정확4배. installation_map.json에 원본 resource/좌표 병합. 원본참조 크기·index SHA·실제색은 mechanical_contract_checks.json, 후보 전부 alpha_max>=16은 candidate_presence.json. 품질 QA를 대신하지 않는다.

후보 SHA `52eacef524ca4a0311d202ab54a29d41294433a7b00204c00ba476ac6341b768`. parts_generated.png는 imagegen exec-37d89547 생성원본. 원본 셀 및 원본 기체 bbox문맥을 참조해 각각 새그림 제작. 원본RGB/알파 복사나 다른기체 재색칠 없음. 생성 alpha bbox 정렬만 사용. prepare_candidate.py로 셀분리 재현.

주의: cell4는 세로 연결부이고 얼굴이 아니다. cell5의 주황 작은 점/청회색 패널 위치와 cell6 끝단이 임의 포구·빈 구멍으로 바뀌었는지 Claude확인 필요. 내부 절단면 외곽선과 접합 지원영역도 미검증. unit276_production_assembly.png는 나머지를 원본으로 둔 제작문맥으로, 최종 HD재생 증거 아님.

Claude 재생:
```powershell
python scripts/verify/verify_runtime_path.py --state test_current/combat/named_attacks/unit_276/diagnostic_preview/mechanical_cutin_168.state --frames 360 --save-frames 255 270 285 300 330 --track-atlas falke285_missing --name falke285
```

같은 팔케 공격의 다른 자세에도 원본이 남을 수 있으며 전체완성 주장 없음.

