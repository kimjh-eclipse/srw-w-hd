# 제작 인계 — 110_430

상태: 새 그림 후보 준비. 라이브 설치·굽기 전이며 실제 HD 재생 판정은 Claude 대기.

- 후보: `candidate_atlas.png` (원본 캔버스의 정확 4배), 원본: `native_atlas.png`.
- 연결 입력: `install_contract.json`, 2종. actual cached OBJ 원본 bytes/팔레트/해시/OAM/상태/frame 포함. IMG 소유는 확정하지 않아 None 유지.
- 제작 근거/생성 원본: `provenance.json`. 원본 RGB 또는 알파를 새 그림에 찍지 않음. 자체 생성 알파와 원본 bbox 위치만 사용.
- 동일 프레임 원본 중복: `same_frame_aliases.json` (0건). 같은 raw bytes/크기/실제 사용색일 때만 한 그림 공유.
- 메모리 prepare_texture 입력 확인: 2/2 불투명 결과 존재. NullCache로 실행했으며 DB/라이브 쓰기 없음. 독립 품질 검사나 실제 HD 재생 검증이 아님.
- 제출 시 현재 RGB/indexed lookup 연결 0개. 기존 연결은 교체하지 않음.
- Claude 원본 상태/프레임: `test_current\parts\native_weapon_source_110_467\unit110_weapon467_source.state` / 430. 전체 원본문맥은 `test_current/parts/actual_mechanical_pose_110_430/whole_native_context.png`.
- 알려진 위험: 생성 장갑 세부, 접합면, 센서색, 가느다란 부분의 폭은 Claude가 원본과 조립 장면에서 확인해야 함. 입력이 비어 있지 않다는 확인을 시각 승인으로 해석하지 않음.

## 연속 원본 두 사각형

OAM1 body64×32와 OAM0 boots32×8은 동일 affine [141,0,0,141], 동일 X중심128 및 Y연속 근거로 하나의64×40 원본 그림에 배치. boots x16,y32; 역산 Y32.37890625와 정수 배치 차이0.37890625 기록. `continuous_source_geometry.json` 참조. 한 벌 새 그림을 원래 두 사각형으로 역분할했으며 runtime attrs 변경 없음. `production_support_check.json`에서 생성 알파16/128 기준 원본 두 사각형 합집합 밖0픽셀. 이는 원본 알파 스탬프나 형태 QA가 아닌 후보 지원영역의 기계적 확인. 실제 접합/rounding 판정은 Claude 대기.
