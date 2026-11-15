# 청록 비행체 #95085 넓은 면 소실 교정 후보

같은 ID1개 교체 미검증 후보, 신규 미연결 증가0. 정상19개 보존. 공식QA/실제HD재생·라이브/코어/DB 쓰기 없음.

## 실제 원본과 결함

- 최신 fixed current machine lost이며 live observed_fixture344_teal_flight_twenty가 동일함을 확인했습니다. 원래 teal_flight_pose170_native1391/packed/install_contract.json actual cached index/전체실제16팔레트/RGB CRC를 현재 spec과 재검산했습니다.
- source native_weapon_source_344_1391/unit344_weapon1391_source.state +170/OAM0/screen109,72/16×16/84texel. 전체 native 문맥은 actual_mechanical_pose_344_170/whole_native_context.png. 실제 기체 소유 IMG/이름은 미확정으로 원래 owner None을 유지했습니다.
- 같은 fullpalette 정상 큰 raw 완전포함0입니다(same_source_parent_matches.json). 정상 부모와 이미 같은 영역이어서 기술보존하는 경우가 아닙니다.
- 현재 actual texture_key로 SQLite를 mode=ro SELECT만 해 구운 RGBA를 읽었습니다. 현재 raw부터 넓은 청록/밝은 면이 가는 발톱3개처럼 재해석됐고 baked에도 같아 native84 중20(23.8%) 미칠이 남았습니다. 기존 IoU .633/미칠 .238/외부0.

## 새 그림

- generated_raw.png: 내장 imagegen 새 출력 exec-24206090-9124-4832-b85b-35e3f3255a70.png 보존. 실제 원본 분리 형태를 하나의 연결판으로 재그렸습니다.
- 위쪽 긴 가로 면/가운데 짧은 가로 면/아래 내려가는 면의 실제 위치·폭, 넓은 왼쪽 지지연결부를 유지하도록 요청했습니다. 손가락/날카로운 발톱/가는 광선/완성 날개로 자동완성하지 않았습니다.
- 실제 어두운 보라색 부분을 키색이나 투명구멍으로 지우지 않고 작은 삽입면으로 남겼습니다. 왼쪽은 인접 기체로 이어지는 절단면이라 가상 검은 캡/둘레선을 넣지 않도록 요청했습니다.
- 생성 자체 RGBA를 bbox 기하 정렬만 했고 원본 RGB/alpha 전사·native mask/알파문턱 삭제·팽창·침식·재색칠은 없습니다. alignment_provenance.json.

## 설치/생산 확인

- installation_map.json #95085만 같은 ID 교체. contract.json actual source+old spec/hash/index/fullpalette/source·lookupflags 보존.
- candidate_atlas.png SHA `6f220107d80b3fddf4f78e3aa7f489c7993f084f0ed6366cf40c82040766853e`, native_atlas.png와 함께 사용. native16×16/그림64×64.
- candidate 및 NullCache prepare 사전기하 flags0, IoU .902/미칠0/외부0. 숫자를 실제 화질/게임완료 판정으로 부르지 않습니다.
- replacement_comparison.png actual원본/current baked/새후보 직접 제작 대조에서 넓은 실제 지지면과 작은 보라 재질의 복원을 확인했습니다.
- 다른 정상19개 spec 불변은 preserved_normal19_latest.json.

## Claude 실제 확인 위험

- 넓은 밝은 민트색 면이 원본의 분리된 밝은 음영보다 부드럽고 밝게 보일 수 있습니다. 작은 실제 보라색 부분을 모델이 삼각 삽입면처럼 단순화했으므로 위치/형태를 실제 크기에서 봐야 합니다.
- 왼쪽 내부절단면은 세부 AA로 가는 어두운 선처럼 보일 여지가 있어 인접 정상 기체와 붙인 모습에서 확인해야 합니다. 별도 검은 캡을 의도하지 않았습니다.
- 원래 OAM사각 끝은 잘린 부분이며 세 선의 뾰족한 발톱으로 해석하면 안 됩니다. 실제 주변 큰 비행체/자세와 연결은 아직 재생 검증하지 않았습니다.
- 이1개로 다른19개 정상파츠·다른 기체·무장·전체 HD 완료를 주장하지 않습니다.
