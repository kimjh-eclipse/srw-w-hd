# 클로드 검증 대기열

## 담당과 갱신 규칙

사용자 최신 지시: **Codex는 그림 제작·연결·굽기·커밋을 진행하고, 독립 검증은 Claude가 담당합니다.**
Codex가 새로 공식 전수 검사나 실제 재생 검증을 반복하지 않습니다. 설치 입력의 크기·실제 해시·팔레트·바인딩 중복·굽기 오류 같은 작업상 기계적 오류는 확인합니다.
이 파일은 제작 중 변경과 반영 직후마다 갱신합니다. 검증 대상을 새 그림으로 바꾸면 이전 검증은 자동 승계하지 않습니다. 결과는 Claude가 별도로 판정합니다.

## 지금 우선 검증/수정할 공통 런타임

|대상|현재 상태|자료와 확인점|
|---|---|---|
|컷인 자기 페이드|Claude95ba46f0 GPU경로수정,남은한계검증|`docs/REVIEW_CUTIN_FADE_FLASH.md`. getter_cutin+30/32, golion_cutin+0~5. source의첫대상EVA/EVB·뒤대상·윈도우색효과허용을래스터시점으로적용. 앞BG효과용foreground와구분|
|윈도우 플래시|Claude d98c4226 반영,확인범위·미적용범위추가검증|기본DLL a6d80b29…,상단window적용. sub/UI/맵/시나리오·색효과허용비트·BLDY/MASTER는별도한계. unit333+28/+30,대사창주변순수원본쌍|
|단색 효과 수집/접합|Claude d98c4226 진단수집옵션반영,그림24개초안연결|verify_runtime_path가unknown_flat을켜며플레이어는끄고있음. flat은known연결로표시. 기본DLLcachedOBJ API포함. 아래24개그림의접합검증필요|

## 신규 제작/반영 대기 묶음

|ID|작업 상태|변경범위·파일|Claude가 볼 장면·알려진 문제|
|---|---|---|---|
|P-22163-24|24개초안연결·굽기완료·Claude미검증|atlas observed_effect_22163_complete24.91861–91876갱신+91917–91924새fill.기본그림candidate_complete24.png, retry는미설치비교선택지|unit299 mechanical_cutin_141+54/55/56.균일cyan미세gradient사각선/white구멍·UI가림.기존16검증은새그림에승계불가.24개전부다시굽기|
|P-MAZINKAISER-179|20종초안연결·굽기완료·Claude미검증|atlas mazinkaiser_running179_pose.새RGB15+기존5갱신,indexed fallback5보존.정확목록은동폴더install_report.json|unit297 weapon1213/frame300+179/190/220.특히slot51→91913 형태IoU.564748 경고. 설치기는기준.70유지하고defer-shape-review로미검증표시.접합/역할/색을통과로보고하지않음|
|P-GETTER-AXE|91896연결·1개굽기오류0·Claude미검증|atlas observed_getter_tomahawk_head,graphics/rework_getter_tomahawk_head.실제source바이트/16팔레트일치.기계무장이므로effect_part태그없음|getter_cutin+207/210/234/258/259/299.도끼중앙홈/날곡률/절단축·오른쪽스파이크/잔상앞뒤.별도독립검사실행안함|

## 반영 완료, Claude 확인 대상

- **그레이트후속18**: atlas great_mazinger_running179_pose. 신규91877–91881/91886–91893,기존82809/7352/7346/7351/7340. `graphics/rework_great_running179_pose`,전용contract/provenance. 작은7340도새그림이므로첫자세+3에도영향. +179/190/220노출·다른팔자세, +3은테츠야컷인에가려육안판정불가. 기존Codex300프레임추적18개HD/vanish0은참고자료이며Claude검증대체아님.
- **겟타별빛/세로섬광2**:91894/91895, observed_getter_glints_21869. `test_current/parts/getter_remaining_effects/effect21869/observed_pair/`,actualRGB/static/effect태그. 별빛+234/세로광선+258/259. 원래12개중관측2단계만이며나머지10개미완료. 굽기2/오류0. 역할변경전Codex재생10/10·4/4HD는참고.
- **22163기존16**:91861–91876, observed_effect_22163_sixteen.24완결후보반영전이므로여전히중앙nativefill8개와접합차이있음. 검증시16개연결성공과효과전체정상을구분.
- **민트38/19645관측7/진겟타머리3/그레이트첫17/코다르16/데스3/파워드레드9/22378효과16**:현재상세binding·자료는HANDOFF_FROM_CODEX_3.md표참고. 최근공식선택133개에명암검토3개64207/82798/91777남음. 이검사에서ROM전체누락완료를뜻하지않음.

