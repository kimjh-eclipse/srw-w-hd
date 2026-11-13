# 신규 효과 5개 고유 묶음 — 원본 제작 계약·그림 후보 인계

## 설치용 후보 (root만 라이브 등록/굽기)

|IMG|새 고유 계약|atlas_id|후보 / 계약|native크기|PNG크기|
|---|---:|---|---|---|---|
|19954|16|observed_effect_19954_new|candidate_19954.png / new_candidate_19954_contract.json|176×32|704×128|
|21921|13|observed_effect_21921_new|candidate_21921.png / new_candidate_21921_contract.json|56×64|224×256|
|22338|24|observed_effect_22338_new|candidate_22338.png / new_candidate_22338_contract.json|168×96|672×384|
|22410|19|observed_effect_22410_new|candidate_22410.png / new_candidate_22410_contract.json|192×64|768×256|
|22497|14|observed_effect_22497_new|candidate_22497.png / new_candidate_22497_contract.json|128×64|512×256|

합계 **86개 계약**. 행별로 w/h, source_x/y, 현재16색 팔레트, index_pixels, raw SHA, RGB/indexhash, rendered OAM attrs/좌표/변형/engine, state/frame, 실제 바인딩 hash 대조가 들어 있다. 후보의 x/y는 새 atlas 안의 위치이며 source_x/y와 두 팔레트 sheet offset을 혼동하지 말 것. 22338 두번째 palette는 y64, 22410/22497 두번째는 y32.

## 생산 무결성
- `mechanical_<IMG>.json`: 4배 크기, PNG SHA, 각 crop maxA≥16 및 원본 불투명 면적 대비 생성 alpha지원 면적≥0.1 확인. 원본 형태 점수/화질 통과 판정 아님.
- 모든 그림은 built-in imagegen 새 생성. 후보 픽셀은 생성본 RGB/alpha만 사용했다. native mask/RGB 강제 복사·native flatcolor 코드칠하기 없음.
- 생성 alpha만 220 threshold + min3/max3으로 미세 외부 잡음 제거. 생성 전체bbox를 native 전체bbox에 위치/크기만 맞춘다. 원본 pixelmask를 찍지 않는다.
- 22410 green variant의 source(16,0,16,16)가 처음 생성에서 빠졌다. 해당 1개를 같은 실제 팔레트의 별도 새 그림으로 생성하여 `repair_22410.py`로 복원했다. 19개 전부 alpha생산 조건 만족. 단 native 형태/실제 연속면 품질은 Claude 대기.
- 22338 최초 생성이 도트를 키운 듯한 계단 형태를 답습하여 새 smooth 출력 `exec-96b1f4c0-0e21-4eef-9614-657b15823f72.png`로 교체했다. 최초 출력은 설치용이 아니다.
- `prepare_candidates.py` 재실행 후 반드시 `repair_22410.py`, `make_comparisons.py`를 실행해야 최종과 같다.

## 기존 계약·중복 보존
- 21279 actual17개 모두 현재 exact. 새 그림 제작/교체 안 함.
- 19954 actual19 중 기존2개, 새 cream/lavender16개. 나머지1개는 16×16 전체 index1 + 검정 RGB 평면으로 여러 source IMG에 동시에 일치한다. 정확한 소유가 모호하여 제작/설치 보류. `contract_19954_0.json`에 별도 보존.
- 22497 actual22 중 기존 safe indexed8개 보존. `existing_indexed_overlap.json`: w/h와 실제 raw index bytes8/8 일치. 현재 팔레트는 런타임에서 공급되는 기존 dynamic binding이며, 같은 그림 색 구성이라는 품질 보장은 하지 않았다.
- `existing_overlap_proof.json`: exact기존19개 중18개는 rawindex+사용색+w/h 직접 일치. legacy4469는 index/palette 필드 없는 이전 형식이어서 원본 reference에서 실제 RGB/색번호 유일성으로 복원, `legacy_4469_reference_proof.json`에 기록(복원 가능 참). 기존 live수정 없음.
- 20928 actual2개는 19954 신규16개와 w/h+raw index bytes+사용 actual 팔레트 모두 동일하다. `cross_batch_same_contracts.json`. **20928의 자체 생성2 후보는 비교 선택지로만 보관하고 기본 설치/신규 숫자에 추가하지 말 것.** 19954가 설치되면 동일 계약을 공유한다.

## Claude 실제 확인 큐
- `observed_contract.json` 및 각 설치계약의 state/frame이 정확한 원본 채집 위치. 원본 cachedOBJ+rendered OAM만 캡처했으며 신규 HD 후보의 실제 재생 검사는 하지 않았다.
- 대표 source: 19954 cream/lavender=unit413 weapon1613 frame600 근처, 21921=unit413 plasma1080/1200, 22338=unit1 attack7108_connected, 22410=unit413 weapon1613 frame1320, 22497=unit413 weapon1613 frame840/2040. 자세한 offset은 개별 계약 frame 참조.
- `comparison_<IMG>.png`: 왼쪽 원본 4배 nearest, 오른쪽 생성 후보. 이것을 생성/등록 완료 판정으로 해석하지 말 것.
- 남은 위험: 19954의 부분 원형/직선 cut 면에 미세한 생성 외곽선이 남을 수 있음. 21921 직선 fill부분의 생성 gradient와 굵기 차이. 22338 작은 입자가 원본보다 기하학적 잎 모양으로 바뀐 부분/얇은 절단선. 22410 두 palette의 색밴드 폭·보정한 작은 continuation과 옆 beam 접합. 22497 바위 facet 과장 및 cyan 단색 조각의 미세 gradient/둥근 형태. 전체bbox 정렬이라 작은 개별 파츠의 위치·곡률 차이 가능.
- 가림/UI/레이어/진동/로딩/실제 팔레트 변형 정상 여부는 검증하지 않았다. Claude에서 각 한벌 전체를 실제 등장시키고 판정해야 한다.

## 생성 프롬프트와 도구
Built-in image_gen, transparent_background=true. 각 native reference를 입력으로 지정하고 다음 제약을 사용했다: 원본 source sheet의 각 part 좌표·크기·각도 유지, 검정은 투명, 원본의 실제 cream/lavender·cyan/blue·orange/red·white/green·green·gray·cyan 색 구성 각각 별도 새 생성, cut면 외곽선 금지, 추가 particle/glow/mist 금지, 원본 계단은 매끈한 연속선으로. 22338 최종은 'NO PIXEL ART, NO stair steps, NO blocky squares, each spike single continuous smooth taper'를 추가. 사용한 생성 원출력은 `generated_<IMG>_<group>.png` 및 생성/등록 스크립트 파일명에 보존했다. 다른 기체나 다른 색 그림 재색칠은 사용하지 않았다.

라이브 library/DB/core/EXE/사용자창/설정 수정 없음. 공식 audit/독립 QA/신규 HD 후보 playback 없음.
