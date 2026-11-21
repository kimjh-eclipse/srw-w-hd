# HANDOFF TO CODEX 10 (Claude → 코덱스)

`HANDOFF_TO_CODEX_9.md`가 3,600줄을 넘어서 이 파일부터 새로 적는다. 아래는 지금 유효한 결정과 열린 항목만 요약한 것이다. 세부 근거는 9번 파일을 참고한다.

## 지금 유효한 결정 (2026-11-20 기준)

- 쉐이더는 xBRZ 4배(`SRWW_NATIVE_OBJ_FILTER=xbrz`)를 쓰고, 다른 필터는 비교하지 않는다(사용자 결정).
- 재색칠 금지는 로봇 파츠에만 적용한다. HUD 숫자(빨간 HP)나 이펙트처럼 로봇이 아닌 그림은 게임 팔레트대로 HD를 보여 준다. 그래도 그림은 원본 팔레트 그대로 그린다.
- 스트라이크 계열(11~22, 39~45)의 공용 파츠는 출처 기체를 하나만 쓴다(`_strike_owner/OWNERS.json`). 이 파츠는 다시 그리지 않는다.
- 아이콘(작은 기체 그림)은 OAM 번호가 작은 조각을 앞에 그린다. 11/19에 다시 만들었다.

## 열린 항목

- 3·4·5번 기체 99자세(11/20 납품): Claude가 검수·분할·설치할 차례다.
- 확대·회전 자세: 894개 중 136개만 그림이 왔다. 판은 `SHEETS/sheet_aNN`에 있다.
- 155~160번 기체: 코덱스 보류 표시가 있어 설치하지 않았다.

## 2026-11-20 컷인 일괄 요청 — 공격 장면의 BG 그림 중 HD가 없는 것 전부

사용자 지시는 다음과 같다: "타이가 골디온 스테이지, 크루제 헬멧, 마징카이저 파이어 블래스터를 비롯해서 비슷한 방식의 컷인들 찾아보고, 모두 요청해."

### 찾은 방법

- 공격 시작 장면 660개(무기 1,804개 중 시작 장면을 만들어 둔 것)를 HD 켠 상태로 끝까지 돌렸다.
- 6프레임마다 BG 레이어를 확인해, HD 컷인이나 HD 배경으로 바뀌지 않았는데 그림 영역에 크게 보이는 레이어를 기록했다. 그 레이어의 타일 바이트를 ROM IMG와 대조해 IMG 번호를 확정했다.
- 표본 4개는 HD 렌더로 원본 그대로인 것을 눈으로 확인했다.
- 단색이거나 빈 레이어(311장)는 그릴 것이 없어 뺐다. 남은 것은 **693장, 302묶음**이다. 묶음은 한 공격에서 번호가 이어지는 그림, 즉 같은 컷인의 연속 프레임이다.

### 자료 — `test_current/parts/cutin_requests/batch_20261120/`

- `INDEX.json`: 묶음별로 IMG 번호, BG 레이어, 장면(공격 시작 state와 프레임), 쓰이는 공격 목록, 캔버스 크기, 이미 같은 번호의 HD 파일이 있는지를 적었다.
- `G<NNN>/<img>_canvas.png`: **이것이 그리기 기준이다.** 그 프레임의 VRAM에서 레이어 전체(맵 크기 전체)를 실제 화면 팔레트로 풀었다. 색 번호 0은 투명이다. `_canvas_4x.png`는 4배 nearest 사본이다.
- `G<NNN>/<img>_screen.png`: 게임 화면 전체. `_layer.png`: 그 레이어만 그린 것(256×192).
- `OVERVIEW_00~06.png`: 묶음마다 대표 화면 한 장씩 모은 목록이다.

### 그리는 법 (기존 컷인 요청과 같다)

- 캔버스 크기의 4배로 그린다. 원본 팔레트 색을 그대로 쓰고 자동 틴트는 하지 않는다. 원본에서 투명(알파 0)인 곳은 알파 0으로 둔다.
- 스크롤되는 배경(캔버스가 화면보다 크고 흐르는 것)은 흐르는 방향의 끝이 이어지게 그린다.
- 같은 묶음의 연속 프레임(표정 변화, 번쩍임 등)은 같은 화풍과 같은 선으로 맞춘다. 묶음 안에서 팔레트만 다른 프레임은 그 팔레트 그대로 따로 그린다(재색칠 금지).
- 위에 겹치는 OBJ 효과(빛줄기, 파편)는 그 레이어 그림이 아니니 그리지 않는다.

### 우선순위

1. 이미 요청했던 세 건은 이번 묶음에도 들어 있다: G011(크루제 22864)·G200(26391 파란 스캔라인), G069(타이가 무대 23591), G025(마징카이저 23021)·G117(24557 녹황 배경).
2. 인물 얼굴과 로봇 클로즈업 컷인. OVERVIEW에서 인물이나 로봇이 보이는 묶음.
3. 무대·배경·효과 그림(속도선, 폭발, 소용돌이, 빛 등).

### 코덱스가 그리지 않아도 되는 것 (Claude 몫)

- G011 22864, G012 22867, G013 22870, G060 23514, G150 24898, G152 25083, G177 25658은 같은 번호의 HD 파일(`graphics/pilot_cutins/cutin_<id>_hd.png`)이 이미 있는데 연결이 안 된다. Claude가 연결을 고친다. 단, 22864 크루제는 기존 그림이 가면 없이 그려져 틀렸으니 새로 그려 달라(9번 파일 11/18 요청 그대로).

### 아직 못 찾은 범위

- 시작 장면이 없는 무기 1,144개(합체·MAP 무기 포함)는 아직 스캔하지 못했다. 시작 장면을 만드는 대로 같은 방법으로 찾아서 추가로 요청한다.

### 추가 스캔 (11/20 10:54, Claude 메모)

- 시작 장면을 888개 더 만들어 스캔했다(무기 1,804개 중 1,558개까지 확인). 합체기·MAP 병기 246개는 시작 장면을 만들 수 없었다.
- 첫 묶음에 없던 그림이 96장 더 나왔다. 이 중 단색이거나 빈 것 44장을 빼고, **52장(28묶음)을 추가로 요청한다.** 자료는 `test_current/parts/cutin_requests/batch_20261120_add/`(구성·그리는 법·우선순위는 위 batch_20261120과 같다)에 있고, 목록 그림은 `OVERVIEW_00.png`이다.

## 2026-11-20 Claude: 계열 출처 정리 + 테두리(부드러운 윤곽) 전체 적용

- 출처 정리: 듀얼(54~57)·가오가이가 8기체(323·324·361·367·368·386·392·403)·블릿츠(53·449)·딘(70·72·92)의 공용 파츠를 각각 한 기체 그림에서만 가져오도록 다시 설치했다(`scripts/assets/family_owner_install.py`, 출처 목록 `pose_packets/_family_owner/<tag>/OWNERS.json`).
- 테두리: 조각 알파를 원본 도트 4배 모양으로 자르던 것을, 그림 자체의 윤곽선 알파를 따르도록 바꿨다. 실루엣 밖 4px 고리는 가장 가까운 조각에 붙인다(`split_object_drawings.EDGE_RING`, `split_fit/cov/`, `package_robot_set`). 진·게이츠로 먼저 확인한 뒤 설치된 기체 전체에 다시 설치하는 중이다(`scripts/assets/softedge_rollout.sh`, 이어서 실행 가능).
- 코덱스에게: 그림 바깥 테두리(검은 잉크선과 안티에일리어싱)가 이제 게임에 그대로 보인다. 윤곽선을 끊기지 않게 그려 달라. 원본 실루엣 밖으로 4px 넘게 삐져나온 부분은 잘린다.

