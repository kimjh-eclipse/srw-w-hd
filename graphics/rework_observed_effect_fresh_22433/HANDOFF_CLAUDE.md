# 실제 FX 22433 신규 그림 제작 인계

- 3 계약 / 3 고유 raw / 실제 전체 팔레트 1개. 원본은 retained rendered_obj_cache 실제 state/OAM/우선순위/변환/팔레트 계약. 대표 입력 `test_current\parts\native_weapon_source_373_1485\unit373_weapon1485_source.state` +340. 전체 frame과 source는 new_candidate_contract.json에 보존.
- 원본 IMG22433 crop과 각 actual raw byte 일치(source_integrity.json). IMG/PLT 기본값을 actual 팔레트로 추정하지 않음. source resource 소유 단정 없이 resource=None.
- 각 실제 palette당 한 새로운 전체 그림. 원본 source 영역이 교차하면 같은 palette의 한 생성 그림에서 나누므로 부분 crop 픽셀 동일. overlap 0쌍. 다른 기체/색변형 재색칠 없음.
- 후보 candidate.png [640, 128] / native_combined.png [160, 32], SHA `788052100eed27504ff1ab7cf5088397d050ecfcd6f367f799a40d9ee46d797b`. own generated_*.png와 입력 reference/native 보존. 원본 RGB/alpha stamp, 코드 색 채움 없음.
- 생산 prepare 3개 모두 maxA>=255, empty=0. 원본 RGB hash 계약 일치. 기존 prepare 분리성분 제거 항목 []. 이 수치는 생산 존재 확인이며 실제 정상 HD 판정 아님.
- 생성 alpha preserve_generated 그대로. threshold220/이진화/MinFilter 없음. 원본 alpha는 source 문맥/geometry 참조용이며 후보에 붙이지 않음.
- 최신 live exact/indexed 중복 0개(latest_live_duplicates.json); 인수 시 root가 다시 최신 상태로 제외할 것.
- 알려진 문제/Claude 큐: 원본보다 둥근 황백색 광선 끝/약한 크림색 음영. 가는 별도 광선의 위치와 source crop 연결은 실제 확인 대기. 얇은 광/부드러운 광이 prepare 분리성분 제거에 의해 손실될 수 있음. 실제 layer 순서/크기/팔레트 변화/부분 연결 검증 대기.
- 라이브/library/DB/core/EXE 변경, 독립 audit/실재생 없음. 실패/보류를 정상 완료 수로 세지 않음.

등록 위치 보정: 생성 alpha1에 멀리 떨어진 미약 흔적이 있어 본체가 과도하게 축소되는 것을 막으려고, 생성 alpha>=8 bbox를 좌표 등록의 크기/위치에만 사용했다. alpha 값은 전혀 threshold하지 않고 전체 자체 RGBA를 affine으로 이동/크기 변경했다. 원본 bbox는 위치/크기 참조이며 원본 mask를 후보에 찍지 않았다. production_report.registration에 실제 좌표가 기록돼 있다.
