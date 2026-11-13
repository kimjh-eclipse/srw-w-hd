# unit50/w226 실제 포탑 제작 — 50_435

- `install_contract.json` 4종, `candidate_atlas.png` 정확4배, `native_atlas.png` 원본. `provenance.json`에 생성파일과 원본 bbox기하 기록.
- 실제 나탈/회색 전함 native 메뉴 공격435~455의 포탑/쌍포 회전 단계. 같은 기체 몸통을 끌어오지 않고 해당 부품만 자체알파로 생성. ROM IMG소유 None 유지.
- 원본 상태는 `test_current/parts/native_weapon_source_50_226/unit50_weapon226_source.state` +435. cached raw/실제16색/attrs/hash 계약 포함. 전체 native문맥 `test_current/parts/actual_mechanical_pose_50_435/whole_native_context.png`.
- 첫 생성의 상단 두 타일에 부품이 중복으로 생성되어 미사용. 최종 exec-c9cc8e2e...는 imagegen으로 각각1부품으로 교정한 새 그림. 원본 RGB/alpha스탬프/다른기체재색칠 없음.
- 제출 시 actualRGB/indexed0. NullCache 메모리 prepare 4/4 불투명 입력 확인만 실시. DB/live/core 미변경. 공식 QA/실제 HD재생 판정은 Claude 대기.
- 알려진 위험: 원본 작은 원형 부품의 구멍/새 검은캡·회전별 포신폭·좌우방향이 새그림에서 정확한지는 Claude 확인 필요. 입력이 불투명하다는 것은 그림 합격이 아님.