## 2026-11-21 Claude: 컷인 연결

- 크루제(G011 22864·G200 26391): 코덱스 11/18 RAW를 실루엣에 맞춰 연결했다. id 19는 그림을 교체하고 맵 지문을 실측값으로 바꿨다. 26391은 새 id 207로 넣었다(`scripts/assets/install_creuset_cutin.py`). **두 그림은 더 그리지 않아도 된다.**
- 이미 HD가 있는데 맵 지문(ROM 맵 폭이 32칸이 아님) 때문에 연결이 안 되던 것 3장을 실측값으로 고쳤다: G150 24898, G152 25083, G177 25658(`scripts/assets/fix_cutin_map_windows.py`). **이 세 장도 그리지 않아도 된다.**
- 밴드 탐색 방식에서 맵 지문이 달라 연결이 안 되던 5장도 실측값으로 고쳤다: 22867, 22870, 22813, 23322, 24405. **그리지 않아도 된다.**
- 23514는 기존 HD의 표정이 원본과 달라(원본은 웃는 입) 연결하지 않았다. **새로 그려 달라.**
- 23076·23299·23317·24640은 타일 지문이 어떤 방식으로도 맞지 않아, Claude가 계속 확인한다. 요청 목록에는 그대로 둔다.

## 2026-11-21 게이츠(74·75·76·93) 다시 그리기 요청 — 사용자 지적

- 문제 1, 얼굴: 지금 그림은 얼굴 아래를 **흰 부리·마스크 모양**으로 그렸다. 원본 도트와 설정은 **어두운(짙은 회녹색) 얼굴, 가로 슬릿 안의 분홍·빨간 모노아이, 그 아래 어두운 턱**이다. 흰색이나 밝은 색은 얼굴에 쓰지 않는다. 모든 자세에 해당한다.
- 문제 2, 위치: 팔·어깨·방패·다리의 위치와 크기가 원본 도트(`unit_74/robot_set/pose_NN/native_4x.png`)와 맞지 않는 자세가 많다(pose_01·pose_03 등). 원본 도트를 아래에 깔고 **윤곽과 부품 위치가 칸 단위로 겹치게** 그려야 한다. 부품을 새로 배치하거나 비율을 바꾸지 않는다.
- 처리: Claude가 74·75·76·93에 HOLD_REDRAW를 걸었다. 롤아웃이 끝나면 설치된 HD 파츠를 끄고, 다시 그린 그림이 오기 전까지 원본(xBRZ)으로 보여 준다.
- 판은 기존 `unit_74/robot_set/SHEETS/sheet_NN`을 그대로 쓴다. 74를 그리면 같은 파츠를 쓰는 93도 해결된다. 75·76은 같은 기체의 다른 세트라 따로 확인한다.

## 2026-11-21 재검수 결과 — 다시 그리기 요청 (설치된 407기체 전수)

- 방법: 자세마다 원본 도트(4배)와 그림을 같은 크기로 나란히 놓고(`pose_packets/_rereview/unit_<U>_NN.png`) 얼굴(눈·턱·마스크 모양과 색)·부품 위치와 크기·없는/지어낸 부품과 색을 봤다. Claude가 불합격 표본과 합격 표본을 직접 다시 확인했다.
- 불합격 74기체. 자세의 30% 이상이 틀린 23기체는 HD를 전부 끄고, 나머지는 틀린 자세에만 쓰이는 파츠만 끈다(롤아웃 직후 적용). 모두 HOLD_REDRAW.
- 흔한 실수(다시 그릴 때 꼭 피할 것): ① 로봇 얼굴을 흰 턱·흰 마스크·사람 얼굴로 바꿈 ② 눈 색 바꿈(청록 눈을 노랑/초록/흰색으로, 분홍 모노아이를 다른 색으로) ③ 자세 전체를 원본보다 어둡게/옅게 칠함 ④ 원본에 없는 손·얼굴·부품을 지어냄 ⑤ 원본의 청록 줄·보석 등 작은 색 디테일을 흰색으로 지움.
- 원본 도트를 아래에 깔고 칸 단위로 겹치게, 원본 팔레트 색만 쓴다. 판은 각 기체의 기존 `SHEETS/sheet_NN`. 틀린 자세만 다시 그리면 된다.

