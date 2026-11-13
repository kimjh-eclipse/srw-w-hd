# 실제 FX 22472 신규 그림 제작 인계

- 16 계약 / 11 고유 raw / 실제 전체 팔레트 2개. 원본은 retained rendered_obj_cache 실제 state/OAM/우선순위/변환/팔레트 계약. 대표 입력 `test_current\parts\native_weapon_source_390_1550\unit390_weapon1550_source.state` +500. 전체 frame과 source는 new_candidate_contract.json에 보존.
- 원본 IMG22472 crop과 각 actual raw byte 일치(source_integrity.json). IMG/PLT 기본값을 actual 팔레트로 추정하지 않음. source resource 소유 단정 없이 resource=None.
- 각 실제 palette당 한 새로운 전체 그림. 원본 source 영역이 교차하면 같은 palette의 한 생성 그림에서 나누므로 부분 crop 픽셀 동일. overlap 8쌍. 다른 기체/색변형 재색칠 없음.
- 후보 candidate.png [768, 512] / native_combined.png [192, 128], SHA `b3d8bf8884152028f1606a49d6d06bb866e4a3a9f584135e1a98729a1c1efd58`. own generated_*.png와 입력 reference/native 보존. 원본 RGB/alpha stamp, 코드 색 채움 없음.
- 생산 prepare 16개 모두 maxA>=255, empty=0. 원본 RGB hash 계약 일치. 기존 prepare 분리성분 제거 항목 [(0, 2), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (9, 1), (10, 2), (11, 2), (12, 1), (13, 1)]. 이 수치는 생산 존재 확인이며 실제 정상 HD 판정 아님.
- 생성 alpha preserve_generated 그대로. threshold220/이진화/MinFilter 없음. 원본 alpha는 source 문맥/geometry 참조용이며 후보에 붙이지 않음.
- 최신 live exact/indexed 중복 0개(latest_live_duplicates.json); 인수 시 root가 다시 최신 상태로 제외할 것.
- 알려진 문제/Claude 큐: 원본보다 추가된 명도 질감/입자/외곽선 변형, 여러 실제 palette 간 작은 형상 차이를 Claude가 실제 OAM에서 확인해야 함. 얇은 광/부드러운 광이 prepare 분리성분 제거에 의해 손실될 수 있음. 실제 layer 순서/크기/팔레트 변화/부분 연결 검증 대기.
- 라이브/library/DB/core/EXE 변경, 독립 audit/실재생 없음. 실패/보류를 정상 완료 수로 세지 않음.

위치 등록은 생성 alpha>=8 bbox로 크기/위치만 계산하며 alpha 자체는 threshold하지 않고 전체 자체 RGBA affine을 사용. 원본mask stamp 없음. 원본보다 실제 더 멀리 그려진 glow를 삭제하지 않는다.

세부 시각 위험: 중앙 연기 고리의 자체 생성 구멍/회오리 굴곡이 원본과 달라졌고 g0가 상대적으로 더 빽빽함. 연기 고리 일부를 그리는 실제 OAM에서 형태/alpha 차이를 우선 확인. 보라구체 밝은 4개 spot과 어두운 팔레트 형상 전환도 확인. 실제 재생 QA를 수행하지 않았으므로 정상 판정으로 쓰지 않는다.
