# Codex 인계32 — 4xBRZ 원본 참조로 미처리 그림 계속

사용자11/16: 기존 받은 미처리 원본은 Codex가4xBRZ를 적용하고, 필터본+원본+화풍으로 이미지 생성. 앞으로 Claude도 같은 방식 자료를 전달. 진행·검증 항목을 핸드오프로 소통.

## Claude → Codex 다음 자료 형식
1. 조립 원본1배 native.png(필터 입력), 좌표 그대로 nearest4x native_4x.png. 시트는 native_sheet_4x.png + layout.json(기본자세 첫칸, 최대9).
2. 같은좌표/같은캔버스 reference_4xbrz.png + reference_4xbrz.json: 실제4xBRZ의 알고리즘/옵션, 원본·출력·layout SHA, 원본 크기/배율. 이미4배인 그림을 다시4배로 늘리지 않습니다.
3. 현재 실제 DeSmuME xBRZ1.4 default ScalerCfg/ARGB4x(투명파츠) 사용. 화면용 Render4xBRZ RGB와 알파 경계 계산이 다름을 표기합니다. 원본색/위치/부품/효과의 기준은 비필터 원본입니다.
4. 도구: scripts/assets/prepare_xbrz_reference.py --unit N --sheet S. 커트인 단일이미지는 --image PATH --input-scale 1(원본1배) 또는4(정확nearest4배 검증됨일때만). 이 작업은 원본·공식layout을 변경하지 않습니다.
5. 필터 출력은 생성 참고자료입니다. 새로 그린 그림/설치후보로 등록하지 않습니다. 원본이 없는 HD파츠를 다른팔레트 재색칠로 메우지 않습니다.

## Codex 실제 이미지 생성
- 실제참조순서: Image1 4xBRZ(주윤곽), Image2 비필터원본(정밀기하/실제색/작은경계 우선), Image3 데스사이즈화풍실물(style-only), 후속은 Image4 자기기체 새첫판(design-only).
- 사람컷인은 원본컷인+필터본+기존인물화풍만 참고하며 기계기체화풍을 얼굴설계로 쓰지 않습니다.
- 손·발·사자머리/실루엣·무장·효과·부분소실/가림을 원본대로, 넓고깨끗한셀면과매끈한잉크선/쨍한원본색으로 새작화합니다. 필터의 둥근얼룩을 임의장갑/눈/얼굴로 의미화하지 않습니다.
- 내장image_gen만사용. PNG RAW그대로/실제prompt·참조SHA·xBRZ정보·layout·STYLE_VERSION·HANDOFF즉시저장. 코드로색/alpha마스크/형태를후수정하지않습니다.
- 해상도 기본생산기준: min(출력W/참조W,출력H/참조H)*4 >=2.5. 미달은보류. 큰9칸판이 도구출력예산을 넘으면 공식판보존, 원본픽셀무resize 별도2x2(기본+후속3)판 및별도layout으로생성. 공식layout직접적용금지. 정밀기하검수는Claude.
- Codex=그림생성/기본출력관찰, Claude=눈검수/정합/조각분할/굽기/연결/게임확인. 출처모호한파츠는 원본의미를추측해완성하지않습니다.

## 재개 분담
- root: 최신HANDOFF_TO_CODEX_8 우선요청 트로와가면 한장컷인. 이후 unit403~429 미완료.
- pink:12404/12602·03부터129~149.
- mihiro:21502/21602부터217~299.
- robot300:380~399/430~472.38001첫9칸반환은배율2.03으로저해상도보류, 별도4자세판으로다시진행.
- 51/188/189 도구moderation보류는우회/재시도하지않습니다.

## 현재 진행
- 트로와가면: live_native.png에실제4xBRZ적용, 필터+비필터게임화면+기존인물화풍으로 한장생성중. 얼굴반쪽/가면/손/머리카락을한그림, 파랑배경·대사창투명지시.
- root40302/40402: 새4xBRZ방식으로생성중.404는 사용자가지적한사자발 정체성과좌우팔귀속을프롬프트에명시.
- 12404/12602/12603: 새방식반환저장,124전4판/126전3판후보완성.125→124전체원본동일공유기록갱신.12602검정실루엣은생산자alpha표시로존재확인. 전부Claude미검수.
- 다음반환부터아래에즉시추가합니다.

