# 실제 FX 21967 신규 그림 제작 인계

- 37 계약 / 17 고유 raw / 실제 전체 팔레트 3개. 원본은 retained rendered_obj_cache 실제 state/OAM/우선순위/변환/팔레트 계약. 대표 입력 `test_current\parts\native_weapon_source_82_351\unit82_weapon351_source.state` +630. 전체 frame과 source는 new_candidate_contract.json에 보존.
- 원본 IMG21967 crop과 각 actual raw byte 일치(source_integrity.json). IMG/PLT 기본값을 actual 팔레트로 추정하지 않음. source resource 소유 단정 없이 resource=None.
- 각 실제 palette당 한 새로운 전체 그림. 원본 source 영역이 교차하면 같은 palette의 한 생성 그림에서 나누므로 부분 crop 픽셀 동일. overlap 26쌍. 다른 기체/색변형 재색칠 없음.
- 후보 candidate.png [768, 768] / native_combined.png [192, 192], SHA `eafef813bdef9fb110ff15a67b52f5887cf3e267f85cdf94a10f693b70c6192d`. own generated_*.png와 입력 reference/native 보존. 원본 RGB/alpha stamp, 코드 색 채움 없음.
- 생산 prepare 37개 모두 maxA>=253, empty=0. 원본 RGB hash 계약 일치. 기존 prepare 분리성분 제거 항목 [(0, 1), (1, 1), (3, 1), (6, 1), (7, 1), (8, 3), (15, 2), (16, 1), (19, 3), (22, 2), (24, 1), (27, 1), (32, 7), (35, 4), (36, 2)]. 이 수치는 생산 존재 확인이며 실제 정상 HD 판정 아님.
- 생성 alpha preserve_generated 그대로. threshold220/이진화/MinFilter 없음. 원본 alpha는 source 문맥/geometry 참조용이며 후보에 붙이지 않음.
- 최신 live exact/indexed 중복 0개(latest_live_duplicates.json); 인수 시 root가 다시 최신 상태로 제외할 것.
- 알려진 문제/Claude 큐: 원본보다 추가된 명도 질감/입자/외곽선 변형, 여러 실제 palette 간 작은 형상 차이를 Claude가 실제 OAM에서 확인해야 함. 얇은 광/부드러운 광이 prepare 분리성분 제거에 의해 손실될 수 있음. 실제 layer 순서/크기/팔레트 변화/부분 연결 검증 대기.
- 라이브/library/DB/core/EXE 변경, 독립 audit/실재생 없음. 실패/보류를 정상 완료 수로 세지 않음.

최신 교정: g0 왼쪽 대형폭발 중앙의 부정확한 낮은alpha/회색 구멍을 imagegen으로 자체 그림에 교정했다. 자체 그림을 navy 배경의 불투명 신규 RGB판본으로 얻고 imagegen으로 navy만 제거, 자기 RGB+자기 alpha를 사용했다. 최종 회색배경 후보에서 중앙은 노란 불투명 화염이고 이전 회색 구멍은 보이지 않는다. rejected_lowalpha_core_*는 실패보존이며 최종아님. 다른 palettealpha 공유/원본RGB/alpha stamp 없음.
생성 alpha>=8 bbox는 위치등록만 사용하며 alpha자체변경 없이 전체 자체 RGBA affine. 실제QA/독립audit 없음.
