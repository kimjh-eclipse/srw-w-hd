# 실제 FX 21921 신규 그림 제작 인계

- 15 계약 / 8 고유 raw / 실제 전체 팔레트 2개. 원본은 retained rendered_obj_cache 실제 state/OAM/우선순위/변환/팔레트 계약. 대표 입력 `test_current\parts\native_weapon_source_43_183\unit43_weapon183_source.state` +330. 전체 frame과 source는 new_candidate_contract.json에 보존.
- 원본 IMG21921 crop과 각 actual raw byte 일치(source_integrity.json). IMG/PLT 기본값을 actual 팔레트로 추정하지 않음. source resource 소유 단정 없이 resource=None.
- 각 실제 palette당 한 새로운 전체 그림. 원본 source 영역이 교차하면 같은 palette의 한 생성 그림에서 나누므로 부분 crop 픽셀 동일. overlap 0쌍. 다른 기체/색변형 재색칠 없음.
- 후보 candidate.png [736, 512] / native_combined.png [184, 128], SHA `11fce0c04e55cce460fa8a5d47b3c32e0da141810e54562de2971d1ad6110c58`. own generated_*.png와 입력 reference/native 보존. 원본 RGB/alpha stamp, 코드 색 채움 없음.
- 생산 prepare 15개 모두 maxA>=245, empty=0. 원본 RGB hash 계약 일치. 기존 prepare 분리성분 제거 항목 [(0, 1), (1, 2), (5, 9), (6, 2), (7, 3), (8, 2), (11, 6), (12, 3), (13, 2)]. 이 수치는 생산 존재 확인이며 실제 정상 HD 판정 아님.
- 생성 alpha preserve_generated 그대로. threshold220/이진화/MinFilter 없음. 원본 alpha는 source 문맥/geometry 참조용이며 후보에 붙이지 않음.
- 최신 live exact/indexed 중복 0개(latest_live_duplicates.json); 인수 시 root가 다시 최신 상태로 제외할 것.
- 알려진 문제/Claude 큐: 원본보다 추가된 명도 질감/입자/외곽선 변형, 여러 실제 palette 간 작은 형상 차이를 Claude가 실제 OAM에서 확인해야 함. 얇은 광/부드러운 광이 prepare 분리성분 제거에 의해 손실될 수 있음. 실제 layer 순서/크기/팔레트 변화/부분 연결 검증 대기.
- 라이브/library/DB/core/EXE 변경, 독립 audit/실재생 없음. 실패/보류를 정상 완료 수로 세지 않음.

## 최종 제작 범위와 알려진 한계
전체생성은 극소 세로선(slot2)과 분리 점선곡선(slot4)이 좌표가 어긋나 prepare에서 거의 사라졌다. repair2_generated.png와 repair4_generated.png를 같은 효과로 별도 새 생성 후 자기 alpha>=32 bbox를 위치 산정에만 사용, native bbox 크기/위치에 own RGBA를 등록했다(small_repairs_registration.json). alpha를 이진화/원본mask전사하지 않았고 최종sheet 한 영역으로 모든 교차 crop이 공유한다. 점선 개수/간격과 원본보다 두꺼운 cyan/glow/사각chip 형상 변화, 기타palette 회색 선의 자체 gray outline/haze는 Claude 실재생 대기. 15계약/8고유raw/2실팔레트.
전체 alpha preserve_generated. native bbox는 위치/크기 참조에만 사용. 라이브/DB/runtime 변경 및 독립 QA/실제 재생 없음.