## 공통 Claude 검증
원본센서색/눈수/얼굴형, 팔/다리귀속·관절연결·사자발등동물부품, 실루엣/좌표/비율/가림/분리, 효과길이/개수/반투명도, 배경알파, 필터얼룩새부품오해, 판간일관성, 출력배율. 후보수는합격/설치/ROM전체완료수가아닙니다.

[비교 실험31](HANDOFF_FROM_CODEX_31.md) · [사용자그림수정30](HANDOFF_FROM_CODEX_30.md)


## 트로와 가면 컷인 신규 RAW 전달
[그림](../test_current/parts/cutin_redraw/trowa_mask/candidate_full.png) · [세부인계](../test_current/parts/cutin_redraw/trowa_mask/HANDOFF.md)

필터본+원본+인물화풍 실제3참조. 가면/손/머리카락/오른얼굴반쪽과녹색눈하나/세로split관찰. 배경/대사창제외. RAW (1448, 1086)로 요청1024×768과같은4:3;Claude전체캔버스정규화후계약좌표분할필요. 실제prompt/refSHA/RAW보존,미검수·미설치.


## 새화풍 그림 전달 unit403 sheet02
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1385, 1136), 원본 (1848, 1516). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 생산자 육안으로 각 자세의 얼굴/원본 가림·슬롯 수를 살폈습니다. 손발귀속·관절·효과와 필터의 뭉침 해석은 Claude 정밀검수 전입니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: NINE slots: TOPLEFT orange/goldlit originalbase, other7robotstates DARKBLUE/silvergrey withred/orangecrests, sourcegreeneyes andcompactflatgrey mask. BOTTOMLEFT ONLY fourorangefireballs+whiteyellowstar withsourceextent, don'tfillrobotthere. Topmiddle bentknees/crouched, toprightfrontalcannonfaceocclusion, midleftoblique/croppedfullsource, midcentrelonggreybladeoverface, midrightgreyweaponverticalcoverface, bottommiddlebladefront, bottomrightlargeangledgreyweapon. Preserve every originalobscured head/body, don'trevealinventedface. Drawgoldfirstslotindependentlyinactualgoldpalette; no autocolourtint. 실제4xBRZ primary + unfiltered원본 + Deathscythe style-only + 자기첫판 design-only.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_403/robot_set/SHEETS/sheet_02/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_403/robot_set/SHEETS/sheet_02/HANDOFF.md)


## 새화풍 그림 전달 unit404 sheet02
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1288, 1221), 원본 (1404, 1332). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 생산자 육안으로 각 자세의 얼굴/원본 가림·슬롯 수를 살폈습니다. 손발귀속·관절·효과와 필터의 뭉침 해석은 Claude 정밀검수 전입니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: NINE slots. This is source ROBOT with REDarm ononeanatomicalside and GREENforearmonother, RED triangularshoulderfins and SILVERBLUE mechanicalbody. FEET ARE MECHANICAL LIONHEADS: retainlioneyes/nose/muzzle/darkopenjaws/metalteeth originalsource, notgenericplainboots. Actualclosedgreyfingerfists distinctfromlionfeet. Baseleftred/rightgreenarmsout. Topmiddlegreenarmraised/kneesangled butsourcepartialrightedgepreserved, toprightHORIZONTALspeedtrailsbeforehead/chest,nometalblades. Middleleftcrouchsmallface/actualarmdirection, midcentregreenfistforward, midrightgreenfistnearshoulder. Bottommiddle ONLYsmallclippedbluegrey fragments andEMPTYgaps; don'tcompletebody. Othersoriginalproperfeet/arms/joints. Image4correctedfirstsheetisownunitdesignonly. Preserveactualheadoneface, no doubledfaces or teethonhumanoidmask, Lionfootteethvalid. 실제4xBRZ primary + unfiltered원본 + Deathscythe style-only + 자기첫판 design-only.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_404/robot_set/SHEETS/sheet_02/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_404/robot_set/SHEETS/sheet_02/HANDOFF.md)


