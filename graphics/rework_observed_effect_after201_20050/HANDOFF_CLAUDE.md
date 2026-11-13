# 실제 FX 20050 신규 그림 제작 인계

- 16 계약 / 16 고유 raw / 실제 전체 팔레트 1개. 원본은 retained rendered_obj_cache 실제 state/OAM/우선순위/변환/팔레트 계약. 대표 입력 `test_current\parts\native_weapon_source_248_1015\unit248_weapon1015_source.state` +320. 전체 frame과 source는 new_candidate_contract.json에 보존.
- 원본 IMG20050 crop과 각 actual raw byte 일치(source_integrity.json). IMG/PLT 기본값을 actual 팔레트로 추정하지 않음. source resource 소유 단정 없이 resource=None.
- 각 실제 palette당 한 새로운 전체 그림. 원본 source 영역이 교차하면 같은 palette의 한 생성 그림에서 나누므로 부분 crop 픽셀 동일. overlap 0쌍. 다른 기체/색변형 재색칠 없음.
- 후보 candidate.png [768, 192] / native_combined.png [192, 48], SHA `5c8277a874b1d3f128c1a525de9c1c45629ad3e54326b10d872158c20decc41e`. own generated_*.png와 입력 reference/native 보존. 원본 RGB/alpha stamp, 코드 색 채움 없음.
- 생산 prepare 16개 모두 maxA>=247, empty=0. 원본 RGB hash 계약 일치. 기존 prepare 분리성분 제거 항목 [(1, 1), (5, 2), (6, 1), (11, 5), (15, 3)]. 이 수치는 생산 존재 확인이며 실제 정상 HD 판정 아님.
- 생성 alpha preserve_generated 그대로. threshold220/이진화/MinFilter 없음. 원본 alpha는 source 문맥/geometry 참조용이며 후보에 붙이지 않음.
- 최신 live exact/indexed 중복 0개(latest_live_duplicates.json); 인수 시 root가 다시 최신 상태로 제외할 것.
- 알려진 문제/Claude 큐: 원본보다 추가된 명도 질감/입자/외곽선 변형, 여러 실제 palette 간 작은 형상 차이를 Claude가 실제 OAM에서 확인해야 함. 얇은 광/부드러운 광이 prepare 분리성분 제거에 의해 손실될 수 있음. 실제 layer 순서/크기/팔레트 변화/부분 연결 검증 대기.
- 라이브/library/DB/core/EXE 변경, 독립 audit/실재생 없음. 실패/보류를 정상 완료 수로 세지 않음.

## 극소 파편 보완과 미해결
- slot13 hash3174226672, native source(128,24,32,8)는 불투명 9px가 여섯 성분으로 떨어진 파편이다. 처음 3개로 잘못 해석한 후보는 prepare 뒤 사실상 비어서 미사용으로 보존했다.
- 최종 tiny13_six_generated.png는 이 효과 자신의 6개 파편을 새로 그린 생성본이다. 자신의 각 생성 성분 RGBA를 원본 성분 bbox 위치/크기에만 정렬했다(tiny13_registration.json). 원본 alpha 모양을 전사하지 않았고 색을 코드로 채우지 않았다. 성분 bbox가 1~2 원본픽셀 크기여서 고해상도 사각 조각 형태/명도 변화는 Claude 판정 대기다.
- 전체 원본 sheet 단일 그림 공유에 이6파편만 새 생성 패치를 같은 sheet 좌표에 붙였다. 부분 교집합은 모두 최종 한 sheet를 읽는다. 다른 15계약 crop이 패치와 교차하는 경우 같은 픽셀로 재준비했다.
- 최종 prepare16 모두 maxA>=16, support ratio<.1 없음. raw source16 계약/실제 palette 그대로, 최신 live 중복0. 이는 생산 존재/해시 정합 확인이고 실제 HD QA는 아니다.
- 20050 전체 생성본은 주변 저알파 cyan haze와 원본보다 두꺼운 작은 glint가 남는다. 알파 threshold/노이즈 제거 필터를 적용하지 않았으며 실제 선 손실·형태·레이어는 Claude에게 요청한다.