| 기체 | 처리 | 다시 그릴 자세와 이유 |
|---|---|---|
| 3 | 틀린 자세 파츠만 끔 (3/37) | pose_26: cloak: original wrapped cloak is mostly purple-grey with thin tan streaks; drawing turns it into a large solid tan cloth covering the torso; pose_28: same cloak colour: purple-grey dominant in original, solid tan sheet in drawing; pose_01: same: cloak drawn as bright tan drape where original is purple-grey with tan highlights |
| 48 | 전체 끔 (12/18) | pose_00: backpack blade: original light-blue/cyan stripe inside the grey blade drawn plain white/grey (detail missing); pose_02: backpack blade: original light-blue/cyan stripe inside the grey blade drawn plain white/grey (detail missing); pose_03: backpack blade: original light-blue/cyan stripe inside the grey blade drawn plain white/grey (detail missing); pose_05: backpack blade: original light-blue/cyan stripe inside the grey blade drawn plain white/grey (detail missing); pose_07: backpack blade: original light-blue/cyan stripe inside the grey blade drawn plain white/grey (detail missing); pose_08: backpack blade: original light-blue/cyan stripe inside the grey blade drawn plain white/grey (detail missing) 외 6자세(전체는 _rereview/MERGED.json) |
| 49 | 틀린 자세 파츠만 끔 (1/5) | pose_01: original has bright red glow lines outlining the head/crest and the left arm (flash frame); drawing has no red glow, identical to the idle pose |
| 50 | 틀린 자세 파츠만 끔 (2/29) | pose_25: turret: original has a black barrel opening with a light-blue rim; drawing puts a saturated royal-blue lens there; orange flame/fins redrawn as a solid orange X-bracket; pose_26: turret: original has a black barrel opening with a light-blue rim; drawing puts a saturated royal-blue lens there; orange flame/fins redrawn as a solid orange X-bracket |
| 52 | 틀린 자세 파츠만 끔 (2/17) | pose_11: original has a grey shield/sword column down the left and a diagonal grey blade through the body; drawing turns the lower body into a mass of red lumps and drops the left grey column; pose_13: same lumpy red body replacing the original's grey blade/shield column on the left; invented white streak across the chest |
| 53 | 전체 끔 (12/17) | pose_01: eyes yellow, original cyan; pose_04: eyes orange/red, original cyan; pose_05: eyes yellow, original cyan; pose_06: eyes yellow/red, original cyan; pose_08: eyes yellow, original cyan; pose_10: eyes yellow, original cyan 외 6자세(전체는 _rereview/MERGED.json) |
| 57 | 전체 끔 (6/18) | pose_09: eyes teal/cyan, original green; pose_10: eyes teal/cyan, original green; pose_11: eyes teal/cyan, original green; pose_13: eyes teal/cyan, original green; pose_14: eyes teal/cyan, original green; pose_15: eyes teal/cyan, original green |
| 58 | 전체 끔 (11/13) | pose_00: face/head drawn cream-beige with cyan visor, original face and chest are teal-green; pose_02: face cream instead of teal-green; pose_03: face and torso cream, original has teal-green face/chest; pose_04: face cream instead of teal-green; pose_05: face cream instead of teal-green; pose_06: face cream instead of teal-green 외 5자세(전체는 _rereview/MERGED.json) |
| 61 | 틀린 자세 파츠만 끔 (1/17) | pose_11: invented white racket/grid oval held in front of face; original has a dark fist/weapon grip there (grid shield only appears in pose_03/08) |
| 71 | 전체 끔 (4/10) | pose_00: invented cyan eye dots on striped face; original has no cyan; pose_01: invented cyan eye dots on face; pose_02: invented cyan eye dots on face; pose_09: invented cyan eye dots on face |
| 74 | 전체 끔 (14/16) | pose_01: white beak/jaw with orange eye; original has dark face, pink mono-eye in slit, dark jaw; pose_02: white beak/jaw with orange eye; original has dark face, pink mono-eye in slit, dark jaw; pose_03: white beak/jaw with orange eye; original has dark face, pink mono-eye in slit, dark jaw; pose_04: white beak/jaw with orange eye; original has dark face, pink mono-eye in slit, dark jaw; pose_05: white beak/jaw with orange eye; original has dark face, pink mono-eye in slit, dark jaw; pose_06: white beak/jaw with orange eye; original has dark face, pink mono-eye in slit, dark jaw 외 8자세(전체는 _rereview/MERGED.json) |
| 75 | 전체 끔 (9/16) | pose_02: bright white faceplate/jaw under red eye; original face/jaw is dark grey with red mono-eye in slit; pose_03: bright white faceplate/jaw under red eye; original face/jaw is dark grey with red mono-eye in slit; pose_04: bright white faceplate/jaw under red eye; original face/jaw is dark grey with red mono-eye in slit; pose_05: bright white faceplate/jaw under red eye; original face/jaw is dark grey with red mono-eye in slit; pose_11: bright white faceplate/jaw under red eye; original face/jaw is dark grey with red mono-eye in slit; pose_12: bright white faceplate/jaw under red eye; original face/jaw is dark grey with red mono-eye in slit 외 3자세(전체는 _rereview/MERGED.json) |
| 86 | 틀린 자세 파츠만 끔 (1/19) | pose_12: invented white racket/grid oval held in front of face; original has a dark fist/weapon grip there (same error as unit_61 pose_11) |
| 93 | 전체 끔 (16/18) | pose_00: white beak/jaw plate under red eye; original has dark face, pink mono-eye in slit, dark jaw; pose_01: white beak/jaw plate under red eye; original has dark face, pink mono-eye in slit, dark jaw; pose_02: white beak/jaw plate under red eye; original has dark face, pink mono-eye in slit, dark jaw; pose_03: white beak/jaw plate under red eye; original has dark face, pink mono-eye in slit, dark jaw; pose_04: white beak/jaw plate under red eye; original has dark face, pink mono-eye in slit, dark jaw; pose_05: white beak/jaw plate under red eye; original has dark face, pink mono-eye in slit, dark jaw 외 10자세(전체는 _rereview/MERGED.json) |
| 96 | 틀린 자세 파츠만 끔 (1/10) | pose_09: head/torso drawn about 1.5x too large and shifted right; red V-crest and left-side red fin/hand of the original missing, figure cropped with blurred edge at right |
| 109 | 틀린 자세 파츠만 끔 (3/26) | pose_09: body and shoulders drawn light lavender/white where original is dark grey/black (only crest/details light); pose_10: whole body, backpack and binder drawn light lavender/white instead of the original dark grey/black armour; pose_25: same as pose_09: light lavender/white armour instead of dark grey, shoulder block wrong tone |
| 113 | 틀린 자세 파츠만 끔 (1/17) | pose_04: wide grey horizontal bar/arms across chest in original replaced by separate fists at shoulders and solid blue chest |
| 125 | 틀린 자세 파츠만 끔 (1/28) | pose_00: the two binders above the head (each with vent openings and pale panels) are drawn as one plain dark-grey arc; head drawn larger and higher than original |
| 131 | 틀린 자세 파츠만 끔 (2/26) | pose_20: head crest and left shoulder drawn as large solid yellow-orange plates where original is crimson with thin orange trim; silver fins at upper right lost; pose_22: same as pose_20: oversized yellow-orange crest/shoulder plates instead of crimson head with thin orange trim |
| 136 | 틀린 자세 파츠만 끔 (3/27) | pose_05: both forearms drawn orange where original arms are crimson (only belt D-buckle is orange); pose_21: head crest/shoulder drawn as large solid yellow-orange plates where original is crimson with thin orange trim; pose_23: same as pose_21: oversized yellow-orange crest and shoulder plates instead of crimson |
| 138 | 틀린 자세 파츠만 끔 (1/17) | pose_16: helmet and left shoulder drawn bright blue where original is dark grey/black with only blue edge highlights; left arm drawn across the chest while original's left side shows dark grey arm/shoulder block |
| 144 | 틀린 자세 파츠만 끔 (2/16) | pose_02: open hand with spread fingers invented at upper left where original has the blue spiral-patterned shoulder armour; pose_10: extra raised V-sign hand invented above the left fist; original has only one grey fist on the left |
| 147 | 전체 끔 (12/17) | pose_00: helmet gem drawn green where original is a yellow pixel/gem (green is not in the original palette); pose_02: helmet gem drawn green where original is a yellow pixel/gem (green is not in the original palette); pose_03: helmet gem drawn green where original is a yellow pixel/gem (green is not in the original palette); pose_04: helmet gem drawn green where original is a yellow pixel/gem (green is not in the original palette); pose_05: helmet gem drawn green where original is a yellow pixel/gem (green is not in the original palette); pose_06: helmet gem drawn green where original is a yellow pixel/gem (green is not in the original palette) 외 6자세(전체는 _rereview/MERGED.json) |
| 148 | 전체 끔 (14/20) | pose_00: face under helmet drawn as pale grey-white mask with white eyes; original has a yellow eye on the orange helmet and a dark grey face with cyan; pose_03: face under helmet drawn as pale grey-white mask with white eyes; original has a yellow eye on the orange helmet and a dark grey face with cyan; pose_04: face under helmet drawn as pale grey-white mask with white eyes; original has a yellow eye on the orange helmet and a dark grey face with cyan; pose_05: face under helmet drawn as pale grey-white mask with white eyes; original has a yellow eye on the orange helmet and a dark grey face with cyan; pose_06: face under helmet drawn as pale grey-white mask with white eyes; original has a yellow eye on the orange helmet and a dark grey face with cyan; pose_07: face under helmet drawn as pale grey-white mask with white eyes; original has a yellow eye on the orange helmet and a dark grey face with cyan 외 8자세(전체는 _rereview/MERGED.json) |
| 152 | 틀린 자세 파츠만 끔 (6/24) | pose_10: invented white cartoon eye (white sclera with pupil) under the helmet; original face there is dark with orange eye/slit only; pose_11: invented white cartoon eye (white sclera with pupil) under the helmet; original face there is dark with orange eye/slit only; pose_12: invented white cartoon eye (white sclera with pupil) under the helmet; original face there is dark with orange eye/slit only; pose_14: invented white cartoon eye (white sclera with pupil) under the helmet; original face there is dark with orange eye/slit only; pose_15: invented white cartoon eye (white sclera with pupil) under the helmet; original face there is dark with orange eye/slit only; pose_16: invented white cartoon eye (white sclera with pupil) under the helmet; original face there is dark with orange eye/slit only |
| 182 | 틀린 자세 파츠만 끔 (1/13) | pose_08: head crest drawn as a dark navy filled hood with white blot instead of the original open silver two-prong claw crest |
| 190 | 전체 끔 (10/17) | pose_01: cyan eye on helmet side missing (original shows cyan eye; drawing has only yellow face); pose_02: cyan eye missing on head; pose_03: cyan mono-eye replaced by yellow visor face; original face shows cyan eye; pose_06: cyan eye missing; pose_07: cyan eye missing; face drawn as yellow visor; pose_08: cyan eye missing; head shows yellow visor instead 외 4자세(전체는 _rereview/MERGED.json) |
| 191 | 틀린 자세 파츠만 끔 (4/18) | pose_02: blue head-fin highlights missing (original shows blue accents at head/fins); pose_03: blue fin accent at top right missing; pose_07: blue fin accent on head crest missing; pose_17: blue head fin accents missing; head crest drawn plain red |
| 193 | 틀린 자세 파츠만 끔 (1/19) | pose_04: left side fist/arm (grey ring with dark interior) redrawn as a smooth teal dome; orange vent lights changed to yellow |
| 205 | 틀린 자세 파츠만 끔 (3/22) | pose_01: foot sole redrawn as grey hex plate with orange bullseye; original sole is red spiral with grey rim (orange colour not in original); pose_02: same: big foot sole is grey plate with orange bullseye instead of red spiral/grey rim; pose_17: same: foot sole grey plate with orange centre instead of red spiral |
| 206 | 틀린 자세 파츠만 끔 (1/17) | pose_12: yellow eye added where original shows none (face hidden); lower body drawn as one pointed leg, original shows two leg tips (left leg missing) |
| 211 | 전체 끔 (6/16) | pose_00: cyan eye(s) between orange V-crest missing (original 165 cyan px, drawing ~6); pose_05: cyan eye missing on face; pose_06: cyan eye missing on face; pose_10: cyan eye missing on face; pose_11: cyan eyes missing; face area drawn plain grey under the crest; pose_15: cyan eye missing on face |
| 213 | 전체 끔 (7/16) | pose_03: hands drawn as dark navy fists; original hands are light gray open claws; pose_08: left hand dark navy fist; original gray claw; pose_09: hands dark navy fists; original gray claws; pose_10: extended right hand is a dark navy fist; original is a light gray open claw; head antennae drawn as large curved white horns instead of thin straight gray rods; pose_11: lower-left hand dark navy; original gray; pose_12: left hand dark navy fist; original gray claw 외 1자세(전체는 _rereview/MERGED.json) |
| 220 | 틀린 자세 파츠만 끔 (1/17) | pose_12: invented a yellow-eyed face in the middle of the curled body; original shows no face/eye in this pose |
| 225 | 틀린 자세 파츠만 끔 (2/21) | pose_16: forward left hand drawn as a dark maroon fist; original hand is light gray/white; pose_22: face missing: original shows front face with green eyes under the raised lance, drawing shows helmet/back with no eyes; big red-yellow arm band invented on the left and torso drawn wider than original |
| 227 | 틀린 자세 파츠만 끔 (1/31) | pose_29: face missing: original shows red helmet with green eyes in the middle of the body; drawing covers it with a big white shoulder spike and shows no eyes, torso/shoulder layout differs |
| 232 | 틀린 자세 파츠만 끔 (2/7) | pose_05: face: original has two red eyes plus red mouth dot; drawing has a single central pink mono-eye; body glossier/lighter than other poses; pose_09: colour/design: drawing is bright mint-green with a white face plate and silver crest; original is the same dark-green armour as other poses with red twin eyes and no white face |
| 244 | 틀린 자세 파츠만 끔 (1/32) | pose_16: invented a large yellow hair/plume mass behind the head at upper right; original has only a thin yellow strand at the face centre and white/pink there |
| 250 | 틀린 자세 파츠만 끔 (1/20) | pose_09: invented an orange/yellow beak-like part at the mouth under the face and the spear grip is drawn as a short blue tube jammed into the face; original has no orange part there, spear held low at left |
| 253 | 틀린 자세 파츠만 끔 (1/17) | pose_02: face area: original shows a white dome head with pink eye on the left; drawing replaces it with a green hand clawing over the face and a cracked white helmet, face no longer readable |
| 257 | 틀린 자세 파츠만 끔 (3/19) | pose_07: body armour drawn light lavender/white; original is dark gray/black armour (looks like unit_256 palette); pose_11: body armour light lavender/white instead of the original dark gray/black; pose_13: legs and body light lavender instead of original dark gray/black |
| 263 | 틀린 자세 파츠만 끔 (2/35) | pose_23: invented a large front-facing helmet with green visor at centre-left; original shows the head turned away (no visible eye), crouched body under the sword arm; pose_26: gun redrawn as a big pistol with round muzzle facing the viewer, larger than the original's boxy side-on cannon |
| 264 | 틀린 자세 파츠만 끔 (1/35) | pose_13: head/face area is black (dark helmet + black face around green eyes) and chest heavily dark in original; drawing renders helmet and body light silver-gray |
| 271 | 틀린 자세 파츠만 끔 (2/16) | pose_00: eyes drawn plain black dots; original eyes have pink/red lit pupils in dark sockets; pose_08: same: pink-lit eyes drawn plain black |
| 273 | 틀린 자세 파츠만 끔 (1/46) | pose_02: head turned from profile to front with one big red eye; left arm forward (Claude check) |
| 280 | 틀린 자세 파츠만 끔 (1/27) | pose_11: head drawn as a blank light-grey helmet with no red eyes (original has two red eyes on the dark face) and only a red mouth mark; plume drawn as a closed arc over the back |
| 281 | 틀린 자세 파츠만 끔 (4/19) | pose_00: face: original has a dark grey recessed face (skull-like) around the red eyes and mouth under the tan hood; drawing paints the whole face flat tan; pose_03: same: dark face area replaced with plain tan; pose_09: same dark-face loss; pose_13: same dark-face loss |
| 301 | 틀린 자세 파츠만 끔 (2/21) | pose_08: original left arm stretched straight out to the far left (fist at sprite edge); drawing bends it so the fist sits at the chest; grey mask/jaw over lower face replaced by pink face with white grin; pose_01: face: original lower face is a large grey jaw/grille wrapping to a grey collar; drawing shows pink face with white teeth and a thin grey ring plus a yellow scarf |
| 322 | 틀린 자세 파츠만 끔 (1/9) | pose_08: two large light fists drawn clasped over chest/below face; original shows dark spiky wing feathers over torso with no visible fists |
| 327 | 전체 끔 (8/25) | pose_00: face: glowing GREEN eye; original face is white with orange eye pixels and red mouth dot (no green); pose_04: face: green eye instead of orange; pose_07: face: green eye instead of orange; pose_08: face: green eye instead of orange; pose_14: face: green eye + orange nose; original has orange at eye level and red mouth dot; pose_17: face: green eye instead of orange 외 2자세(전체는 _rereview/MERGED.json) |
| 332 | 전체 끔 (17/19) | pose_00: face: white face with large YELLOW eye; original face is orange/peach with pink eye and yellow-red mouth mask; pose_02: face: white face with large YELLOW eye; original face is orange/peach with pink eye and yellow-red mouth mask; pose_03: face: white face with large YELLOW eye; original face is orange/peach with pink eye and yellow-red mouth mask; pose_05: face: white face with large YELLOW eye; original face is orange/peach with pink eye and yellow-red mouth mask; pose_06: face: white face with large YELLOW eye; original face is orange/peach with pink eye and yellow-red mouth mask; pose_07: face: white face with large YELLOW eye; original face is orange/peach with pink eye and yellow-red mouth mask 외 11자세(전체는 _rereview/MERGED.json) |
| 333 | 전체 끔 (15/20) | pose_00: forehead/visor: orange X-shaped visor drawn; original has red oval forehead plate with yellow Y emblem; pose_01: forehead/visor: orange X-shaped visor drawn; original has red oval forehead plate with yellow Y emblem; pose_03: forehead/visor: orange X-shaped visor drawn; original has red oval forehead plate with yellow Y emblem; pose_04: forehead/visor: orange X-shaped visor drawn; original has red oval forehead plate with yellow Y emblem; pose_05: forehead/visor: orange X-shaped visor drawn; original has red oval forehead plate with yellow Y emblem; pose_06: forehead/visor: orange X-shaped visor drawn; original has red oval forehead plate with yellow Y emblem 외 9자세(전체는 _rereview/MERGED.json) |
| 361 | 전체 끔 (24/30) | pose_01: face: grey/silver faceplate with RED eyes; original face is green with magenta/pink eye pixels and green centre gem (no grey mask, no red); pose_02: face: grey/silver faceplate with RED eyes; original face is green with magenta/pink eye pixels and green centre gem (no grey mask, no red); pose_03: face: grey/silver faceplate with RED eyes; original face is green with magenta/pink eye pixels and green centre gem (no grey mask, no red); pose_06: face: grey/silver faceplate with RED eyes; original face is green with magenta/pink eye pixels and green centre gem (no grey mask, no red); pose_07: face: grey/silver faceplate with RED eyes; original face is green with magenta/pink eye pixels and green centre gem (no grey mask, no red); pose_09: face: grey/silver faceplate with RED eyes; original face is green with magenta/pink eye pixels and green centre gem (no grey mask, no red) 외 18자세(전체는 _rereview/MERGED.json) |
| 363 | 틀린 자세 파츠만 끔 (2/23) | pose_14: chest: bright glowing CYAN panel; original chest panel is pale green-white (no cyan glow); pose_22: chest: glowing CYAN panel with 'ES' shape; original is pale grey-green striped plate |
| 364 | 틀린 자세 파츠만 끔 (2/21) | pose_02: whole body recoloured dark grey/olive with black fists; original is bright green/teal; pose_10: whole body recoloured dark grey/olive; original bright green/teal |
| 365 | 전체 끔 (8/25) | pose_00: eyes drawn yellow, original eyes pink; blades lost pink tint; pose_01: eyes yellow instead of pink; claw blades white/green, original yellow-pink; pose_03: eyes yellow instead of pink; pose_07: face blurred/melted, visor shape lost; pose_12: face missing: head drawn as green blob with no grey faceplate/eyes; pose_13: claw blades white/green instead of yellow-pink 외 2자세(전체는 _rereview/MERGED.json) |
| 367 | 전체 끔 (16/39) | pose_09: chest lion head drawn with closed beak-like mouth; original lion has open fanged mouth; pose_10: lion chest closed mouth, head face drawn as orange box mask; pose_11: head enlarged with orange mask face, original small head; pose_13: head enlarged orange mask; arm/fist oversized; pose_14: lion chest closed mouth instead of open fanged; pose_15: lion chest closed mouth instead of open fanged 외 10자세(전체는 _rereview/MERGED.json) |
| 369 | 틀린 자세 파츠만 끔 (6/25) | pose_04: invented human face (nose/lips) under helmet; original robot face with visor-like light area; pose_14: invented human face with nose and mouth; original white visor face with yellow eye; left hand/weapon position differs; pose_17: invented human face; pose_18: invented human face; pose_21: invented human face; pose_24: invented human face |
| 370 | 틀린 자세 파츠만 끔 (2/23) | pose_14: palette darkened to dull brown/olive, original gold-orange; pose_22: palette darkened to dull brown/olive, original gold-orange |
| 371 | 틀린 자세 파츠만 끔 (4/26) | pose_13: invented human face under helmet instead of pink mono-eye visor; pose_24: invented flesh human face instead of visor/pink eye; palette darker olive; pose_25: invented human face (nose) instead of visor/pink eye; palette darkened olive-brown; pose_26: invented human face, gun drawn pink/flesh colour |
| 373 | 전체 끔 (19/19) | pose_00: white/grey faceplate, original face is gold with pink eye; pose_01: white faceplate; pose_02: white faceplate; pose_03: white faceplate; pose_04: white faceplate; pose_05: white faceplate 외 13자세(전체는 _rereview/MERGED.json) |
| 374 | 틀린 자세 파츠만 끔 (1/28) | pose_22: red mono-eye missing, face drawn as human-like face; palette paler/duller than original |
| 375 | 틀린 자세 파츠만 끔 (4/21) | pose_09: invented grinning human-like face; pose_10: invented human face with closed eyes; pose_15: pale pinkish human face, palette paler than original; pose_22: palette pale/desaturated, pinkish face invented |
| 377 | 틀린 자세 파츠만 끔 (1/26) | pose_25: translucent ghost smears over head and both arms; head shape distorted vs original |
| 379 | 틀린 자세 파츠만 끔 (2/9) | pose_01: eyes drawn as white bars on black; original eyes are white with red pupils (as in pose_03); pose_02: eyes drawn as white bars; original white eyes with red pupils |
| 394 | 틀린 자세 파츠만 끔 (2/13) | pose_04: whole body washed out to pale peach/white, original saturated copper-orange; ghost blur over arm/sword; pose_12: body washed out pale peach/white instead of copper-orange |
| 399 | 틀린 자세 파츠만 끔 (3/21) | pose_07: palette lightened to pale pink, original dark mauve/maroon; pose_15: palette lightened to pale pink, original dark mauve; pose_17: palette lightened to pale pink, original dark mauve |
| 404 | 틀린 자세 파츠만 끔 (1/36) | pose_19: fragment recoloured solid red dome; original is peach/tan with dark red and green specks |
| 409 | 전체 끔 (9/14) | pose_00: mono-eye drawn orange/yellow iris; original eye is pale white with red rim; pose_01: mono-eye orange/yellow instead of pale white with red rim; pose_03: mono-eye orange instead of pale/red; pose_04: mono-eye orange instead of pale/red; pose_05: mono-eye orange instead of pale/red; pose_06: mono-eye orange instead of pale/red 외 3자세(전체는 _rereview/MERGED.json) |
| 419 | 전체 끔 (13/20) | pose_01: face: original light-blue (cyan) eye slit drawn as white/none; pose_02: face: cyan eye slit missing (white slit instead); pose_04: face: cyan eye slit replaced by white slit; pose_05: face: cyan eye slit replaced by white slit; pose_07: face: cyan eye slit replaced by white slit; pose_08: face: cyan eye slit missing 외 7자세(전체는 _rereview/MERGED.json) |
| 472 | 전체 끔 (14/24) | pose_00: face: mono-eye drawn light-blue/cyan; original eye is red inside the dark-blue visor; pose_02: face: mono-eye drawn light-blue/cyan; original eye is red inside the dark-blue visor; pose_03: face: mono-eye drawn light-blue/cyan; original eye is red inside the dark-blue visor; pose_04: face: mono-eye drawn light-blue/cyan; original eye is red inside the dark-blue visor; pose_08: face: mono-eye drawn light-blue/cyan; original eye is red inside the dark-blue visor; pose_09: face: mono-eye drawn light-blue/cyan; original eye is red inside the dark-blue visor 외 8자세(전체는 _rereview/MERGED.json) |
| 477 | 틀린 자세 파츠만 끔 (1/20) | pose_17: shoulders redrawn as large red-gem shields and arms crossed in front of chest; original is a dark-grey body with small magenta marks and one hand raised at top-left holding the blue item |
| 479 | 틀린 자세 파츠만 끔 (2/16) | pose_00: backpack blade: original light-blue/cyan stripe inside the grey blade drawn plain white/grey (detail missing); pose_02: backpack blade: original light-blue/cyan stripe inside the grey blade drawn plain white/grey (detail missing) |
| 490 | 틀린 자세 파츠만 끔 (1/25) | pose_18: original is a uniform near-black silhouette; drawing is a lighter purple-grey body with visible green eye, red accents and blue core |

