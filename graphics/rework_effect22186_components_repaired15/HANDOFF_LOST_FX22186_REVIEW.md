# 22186 이펙트 문제15 교체 후보 인계

상태: **공식 미검증 후보15 = 새 그림13 + 정상 부모 그림의 포함 영역 공유2**. 신규 누락이나 새 완성 수 증가 없음. 공식 검사·실제 HD 재생은 Claude 담당이다. 라이브/DB/코어 변경은 하지 않았다.

## 파일과 설치

- installation_map.json / candidate_atlas.png / native_atlas.png / contract.json을 함께 사용한다.
- 후보 SHA256: 92b0deba18a541a541feac51e994df9fba77101469da1f338e89353a9b1d7d4b
- 새 그림13: 93382,93383,93377,93378,93385,93386,93387 / 93390,93392,93397,93395,93400,93391.
- 기존 큰 생성 그림에서 같은 영역을 공유하는 child2: #93407←정상 #93393 아래16행, #93408←정상 #93394 아래16행. 별도 새 그림으로 세지 않는다.
- 정상18의 전체 spec SHA는 preserved_normal18.json / latest.json에서 모두 불변이다.

## 실제 원본과 색

15개 모두 next_confirmed_fx_source/art_22186/source_contract.json에 보존된 실제 cached OBJ다. 대표 fixture는 native_weapon_source_4_19/unit4_weapon19_source.state +510/515/520/593, 개별 frame/video_epoch/OAM/attrs/flip/actual full BGR555 palette는 contract.json에 보존했다. 미관측 ROM 패턴 확장이 아니다. 실제 IMG22186 대응 좌표와 원래 소유 미확정 상태를 유지했다.

mechanical_input_identity.json에서 index bytes/전체 실제 팔레트/크기와 BGR555 CRC를 다시 계산해 기존15 ID와 일치했다. source_intersection_review.json은 정상 큰 그림과 겹치는2개를 찾아냈다. shared_normal_parent_child_proof.json에서 같은 raw 원본 부분/전체 팔레트/리소스를 검산하고 기존 생성 RGBA를 그대로 공유했다. 원본 도트의 RGBA나 alpha를 후보에 덮어 찍지 않았다.

밝은7은 흰 핵+실제 연민트 가장자리이고 암회색6은 실제 #181818~#414141 불투명 방전 덩어리다. 두 그룹은 raw형상이 같아도 실제 전체 팔레트가 달라 독립 생성했다. 밝은/어두운 그림이나 alpha를 서로 재색칠/복사하지 않았다.

## 제작 방식과 작은 성분

imagegen 스킬의 기본 내장 도구 사용. reference_group0.png / group1.png는 원본과 위치 참조, generated_bright_raw.png / generated_dark_raw.png는 원본 생성 결과를 불변 보존했다. 전체 생성 RGBA를 각 원본 bbox 위치/크기로 기하 정렬했다. alpha160은 정렬 앵커 측정에만 쓰였고 출력 alpha 임계처리/형태 닫기/픽셀 삭제는 하지 않았다. 생성 원본과 프롬프트는 PROMPT_SET_KO.md 참조.

두 흩어진 불씨 그림 #93377/#93390는 실제 원본9성분이며 생성된 고알파 성분도9개다. 초안 프롬프트에는8개라고 잘못 적혔지만 실제 생성물은 원본과 같은9개라 9개를 모두 보존했다. 한 성분도 임의 삭제하지 않았다.

NullCache의 prepare_texture로 후보15를 메모리에서만 준비했다. 원본 **31개 성분의 각 bbox**에 유효 paint(alpha16 이상)가 모두 남는다(per_component_prepare_presence.json). 전체 maxalpha만 확인한 것이 아니다. 이것은 작은 성분 소실 방지를 위한 생산 진단이며 공식 화질 QA 통과가 아니다.

## Claude 확인 필요

- 새 그림은 원본처럼 굵은 본체를 보존했지만 민트 가장자리 둥글기/명암이 강해질 수 있다. 밝은 효과의 원래 각진 끝과 실제 곡률을 비교한다.
- 암회색6은 투명 구멍으로 바꾸지 않았으나 생성 모델의 부드러운 명암/반투명 AA가 원본과 다른 농도로 보일 위험이 있다. prepared_alpha_colour_statistics.json에 통계만 기록했고 색·alpha를 강제로 맞추지 않았다.
- 정상 부모2에서 가져온 child는 원시 생성 RGBA 공유다. parent/child를 각각 prepare할 때 정렬 결과가 같은지, 실제 겹침 경계가 연속인지 Claude가 확인해야 한다. 별도 새 그림 해결로 주장하지 않는다.
- fixture +510~520의 동시 방전, +593의 dark child와 기존 큰 그림 전환을 확인한다. 모션/효과 플래그, lookup역할, dynamic_palette는 원래대로 유지한다.
