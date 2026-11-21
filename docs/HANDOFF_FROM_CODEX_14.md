# Codex → Claude 핸드오프 14

현재 입력은 **HANDOFF_TO_CODEX_5.md**입니다. 최신 상태는 이 파일을 읽어 주세요. 13번은 이전 회차 기록입니다. 이 파일도 20KB/300행에 도달하면 15번으로 이동합니다.

## 긴급: 미사일 95420 패킷 번호 불일치로 철회

- **`missile95420_broad_shared_v2`는설치금지**. 외부bindings[95419,95420]와계약원본해시가불일치했습니다. 원본 hash1671582883은실제ID95420(배열95419), hash4013075440은ID95421(배열95420)입니다. 패킷작성자가배열인덱스를표시ID로쓴오류입니다.
- `ready_candidates`에서제거하고`withdrawn_candidates`로옮겼습니다. root확인시기존패킷의설치이력은없었습니다. 기존PNG/contract/SHA는변경하지않았습니다.
- **ID수정본인계**: `test_current/parts/missile95420_broad_shared_v2_corrected_ids/candidate_packet.json`,목표95420/95421. root도각계약의hash/index/raw/full16 및현재`bindings[ID-1]`/prior spec를대조해일치확인후큐에추가했습니다. 그림RGBA/SHA는그대로인메타수정이므로새그림으로세지않습니다. 옛패킷은계속설치금지,공식그림판정은Claude대기입니다.
- 모든표시ID는 **1-based, 실제배열 `bindings[ID-1]`**입니다. 임시`binding_id`필드나0-based인덱스로바꾸지마세요. 번호만아니라해시/index/raw/full16도일치시켜야합니다.

## 생성 한도 — 지금 가능한 작업과 대기 구분

- 2026-11-14 이미지 생성에서 `429 usage_limit_reached` 발생. 도구가 준 reset epoch1794650074는 **한국시간 18:54:34**입니다. 추가 이미지 호출·CLI/API 우회는 하지 않습니다.
- 이미 생성된 그림의 기계적 패킹/좌표등록·후보인계와 원본/팔레트/공유관계 준비는 계속합니다. 생성되지 않은rank10/11/12/14는그림완료로세지않습니다.
- 최신등록후보: `root22163_edge_registration/candidate_packet.json`(95429/95430 끝점), `root_remaining_94793/candidate_packet.json`(17자체재질/42입자). 둘다공식판정대기입니다. 아래해당항목참고.
- 19818은큰돌2개를남긴이전후보거부유지. 정확한부모는 **표시ID92856 = bindings[92855], source/atlas[160,64,32,32]**입니다. 큰돌92857[160,80,16,16]·92862[176,80,16,16]도같은부모안입니다. 이전후보가상반부만고쳐이큰돌두개를남겼습니다.
- `repair19818_whole_source_ready`의초기두master지적은작업자의표시ID/배열인덱스혼동으로철회됐습니다. 잘못된설명을현재 문서에서삭제했습니다. canonical정정파일은 **corrected_contract.json**입니다. two_master_contract.json는실제계약이아닌superseded포인터로바꿨습니다. 부모92856/원래7개및표시ID·배열index·hash·source/atlas를분리했습니다. 원본스냅샷은새그림이아닙니다.
- 최신생산배정/완료후보/생성대기구분은`docs/ART_PRODUCTION_WORK_STATUS.json`에도기록했습니다. 첫9묶음98계약은후보가있는범위이며98개게임합격완료라는뜻이아닙니다.

## 역할·현재 진행

- 사용자 지시대로 Codex는 새 그림과 원본·팔레트·공유 좌표 계약을 제작합니다. **연결·굽기·공식 검사·실제 재생 검증·런타임/폰트는 Claude 담당**입니다. Codex가 중앙 라이브러리·DB·코어·설치 manifest·EXE를 수정하지 않았습니다.
- 후보 목록은 `docs/PENDING_ART_INSTALL_QUEUE.json`, 실제 설치/거부는 `docs/ART_INSTALL_DONE.json`이 기준입니다. 제출 이력 전체를 미완료 수나 게임 반영 완료 수로 세지 않습니다.
- 화면 강제 끄기·컴퓨터 종료·사용자가 테스트 중인 창 조작을 하지 않습니다. EXE/배포팩/푸시는 지금 역할에 포함하지 않습니다.
- 최신 ROM 미연결 수는 Claude5 기준 **10,214종**. 작은64texel미만 제외 작업 범위는 **919묶음 / 590IMG / 6158파츠**입니다. 이번 후보를 연결·재검사하기 전 이 수치에서 임의로 빼지 않습니다.
- 최근 Claude측정은15:14의3486개, 격리는15:15의11개입니다. 최신불합격합계는현재입력에서별도기재되지않았으므로이전178개를현재합계로반복하지않습니다. 그림을다시제출해도합격으로바꾸지않습니다.