## 2026-11-21 전체 그림 + 파츠 구성 함께 — 시범 196 아르스트로메리아 (사용자 지시)

- 코덱스는 지금처럼 **자세 전체 그림**을 그린다. 다만 원본 전체 그림 위에 파츠(게임 조각) 칸과 번호를 표시한 자료를 함께 주니, **각 파츠가 원본 칸의 위치와 크기에 그대로 맞고, 같은 번호의 파츠는 모든 자세에서 똑같이** 그려지도록 한다. Claude는 원본 파츠 위치를 찾아 그 크기만큼씩 잘라 쓴다.
- 이유: 지금은 같은 파츠(예: 머리 #5)가 자세마다 크기와 위치가 달라, 잘라 내면 다른 자세와 맞지 않는다(`WHY_head_differs_per_pose.png`).
- 지시 전문과 자료는 `test_current/parts/redraw_requests/unit_196/REQUEST.md`에 있다. pose_00·04·09·05를 먼저 그려 확인을 받은 뒤 나머지를 그린다.

## 2026-11-21 다시 그리기 — 파츠가 자세마다 다르게 그려진 151기체 (사용자 지시 "심한 151개부터")

- 방법과 규칙은 위 196 절과 같다. 원본 전체 그림 위에 파츠 칸·번호를 표시한 `ASSEMBLY_pose_NN.png`를 보고 **자세 전체 그림**을 다시 그린다. 각 파츠는 원본 칸의 위치·크기에 맞추고, 같은 번호는 모든 자세에서 똑같이 그린다.
- 기체별 자료와 지시는 `test_current/parts/redraw_requests/unit_<U>/`(`REQUEST.md`, `ASSEMBLY_pose_NN.png`, `PART_ATLAS_guide.png`)에 있다. 196은 시범이니 먼저 받아 확인한 뒤 나머지를 진행한다.
- 판정 기준: 설치된 파츠로 각 자세를 조립해 그 자세 그림과 비교했을 때 색이 크게 다른 픽셀 비율. 기체 평균이 0.20 이상이면 이 목록에 넣는다(괜찮은 스트라이크는 0.07~0.09). 결과는 `pose_packets/ASSEMBLY_MISMATCH.json`.
- 어긋남이 큰 순서로 그린다:

120 미겔전용 진(0.369), 314 전투수 사이코베어(0.359), 311 지옥왕 고든(0.356), 328 뇌룡(0.352), 345 EI-27(0.327), 367 가오가이가(0.32), 330 격룡신(0.319), 113 X아스트레이(0.318), 371 풍룡(0.312), 205 야천광(0.311), 195 슈퍼 에스테바리스(0.309), 121 시구・딥 암즈(0.308), 194 에스테바리스 커스텀(0.305), 90 조노(0.296), 79 스트라이크 대거(0.293), 96 건담 아스트레이R(0.293), 372 뇌룡(0.292), 421 리스(0.292), 327 풍룡(0.29), 325 빙룡(0.287), 301 보스보롯트(0.286), 332 강룡신(0.282), 125 하이페리온(0.28), 331 환룡신(0.28), 458 EI-27(0.28), 52 이지스 건담(0.28), 403 가오파이가(0.277), 453 발아룸(0.276), 249 테카맨 아키(0.275), 357 합체원종(0.275), 463 기계수가라다브라MK01(0.273), 489 테츠진(0.271), 112 드레드노트(0.27), 340 EI-11(0.27), 377 볼포그(0.27), 227 B테카맨 블레이드+P(0.267), 213 리브(0.266), 212 EDF솔리드 아머(0.265), 225 테카맨 블레이드+P(0.265), 110 아스트레이G공 미나(0.264), 109 건담 아스트레이G공(0.262), 124 하이페리온(0.262), 380 마이크・사운더스13세B(0.262), 361 가오가이가(0.259), 204 육련(0.258), 123 하이페리온(0.257), 471 윙 건담 제로(0.257), 475 기므렛・엠페러(0.257), 461 ???(0.256), 39 스트라이크 루즈(0.252), 150 에스테바리스 공중(0.251), 373 초룡신(0.251), 196 아르스트로메리아(0.249), 404 고라이온(0.249), 391 기므렛・엠페러(0.248), 111 드레드노트(0.246), 122 리제너레이트(0.245), 192 에스테바리스 커스텀(0.244), 247 테카맨 베스나(0.244), 117 이라이쟈전용 진(0.243), 374 격룡신(0.243), 107 건담 아스트레이G(0.242), 98 건담 아스트레이RP(0.242), 244 테카맨 이벨+γ호(0.241), 370 염룡(0.241), 375 환룡신(0.24), 326 염룡(0.238), 131 소드 카라미티(0.237), 211 버드맨(인간형)(0.235), 339 EI-01(0.235), 392 스타 가오가이가(0.235), 399 피아・데켐・피크(0.235), 401 발파레파・플라쥬너(0.234), 413 발호크(0.234), 250 테카맨 아키+PII(0.233), 72 딘(0.233), 376 강룡신(0.232), 396 피바타(0.231), 71 딘(0.231), 203 적시기(0.23), 148 에스테바리스 공중(0.229), 226 B테카맨 블레이드(0.229), 329 초룡신(0.229), 146 에스테바리스 공중(0.228), 308 요기계수 드라고1(0.228), 145 에스테바리스 공중(0.227), 310 기계수가라다브라MK01(0.227), 80 카라미티 건담(0.227), 179 마진(0.226), 60 진(0.226), 85 진(0.226), 336 마이크・사운더스13세B(0.225), 469 킹 제이더(0.225), 94 스트라이크 대거(0.225), 13 에일 스트라이크 건담(0.224), 136 소드 카라미티(0.224), 17 에일 스트라이크 건담(0.224), 18 에일 스트라이크 건담(0.224), 333 볼포그(0.224), 48 저스티스 건담(0.224), 114 쟝 전용 M1아스트레이(0.222), 233 테카맨 소드(0.222), 334 빅 볼포그(0.222), 144 에스테바리스 0G(0.221), 342 EI-15(0.221), 70 딘(0.221), 38 M1아스트레이(0.22), 57 듀얼 건담AS(0.219), 3 건담 샌드록�(0.218), 484 페츌온(0.218), 119 진・하이메뉴버(0.217), 2 건담 헤비암즈�(0.217), 232 테카맨 대거(0.217), 309 악의 비너스(0.217), 338 킹 제이더(0.217), 395 폴턴(0.217), 491 소드 카라미티(0.217), 359 존다로봇(0.216), 248 테카맨 베스나+α호(0.215), 317 악령장군 하디아스(0.215), 388 광룡(0.215), 108 건담 아스트레이G공(0.214), 300 아프로다이A(0.214), 126 하이페리온2호기(0.213), 245 테카맨 조마(0.213), 324 스타 가오가이가(0.213), 335 마이크・사운더스13세C(0.213), 323 가오가이가(0.212), 420 발아룸(0.212), 56 듀얼 건담(0.212), 118 이라이쟈전용 진�(0.208), 293 진・겟타3(0.208), 302 비너스A(0.208), 379 마이크・사운더스13세C(0.206), 473 조노(0.206), 68 조노(0.206), 116 리・홈(0.205), 4 알트론 건담(0.205), 479 저스티스 건담(0.205), 206 오건(0.204), 319 암흑대장군(0.204), 365 볼포그(0.204), 257 테카맨 데드(0.202), 472 플랜1058 코다르i(0.202), 88 바쿠(0.202), 99 파워드 레드(0.202), 55 듀얼 건담AS(0.201), 61 시구(0.201), 86 시구(0.201), 152 에스테바리스 육지(0.2), 27 S 스카이 글래스퍼1(0.2)

## 2026-11-21 Claude: 시작 시간 추가 개선 (공유 실행 코드 수정 예고)

코덱스의 9ddb81f3(파츠 목록 캐시)을 검토했다. 세 방식(옛 방식, 캐시 있음, 캐시 없음)의 첫 전투 화면 픽셀 해시가 같았고, 캐시가 있을 때 시작 준비가 약 15초에서 8초로 줄었다(재설치가 함께 도는 상태에서 측정). 이어서 아래 두 곳을 Claude가 고친다. 결과 화면은 바뀌지 않는다.

- `emulator/hd_parts_registration.py` `registration_stamp`: 시작할 때마다 아틀라스 1,110개의 그림·참조 파일을 모두 읽어 해시를 낸다. 그런데 11/08 등록 캐시(npz)와는 이미 값이 달라 결과가 버려진다. 파츠 목록 해시와 각 파일의 크기·수정 시각이 같으면 저장해 둔 지문을 다시 쓰도록 바꾼다(`emulator/hd_parts.py` 호출부에 목록 해시 전달).
- `emulator/robot_sprite_switch.py`·`emulator/hd_core.py`: 11/19에 Claude가 넣은 로봇 분류(`classify`)가 시작할 때마다 약 1초를 쓴다. 결과를 파츠 목록 해시에 묶어 캐시한다.
- 결과(11/21 09:40): 두 캐시를 적용했다. 지문은 전체 계산 0.91초 → 캐시 적중 0.19초, 로봇 분류는 0.11초 → 0.02초다. 시작 준비 합계는 같은 조건에서 3회씩 번갈아 재서 4.7~4.8초 → 4.0~4.3초였고, 첫 전투 화면의 픽셀 해시는 같다. 아틀라스 한 개의 수정 시각을 바꾸거나 목록 해시가 달라지면 다시 계산하는 것도 확인했다. 캐시 파일은 `%LOCALAPPDATA%/SRW_W_HD/cache/registration-stamp.json`과 `robot-binding-ids.json`이다. 고치기 전 파일은 `emulator/*.bak_perf`로 남겼다.
- 알아 둘 점: 지문은 파일 크기와 수정 시각만 본다. 같은 크기·같은 시각으로 내용만 바뀐 아틀라스는 감지하지 못한다(`atlas_stats`와 같은 수준).

## 2026-11-21 Claude: 정정 — `hd_parts_registration.py`는 내용을 바꾸면 안 된다

- 위 시작 시간 개선에서 지문 캐시 코드를 `emulator/hd_parts_registration.py`에 넣었다가, 구워 둔 텍스처 107,788개가 전부 무효가 됐다(09:35~09:50 약 15분). 이 파일의 바이트가 텍스처 열쇠(`registration_content`)에 들어가기 때문이다.
- 파일을 HEAD와 같은 내용으로 되돌렸고(줄바꿈 정규화 SHA 일치 확인), 캐시는 새 파일 `emulator/registration_stamp_cache.py`로 옮겼다. `hd_parts.py`는 `cached_registration_stamp`를 부른다. 되돌린 뒤 구운 파츠 107,632개가 다시 맞는다.
- 그 15분 사이 설치된 기체(170·174·175·177·183 등)와 11/19에 그림을 바꾼 아이콘(secondary_unit) 190개는 굽지 않은 상태다. `scripts/assets/bake_parts.py`로 다시 구워야 한다.
- 측정(플레이어와 같은 비동기 경로): 구운 파츠 읽기는 중앙값 1.05ms이고 같은 프레임에 표시된다. 늦는 것은 정확한 바인딩이 없는 OBJ의 실행 중 타일 조립이다(작업자 1개, 동시에 2건). unit_2 weapon_12에서 처음 볼 때 중앙값 5프레임·p90 114프레임, 디스크에 조립 결과가 있어도 p90 25프레임이었다. 스프라이트가 화면에 머무는 시간은 중앙값 3~4프레임이라, 조립이 끝나기 전에 지나가는 조각이 많다.

## 2026-11-21 Claude: 196 시범(single_pose00/04/09/05) 조립 결과

- 원본 파츠 크기대로 잘라 4자세를 조립했다(`test_current/parts/redraw_requests/unit_196/pilot_set/PILOT_RESULT.png`: 원본 / 시범 그림 / 조립 결과).
- pose_00·09·05: 조립 결과가 시범 그림과 거의 같다. 파츠 칸 맞춤이 통한다. 이 방향이 맞다.
- pose_04: 조립하면 앞쪽 집게가 조각나고 머리 위가 지저분하다. 04 그림의 머리(#14)와 집게 파츠가 00·09와 다른 위치·모양으로 그려져서, 공유 파츠가 다른 자세 것으로 붙는다. **04는 #14 머리와 앞 집게를 00·09와 같은 모양·크기로, 원본 칸에 맞춰 다시 그려 달라.**
- 사용자 확인 뒤 196 나머지 자세와 151기체로 넓힌다.

## 2026-11-21 확대 지시 (사용자 "넓혀") — 196 나머지 + 151기체, 시범과 같은 방식

- 시범 방식이 통했다(pose_00·09·05 조립 결과가 그림과 같음). 이 방식으로 **196의 나머지 자세(04 다시 그리기 포함)와 `redraw_requests/HEAVY_151.txt`의 151기체 전 자세**를 그린다.
- 방식: 자세마다 따로 한 장씩(single_poseNN) 그린다. 캔버스는 그 자세의 `pose_NN/native_4x.png` 크기이고, 원본 위에 정확히 겹치게 그린다. 각 파츠는 `ASSEMBLY_pose_NN.png`의 칸 위치·크기에 맞춘다.
- **공유 파츠 일관성이 핵심이다.** 같은 번호의 파츠(특히 머리·얼굴)는 기체의 모든 자세에서 같은 모양·크기·명암·세부 위치(눈, 센서, 줄무늬)로 그린다. 먼저 그 기체의 기준 자세 하나를 그리고, 다른 자세는 그 기준의 파츠 모양을 그대로 옮겨 그린다.
- 원본 팔레트 색만 쓰고, 얼굴을 흰색이나 사람 얼굴로 바꾸지 않는다. 바깥 윤곽선은 끊기지 않게, 원본 실루엣 밖 4px 이내로 그린다.
- 전달 형식은 시범과 같다: `test_current/parts/redraw_requests/_codex_<날짜>/unit_<U>/single_poseNN/RAW_imagegen.png` + `layout_snapshot.json`(canvas, source_region_in_request) + 기체별 DELIVERY.json.
- 순서는 HEAVY_151의 순서(어긋남이 큰 기체부터)대로 하고, 10기체마다 HANDOFF_FROM_CODEX에 적어 달라. Claude가 받는 대로 잘라 조립해 검수·설치한다.

## 2026-11-21 Claude: 기존 HD가 다른 색으로 그려진 컷인 — 새로 그려 달라

- 23299(환룡신)·23317(격룡신): 기존 HD는 금색 기체(다른 팔레트판)로 그려졌다. 이 장면의 원본은 회색·초록 보석이다. 지문을 맞춰 연결해 보니 금색이 나와서 되돌렸다. **이 장면 색 그대로 새로 그려 달라**(batch 자료의 `_canvas.png`가 이 장면 색이다).
- 23076(랑그 MAP)·24640(데스사이즈 바위 고리): 기존 HD가 이 화면 레이어와 맞지 않는다. batch 자료 기준으로 새로 그려 달라.
- 23514(미나 웃는 얼굴)는 코덱스 새 그림으로 연결을 마쳤다.


## 2026-11-21 (Claude) PC 배포본이 구운 텍스처를 담아 읽도록 수정

문제: 배포용 실행 파일은 구운 저장소를 `data/cache/parts_baked.sqlite`에서만 읽었고(`runtime_paths.texture_cache`),
배포본은 아틀라스를 WebP(최대 960px)로 바꿔 담아서 텍스처 키(아틀라스 파일 크기·내용 해시 포함)가 달라졌다.
그래서 구운 파일을 넣어 줘도 하나도 맞지 않고, 받은 사람 PC에서 파츠를 처음부터 다시 만들었다.

수정 (백업 `*.bak_shipbaked`):
- `emulator/runtime_paths.py`: `shipped_texture_store(default, writable)` 추가. 배포 실행 파일일 때 `graphics/parts_baked.sqlite`를
  읽기 전용 배포 저장소로 돌려준다. 소스 체크아웃에서는 None. 테스트용 환경 변수 `SRWW_SHIPPED_BAKED=<파일>`.
- `emulator/parts_disk_cache.py`: `PartsDiskCache`가 사용자 저장소(쓰기)에 없으면 배포 저장소(읽기 전용, immutable)에서 읽는다.
  `keys()`는 둘의 합집합. 쓰기(`put`, `assembly_misses`)는 전과 같이 사용자 저장소로만 간다.
- `emulator/hd_parts.py`: `atlas_identity`가 배포 저장소 옆의 `parts_baked_atlases.json`에 있는 아틀라스는 파일을 읽지 않고
  그 표의 크기·해시를 쓴다(`shipped_atlas_identities`). 표에 없는 아틀라스는 전과 같다.
- `distribution/pack_baked_store.py` (신규): 지금 쓰는 파츠의 텍스처만 골라 `<대상>/parts_baked.sqlite`(단일 파일, WAL 아님)와
  `<대상>/parts_baked_atlases.json`을 쓴다. 2GiB 이상이면 실패(깃허브 릴리즈 파일 한도).
- `distribution/build_portable.py`: `graphics/parts_baked*`를 그대로 복사하지 않고(WAL 미반영 사본 방지) 위 스크립트를 호출한다.
- `emulator/hd_parts_registration.py`는 건드리지 않았다(바이트가 텍스처 키에 들어간다).

검증 (`build/shipped_baked_stage`에 포장, 배포 조건 모사: FROZEN, 빈 사용자 저장소, 아틀라스 파일 조회 금지):
- 포장: 키 105,771개 중 105,582개 수록, 1,469MB (2GiB 미만).
- 읽기: 쓰는 파츠 107,905개 중 107,716개 키 일치·디코딩 성공, 실패 0, 사용자 저장소 0행.
- 없는 189개 = 굽지 않은 파츠(기체 170·171·174·175·177·183의 51개 + 맵 아이콘 138개). `bake_parts.py`로 구운 뒤 다시 포장하면 들어간다.

안 한 것:
- `dist/SRW_W_HD` 재빌드(실행 파일·그림 변환)는 하지 않았다. 지금 dist는 11/13 것이라 이 수정이 들어 있지 않다.
- 실제 배포 실행 파일(SRW_W_HD.exe)로 띄워 본 확인은 재빌드 뒤에 해야 한다.
- 런타임 조립(바인딩 없는 스프라이트) 결과는 배포 저장소에 넣지 않는다. 전과 같이 사용자 PC에서 만든다.
- Assets 압축 파일 전체가 2GiB를 넘는지는 재빌드해 봐야 안다. `archive_portable.py`는 Assets를 더 쪼개지 못한다.
