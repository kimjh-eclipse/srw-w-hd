# 실제 FX 21877 신규 그림 제작 인계

- 7 계약 / 7 고유 raw / 실제 전체 팔레트 1개. 원본은 retained rendered_obj_cache 실제 state/OAM/우선순위/변환/팔레트 계약. 대표 입력 `test_current\parts\native_weapon_source_235_948\unit235_weapon948_source.state` +715. 전체 frame과 source는 new_candidate_contract.json에 보존.
- 원본 IMG21877 crop과 각 actual raw byte 일치(source_integrity.json). IMG/PLT 기본값을 actual 팔레트로 추정하지 않음. source resource 소유 단정 없이 resource=None.
- 각 실제 palette당 한 새로운 전체 그림. 원본 source 영역이 교차하면 같은 palette의 한 생성 그림에서 나누므로 부분 crop 픽셀 동일. overlap 1쌍. 다른 기체/색변형 재색칠 없음.
- 후보 candidate.png [512, 256] / native_combined.png [128, 64], SHA `47db9e86c3e1f27886f3879d34314cfcf869c5d435dbf13a1689b5612e276fb2`. own generated_*.png와 입력 reference/native 보존. 원본 RGB/alpha stamp, 코드 색 채움 없음.
- 생산 prepare 7개 모두 maxA>=255, empty=0. 원본 RGB hash 계약 일치. 기존 prepare 분리성분 제거 항목 [(3, 1)]. 이 수치는 생산 존재 확인이며 실제 정상 HD 판정 아님.
- 생성 alpha preserve_generated 그대로. threshold220/이진화/MinFilter 없음. 원본 alpha는 source 문맥/geometry 참조용이며 후보에 붙이지 않음.
- 최신 live exact/indexed 중복 0개(latest_live_duplicates.json); 인수 시 root가 다시 최신 상태로 제외할 것.
- 알려진 문제/Claude 큐: 원본보다 추가된 명도 질감/입자/외곽선 변형, 여러 실제 palette 간 작은 형상 차이를 Claude가 실제 OAM에서 확인해야 함. 얇은 광/부드러운 광이 prepare 분리성분 제거에 의해 손실될 수 있음. 실제 layer 순서/크기/팔레트 변화/부분 연결 검증 대기.
- 라이브/library/DB/core/EXE 변경, 독립 audit/실재생 없음. 실패/보류를 정상 완료 수로 세지 않음.

## 구체적 미해결 위험
커다란 흰 내부는 생성본 자체로 채워졌으나 일부 경계 계단과 내부 절단선의 얇은 윤곽이 남음. 원본보다 표면 gradient 변화/외부 저알파 haze가 남아 실제 조립 접합 Claude 확인 필요.
본 묶음은 생성 alpha >=8 bbox를 위치/크기 등록에만 사용했고 RGBA 픽셀 alpha는 그대로 보존. 원본 mask/stamp 없음.
