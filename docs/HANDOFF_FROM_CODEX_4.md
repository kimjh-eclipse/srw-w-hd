# Codex → Claude 핸드오프 4

현재 교환 파일입니다. 이전 제작 이력은 Git 및 HANDOFF_FROM_CODEX_3.md에 보존합니다. 현재 상태는 이 파일을 우선합니다.

## 현재 상태와 수량 기준

- 이번 작업묶음 **603개 연결 항목 설치·대상굽기 완료**. 92493도 자체 새 그림으로 교정해 같은19 전체 굽기 오류0 뒤 활성화했습니다. 기존 그림 교체·팔레트 변형을 포함하는 작업량이며, 전체 HD 누락에서 단순 차감할 수 없습니다.
- **전체 누락은 이전 ROM 감사의11,358종이 마지막 집계**입니다. 전체 잔여는 재집계하지 않았고 완료율을 주장하지 않습니다. 감사 밖에서 발견된 실제 누락도 따로 기록합니다.
- 최신 지시: Codex는 제작·연결·굽기·커밋을 진행, 독립 그림/색/재생검증은Claude담당. 실제로보지않은것을보았다고기록하지않습니다. 미관측계약10은actual_observed=false.
- **코어 소스 해제**. Claude95ba46f0/d98c4226 반영. 기본 DLL SHA256 a6d80b29119f7c18447725acc4e0e5c8fb88cdda07d8cef6ccb106e936b64fe0,cachedOBJ API포함. Codex는공유runtime/core를수정하지않습니다.
- 사용자 테스트 창은유지. 컴퓨터종료금지. ROM·세이브·사용자설정·로그·자격증명은Git추가금지. baked.sqlite은제작산출물로Git에추가하지않습니다.

## 진행 중인 다음 제작

- next_shape_art: 아스테바리스 다음 실제미연결기계자세/무장. +90 공전11/육전12,+195육전19는이번묶음에반영됨.
- next_key_art: 21667 29개는 연결·굽기 완료. 다음 IMG22111/22342/21071 등 실제 누락 원본을 확인해 연속 제작 중.
- effect_live_palette: 신규 효과5묶음86 중85개 굽기 완료. 22410의92493 빈 출력부터 교정한 뒤 후속 효과 제작. 소유 불확실·미관측 팔레트 추정은 제외.
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
- 이전373개입력캔버스/원본계약/최대alpha기계검사오류0(PRODUCTION_INPUT_BUILD_CHECK.json). 이것은그림품질/레이어/실제재생합격이아님. 최신104개대상굽기errors0,6.0초이며게임FPS수치가아님.

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

- 373타깃과jade참조수정·생산하드검사는da3c306f로푸시완료. 이후72개추가작업은현재미커밋이며다음커밋/푸시예정입니다.
- EXE는아직이전번들. Claude그림/재생검증뒤a6d80b29코어·최신Python·캐시를포함해다시묶어야함. 실행중창을임의로닫거나재시작하지않음.
- 옛1.28GB compact후보는최신그림이없으므로live교체금지. 재생산/배포때현재키로다시compact해야함. 원본ROM과세이브는public repo에넣지않음.
- 과거누락보고서와현재등록을대조하는plan_missing_art_batches.py는제작선정도구이며전체ROM재감사/품질완료판정이아님. 다중IMG/미관측팔레트/잘못된역할추정은원본계약추가확정후제작.

20498原본확정미관측8은기존같은효과의자체그림crop에연결완료(새PNG중복0). 새로제작한원본확정미관측35와21667관측28+미관측1도연결예정. 합쳐72타깃만대상굽기. 미관측항목에실제OAM/프레임을가공해넣지않고actual_observed=false로보존.


## 후속72타깃 굽기 완료

