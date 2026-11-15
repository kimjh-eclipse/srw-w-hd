# unit111/w471 좁은 회청색 연결편 1개 교정 후보

상태: 기존 #94874 같은 ID 미검증 새 후보. 다른 정상5개 보존. 신규 누락 증가0/공식QA·실제HD재생·라이브/코어/DB 쓰기 없음.

## 입력과 실제 결함

- 최신 fixed current machine lost이며 live observed_unit111_weapon471_six가 동일한 것을 확인했습니다. 원래 unit111_weapon471_attack350_missing/contract.json의 actual cached OBJ/OAM/전체16색을 읽고 raw RGB CRC/인덱스/실제 fullpalette를 현재 spec과 검산했습니다.
- fixture source_mechanical_fixed_111_471_350/source_pose.state +0, OAM8, screen145,71,16×8,actual opaque38. 원본 IMG9871/PLT1665bank0 근거는 원래 패킷 rom_indices_identity/full_palette_phase_proof에 보존돼 있습니다.
- unit111_native_context.png는 512×384(2배)이므로 actual 좌표를2배로 겹친 actual_bbox_context.png를 확인했습니다. 기계 구조 옆의 회청색 곡선 연결편이며 백색 광선/반짝임으로 임의 분류하지 않았습니다. 카탈로그 기체명과 세부 해부학적 명칭은 확정하지 않았습니다.
- 같은 fullactualpalette 기존 큰 raw 완전포함은0(same_source_parent_matches.json)이며 정상 부모와 이미 같은 child를 새로 그리는 경우가 아닙니다.
- 현재 actual texture_key로 SQLite를 mode=ro SELECT만 해 실제 baked를 읽었습니다. raw부터 고형 회색 측면이 사라져 가는 반투명 흰 선으로 바뀌었고 baked에도 같습니다. 원본 IoU .319/미칠 .553(38 중21 정도)/외부0입니다.

## 새 그림

- generated_raw.png는 imagegen exec-2d7afc32-1470-4e44-94b5-03b522acc765.png 새 출력 그대로 보존했습니다. 실제 원본/whole bbox 문맥을 참조하고 기체를 통째로 자동완성하지 않았습니다.
- 평평한 왼쪽 끝/작은 윗 탭, 완만히 내려가는 실제 곡률, 오른쪽 짧은 세로 단면을 유지한 고형 회청색 띠를 요청했습니다. 옅은 회색 가운데/짙은 회청색 측면을 둘 다 칠하고 끝을 바늘로 가늘게 하지 않았습니다.
- 자체 생성 RGBA 전체를 원본 bbox에 기하 확대/정렬만 했습니다. 원본 RGB/alpha 찍기·native mask/알파문턱 삭제·침식/팽창·재색칠은 없습니다. alignment_provenance.json.
- 원본의 도트를 그대로 확대하지 않고 연속한 면과 매끈한 곡률로 그렸습니다.

## 인수 파일과 검사

- installation_map.json 같은 #94874만 교체. contract.json old_spec/hash/index/full16/lookup flags·resource/source좌표 유지.
- candidate_atlas.png SHA `1ae81e219c8be1a3301f22a5b7fcb34765fa57acc2d6c9cdb700b056f584fa1b`, native_atlas.png 같이 사용. 실제4배64×32.
- candidate/NullCache prepare 사전기하 flags0, IoU .636/미칠 .132/외부0. 수치 개선을 실제 완료라고 부르지 않습니다.
- replacement_comparison.png는 실제 원본/현재 baked/새 후보입니다. 직접 제작 대조에서 고형 두께·탭/평평한 끝 복원을 확인했습니다.
- 정상5 spec 불변 비교 preserved_normal5_latest.json.

## Claude 확인 위험

- 원본38texel 중약5texel의 위치/AA 차이가 남습니다. IoU .636은 기준에 가깝고 실제 곡선 굽음이 주변 기계와 이어지는지 확인해야 합니다.
- 새 그림의 회색 중앙면과 짙은 측면 명암이 원본보다 단순하거나 넓어 보일 수 있습니다. 실제 접합 끝을 새 외곽선/캡처럼 보이게 하지 않았는지 판정 필요합니다.
- source pose +0에서 실제 HD 조립과 원본을 비교해야 하며 전체 기체·무장 모든 자세를 이번1개로 완료 처리하지 않습니다.
