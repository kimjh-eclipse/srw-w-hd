# 실제 FX 22352 신규 그림 제작 인계

- 5 계약 / 5 고유 raw / 실제 전체 팔레트 2개. 원본은 retained rendered_obj_cache 실제 state/OAM/우선순위/변환/팔레트 계약. 대표 입력 `C:\Emul\Workshop\SRW_W_HD\test_current\parts\borrowed_shape_rework\source_mechanical_260_1058\source_pose.state` +0. 전체 frame과 source는 new_candidate_contract.json에 보존.
- 원본 IMG22352 crop과 각 actual raw byte 일치(source_integrity.json). IMG/PLT 기본값을 actual 팔레트로 추정하지 않음. source resource 소유 단정 없이 resource=None.
- 각 실제 palette당 한 새로운 전체 그림. 원본 source 영역이 교차하면 같은 palette의 한 생성 그림에서 나누므로 부분 crop 픽셀 동일. overlap 0쌍. 다른 기체/색변형 재색칠 없음.
- 후보 candidate.png [768, 256] / native_combined.png [192, 64], SHA `57d0f1ed284bf09feaccd17f26e5e1794d1e4cca324770ea6d35f515e13e5010`. own generated_*.png와 입력 reference/native 보존. 원본 RGB/alpha stamp, 코드 색 채움 없음.
- 생산 prepare 5개 모두 maxA>=255, empty=0. 원본 RGB hash 계약 일치. 기존 prepare 분리성분 제거 항목 [(2, 2)]. 이 수치는 생산 존재 확인이며 실제 정상 HD 판정 아님.
- 생성 alpha preserve_generated 그대로. threshold220/이진화/MinFilter 없음. 원본 alpha는 source 문맥/geometry 참조용이며 후보에 붙이지 않음.
- 최신 live exact/indexed 중복 0개(latest_live_duplicates.json); 인수 시 root가 다시 최신 상태로 제외할 것.
- 알려진 문제/Claude 큐: 두 팔레트 별도 생성으로 화염 굴곡이 약간 다름. 왼쪽 큰 불꽃보다 오른쪽 좁은 flame의 색/길이를 실제 OAM에서 우선 확인. 상단 극소 파편이 생성 중 복수로 표현됐으나 현재 대상 crop은 주로 하단/오른쪽. 얇은 광/부드러운 광이 prepare 분리성분 제거에 의해 손실될 수 있음. 실제 layer 순서/크기/팔레트 변화/부분 연결 검증 대기.
- 라이브/library/DB/core/EXE 변경, 독립 audit/실재생 없음. 실패/보류를 정상 완료 수로 세지 않음.

등록 위치 보정: 생성 alpha1에 멀리 떨어진 미약 흔적이 있어 본체가 과도하게 축소되는 것을 막으려고, 생성 alpha>=8 bbox를 좌표 등록의 크기/위치에만 사용했다. alpha 값은 전혀 threshold하지 않고 전체 자체 RGBA를 affine으로 이동/크기 변경했다. 원본 bbox는 위치/크기 참조이며 원본 mask를 후보에 찍지 않았다. production_report.registration에 실제 좌표가 기록돼 있다.
