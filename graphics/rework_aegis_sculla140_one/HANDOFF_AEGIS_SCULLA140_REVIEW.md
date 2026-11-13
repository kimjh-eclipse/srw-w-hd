# 이지스 무장 초기 자세 연결부 1종 — 미검증 후보

- 실제 메뉴 unit52/weapon236, 메뉴 140프레임. `source_mechanical_52_236/source_pose.state` +0, cached OBJ OAM13, 엔진0/팔레트0, 16×32, RGB 793983255.
- 실팔레트와 원본 바이트 확인: IMG8352 (240,0), PLT1357 bank0의 사용 색 번호 전부 일치. 리소스 첫 일치는 바이트 증거이며 고유 소유자 판정은 아님.
- 실제 전체 기체 16 OAM 중 이 연결부만 exact0/indexed0 미연결. 나머지는 기존 연결 의존관계로 보존. 녹색 눈·자홍 장갑·회청색 연결부를 혼동하지 않음.
- 새 그림은 원본 회청색/짙은 청회색 홈/자홍 장갑 절단부만 제작. 생성 원본 보존. 생성 자체 알파 64 미만만 RGBA0, 고알파 불변. 원본 RGB/알파 스탬프 사용 없음.
- 후보 SHA256: cd55d60a0916cb1a8116c56ea1ba87bc08a3eece4537a5f22cee8c991a21daf8
- 연결 입력: installation_map.json / candidate_atlas.png / native_atlas.png. raw 해시·원본 팔레트·크기 기계적 검사 완료.
- 제작 조립: native_pose_production.png / candidate_pose_production.png. 공식 시각/실재생 QA 아님.
- Claude 확인: 오른쪽 자홍 절단부 경계가 기존 몸체와 맞는지, 생성된 연결부 두께와 검은 홈이 원본에 비해 과장되지 않는지, 다른 OAM 자세에서도 연결이 맞는지. 아직 미검증.
- 기본 DLL 경로와 실제 SHA는 계약에 보존. 라이브/DB/코어 수정 없음.
