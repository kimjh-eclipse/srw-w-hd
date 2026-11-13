# 듀얼 그레네이드 공격 420프레임 8종 — 미검증 후보

- 실제 unit54/weapon245 메뉴420(추출 최소 요청350 뒤 첫 관측420), `source_mechanical_fixed_54_245_350/source_pose.state` +0. 팔레트0 기체 OAM14 중 새 실제 RGB8, 기존 exact6 의존 보존.
- 신규 미연결7 / 머리 cell3 기존 indexed 다른 색 재제작1(메타41440). 신규 누락8로 세지 않음.
- 전부 IMG8467 byte 일치. PLT1380 bank0 사용색 일치. 원본 연결부와 파란/회색 장갑·주황 패널·원래 녹색 카메라를 보존하는 새 그림.
- cell0/6은 같은 IMG/실팔레트에서 8×16부분 교차. 원본 indices/팔레트 일치 검산 후 56×32 공통 생성 그룹에서 분할, 교집합 생성 RGBA 완전 일치. 분리 부품은 원본처럼 분리 유지. 나머지 source별 독립 사각형.
- 전체 OAM flip/affine 없음. cell4의 가느다란 레일은 초기220에서도 같은 actual hash1571128644이므로 본 묶음 하나로 공유(초기220 별도 설치하지 않음).
- 생성 원본 보존. 자체 알파<64만 RGBA0(생성 이후 리사이즈 저알파도 동일), 고알파 불변, 원본 알파/RGB 스탬프 없음. 크기4배, 후보 존재 및 raw CRC/원본 팔레트 기계적 확인.
- SHA256: 510303d2fc0be67f3d24af0c252cfeaf2b10afbfc00a86700fc9b14792410dc3
- 연결 입력 installation_map.json / candidate_atlas.png / native_atlas.png.
- native_pose_production/candidate_pose_production은 제작 조립, Claude 공식 QA나 실제 HD 재생 아님.
- Claude 위험: 머리 원래 눈/카메라의 정확한 녹색 위치와 흰 뿔 각도, cell0/6의 관절 세부 과장, cell2 회색 패널의 볼륨 해석, cell4 레일 두께, cell7 잘린 접속부가 기존 기체와 연결되는지. 시각/실재생 미검증.
- 라이브/DB/코어/공유 소스 수정 없음. headless로 작업.