## Claude 설치 판정 인수 — 15:04까지

- 새누락 rank1 IMG21948/bank0 17개·rank2 IMG22163/bank0 9개 설치·판정통과를 인수했습니다. 원본색/위치가맞는그림이라는판정이며이문서에서무장전체실제재생완료로확장하지않습니다.
- 미사일 기본41개 후보도 설치됐고 본체1개는형태경고가남았습니다. 어두운12개중 #95420 사선폭124→82 불합격은next_key가재작업합니다.
- 원래8기체부품(발호크4/토라스4), 기존교정93582/94993·94994/21071/19999/21427/94582/92815/92400/93782/93417/95043/94103/94231의설치·판정통과를인수했습니다.
- **19818 청회색 후보 거부**: 위작은범위만고쳐큰돌92857/92862의보라색이남았고92853/92861도격자처럼보입니다. 부모전체원본영역의큰돌까지재제작해야하며지난후보를합격으로바꾸지않습니다.
- **시작메뉴24개는 설치 후 비활성화**됐습니다. 아래화면OBJ의15·15레지스터혼합이전달되지않아불투명해지는runtime문제는Claude담당입니다. PUSH START도해결전설치보류. 새메뉴그림으로이문제를덮지않습니다.
- rank4 IMG21785/bank0중 #95409 사선폭69→40 불합격은next_shape가재작업합니다. 다른5개불변.
- rank5 IMG22163/bank1중 #95429 곡선/95430 사선이각각226→170,146→107로가늘어새생성폭교정후보를인계했습니다: `test_current/parts/root22163_bank1_width_fix/candidate_packet.json`. 정상9계약및두ROI밖RGBA0픽셀변경. 제작용누적alpha면적은214.8/162.5 native-equivalent였으나Claude의texel소실검사와다른값이므로합격판정이아닙니다. 원본226/146과의실제형태·폭·끝점은다시봐주세요.
- #95409도 `borrowed_shape_rework/repair95409_white_diagonal_v2/queue_entry.json`으로새폭교정인계했습니다. 다른5개불변,제작표본69/73은공식검증이아닙니다.
- #95429/95430 끝점재교정: `test_current/parts/root22163_edge_registration/candidate_packet.json`. 새생성아닌기존자체RGBA의기계적대각등록/clip후보입니다. 현재live입력과같음을확인한뒤작업,정상9계약/ROI밖0픽셀변경. 제작반alpha bbox는둘다[0,0,32,32],면적249/168이나공식texel/베이크검사와다릅니다. 원본alpha전사/팽창없음. 곡률·줄폭·칸간이어짐이원본과맞는지Claude판정후부적절하면거부해주세요.
- 전체화면5개(로고·별·지구·프롤로그2)는아직일반파츠설치밖의배경연결대기입니다.

## 사용자 제보: HP 라벨·게이지 및 유색 글자

최신 사용자 화면의 **보조 디스플레이 노란HP 라벨과 초록/빨강 게이지가 도트로 남습니다. 체력 숫자는 HD로 보입니다.** `docs/USER_VISUAL_REPORTS_CURRENT.md`9항에 원본 스크린샷 경로를 기록했습니다.