### 권장 재생 명령 틀(Claude 실행용)

Python311, C:작업공간에서:
```
python -X utf8 scripts/verify/verify_runtime_path.py --state <실제state> --frames 300 --pure-native --save-frames <offset들> --track-atlas <새atlas> --name <고유검증명>
```
`--pure-native`는별도HD-disabled프로세스원본을같은offset으로재생합니다. 예전저장쌍의좌측은HD suppression후framebuffer일수있으므로순수원본으로쓰지마세요.
도구결과REVIEW/INCOMPLETE와그림의정확성은별개입니다. 얼굴/몸통오연결,색/절단면/눈중복,대사창가림/효과앞뒤,fade/flash를실제쌍으로보아야합니다.

## 코드/바이너리 검증 대상

1. 효과의기체폴백제외: hd_core.py/srww_parts_impl.h/srww_hd.h/libretro.cpp. 기본10%기체보호유지,명시effect_part만제외. 기존162상태×90raw판정A/B와unready1249자료는effect_guard_review/. 정상기체보호와미준비원본보존을Claude가확인.
2. cachedOBJ읽기API: srww_texture_cache.h/srww_hd.h/libretro.cpp. **Claude가d98c4226기본DLL에포함**,별도진단DLL도보존. 읽기전용capacity/엔진/OAM검사,known8snapshot/invalid5/240frame일치자료는HANDOFF_COMPLETE24_AND_API.md. Codex는이3파일수정종료,Claude수정과충돌안하게공유코드추가수정중단.
3. build/frozen_update EXE는새window/cachedAPI코어와fade코드로재묶기예정. 기존번들은구버전. dist팩미갱신,PNG→WebP내용해시·baked키호환과실제배포팩검증별도필요.
4. 구운DB정리후보: baked_store_compaction/candidate.sqlite 1.28GB. live2.58GB는그대로. 현재87348유효키만복사·재인코딩없음. 이후새그림추가되어후속키를포함해다시생성해야함. 후보를현재live로바로덮지말것.

## 배포/커밋 처리

전체완료율160/11358같은비율은사용하지않습니다. 바인딩·원본고유파츠·팔레트변형·OAM중복은서로다름.
전체기체목표를유지하되83개테스트기체/보유장면을우선배포검증목록으로구분. 검증완료범위와미포함범위를배포설명에명시.
Codex가검증된변경부터기능별선택커밋을진행합니다. ROM/세이브/사용자설정/오류로그/거대미추적DB를일괄추가하지않습니다. 푸시·EXE팩갱신은별도상태기록.

## 코어 소스 해제
Codex의코어작업은종료했고046a9701에읽기API를남겼습니다. 전체해제범위/진단DLL과기본DLL차이/정확fill8계약은HANDOFF_FROM_CODEX_3.md상단의같은제목을확인하세요. Claude가윈도우마스크·단색수집조건과기본DLL빌드를진행할수있습니다. Codex는공유코어파일을추가수정하지않고그림작업을계속합니다.

## 제작 도구 변경 확인 대상
- bake_parts.py가매번773색표를재계산하지않고기존정확palette해시색표를재사용,새색표만계산하고npz는임시파일후atomic교체.91896필요굽기에서772재사용/1추가,오류0,9.8초. 실게임FPS개선주장이아님. Claude는누락/신규팔레트·기존table동일성을확인할수있음.
- 일반설치기--defer-shape-review는시각경고를독립검증대기열로넘기며.70기준/측정값은그대로기록. actualhash/index/palette/크기/prefix검산은해제하지않음. 낮은형태를통과로표시하지않음.

