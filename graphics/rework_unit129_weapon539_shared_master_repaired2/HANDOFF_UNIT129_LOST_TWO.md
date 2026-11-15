# unit129/w539 두 연속 기계조각 소실 교정 후보

상태: 같은 ID #94994/#94993 새 후보. 신규 미연결 증가0. 라이브/공식 QA/실제HD 재생/DB쓰기/코어변경 없음.

## 실제 원본과 현재 그림 대조

- 최신 current classified machine lost이며 live atlas observed_unit129_weapon539_nine가 같은 것을 확인했습니다. 원래 source는 unit129_weapon539_attack350_missing/contract.json의 actual cached OAM 두 행입니다.
- source_mechanical_fixed_129_539_350/source_pose.state +0, 화면 위치188,76 큰32×16과220,76 작은8×8. 실제 source IMG10442의168,16/200,16으로 맞닿고 full16은 같은 PLT1781 bank0입니다. source 정보는 원래 source_identity/fullpalproof와 실제 raw를 대조한 계약입니다. 카탈로그 해부학적 역할을 추정하지 않았습니다.
- 현재 live actualRGB/index/전체 실제 palette와 원래 cached 계약의 CRC를 재계산해 일치시켰습니다. 현재 texture_key로 SQLite를 mode=ro로 열어 SELECT만 해 baked RGBA를 읽었습니다. 원본 상태와 현재 구운 상태를 모두 저장했습니다.
- 큰조각 원본322texel 중33.5% 미칠, 끝7texel 중42.9% 미칠입니다. 실제 원본의 은회색 하부 구조가 큰 파츠 새그림에서 없어졌고 작은 끝도 가늘어졌습니다. 따라서 소수 AA 차이로 보존하지 않고 새로 그렸습니다.
- 정상 부모 안의 동일 child가 아니며 서로 맞닿는 두 파츠입니다. 정상 다른7개는 spec 불변으로 보존(preserved_normal7_latest.json). 다른 실제 unit130 의존파일의 hash1901310391은 이번 두 hash와 달라 이번 교체가 그 장면까지 해결했다고 넓혀 주장하지 않습니다.

## 새 그림과 분할

- generated_master_raw.png: imagegen 새 출력 exec-3f79391f-2934-4bbf-ac22-b390686cb091.png. 기존 잘못된 그림을 재색칠하지 않았습니다.
- 전체 actual40×16 원본을 하나의 참조로, 파란 두 장갑과 오른쪽 은회색 상부 연결부뿐 아니라 하부까지 이어지는 실제 재질을 새로 그렸습니다. 임의의 손가락/나사/돌기/광선/단순 도트확대 없이 연속 평면 명암으로 요청했습니다.
- 자체 생성 RGBA의 전체 bbox를 기하 정렬만 했습니다. 원본 RGB/alpha 전사·알파 문턱 삭제·native mask/침식/팽창은 없습니다.
- continuous_master_hd.png의 같은 생성 영역을32×16과8×8 원래 OAM 사각으로 분할했습니다. continuous_generated_split_proof.json은 두 최종 crop 모두 같은 master와 RGBA 완전동일함을 증명합니다. 잘린 경계에 별도 검은 캡이나 다른 새그림을 넣지 않았습니다.
- 작은8×8 사각 아래 불가용 영역에는 생성 AA가14픽셀(alpha16 이상/최대106) 걸칩니다. alpha128이상은0이며 원래 OAM 사각 crop으로 제외됩니다. 이 남은 반투명 차이를 숨기거나 원본 지원 마스크를 찍지 않았습니다(master_split_support.json).

## 설치

- installation_map.json: 큰 #94994→source_cell0/atlas_box0,0,32,16; 작은 #94993→source_cell1/atlas_box32,0,8,8.
- contract.json actual hash/index/fullpal/source original/old flags 보존. candidate_atlas.png/native_atlas.png와 함께 사용.
- candidate_atlas.png SHA256 `b5e0f73a680eba8c846c5c2a50c939e6650967af7cad577e6bafe5fee1b9731e`.
- candidate 및 NullCache prepare 사전기하 flags0. 큰조각 IoU .943/미칠 .009/외부0, 작은끝 .875/미칠0/외부0.
- continuous_replacement_comparison.png는 actual 원본/현재 baked/새 그림 순서입니다. 직접 제작 비교에서 은회색 하부 복원/끝의 연속성을 확인했으나 공식 QA·실제 게임 완료 판단이 아닙니다.

## Claude 확인 위험

- 새로운 은회색 하부와 큰 파란 장갑의 경계가 기존 정상 기체 부품과 이어지는지 실제 자세에서 확인해야 합니다. 모델의 매끈한 금속 하이라이트가 원본보다 밝거나 평면적일 수 있습니다.
- 실제 작은 끝 7texel은 경계 AA에 민감하며 여전히 IoU .875 차이가 남습니다. OAM 불가용 영역의 반투명14픽셀 제외 영향도 실제 조립에서 확인 필요합니다.
- 전체 팔/전체 무장 완료가 아니라 같은 실제 두 조각의 교체입니다. 다른 색 단계/관측되지 않은 자세/다른 unit130까지 완료로 세지 않습니다.
