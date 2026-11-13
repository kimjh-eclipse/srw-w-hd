# 실제 FX 19915 신규 그림 제작 인계

- 29 계약 / 19 고유 raw / 실제 전체 팔레트 2개. 원본은 retained rendered_obj_cache 실제 state/OAM/우선순위/변환/팔레트 계약. 대표 입력 `test_current\parts\native_weapon_source_95_391\unit95_weapon391_source.state` +335. 전체 frame과 source는 new_candidate_contract.json에 보존.
- 원본 IMG19915 crop과 각 actual raw byte 일치(source_integrity.json). IMG/PLT 기본값을 actual 팔레트로 추정하지 않음. source resource 소유 단정 없이 resource=None.
- 각 실제 palette당 한 새로운 전체 그림. 원본 source 영역이 교차하면 같은 palette의 한 생성 그림에서 나누므로 부분 crop 픽셀 동일. overlap 0쌍. 다른 기체/색변형 재색칠 없음.
- 후보 candidate.png [1024, 512] / native_combined.png [256, 128], SHA `dc236e8e3bd842c12ee03710a539fa0988612d0503a35a7057c2fe834a3d139b`. own generated_*.png와 입력 reference/native 보존. 원본 RGB/alpha stamp, 코드 색 채움 없음.
- 생산 prepare 29개 모두 maxA>=255, empty=0. 원본 RGB hash 계약 일치. 기존 prepare 분리성분 제거 항목 [(0, 1), (3, 1), (4, 1), (6, 1), (7, 1), (8, 1), (11, 1), (12, 1), (13, 1), (14, 1), (23, 1), (24, 1)]. 이 수치는 생산 존재 확인이며 실제 정상 HD 판정 아님.
- 생성 alpha preserve_generated 그대로. threshold220/이진화/MinFilter 없음. 원본 alpha는 source 문맥/geometry 참조용이며 후보에 붙이지 않음.
- 최신 live exact/indexed 중복 0개(latest_live_duplicates.json); 인수 시 root가 다시 최신 상태로 제외할 것.
- 알려진 문제/Claude 큐: 원본보다 추가된 명도 질감/입자/외곽선 변형, 여러 실제 palette 간 작은 형상 차이를 Claude가 실제 OAM에서 확인해야 함. 얇은 광/부드러운 광이 prepare 분리성분 제거에 의해 손실될 수 있음. 실제 layer 순서/크기/팔레트 변화/부분 연결 검증 대기.
- 라이브/library/DB/core/EXE 변경, 독립 audit/실재생 없음. 실패/보류를 정상 완료 수로 세지 않음.

## 최종 제작 범위와 알려진 한계
원본의 우측 큰 흰 L면 slot5(source192,0,64,32)는 전체생성에서 투명하게 빠져 두 차례 교정했다. 최종 whiteplane5_generated.png 자기 RGB/alpha를 해당 crop 위치에 resize해서 복원(whiteplane5_patch.json), 원본 mask/색 채움 없음. 거친 바깥 AA/얇은 암선과 대각 경계/내부코너가 원본과 다를 가능성 Claude 확인 필요. 나머지28 계약 원래 생성영역 보존. 기본 밝은 팔레트19+황색 팔레트10은 고유 raw19종의 두 실색 구성이지 고유 도형29종을 뜻하지 않음.
전체 alpha preserve_generated. native bbox는 위치/크기 참조에만 사용. 라이브/DB/runtime 변경 및 독립 QA/실제 재생 없음.