## 반영 묶음 고정 기록
마징카이저20+원형효과24=44개굽기완료/오류0,773색표전부기존해시로재사용. `test_current/parts/current_production_batch/handoff_manifest.json`에대상binding별spec SHA256과atlas이미지/참조SHA256을저장했습니다. 후속무관그림추가로전체library SHA가달라져도대상spec/atlas가같은지대조해검증결과범위를판단하세요. 새그림의독립검증은미실행입니다.

## 새 반영 묶음55 — 검증 대기
|묶음|반영|Claude 확인점|
|---|---|---|
|21798 광선/폭발29|91925–91953, observed_effect_21798_29.2실제팔레트/exactRGB/static/effect|unit19 mechanical_cutin_168 +12/14/16/20/22/24/26/28/32/34/38/66/70/72.형태참고경고91929/91933/91936/91939(0.70기준미달),가는직선/불꽃꼬리/파편위치·alpha프린지|
|겟타22053 충격광/파편8|91954–91961, observed_getter_effect_22053.중첩crop은연속그림공유|getter_cutin+76/78/137/139/147/151/155.형태참고경고91956–91961,연속부분의색/면적/절단선검증필요. 새그림모두미검증|
|마징카이저초기18|mazinkaiser_initial3_pose,12기존RGB교체+6새RGB. 정확binding은전용install_report.json|unit297weapon1213/frame300+3및초기컷인소실후노출.20OAM/18고유,기존17920개와rawhash교집합0.머리/날개연속생성후분할했으나접합·색/역할은Claude판정|

55개대상굽기완료/오류0(8.9초,기존palette773재사용/2개추가). `test_current/parts/production_batch_55/handoff_manifest.json`에대상spec/atlas SHA256과binding목록기록. 검증완료를의미하지않습니다.


## 최신 추가 제작 — 고유83종 (Codex, 11월13일)

현재 상세/번호는 `HANDOFF_FROM_CODEX_4.md` 및 `PRODUCTION_ART_BATCH_CURRENT.json`이 기준입니다. 이전 _3.md의 작업예약·옛 DLL상태는 종료됐습니다.

- 데스사이즈7086 일반20: `duo_map_attack.state +120`. continuous그림 사용. 뿔 금색/눈 초록/팔·몸체·날개·낫 접합.
- 데스사이즈 접힌날개14+기존1 의존: `duo_cutin.state +180`. 얼굴 가림은 원본문맥, 작은 연결부/키색/컷인·UI순서.
- 코다르 분신14: `unit280/mechanical_cutin_168.state +90`. cached26OAM14unique. 옛17입력 phantom3은 미설치. 좌우단검/본체·기존중앙기체 스타일.
- 겟타pole2: `getter_cutin.state +56/57/59/90/110/126/207/234`. 도끼축·잔상 역할/접합. effect태그없음.
- 21948새17: unit413 weapon1610 frame360+112~128,frame600+31/63~94. 기존exact14보존. 흰중심·민트선 이음매. gray2는20498과exact공유 binding91986/91987.
- 20498회색2: unit413 weapon1610 frame600+31 OAM3/4. 상하곡선접합/희미한alpha.
- 샌드록16 기존그림교체: `quatre_cutin_full.state +0`.17OAM16unique. 컷인이몸체를가리는state이므로 body판정에 별도관측도 필요. 금색13/노랑14/초록15 배치·두얇은셀5/9·스카프/장갑 이음매.

첫67+샌드록16 굽기 오류0. **독립 검증 미실행**이며 감사/재생 검증은 Claude 담당. 검증 전 EXE재묶기/배포팩 갱신은 대기.


## 후속23종

- 데스사이즈 forecast14: `duo_map_forecast.state +0`, atlas deathscythe_forecast_closed_pose.17OAM/14unique, 기존normal/접힌날개그림과별도팔레트. 닫힌날개/낫·눈·V-fin/손잡이/발 접합. 설치/굽기완료,오류0.
- 효과20498 white7: unit413 weapon1610 frame360/600의39문맥중신규7만. 기존32exact보존. atlas observed_effect_20498_white7. 흰core·민트띠/미세키프린지·기존그림과접합. 설치/굽기완료,오류0.
- 데스사이즈 scythe150 두조각: duo_cutin+150,92083/92084. 연속64×16그림에서좌우분할. body13의존 pose_dependencies.json. 입력IoU .7185/.7055로기준바로위이므로특히얇은날실루엣확인. 독립시각검증대기.


