# 실제 FX 22052 신규 그림 제작 인계

- 7 계약 / 7 고유 raw / 실제 전체 팔레트 1개. 원본은 retained rendered_obj_cache 실제 state/OAM/우선순위/변환/팔레트 계약. 대표 입력 `test_current\parts\native_weapon_source_249_1020\unit249_weapon1020_source.state` +645. 전체 frame과 source는 new_candidate_contract.json에 보존.
- 원본 IMG22052 crop과 각 actual raw byte 일치(source_integrity.json). IMG/PLT 기본값을 actual 팔레트로 추정하지 않음. source resource 소유 단정 없이 resource=None.
- 각 실제 palette당 한 새로운 전체 그림. 원본 source 영역이 교차하면 같은 palette의 한 생성 그림에서 나누므로 부분 crop 픽셀 동일. overlap 11쌍. 다른 기체/색변형 재색칠 없음.
- 후보 candidate.png [384, 128] / native_combined.png [96, 32], SHA `0228de2ea726c10db1bef2f6c437b103a2961c3e13d8d7cbe19ce10d369e3bc8`. own generated_*.png와 입력 reference/native 보존. 원본 RGB/alpha stamp, 코드 색 채움 없음.
- 생산 prepare 7개 모두 maxA>=255, empty=0. 원본 RGB hash 계약 일치. 기존 prepare 분리성분 제거 항목 []. 이 수치는 생산 존재 확인이며 실제 정상 HD 판정 아님.
- 생성 alpha preserve_generated 그대로. threshold220/이진화/MinFilter 없음. 원본 alpha는 source 문맥/geometry 참조용이며 후보에 붙이지 않음.
- 최신 live exact/indexed 중복 0개(latest_live_duplicates.json); 인수 시 root가 다시 최신 상태로 제외할 것.
- 알려진 문제/Claude 큐: 원본보다 추가된 명도 질감/입자/외곽선 변형, 여러 실제 palette 간 작은 형상 차이를 Claude가 실제 OAM에서 확인해야 함. 얇은 광/부드러운 광이 prepare 분리성분 제거에 의해 손실될 수 있음. 실제 layer 순서/크기/팔레트 변화/부분 연결 검증 대기.
- 라이브/library/DB/core/EXE 변경, 독립 audit/실재생 없음. 실패/보류를 정상 완료 수로 세지 않음.

## 구체적 미해결 위험
生成물은 원본보다 개별 파편에 두께/주황 테두리가 추가됐으며 사각성도 남음. 실제 가는 흩어진 파편의 역할·겹침을 Claude 판정 대기.
본 묶음은 생성 alpha >=8 bbox를 위치/크기 등록에만 사용했고 RGBA 픽셀 alpha는 그대로 보존. 원본 mask/stamp 없음.