- HP값·비율을 정적 그림에 굽지 말고, 게이지 트랙/채움/테두리/감소 애니메이션을 동적 HUD 공통 경로로 처리해 주세요. 적/아군·정상/저체력·상단/보조 화면 모두 확인 대상입니다.
- 같은 문서6~8항: 중앙 `攻·防·反`, 결과창 초록 이름/경험치/레벨 숫자, 정신 메뉴 청록 `신뢰`가 원본으로 남습니다. 원래 색을 유지한 공통 폰트 처리를 부탁합니다.
- 위는 런타임/폰트 인계이며 Codex가 해결 또는 실제 반영 완료했다고 보고하지 않았습니다.
- 읽기 전용 코드 추적: `emulator/hd_fonts.py:218`에서 `hud_labels`를 찾지만, 222행의 `if hp and en and en[0]-hp[0]==128 and hp[1]==en[1]` 안에서만 229행 `hud+=hud_labels`를 실행합니다. 제보의 보조 화면은 HP두 개만 있고EN이없어 이 조건으로 라벨이 누락될 가능성이 있습니다. **실제 인식 결과를 재현 측정한 결론은 아니며 코드상 원인 후보**입니다. 글자 라벨 채택을 상단 HP/EN 숫자 배치조건과 분리하고, 별도 동적 게이지 경로를 확인해 주세요. Codex는 파일을 읽기만 했습니다.
- HP 원본 인계완료: `test_current/ui/subscreen_hp_hud_source/HANDOFF_SUBSCREEN_HP_HUD_SOURCE.md`. 물리보조engine1 BG0가라벨/숫자/바, BG1이판프레임. IMG4651/PLT4650, HP원본타일[160,8,24,8]중실제글자14×6. 노란HP실제bbox는왼쪽[53,98,14,6]/오른쪽[133,98,14,6],바[53,104,70,5]/[133,104,70,5]. 순수원본안정2시점적1308→0/아군5000으로동적bar확인(제보239와다름명시). 중간1060 MMU/native시점차는최종계약제외.
- 기존`battle_hud_glyphs.npz`라벨테이블은16×16(HP/EN각1개)입니다. 보조화면의14×6라벨이동일패턴으로인식되는지부터확인해야하므로 **HP+EN조건만고치면충분하다고단정하지않습니다.** 작은HP패턴/하단BG경로/동적채움타일을함께연결해 주세요. source패킷은원본자료이며HD수정완료아닙니다.

## 제작 패킷 위치 — 현재 설치 상태는 위 판정 인수 참고

### 타이틀·시작 메뉴·프롤로그

- 로고: `test_current/parts/title_logo_hd/candidate_packet.json`. ROM IMG38/PLT36/PAT39 전체 master. **일반 파츠 설치기 대상 아님**. 실제 레이어/스크롤/글자 정확도 확인 필요.
- 타이틀 별·지구: `test_current/parts/title_earth_hd/ready_screen_candidates.json`. IMG11/SCR20 별·IMG12/SCR21 지구, PLT0. 실제 타일512종 전부 일치. 각각960×480crop 및960×1920fullmap 패딩. 두 레이어의 독립 스크롤 유지. BG0 녹색 placeholder를 로고로 등록하지 마세요. 폴더의 PLT45 탐색본은 잘못된 초기 후보라 사용 금지.
- 프롤로그: `test_current/parts/prologue_space_hd/ready_background_candidate.json`. IMG41/SCR43·IMG42/SCR44/PLT40, 새960×720 두 장. 별도 한국어 본문을 배경에 굽지 않았습니다.
- 위 전체 화면 그림은 큐의 `ready_screen_candidates`입니다. 레이어 페이드/투명/가림/실제 연결은 Claude 확인 대상입니다.
- 시작 메뉴: `test_current/ui/start_menu_hd_candidate/queue_entry.json`. actual24새조회키/9그림재료. NEW GAME/LOAD/CONTINUE, 선택/비선택. engine0 OBJ/원래15·15블렌드 보존 필요.
- PUSH START: `test_current/ui/push_start_hd_candidate/queue_entry.json`. actual4새조회키/단어master1. 프레임4키는 메뉴24키와 중복이므로 새 키로 더하지 않았습니다.

### 사용자 제보 기체

- 발호크 발901/2364: `test_current/ui/valhawk_feet901_2364_candidate/queue_entry.json`. 실제 앞발/뒤발목 별개 조각을 같은 시트에서 그렸습니다. 두 raw가 다른 숨긴 장갑이어서 한 완성발을 단순 역투영하지 않았습니다.
- 발호크 총4481/4482: `test_current/ui/valhawk_rifle4481_4482_candidate/queue_entry.json`. actual 검정/회색/분홍64×16 연속master. 기존 흰/파랑 그림의 재색칠로 메우지 않았습니다.
- 토라스4985/4988/4996/4997: `test_current/parts/taurus_joint_master_art4/ready_candidate.json`. actual unit8/IMG1219/PLT1220. 기존그림crop만으로머리·등수평선재현. 새56×48자세master에서4부품을잘라연결했습니다. 다른10개/기존중앙PNG 보존. 제작 OAM 조립 미리보기에서 선은 없어졌지만 실제HD재생 판정은 아닙니다.
- 위8개는 초기5263 범위의 **사용자 직접 제보에 따른 별도 교정 후보**입니다. 원래 라이브 그림·메타데이터는 수정하지 않았습니다.
- 미히로full컷인: 새 그림0. 기존 `graphics/pilot_cutins/cutin_24924_hd.png`, IMG24924/PLT24923/MAP24925/cutin65가 존재합니다. `test_current/parts/mihiro_full_cutin_source/HANDOFF_PRODUCTION.md`에서 실제 연결을 추적해 주세요.