## 사용자 반려11/16: 이 판 설치 금지
exec-18c8515b-7051-4fb8-ae3a-1560be73105d.png가 많이 잘못 그려졌다고 사용자가 지적했습니다. 팔·다리·손과 전면에 겹친 부분을 프롬프트에서 날/포신 등으로 추정한 것이 원본 구조를 바꾼 가능성이 있습니다. 후보를 user_rejected_structure로 보존했습니다. 같은 실패 그림을 새 설계참조로 전파하지 않습니다. 개별 원본 자세와4xBRZ를 다시 직접 대조하여 재작화합니다. 이 문서 이전의 생산자 확인 문구는 합격을 뜻하지 않습니다.


## User rejection: unit403 sheet02 alternate repair
Part03 top-right pose14 chest/abdomen and top-left gold base24 rejected. Entire three alternate outputs remain producer HOLD, do not install or reuse as design references. User reports excessive malformed chest structure. Redraw correction pending using actual native and 4xBRZ, no palette donor. Claude: verify original chest/forearm topology, limb identity, gold base head/chest contours; repeated base occurs in all three alternate plates.

### Claude에게 원본 구조 확인 요청 — unit403 pose24/14
금색 pose24의 head/chest/arm 형태를 imagegen이 반복적으로 오해해 사용자 추가 반려. source native 자체도 작은 겹침이 많아 단정 금지. 실제 전투 프레임과 대조해 gold base가 적절한 공통기본자세인지, chest의 실제 윤곽과 손/팔의 겹침 순서를 표시한 참조 부탁드립니다. pose14도 chest와 중앙 손/팔 경계 표시 요청. 새 correction RAW는 generated_chest_gold_correction.png이며 아직 producer HOLD, 기존 반려와 비슷한 gold 구조가 남아 완료로 인정하지 않음. 이번 새 요청을 위해 다른 로봇 작업은 계속함.

### 11/16 incoming8 최신 수신
Claude 19:50에 남은 공식519장 actual4xBRZ 생성해 참조총547장 준비. 앞으로 있는 참조는 그대로 재사용. 팔레트 변형은 runtime 원본표시로 확정되어 별도생성하지 않음. 다만 이번 unit403 gold pose24는 공식layout 공통base로 들어있고 사용자 직접형태수정요청이 있어 source별 fresh시험만 진행. 일반 정상팔레트로 재색칠하지 않음. Claude: gold24를 공통base로 계속 둘지 검토 요청. 트로와는 기존 user_report 아트 설치완료 확인; 새cutin_redraw 아트는 중복후보이므로 자동대체불필요.

Gold24 fresh source-only trial also HOLD: smoother but knee-cone hardware and original proportions/details lost. RAW pose_24/gold_fresh_redraw.png not installable. Specific annotation request at pose_24/HANDOFF_GOLD_USER_REJECTION.md; original weapon1585 obj056 pose286 frames1078..1140. Do not reuse this generic-looking redesign.

unit404 sheet03 candidate_sheet.png delivered RAW, 3.544px/native. Official9slot layout. Source middle-left/middle-centre partial pieces preserved; speedtrails and arm/foot identities formal QA at per-sheet HANDOFF.

## 병행 전달 갱신 (11/16, 각 폴더 HANDOFF 우선)
- 124~149 담당: 132 전3판,133 전3판,13601,13701 신규 후보. 13203 원본없는 흰잔상 draft 보존 후 단일수정. 134→129,135→130은 전체원본/순서/layout 동일 증거 기록에 한해 공유, 재색칠 없음.
- 215~299 담당: 224 sheet01 ALT4 plate03/04, sheet02/03, sheet04 ALT4 plate01; 22501/02 전달. 224 거대한 흰효과 plate01은 구멍메움 문제 HOLD, plate02 아직 미작화. 22502 첫 채색오류 draft 보존하고 재작화 원본색 복구.
- 380~399 및430~472 담당: 380 alternate 9후보 + 마지막04alt01 RAW HOLD(원본 상하분리된 틈을 잇는 오류). 공식저해상도9판은 HOLD. 381,382,383,384,385,38601~03 신규 후보; 눈/손발귀속/원본부분상태/잔상/실루엣·알파 검토는 각HANDOFF. 38603 좌하 원본머리소실 유지, maxalpha254 및 투명RGB는 Claude 확인대상.
- 전부 producer 기본확인과 배율통과를 뜻하며 Claude 눈검수/정합/설치 완료를 뜻하지 않음. 사용자 반려403은 별도HOLD가 우선.

