# 라고우 2연 빔샤벨 초기 자세 6종 — 미검증 후보

- 실제 unit64/weapon287 메뉴250. `source_mechanical_64_287/source_pose.state` +0. 팔레트0 기계 OAM18 중 실제 미연결6종(exact0/indexed0), 기존 exact12 의존 보존.
- 원본 IMG8755의 16×16 사각형6개: (32,0),(64,0),(48,0),(32,16),(48,16),(64,16). cached raw indices/실팔레트 사용색 일치, 모든 flip/affine 없음. 사각형 면적 교차 없음.
- whole native의 4족 기체 다리·몸통 접속부 문맥을 보존. 주황/황토 장갑과 짙은 보라회색 돌기. 실제 노랑 L자 영역을 눈이나 아이콘으로 만들지 않음.
- 첫 생성 cell1이 노랑 세 점을 발명하여 폐기(rejected_invented_three_yellow_dots.png). 후속 imagegen이 검정 홈 안 원본 노랑 L자 한 영역으로 교정. 최종 parts_generated_raw.png 사용.
- 화면에 보이는 RGB 후광 견본은 실제 알파0. 생성 자체 alpha<64만 RGBA0, 고알파 불변. 원본 RGB/alpha 스탬프 없음. raw hash/팔레트·후보 존재·4배크기 기계적 확인.
- SHA256 804ae3495fa55b804b75999b7407fad06ce6551761199364fc8cfeddac9ebb20
- 설치 입력 installation_map.json/candidate_atlas.png/native_atlas.png. 제작 조립 native/candidate_pose_production은 공식 QA/HD 재생 아님.
- Claude 위험: 작은 장갑을 새 그림이 둥글게 과장한 정도, 실제 두 갈래/세 작은 연결돌기의 지지 영역, cell1 노랑 L과 검정홈 배치, 기존 다리와 절단 경계. 실제 시각/재생 미검증.
- 라이브/DB/코어 수정 없음, 모니터 off/headless 유지.