### 미사일·흰 궤적·연기

actual unit172/weapon737, IMG20224/20225. 아래4개는 **총41개 계약의 새 그림 후보**이지41장·41개 설치 완료가 아닙니다.

- `test_current/parts/missile20224_smoke_six/candidate_packet.json`:6계약.
- `test_current/parts/missile20225_body_eleven/candidate_packet.json`:11계약.
- `test_current/parts/missile20224_trails_first_four/candidate_packet.json`:11계약.
- `test_current/parts/missile20224_remaining_thirteen/candidate_packet.json`:13계약. 넓은 분사면은 추가 재생성 원천SHA 포함.
- 기본42 중 나머지1은93738의 기존 부모 포함 관계로 연결 확인 대상입니다.
- 어두운12단계도 새후보2묶음 인계: `missile20224_dark_phase0_six/candidate_packet.json` / `missile20224_dark_phase1_six/candidate_packet.json`. 각각6계약, 실제 두 팔레트로 독립 생성. 최초채집54범위는 **새후보53계약+기존부모포함관계검토1**입니다. 설치·실제QA완료가아닙니다. `native_weapon_source_172_737/palette_phase_aliases_pending.json`:기본과raw/크기같은것2개,나머지10개는별도raw. 전부 단순 밝기 변형으로 닫지 않았습니다.
- `native_unmodified_*.png`는HD-off 원본 문맥. `cached_*.json`은 실제 raw/fullpal 입력. 기존 `native_*.png`는HD숨김이 섞일 수 있어 순수 원본 문맥으로 쓰지 않습니다.
- 후반새그림5계약도큐인계: `missile20224_later_basic_four/candidate_packet.json` 및 `missile20224_later_dark_trace_one/candidate_packet.json`.5계약/4구성,선행53과별도. 기존master공유5는`native_weapon_source_172_737/later_source/own_master_relationships_five.json`의정확원본관계로연결검토하며새그림으로세지않습니다.
- 후반450~960의실제158계약source대조: exact61+indexed82+기존생성master공유5+93738관계1+후반새후보5+64미만원본유지4=158. `later_source/source_scope_reconciliation.json`. **이원본계약범위에서64이상미해결0이라는뜻이지무장전체HD합격/실제재생완료가아닙니다.** 95420격리도그대로별도입니다.
- `missile95420_broad_shared_v2`는번호불일치로철회,`missile95420_broad_shared_v2_corrected_ids`의95420/95421메타수정본을인계했습니다. 위긴급항목참고.

### 전체 누락 목록 신규

- rank1 IMG21948/bank0: `test_current/parts/missing_packets/img21948/queue_entry_bank0.json`,17새조회키/768×256. actual11·ROM보충6 유지.
- rank2 IMG22163/bank0: `test_current/parts/missing_packets/img22163/queue_entry_bank0.json`,9새조회키/768×256. actual9. 현재활성키0을확인하고제작. 왼쪽미대상흰원은후보alpha0.
- rank4 IMG21785/bank0/6종도 후보완료·큐등록: `test_current/parts/missing_packets/img21785/queue_entry_bank0.json`. actual4·ROM보충2. 담당자는 rank6 IMG21657/bank0/13종을 다음제작중입니다.
- rank6 IMG21657/bank0/13종과rank7 bank1/11종도후보완료·큐등록. 같은폴더각queue_entry_bank0/1.json. 실제팔레트별독립생성,13/13·11/11실제관측. 처음짙은테두리출력제외. source/hash/SHA확인만이며공식HD판정아님.
- rank3 IMG19645/bank0/22조회키도 후보완료·큐등록: `test_current/parts/missing_packets/img19645/queue_entry_bank0.json`. actual4·ROM보충18. 이전3개빔과다른미연결키만제작했습니다. 담당자는 rank8 IMG19645/bank1/7종으로진행중입니다.
- rank8 IMG19645/bank1/7종도후보완료·큐등록(actual2/ROM보충5). rank9 IMG21785/bank1/2종도후보완료·큐등록(actual2). 실제색으로각각독립생성했습니다.
- **생성대기**: rank10 IMG21948/bank1/12키(`SOURCE_ONLY_bank1.json`), rank11 IMG21071/bank0/29키(실관측1·ROM보충28, `new_missing21071_bank0_production/HANDOFF_IMG21071_SOURCE_WAITING.md`), rank12/14 IMG22419/bank0·1/7키(전부ROM보충, `generation_waiting_source.json`). 각native/contract불변, 후보PNG없음/생성0/설치큐없음.
- rank5 IMG22163/bank1/11계약 새후보도 인계했습니다: `test_current/parts/missing_packets/img22163/queue_entry_bank1.json`. live RGB/indexed 활성0, actual7·ROM보충4. bank0재색칠없이실제4색노랑8구성새생성. 가운데64×64는32×32애니메이션4조각으로분리. 원호/섬광미세가시·선폭·clip·페이드Claude판정대기.
- 위 rank5의 현재 그림은 **candidate_bank1_clipped.png**, SHA `8a5d9151606750c4273a65598273fa11cb063b153a88630d5a6e814d46204e65`입니다. 최초 candidate_bank1.png는잘린직선끝의생성투명여백을피하려고철회했습니다. old PNG/SHA와queue_entry_bank1_before_clip.json은보존, 큐의superseded_candidates로이동했습니다. default queue_entry_bank1.json은새그림을가리킵니다.

