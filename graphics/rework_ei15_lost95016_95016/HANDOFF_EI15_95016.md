# 95016 분홍·검정 고형면 교정 후보

상태: 같은 ID 95016 교체 후보, Claude 판정 대기. 신규 그림 누락 수에는 추가하지 않습니다.

- `installation_map.json` / `candidate_atlas.png` / `native_atlas.png` / `contract.json`.
- 실제 원본: unit342/무장1385 상태 +470, OAM12, 화면 (229,74), 8×8, 실제 불투명 8texel, 반전·아핀 없음. RGB해시4060283842. 실제 index+전체 BGR555로 재계산 일치.
- 원본은 버건디 윗줄, 분홍 가운데 줄, 불투명 검정 오른쪽 위/왼쪽 아래의 작은 접합면입니다. 기존 그림은 가는 빛나는 가로띠로 바뀌어 검정 재질을 잃었습니다. 실제 전체 기체 문맥과 cached OAM을 보존했으며 더 구체적인 해부학적 명칭은 확정하지 않습니다.
- 같은 전체 팔레트와 원본 index 사각형을 포함하는 다른 바인딩은 찾지 못했습니다. 정상 19개는 `preserved_normal19.json` 그대로 보존했습니다.
- 자체 imagegen 새 재료로 세 가지 분홍 영역과 불투명 검정 면을 복원했습니다. 원본 RGB/알파 전사, 알파 문턱 삭제, 코드 재색칠은 없습니다. 생성 원본과 정렬 근거를 보존했습니다.
- SHA256 `30217655866b1de68ac4c9c438beb4dc736a185e626837ae87c8130dfc15540f`, 4배 32×32. 후보/NullCache prepare 사전 기하는 `candidate_geometry_preflight.json` / `root_geometry_preflight.json` 참조. 이 수치는 실제 재생 합격 판정이 아닙니다.
- 알려진 위험: 아주 작은 면이므로 자체 생성의 완만한 명암이 원본의 평평한 색 구획과 달라 보일 수 있습니다. 검정 면의 두께와 인접 기체 파츠 접합은 Claude 실제 장면 판정이 필요합니다.
- Claude 상태: `test_current/parts/native_weapon_source_342_1385/unit342_weapon1385_source.state` +470 및 전후. 라이브·공유코드·DB·코어 수정이나 공식 QA/HD 재생은 하지 않았습니다.
