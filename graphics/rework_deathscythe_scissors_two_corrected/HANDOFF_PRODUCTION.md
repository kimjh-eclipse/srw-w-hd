# 데스사이즈 시저스 #93984/#93985 무장 조각 교체 후보

입력은 이 폴더 install_contract.json/candidate_atlas.png/native_atlas.png/provenance.json입니다. 기존 같은 ID 2개 교체용, 신규 연결 증가0. 다른 정상 #93983/#93986은 수정하지 않았고 other_two_preserved.json에 기존 RGBA SHA와 원본 hash를 기록했습니다.

실제 source는 unit1/weapon7 +400에서 고정한 source_mechanical_fixed_1_7_400/source_pose.state +0 cached OAM1/3입니다. IMG7105 (88,64)32×32 및 (224,136)32×16이며 기존4개 원본 사각형끼리 공유/포함은 없다는 이전 source_intersection_proof를 확인했습니다. 원래 실제 보라 회색 팔레트·인덱스·해시·슬롯을 보존했습니다.

얇은 고리·가는 봉처럼 남은 기존 후보 대신 넓은 중앙 보라회색 판, 원래 꺾인 축·갈고리와 굵기, 실제 어두운 안쪽을 새 그림으로 유지하도록 만들었습니다. 생성 exec-4e7977ee-26c1-41c3-9ed6-54a80d3aa698.png. 각 조각 생성 자체 알파와 원본 bbox 기하로 정렬했으며 원본 RGBA/알파 복사·220문턱·침식/팽창은 없습니다. 메모리 준비2개 비어 있지 않음은 생산 입력 확인입니다.

source_candidate_pair.png 위 원본/아래 후보입니다. 클로드 확인점: 원래 갈고리 안쪽 투명/어두운 부분과 면 폭, 세워진 날개판 각도, 축 꺾임·실제 부품과 이어지는 끝 단면, 원본보다 또렷한 검은 외곽선과 판 분절이 과한지. 생성은 원본보다 매끈한 직선/곡선으로 표현되며 정확한 조립/형태 합격은 독립 판정 대기입니다.

기존 팔/커프·암부 판2개는 이 교정 범위가 아니고 전체 기체/무장 완료라고 하지 않습니다. 실제 전체 원본 문맥은 borrowed_shape_rework/deathscythe_scissors400_missing/unit1_native_context.png와 원래 계약에 있습니다.

라이브 메타/DB/코어/공유 실행 코드 수정 없음. 공식 QA/독립 HD 재생은 하지 않았고 클로드 대기입니다. 모니터를 깨우는 입력 없음.