### 불합격 재작업

- 93417: `test_current/parts/root_unit373_step_repair/candidate_packet.json`. 지난 root 후보의2배폭 오독을 정정. 원본35texel/1texel선/중앙단차. actual flip_x 방향/알파/이음매 확인 필요.
- 95043: `test_current/parts/root_effect394_particles_thick/candidate_packet.json`.13개 사선폭 새 교정. 정상95039 제외. 짧은획 타원화·접촉·폭은 판정 대기.
- 19818: `test_current/parts/repair19818_slate_repaint/candidate_packet.json`.92853/92854/92855/92856/92857/92861/92862. 이전 보라 후보 거부를 반영해 청회색5재료로 재제작. 지정scope밖0픽셀변경. 미세1texel은HD이득제한. 색·폭·공유접합 확인 필요.
- 94103: `test_current/parts/root_remaining_94103/candidate_packet.json`. 원본5개단색실루엣을 새 연속음영/곡선으로 제작. HD세부이득제한, actual 동적팔레트/lookup플래그 보존 필수.
- 94793: `test_current/parts/root_remaining_94793/candidate_packet.json`.42입자/17자체생성재질. 둥근버튼형첫생성제외,각진빛조각/연속색면선택. 원본위치·색방향·같은형태공유유지.1texel점HD이득제한,색면비율·면적·형태판정대기.
- 94231: `test_current/parts/root_remaining_94231/candidate_packet.json` 인계. 첫 출력의 연노랑 중심 누락을 수정 생성했습니다. 두 성분 간격/왼쪽clip/원천owner미확정·동적색모드 유지. 중심면적·폭·알파판정대기.
- 21427 rebase: `test_current/parts/repair21427_shared_master_rebase/ready_candidate.json`. 그림SHA는같아도contract는새값. `rebase_source_outside_proof.json`에현재source/실제RGBA/밖픽셀근거. 과거stale패킷대신이쪽사용.
- 그밖에93582/94993·94994/94582/92815/92400/93782/21071/19999공유영역 후보도 큐에 인계했습니다. 지난 시각 합격을 임의로 뒤집거나 다른 기체 재색칠로 메우지 않았습니다.

## 검증 시 구분

- 원본 채집·제작 조립 미리보기·SHA 확인은 최종 실제HD재생 검증이 아닙니다.
- 같은 master를 공유해도 원본 형태/색이 틀릴 수 있으니 그림 자체를 판정해 주세요.
- 각 패킷의4파일SHA와 시작 시 spec SHA를 확인해 주세요. 이후중앙spec이바뀌었다면무조건현재SHA로갈아끼우지말고source/raw/fullpal/밖픽셀을확인한별도rebase가필요합니다.
- 생성자체RGBA를 사각crop/resize해 배치했습니다. 원본RGB/alpha전사·문턱삭제·형태학으로검사만통과시키지않았습니다.


## 다음 기록: 15번
현재 상태와 새 제보는 HANDOFF_FROM_CODEX_15.md로 이동했습니다. 이후 15번을 읽어 주세요.
