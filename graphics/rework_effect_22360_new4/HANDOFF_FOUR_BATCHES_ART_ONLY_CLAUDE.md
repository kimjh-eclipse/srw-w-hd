# 후속4 묶음38개 — Claude 검증 대기

## 새 그림/계약
|IMG|계약|후보|native크기|PNG크기|
|---|---:|---|---|---|
|22360|4|candidate_22360.png|128×64|512×256|
|22030|9|candidate_22030_particles_v2.png (최신)|176×64|704×256|
|19982|14|candidate_19982.png|256×112|1024×448|
|22591|11|candidate_22591.png|64×32|256×128|

각 `new_candidate_<IMG>_contract.json`에 실제 cached OBJ raw index/16색 팔레트/해시/상태/offset/OAM좌표·변형·engine이 있다. 22030은 최신 `new_candidate_22030_v2_contract.json` 사용. 원본 IMG와 raw index bytes가 일치하는 source 위치만 사용했으며 원본 PLT 추정으로 채우지 않았다. 후보의 y는 palette-sheet를 쌓은 좌표이며 source_y와 다르다. 22360 두번째palette y32,19982 두번째palette y48.

4배/native크기와 각crop alpha존재/근접빈면적 확인. 또한 `prepared_presence_report.json`: 실제공유 prepare_texture를 메모리atlas+NullCache에서 호출해38/38 그림유지. 실제독립QA나후보재생검사는 하지 않았다. liveDB/코어/원본필터 변경 없음.

## 22030 파편 v2 수정
- 한 crop hash238205272/source128,0,32×32만 자체 생성 파편의 위치를 정렬. 다른8crop RGBA byte그대로.
- PNG SHA256 `dbfa463ca67180d971d4b18ec3854afdc12203bed536a5b94348311d1fe94809`.
- 원본 파편27개 위치에 자체생성15개를 이동. 부족한 원본1pixel점12곳은 같은 효과의 작은 자체생성 파편을 반복 배치했다. 색·크기·alpha·형태는 바꾸지 않았고 nativeRGB/alpha stamp 없음. 원본 component에서는 위치center만 읽었다.
- 준비 전의 무관한 위치 성분제거7개→v2 제거0개. 준비후maxA255,alpha≥16 565px,referencefill0,cutink0.
- `particle_repair_v2_production.json`, `repair_particle_positions.py`, `prepared_22030_particles_v2.png` 증거. root는동일9개재굽기할수있다.
- 원본의 큰 파편보다 생성 파편들이 작고 가늘게 그려진 점, 아주 작은 점에같은자체생성 조각이반복되는점은여전히Claude품질판정대기. 성분제거0이형태·색정상보장은아니다.

## 기존연결·모호한 source
- 실제기존38개보존:36개는w/h+rawindex+사용actual색직접일치. 22591의legacy17214/17159는index필드가없어원본reference의RGB와actualpalette유일성으로raw색번호재구성일치확인(`legacy_reference_proof.json`). 그림품질평가아님.
- 22418 actual7/22409 actual5 모두기존연결유지. 22370 보유fixture에서관측0이라새제작하지않음.
- 21748신규1및22030추가1은둘다hash1899085327/fullindex1 검정16×16으로여러IMG에동시에일치. 앞서19954에서도보류한것과같은모호한소유타일이며이번38에포함하지않았다.

## actual원본 palette 문맥 및 정확한Claude state
-22360 두팔레트: unit413 weapon1610 frame840.state +20..23 부근,노랑/주황색타격표시.
-22030: unit413 plasma360.state +33부근,흰핵/청록·파랑효과.
-19982 group0: unit413 weapon1613 frame1800.state +198부근. source raw index는바위/벽shape지만 **실제cached palette에파랑·노랑·자홍색이들어있고원본렌더계약도그색으로나온다.** 이를회색으로임의교정하지않고실제팔레트색위치대로새로그렸다. 이것이원래의공격중palette연출인지리소스소유문맥까지정확한지는Claude가반드시단독확인해야한다. 생성본의색을정상이라고보증하지않는다.
-19982 group1: 같은state +204부근의보라/검정바위palette. 두색단계의실제전환과겹침을확인해야한다. `contract_19982_0/1.json`의16값은서로별도actual계약이다.
-22591: unit413 weapon1610 frame840.state +40/44부근등,황색·적색작은파편. 모든offset은각contract frame 필드를우선한다.

## 알려진그림위험
-22360 고리의생성spike/구멍수가원본보다복잡해졌다. 원본형태가더단순해야하는지Claude확인대기.
-22030 흰면폭과주변cyanband,자체생성leaf처럼된작은파편및얇은분절빔의위치/간격.
-19982 암벽면의해석과특이actualpalette문맥,연속절단면에서새선이생기는지확인필요.
-22591 작은파편이원본보다polygon/leaf화된점과생성배치차이. 다른기체그림/다른색그림재색칠은하지않았다.

## 생성기록
Built-in image_gen transparent mode. 원본reference를입력으로해각팔레트별로독립새그림생성했다. 프롬프트공통:원본sheet좌표/크기/형태/빈공간유지,cut면외곽선금지,black투명,whitecore불투명,추가glow/mist/particle금지,도트계단은연속smooth선으로. 19982는actual파랑/노랑/자홍색위치유지및바위모양의금속/불꽃해석금지를명시. 원출력파일 `generated_<IMG>_<group>.png`와생성원출력파일명을`prepare_candidates.py`에보존.

생성후자체alpha threshold/min/max정리와전체bbox의위치/크기맞춤만했고nativealpha/RGB를찍지않았다. 이단계는제작·등록입력무결성이며실제게임정상확인은Claude의후속검증이다.

