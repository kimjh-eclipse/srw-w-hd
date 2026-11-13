# 실제 FX 19584 신규 그림 제작 인계

- 26 계약 / 21 고유 raw / 실제 전체 팔레트 2개. 원본은 retained rendered_obj_cache 실제 state/OAM/우선순위/변환/팔레트 계약. 대표 입력 `test_current\parts\native_weapon_source_57_259\unit57_weapon259_source.state` +425. 전체 frame과 source는 new_candidate_contract.json에 보존.
- 원본 IMG19584 crop과 각 actual raw byte 일치(source_integrity.json). IMG/PLT 기본값을 actual 팔레트로 추정하지 않음. source resource 소유 단정 없이 resource=None.
- 각 실제 palette당 한 새로운 전체 그림. 원본 source 영역이 교차하면 같은 palette의 한 생성 그림에서 나누므로 부분 crop 픽셀 동일. overlap 29쌍. 다른 기체/색변형 재색칠 없음.
- 후보 candidate.png [704, 512] / native_combined.png [176, 128], SHA `36696e865a258d4d1af0a1f6c6d134dcd9751ecd9e9187ee6f14987b2fd71f22`. own generated_*.png와 입력 reference/native 보존. 원본 RGB/alpha stamp, 코드 색 채움 없음.
- 생산 prepare 26개 모두 maxA>=254, empty=0. 원본 RGB hash 계약 일치. 기존 prepare 분리성분 제거 항목 [(0, 2), (2, 3), (3, 3), (4, 1), (5, 1), (10, 3), (15, 2), (17, 1), (19, 1), (21, 1)]. 이 수치는 생산 존재 확인이며 실제 정상 HD 판정 아님.
- 생성 alpha preserve_generated 그대로. threshold220/이진화/MinFilter 없음. 원본 alpha는 source 문맥/geometry 참조용이며 후보에 붙이지 않음.
- 최신 live exact/indexed 중복 0개(latest_live_duplicates.json); 인수 시 root가 다시 최신 상태로 제외할 것.
- 알려진 문제/Claude 큐: 원본보다 추가된 명도 질감/입자/외곽선 변형, 여러 실제 palette 간 작은 형상 차이를 Claude가 실제 OAM에서 확인해야 함. 얇은 광/부드러운 광이 prepare 분리성분 제거에 의해 손실될 수 있음. 실제 layer 순서/크기/팔레트 변화/부분 연결 검증 대기.
- 라이브/library/DB/core/EXE 변경, 독립 audit/실재생 없음. 실패/보류를 정상 완료 수로 세지 않음.

위치 등록은 생성 alpha>=8 bbox로 크기/위치만 계산하며, alpha 자체를 threshold하지 않고 전체 자체 RGBA affine으로 변형한다. 원본mask는 사용하지 않는다. 미약한 떨어진 alpha1 흔적 때문에 본체가 과도하게 축소되는 것을 피하기 위한 자체 위치 보정이다.

단색 실제 입력도 확인해 4개 계약을 추가 포함했다(flat_actual_additions.json). actual palette/range/size/raw가 IMG19584 내부 균일 영역에 일치하는 위치를 보존. 모든 source가 단색이라 IMG소유 자체는 확정 못하므로 owner=false/resource=None. 22 nonflat+4flat=26이며, palette2/고유raw21이다. 같은 full 생성그림의 해당 영역을 잘라 partial 교집합도 공유한다. 생성 그림의 평면 내부가 원본보다 약한 gradient를 갖고 있으므로 **flat fill 연결부 사각 seam/명도차**를 Claude가 실제 +435/470/475에서 우선 확인해야 한다. native uniform color로 코드 덧칠하지 않았다.