## 추가 샌드록9 / jade6

- sandrock_weapon_closeup_cached_pose:9종(38668/38635/38649/38647/38622/38652/92091/38633/38628),기존8교체+1신규. sandrock_closeup_cutin_full.state+0 body캐시계약. sourceframe은플래시라그대로가시성판정금지. Claude전후프레임순수원본쌍확인. 원본빈틈/허리직사각조각/얇은cell6/전체접합·색. 설치/굽기오류0.
- observed_effect_20498_jade6:92094~92099,기존exact4보존. unit413 weapon1610 frame360+112/+114문맥. **단색3751420720의생성그림에옅은gradient남음**. root는도트색채움으로숨기지않고미완료품질이슈로인계. 두연속plume접합/색/alpha확인. 설치/굽기오류0은화질합격아님.


## 최신 추가·교정 (전체누락수와분리)

- green7084/7085:92100~92109. actual팔레트별새그림. 가는2(92100/92101)는새생성후PCA기하등록만수행(원본RGB/alpha stamp없음),다른8불변. IoU .164/.179→.682/.683,기준.70미만경고유지. thin2단계그림이아닌좌표/선폭정리,실제재생판정필요. duo_map_attack+30/+60. 10전부재굽기완료.
- 19600새2:92110/92111,unit413 weapon1610 frame360+112/+114. 기존73exact보존. jade/white곡률·명암·기존그림접합.
- 그레이트thunder168새10:82822/92113~92121. unit299 mechanical_cutin168+0 body20OAM19unique중old9보존. 실제미연결추가1/indexed교정8/exact교체1. 원본·후보 전체문맥과의존계약은graphics/rework_great_thunder168_cached. source프레임버퍼는HD-enabled라pure-native증거로쓰지말것.
- 19645새3:92122~92124. unit333 mechanical168+34/+46. 두가는2색slash는입력IoU.558/.640경고. 선폭/라벤더끝·팔레트·알파/기존7접합.
- 22378late:67unbound RGB가형태2의연속fade변형. test_current/parts/effect_22378_late/{observed_contract.json,new_22378.json}. 67새그림/재색칠바인딩으로메우지않음. Claude가팔레트fade를원본색번호/블렌드로보존할경로를검토필요. 기본두형태그림은제작담당별도진행.

이번작업타깃146모두대상굽기완료. **이는전체11,358누락의감소146이아니며전체잔여재집계아님**. production선정큐는구형누락계약과현재등록의대조일뿐QA가아닙니다.


## 최신373개 작업대상 — 전체누락감소수와분리


- 현재정확목록/그림SHA는 PRODUCTION_ART_BATCH_CURRENT.json,현재요약은HANDOFF_FROM_CODEX_4.md.373은기존그림교체/팔레트별항목포함작업량이고11,358누락에서단순차감금지. 실제미관측10은actual_observed=false.
- **root연결오류수정**:20498jade6 HD512×128/잘못참조256×128→정상참조128×32로교체.92094~92099다시굽기.캔버스잘못읽기로사라졌던위치가실제로표시되는지확인.
- **21819 생성누락4복원**:반원1+alpha최대5점선3.동일효과자체생성pixels만복원/새그림.28종재굽기완료.원래검정2/나머지24불변,최신그림SHA참조. cropped끝윤곽·band/brightness/원형반원구멍유무·점선폭검토.
- **21080 총51계약**:관측41+원본/팔레트확정미관측10(9새shape/1다른bank). unit325_weapon1321_source.state +250~270/+485~510가41의문맥.단색cell4누락은생성도구교정.추가10을실제본것으로판정하지않음.작은점/단색fill/두bank의shape/색/레이어확인.
- **21657 노란29/붉은16**,19584회색32:입력source/palette개별확정,기존정확공유보존.19584는먼지가렌즈형으로변했을가능성·원호곡률/띠·작은crop끝선.구체state/offset은graphics제작폴더HANDOFF파일.
- **21695 회색기류16**:unit1 attack_7108_connected+50~63. low-alpha주변흰/자홍RGB프린지·구름폭·갈고리위치/원본이음매검토.
- **17168 패널4(root생성)**:unit348/weapon1400 source_pose+0.한80×80그림에16px겹침4crop을공유. 기체/효과역할분류미확정(effect태그보류).실제affine/앞뒤/가림·원본모양/무늬/밝기확인.
- **아스테바리스+90 공전11/육전12,+195 육전19**:기체별actualpalette생성,기존OAM의존별도보존.손목/무장절단면cap·손가락자동완성/색영역/아주작은셀·pose전체선굵기검토.각계약에개별unit/state/OAM/offset.원본IMGindex와동일이지만ROM PLT번호까지전색상확정이라는주장은없음.
- 전체373입력캔버스/원본계약/nearempty기계검사오류0(PRODUCTION_INPUT_BUILD_CHECK.json).입력품질/게임재생합격은아님.최신104타깃굽기도오류0.빈/nearempty그림하드거부가추가됐고errors>0이면빌드실패.
- 22378late67계약은shape2의fade. 기본그림2만있고65를자동으로해결한것아님. fade_palette_characterization.json의최대근사잔차16.37/255로단순RGB배율의정확성도보장못함.공통팔레트fade처리검토요청.


