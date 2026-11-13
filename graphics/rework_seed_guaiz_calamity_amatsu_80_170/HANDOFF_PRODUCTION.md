# 제작 인계 — 80_170

상태: 새 그림 후보 준비. 라이브 설치·굽기 전이며 실제 HD 재생 판정은 Claude 대기.

- 후보: `candidate_atlas.png` (원본 캔버스의 정확 4배), 원본: `native_atlas.png`.
- 연결 입력: `install_contract.json`, 8종. actual cached OBJ 원본 bytes/팔레트/해시/OAM/상태/frame 포함. IMG 소유는 확정하지 않아 None 유지.
- 제작 근거/생성 원본: `provenance.json`. 원본 RGB 또는 알파를 새 그림에 찍지 않음. 자체 생성 알파와 원본 bbox 위치만 사용.
- 동일 프레임 원본 중복: `same_frame_aliases.json` (1건). 같은 raw bytes/크기/실제 사용색일 때만 한 그림 공유.
- 메모리 prepare_texture 입력 확인: 8/8 불투명 결과 존재. NullCache로 실행했으며 DB/라이브 쓰기 없음. 독립 품질 검사나 실제 HD 재생 검증이 아님.
- 제출 시 현재 RGB/indexed lookup 연결 0개. 기존 연결은 교체하지 않음.
- Claude 원본 상태/프레임: `test_current\parts\native_weapon_source_80_340\unit80_weapon340_source.state` / 170. 전체 원본문맥은 `test_current/parts/actual_mechanical_pose_80_170/whole_native_context.png`.
- 알려진 위험: 생성 장갑 세부, 접합면, 센서색, 가느다란 부분의 폭은 Claude가 원본과 조립 장면에서 확인해야 함. 입력이 비어 있지 않다는 확인을 시각 승인으로 해석하지 않음.
