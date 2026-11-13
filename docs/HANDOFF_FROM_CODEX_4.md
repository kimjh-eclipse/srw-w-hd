# Codex → Claude 핸드오프 4

현재 교환 파일입니다. 이전 제작 이력은 Git 및 HANDOFF_FROM_CODEX_3.md에 보존합니다. 현재 상태는 이 파일을 우선합니다.

## 현재 상태와 수량 기준

- 이번 작업묶음 **373개 연결 항목** 설치·대상굽기 완료. 기존 그림 교체·팔레트 변형을 포함하는 작업량이며, 전체 HD 누락에서 단순 차감할 수 없습니다.
- **전체 누락은 이전 ROM 감사의11,358종이 마지막 집계**입니다. 전체 잔여는 재집계하지 않았고 완료율을 주장하지 않습니다. 감사 밖에서 발견된 실제 누락도 따로 기록합니다.
- 최신 지시: Codex는 제작·연결·굽기·커밋을 진행, 독립 그림/색/재생검증은Claude담당. 실제로보지않은것을보았다고기록하지않습니다. 미관측계약10은actual_observed=false.
- **코어 소스 해제**. Claude95ba46f0/d98c4226 반영. 기본 DLL SHA256 a6d80b29119f7c18447725acc4e0e5c8fb88cdda07d8cef6ccb106e936b64fe0,cachedOBJ API포함. Codex는공유runtime/core를수정하지않습니다.
- 사용자 테스트 창은유지. 컴퓨터종료금지. ROM·세이브·사용자설정·로그·자격증명은Git추가금지. baked.sqlite은제작산출물로Git에추가하지않습니다.

## 진행 중인 다음 제작

- next_shape_art: 아스테바리스 다음 실제미연결기계자세/무장. +90 공전11/육전12,+195육전19는이번묶음에반영됨.
- next_key_art: 21667 실제관측28+같은원본/확정팔레트의미관측1,총29후보제작. 21080은관측41/미관측소스확정10분리반영됨.
- effect_live_palette: 실제팔레트16값과ROM PLT가동일한bank에서미관측원본계약확장.19584/21819는다중IMG소유불확실성있어추정제외,20498단일IMG의자체그림보유범위우선.
- root: 새후보인수·하드입력검사·라이브연결·대상굽기·검증큐·커밋/푸시. 동일효과자체그림의정확crop은가능,다른기체그림재색칠로누락메우기금지.

## 현재 그림 묶음

정확한 바인딩번호/그림SHA/입력경고는 PRODUCTION_ART_BATCH_CURRENT.json. 각graphics제작폴더의pose_contract.json,installation_report.json,제작인계문서를함께보세요. 아래수는개별그림·팔레트연결항목이며기체수/고유형태수/전체누락감소수가아닙니다.

|아틀라스|이번 대상 수|현재 상태|
|---|---:|---|
|observed_getter_pole_forms|2|Claude검증대기;입력형태경고있음|
|observed_effect_21948_new17|17|Claude검증대기;입력형태경고있음|
|codarl_clones90_cached_pose|14|Claude검증대기|
|deathscythe_normal_7086|20|Claude검증대기|
|observed_effect_20498_gray2|2|Claude검증대기;입력형태경고있음|
|deathscythe_folded_wings_pose|14|Claude검증대기|
|sandrock_cached_pose|16|Claude검증대기|
|deathscythe_forecast_closed_pose|14|Claude검증대기|
|observed_effect_20498_white7|7|Claude검증대기|
|deathscythe_scythe150_continuous|2|Claude검증대기|
|sandrock_weapon_closeup_cached_pose|9|Claude검증대기|
|observed_effect_20498_jade6|6|Claude검증대기|
|deathscythe_green_arcs_7084_7085|10|Claude검증대기;입력형태경고있음|
|observed_effect_19600_last_two|2|Claude검증대기|
|great_thunder168_cached_pose|10|Claude검증대기|
|observed_effect_19645_new_three|3|Claude검증대기;입력형태경고있음|
|getter_true_missing_22054_22062|4|Claude검증대기;입력형태경고있음|
|observed_effect_22378_late_base_two|2|Claude검증대기|
|observed_effect_21657_yellow29|29|Claude검증대기|
|observed_effect_22673_three|3|Claude검증대기|
|observed_panel_17168_four|4|Claude검증대기|
|observed_effect_21657_red16|16|Claude검증대기|
|observed_effect_21695_sixteen|16|Claude검증대기|
|observed_effect_19584_gray32|32|Claude검증대기;입력형태경고있음|
|aestivalis_flight_missing90_arms11|11|Claude검증대기|
|aestivalis_ground_missing90_arms12|12|Claude검증대기|
|observed_effect_21819_four_levels28|28|Claude검증대기;입력형태경고있음|
|observed_effect_21080_complete51|41|Claude검증대기|
|observed_effect_21080_complete51|10|소스/팔레트확정·해당형태재생미관측|
|aestivalis_ground195_missing19|19|Claude검증대기;입력형태경고있음|

