# 실제 FX 21748 신규 그림 제작 인계

- 16 계약 / 16 고유 raw / 실제 전체 팔레트 3개. 원본은 retained rendered_obj_cache 실제 state/OAM/우선순위/변환/팔레트 계약. 대표 입력 `test_current\parts\native_weapon_source_100_420\unit100_weapon420_source.state` +550. 전체 frame과 source는 new_candidate_contract.json에 보존.
- 원본 IMG21748 crop과 각 actual raw byte 일치(source_integrity.json). IMG/PLT 기본값을 actual 팔레트로 추정하지 않음. source resource 소유 단정 없이 resource=None.
- 각 실제 palette당 한 새로운 전체 그림. 원본 source 영역이 교차하면 같은 palette의 한 생성 그림에서 나누므로 부분 crop 픽셀 동일. overlap 2쌍. 다른 기체/색변형 재색칠 없음.
- 후보 candidate.png [768, 768] / native_combined.png [192, 192], SHA `6974732b432063755aa6dbb01e2cdffb2fd30c4b4534cba7a209a8878564e377`. own generated_*.png와 입력 reference/native 보존. 원본 RGB/alpha stamp, 코드 색 채움 없음.
- 생산 prepare 16개 모두 maxA>=255, empty=0. 원본 RGB hash 계약 일치. 기존 prepare 분리성분 제거 항목 []. 이 수치는 생산 존재 확인이며 실제 정상 HD 판정 아님.
- 생성 alpha preserve_generated 그대로. threshold220/이진화/MinFilter 없음. 원본 alpha는 source 문맥/geometry 참조용이며 후보에 붙이지 않음.
- 최신 live exact/indexed 중복 0개(latest_live_duplicates.json); 인수 시 root가 다시 최신 상태로 제외할 것.
- 알려진 문제/Claude 큐: 원본보다 추가된 명도 질감/입자/외곽선 변형, 여러 실제 palette 간 작은 형상 차이를 Claude가 실제 OAM에서 확인해야 함. 얇은 광/부드러운 광이 prepare 분리성분 제거에 의해 손실될 수 있음. 실제 layer 순서/크기/팔레트 변화/부분 연결 검증 대기.
- 라이브/library/DB/core/EXE 변경, 독립 audit/실재생 없음. 실패/보류를 정상 완료 수로 세지 않음.

## 基본형태 / 실제 색변형 구분 (최종)
- 16계약은 각각 고유 raw 도형의 현재 관측 중 가장 밝은 실제 palette를 골랐다. 원본에 관측되지 않은 기본색이나 PLT색을 추정하지 않았다. 다른 11개 actual 색변형은 held_fade_source_base_pairs.json에 base hash/원본actual/state/frame/기본후보 그림을 연결했다. 이 11개는 신규그림 및 완료수 제외.
- 실제 palette별로 각자 새 그림을 생성했다. 21748은 3팔레트(분홍/청백/어두운청색),22409는 2팔레트(분홍/청백)이며 다른 palette의 RGB/alpha를 빌리거나 재색칠하지 않았다. 같은 source IMG 영역의 교집합은 palette마다 한 sheet를 나눠 같은 픽셀을 공유한다.
- 미해결: 원본의 거의 일정한 pale 면이 생성본에서는 테두리 gradient가 강해지고, 실제 alpha가 아주 작은 외부 흰색/자홍/청색 haze가 남는다. 자동 알파threshold로 일괄삭제하지 않았음. 내부 직선 절단면의 명암 연결/흰 중심 불투명 유지/가는 파편 및 빔효과 전면순서는 Claude 실제조립 검증 대기. 약한 haze를 새 유효효과라고 확정하지 않음.
- source_overlap.json/production_report.json은 제작 입력/준비 존재 확인이며, 실제 시각정상 QA가 아니다. 라이브/DB/runtime 변경 없음.