## 후속72대상 (총445작업타깃,전체누락감소수아님)

- 21667 신규29:실제관측28/소스·팔레트확정미관측1. unit224mechan143,249mechan131/143의+133/+150등,정확개별offset은graphics/rework_effect_21667_twenty_nine/HANDOFF. 노란점/흰궤적·회청기류의곡률/폭/낮은alpha테두리/단색광점확인.
- 20498 추가미관측8은기존white7/jade6의같은효과자체새그림의정확crop으로공유. source_contract_extensions/new_20498_unobserved_contract.json 및report. source/PAT/actualPLT16근거보존. 실제해당shape를재생에서봤다는주장아님.
- 20498 추가새그림35:source/PAT/actualPLT16확정,shape재생미관측. 큰불투명연속면은생성alpha가빠져자체생성alpha/색으로복원했으며원본mask/RGB복사없음. x64접합/절단면선/전체단색면·두bank밝기/실제레이어검토. native는256×192fullbankpair,128×64patchpair가아님.
- 최근72굽기오류0. 현재총445연결항목엔기존그림교체·팔레트별계약포함,11,358총누락에서차감불가. 독립시각/실제재생미검증상태유지.


## 신규 효과 5묶음 86계약 (85개 굽기, 1개 교정 중)

- IMG19954 신규16, IMG21921 신규13, IMG22338 신규24, IMG22410 신규19, IMG22497 신규14. 자세한 source/state/frame은 각 graphics/rework_effect_<IMG>_new<개수>/pose_contract.json 및 ART_REVIEW_NOTES.md 참조.
- 19954 검정 평면1은 source 소유가 모호하여 제외. IMG20928의2개는19954와 raw index/사용색/크기 동일해 중복집계하지 않았습니다.
- 22410의92493은 굽기 후 거의 투명하여 연결을 비활성화했습니다. native fallback 유지. 후보 교정 뒤 전체19를 다시 구울 때 갱신하겠습니다. 기존85개 굽기는 오류 없는 저장 결과이며 실제 재생/품질 합격이 아닙니다.
- 서로 다른 팔레트의 색/밝기, crop 경계의 연속면과 인공 외곽선, 반원/원호/광점의 형태, 전경 효과와 대사창 가림을 확인해 주세요. source 미관측과 실제 관측 구분은 계약필드 그대로 유지합니다.


## 추가 실제무장9와 효과57

- FMP총92510/92511:unit261 mechanical_cutin_168+15,ROM13662/144,48및120,24. 생성총모양의충실도/총-손목접합/단차와절단면선을우선확인. ground150팔92513~92518:unit151~156+150,기존72OAM보존.19954추가92512는실제+198.
- 22410의92493교정후19전체재굽기오류0,같은ID활성화완료.다른18crop RGBA불변.여전히입력겹침낮은92489/92490등은형태확인필요하며완료판정아님.
- IMG22111=24(관측16/미관측8),22342=33(관측15/미관측18) 굽기오류0.각graphics/rework_effect_<IMG>_new<개수>/HANDOFF_ART_TO_CLAUDE.md 및pose_contract.json의source/state/frame참조. 선폭·질감·색단계·파편/연속면과가림검토.