## 발견해 고친 제작 연결 결함

- **jade6 참조캔버스크기 오류는root 연결실수**. HD512×128에참조256×128을등록해잘못된비율로빈영역을읽음. 올바른128×32 native_full_plume.png로교체,92094~92099 다시굽기완료. 그림자체재색칠은없음.
- 설치기는HD/native 정확4배,참조alpha/사용RGB와원본index·actual팔레트동일,원본있는데생성crop maxalpha<16을하드오류로처리. 굽기도nonempty원본→near-transparent결과를실패로반환하고errors>0이면exit1.
- **21819 생성누락4**: 실제half-disc를추가발명으로오해해뺀1개,alpha최대5였던점선3개. 같은효과자체생성반원회수+점선새생성으로교정. 다른24개와검정2는불변.28개설치·굽기완료.
- **21080 단색fill누락**: 실제8×16흰면을생성도구로다시그려해당자체그림영역만교체.41개관측계약과10개원본계약모두설치·굽기.10개는실제로재생에서보았다고하지않음.
- 이번373개입력캔버스/원본계약/최대alpha기계검사오류0(PRODUCTION_INPUT_BUILD_CHECK.json). 이것은그림품질/레이어/실제재생합격이아님. 최신104개대상굽기errors0,6.0초이며게임FPS수치가아님.

## Claude 우선 확인

- 상세장면/offset/알파·형태경고는CLAUDE_VERIFICATION_QUEUE.md 및각제작인계. 새후보로바꾼묶음에이전검증승계금지.
- jade6:수정된좌표비율에서실제표시와상하연속접합. 단색3751420720의옅은생성gradient는여전히품질검토사항.
- 21819:half-disc/점선4복원,반원core/단색·점선폭/밝기4단계/잘린면얇은윤곽.19584:먼지를렌즈처럼해석했을가능성/원호band·crop끝선,일부입력겹침낮음.
- 21080:관측41은unit325_weapon1321_source.state+250~270/+485~510.추가10은9미관측shape+1다른bank계약. 작은점/단색fill/두bank기하·색/가림을확인.
- 아스테바리스:+90 공전145~150 11고유,육전151~156 12,+195 육전151~155 19. 전체pose의기존연결의존도함께확인. 손가락자동완성/손목cap/아주작은조각/색영역/전체기체선굵기.
- root17168패널4:하나의80×80새그림에서16px겹침을공유. source_pose.state+0.기체본체/효과의미분류미확정이므로effect태그를강제로넣지않았음. 실제역할/affine·가림/선·색을확인.
- 22378late:고유shape2의67fade RGB계약.기본2그림만제작,나머지65변형은자동해결주장안함. fade_palette_characterization.json은원본팔레트색의근사계수자료이며최대잔차16.37/255라단순RGB배율만으로정확하다는보장없음.공통fade런타임처리검토필요.
- Core mask의sub/UI/폰트/맵/시나리오미적용·동시foreground와cutin self-blend한계는Claude이전기록대로남아있음.

## 배포·Git

- 이전146타깃까지5c34ff36으로푸시완료. 이번추가와jade참조수정은곧별도커밋/푸시하며결과를갱신합니다.
- EXE는아직이전번들. Claude그림/재생검증뒤a6d80b29코어·최신Python·캐시를포함해다시묶어야함. 실행중창을임의로닫거나재시작하지않음.
- 옛1.28GB compact후보는최신그림이없으므로live교체금지. 재생산/배포때현재키로다시compact해야함. 원본ROM과세이브는public repo에넣지않음.
- 과거누락보고서와현재등록을대조하는plan_missing_art_batches.py는제작선정도구이며전체ROM재감사/품질완료판정이아님. 다중IMG/미관측팔레트/잘못된역할추정은원본계약추가확정후제작.