unit404 sheet04/05 RAW candidates delivered with source+actual4xBRZ+mandatoryDeathstyle+correctedownsheet01 refs. Unit404 all5sheets now candidates (NOT Claude QA done). sheet04 top-right lionfoot raised, bottom-left dark state+trails; sheet05 fourposes/remaining blank. See per-sheet HANDOFF for arm/foot and face boundaries.

unit405 sheet02/ALT4/part02 fourpose RAW candidate delivered, 4.996px/native. Separatealternate layout only. Purple monster/teeth/mouth source preserved, Claude facial contour/limb/buckle/crown and alignment QA pending. part01/03 and officialsheet03 still pending.

## 사용자 요청 재작화 실제 전달 — unit403 gold24 / chest14
pose_24/candidate_structure_redraw.png NEW RAW: 원본의 긴 둥근가슴밝은면·양쪽무릎콘 복원. pose_14/candidate_structure_redraw.png NEW RAW: 추정한 맞잡은주먹덩어리 삭제, 긴왼쪽은색면/짧은오른쪽면/중앙검정틈 복원. 각source_structure_redraw_request.json actualrefSHA, review JSON, HANDOFF_STRUCTURE_REDRAW.md 참조. 예전 gold_fresh_redraw.png와 part03 generated는 여전히 반려. 새단독아트 원본정합/분할은 Claude, corrected candidate=검수완료 아님. 나머지 유사 pose11/15도 계속 재작화.

unit405 sheet02 ALT4 part01/03 delivered RAW candidates; all3alternateparts now complete(unreviewed). Part01 oval-piece transparent holes/greyspikes and huge pink leftfan stepped crop; part03 righttriangle hardcuts+blankcell need exact source QA. All references/filter/layout SHA per folder. Official9slot layout forbidden forALT4.

사용자 재지적: literal source_structure_redraw 시안도 whole-body연결/기체정체성부족. 이전2단독corrected_candidate는 사용자추가반려로 읽고 자동설치 금지. 다음시도 identity_structure_redraw: target원본+4xBRZ에 같은기체 원본다른각도18/02를 구조참조로 추가(색/자세donor아님,재색칠금지), Deathstyle. 가슴밝은면/어두운틈 단순추적을 넘어실제관절연결 맞춤. 옛단독들을 이용한조합cell50도 같은오류 전파우려로 그대로설치금지.

## 사용자 승인 확정: unit403 gold pose24
사용자 굳 = exec-b929a731-cef7-4ccb-9f56-34327b12aa5b.png. pose_24/candidate_identity_structure.png RAW 즉시전달. USER_APPROVED_ART.json 정확SHA/범위. 이 그림은 target원본+4xBRZ+동일기체원본다른각도18/02 구조참조+Deathstyle로 새로 그려 얼굴/가슴/팔/무릎 연결을해결한 것. 이전 literal candidate_structure_redraw.png, gold_fresh_redraw.png와혼동금지. 승인범위는 이금색아트만, 다른포즈/정합/설치승인아님. Claude 공식base교체/분할/게임검증 요청.

unit403 pose14/candidate_identity_structure.png RAW新候補(未ユーザー承認/Claude未検収)。同機原画18/02の構造参照で小マスクと胸/腕接続を改善。旧literal候補を代替候補として扱うが元絵正式整合はClaude。goldユーザー承認はこのblue14には適用しない。

unit405 sheet03 candidate_sheet.png RAW delivered 2.991px/native; fourelements/largeleftpinkfan/twolefttendrils/raisedfoot source preserved, ClaudeQA exactcrops/alpha/monsterface/limbs. unit405 now official01 + sheet02 threeALT4 + official03 candidates delivered, no installclaim.

unit403 pose11/15 candidate_identity_structure.png RAW新候補追加。同機原画18+承認gold構造+Deathstyle、target独立原色で再描画。旧source_structure_redraw.pngより頭/胸/腕の連結明確化。goldの承認はblueには適用しない。現行公式9シート02も承認goldを参照して全体描き直し生成中。
