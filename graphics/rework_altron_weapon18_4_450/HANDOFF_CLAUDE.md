# 알트론 무장18 실제 자세 4_450

현재: 새 그림 및 설치 입력. 실제 HD 재생검증/품질 판정은 Claude 담당.

- candidate_atlas.png / native_atlas.png / install_contract.json 3개 / provenance.json. 정확4배.
- 정상 메뉴 fixture `test_current\parts\native_weapon_source_4_18\unit4_weapon18_source.state` +450, OAM [0, 1, 2]. 원본 전체문맥 test_current/parts/actual_mechanical_pose_4_450/whole_native_context.png, 캐릭터 눈/+210은 대상아님.
- 원래 알트론 녹색/은색/황색/적색 source 실제팔레트 유지. 단지 녹색이라는 이유로 조명변형으로 판정하지 않음.
- 이전 연결 preserved_existing_pose.json 보존, 나머지 source remaining_source.json.275 OAM6은 현재activeIndexed 연결 발견하여 후보에서 제외(그림원본만보존), install_contract 대상2개만설치.
- 부품마다 generated intrinsic alpha 사용, source bbox만 기하정렬; 원본RGB/alpha stamp 또는 wholepose 이웃 사각crop 없음.
- actual prepare_texture 메모리 nonempty만 확인. 라이브/DB/코어 수정 없음. 공식QA/HD replay 없음.
- 알려진 위험: 450 대형부품은 원본 자체가 몸체 여러곳을 포함한 직사각형 조각임. 생성기에는 원래 조각만 그리도록 지시했으나 다리/팔 구조를 발명하거나 실루엣/공백을 바꿨을 가능성 있어 Claude 확인 필수. 생성/prepare 성공을 품질 승인으로 해석하지 않음.
