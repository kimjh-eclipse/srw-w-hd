# 실제 FX 21855 신규 그림 제작 인계

- 10 계약 / 10 고유 raw / 실제 전체 팔레트 1개. 원본은 retained rendered_obj_cache 실제 state/OAM/우선순위/변환/팔레트 계약. 대표 입력 `test_current\combat\named_attacks\unit_19\mechanical_cutin_168.state` +200. 전체 frame과 source는 new_candidate_contract.json에 보존.
- 원본 IMG21855 crop과 각 actual raw byte 일치(source_integrity.json). IMG/PLT 기본값을 actual 팔레트로 추정하지 않음. source resource 소유 단정 없이 resource=None.
- 각 실제 palette당 한 새로운 전체 그림. 원본 source 영역이 교차하면 같은 palette의 한 생성 그림에서 나누므로 부분 crop 픽셀 동일. overlap 0쌍. 다른 기체/색변형 재색칠 없음.
- 후보 candidate.png [736, 256] / native_combined.png [184, 64], SHA `68d8238b316d63c3e3b95c00baa8f8de318219d34b0d834b5c9498f522d52b2a`. own generated_*.png와 입력 reference/native 보존. 원본 RGB/alpha stamp, 코드 색 채움 없음.
- 생산 prepare 10개 모두 maxA>=255, empty=0. 원본 RGB hash 계약 일치. 기존 prepare 분리성분 제거 항목 [(0, 1), (1, 1), (2, 1), (3, 1), (7, 1), (8, 1)]. 이 수치는 생산 존재 확인이며 실제 정상 HD 판정 아님.
- 생성 alpha preserve_generated 그대로. threshold220/이진화/MinFilter 없음. 원본 alpha는 source 문맥/geometry 참조용이며 후보에 붙이지 않음.
- 최신 live exact/indexed 중복 0개(latest_live_duplicates.json); 인수 시 root가 다시 최신 상태로 제외할 것.
- 알려진 문제/Claude 큐: 원본보다 추가된 명도 질감/입자/외곽선 변형, 여러 실제 palette 간 작은 형상 차이를 Claude가 실제 OAM에서 확인해야 함. 얇은 광/부드러운 광이 prepare 분리성분 제거에 의해 손실될 수 있음. 실제 layer 순서/크기/팔레트 변화/부분 연결 검증 대기.
- 라이브/library/DB/core/EXE 변경, 독립 audit/실재생 없음. 실패/보류를 정상 완료 수로 세지 않음.

## 최종 제작 범위와 알려진 한계
실제 정상 기본팔레트10계약만 제작. 추가 특수 팔레트1계약(hash2730118576)은 actual 원본에서 초록 사각이 생기는 collapse를 보여 HANDOFF_PALETTE_HOLD.md로 분리했다. 그1은 신규그림/완료수 제외이며 native_1.png/source_contract_with_palette_hold.json에 source/base페어 보존. 초록을 임의로 제거하지 않음. 생성 기본은 원본의 화염/연기보다 두껍고 평면적인 면분할/검은틈 변화, 흰 타격면 내부 질감/외부 미세 glow가 있어 Claude 판단 필요.
전체 alpha preserve_generated. native bbox는 위치/크기 참조에만 사용. 라이브/DB/runtime 변경 및 독립 QA/실제 재생 없음.