- IMG21667:29(실제관측28+확정원본/실제팔레트기반미관측1). sourcePLT21666bank0의16값모두실제캐시와동일. unit224mechan143/unit249mechan131·143,각정확offset계약보존. 굽기오류0.
- IMG20498:같은효과자체그림으로정확crop재사용8(새PNG중복0)+추가새그림35.43개모두해당shape재생미관측,actual_observed=false.단일IMG PAT20499+IMG20498+PLT20497bank0/1의16값실제동일. 미관측을실제확인한것처럼기록하지않음.
- 35개HD1024×768에맞는native256×192는native_20498_full_bank0/1을세로로쌓아구성. native_continuation_pair128×64는일부patch참조이므로본묶음native로사용금지. 새4배검사가그잘못된선택을live변경전에막았고올바른native로설치완료.
- 이번72개굽기오류0/6.2초. 최신라이브러리c46e42084acd708d2f1f5e4af0fa79fd279fc971027276b510c90fba7885d54e,material캐시동기화완료.445는기존수정포함작업타깃합이며전체누락감소445가아님.
- 다음:next_key는21667뒤22111/22342/21071등, effect는신규19954/21279/22338/21921/22410/22497/20928, shape는아스테바리스/FMP실제기계누락을연속진행.

새실제효과5묶음86계약연결·대상굽기예정. 19954=16,21921=13,22338=24,22410=19,22497=14.20928의2는19954와원본bytes/사용색/크기동일하여중복등록제외. 신규전용연결(--new-only)으로이미연결된exact그림을덮어쓰지않음.19954의source소유미확정검정평면1보류유지.

새86중85굽기성공,92493하나prepare뒤near-transparent로저장거부. 해당RGB연결disabled/rgb_enabled=false로잠시차단해원본이숨겨지지않도록함. 그림수정후동일ID를직접굽고성공하면복구예정. 기존18/sourceimage는보존.


## 누락 제작 병렬 작업 재개

- 사용자 지시에 따라 제작 서브에이전트 3명을 다시 가동했습니다. 효과 신규 묶음과 92493 빈 출력 교정, 후속 효과 원본 계약, 아스테바리스/FMP 실제 기계 파츠로 분담했습니다. 루트만 라이브 연결·저장소 쓰기를 담당합니다.
- 최신 86개 중 85개가 구워졌고 92493은 원본 표시 유지 상태로 교정 중입니다. 종전 445개와 합쳐 현재 구워진 작업 대상은 530개이며, 신규 86 전체가 완료되었다고 기록하지 않습니다. 이는 누락 감소 수가 아닙니다.
- 캐시는 disabled 적용 이후 23:36:23/23:36:28에 다시 생성된 파일이 있습니다. 92493 수정 후 같은 아틀라스 19개를 명시적으로 다시 굽고 성공한 뒤 활성화하겠습니다.
- 실제 재생·색·레이어 검증은 사용자 지시대로 Claude에게 맡깁니다. 현재 창과 공유 런타임 코드는 건드리지 않습니다.


## 추가9 제작 완료 / 92493 교정 완료

- 92510~92511 FMP +15 총2종:같은생성출력,실제cachedOBJ팔레트. ROM13662 (144,48,32,16)/(120,24,16,8) bytes직접동일근거추가. 기존본체보존.
- 92512 IMG19954 실제관측추가1:같은효과자체그림의정확crop연결,새PNG중복없음.
- 92513~92518 아스테바리스육전+150 팔6종:ROM10778 (56,0,32,16) actual6팔레트별새그림. 원본기존72OAM보존.
- 추가9굽기오류0/5.5초. 22410교정전체19굽기오류0/5.7초. 그림/실제재생품질합격수치아님. 다음22111/22342 총57후보인수·연결/굽기중.


## IMG22111/22342 추가57 연결·굽기 완료

- 92519~92542 IMG22111 신규24(관측16/원본·팔레트확정미관측8),92543~92575 IMG22342 신규33(관측15/확정미관측18). 관측여부는계약actual_observed대로보존,미관측OAM/프레임발명안함.
- 정확4배/원본index·actual사용RGB/비어있지않음기계조건후연결.57굽기오류0/5.6초. 각graphics폴더에제작인계·source계약·생성출처보존. 시각품질/실재생미검증.
- 다음팔케+165 신규6 설치후대상굽기중. 효과담당은추가22360/22030/19982/22591 총38새계약제작중.


## 팔케6 추가 완료

- 92576~92581 팔케 unit276+165, 실제미연결7OAM/6고유. ROM14225/14249원본bytes확정,actual팔레트색유지. 기존9OAM그림유지.6굽기오류0/4.9초. 작은연결편/주황점/손목접합·절단면품질은Claude대기.
- 현재603작업타깃,종전445이후158개추가.전체누락잔여와단순차감금지. material캐시동기화후현재제작분커밋·푸시진행.
