# Codex → Claude 핸드오프 3

작업공간 `C:\Emul\Workshop\SRW_W_HD`. 이전 파일이20KB에 근접해 최신 상태를 이 파일로 옮겼습니다. 오래된 진행/예약 문구는 폐기했습니다. 앞으로 이 파일을 갱신합니다.
사용자 지시: 최대 병렬 작업, 작업 중·후 인계 기록, ROM/세이브 푸시 금지, 사용자 테스트 창 유지, 컴퓨터 종료 금지.

## 코어 소스 해제

- 해제 시각: 2026-11-13T20:58:54+09:00
- `HANDOFF_TO_CODEX_2.md`의 **런타임 결함 3건(21:10 갱신)**을 읽었습니다. Codex와 모든서브에이전트의공유코어소스수정/빌드는종료했습니다. 이후그림·라이브러리·굽기작업만계속합니다.
- **진단 DLL용 읽기API 변경은 기본 소스에 남깁니다.** 커밋 `046a9701`에포함했습니다. `srww_texture_cache.h`의cachedOBJ복사helper, `srww_hd.h`선언, `frontend/libretro/libretro.cpp`의`retro_srw_copy_cached_obj` export입니다. draw/가림/unknown수집/knownlookup조건은이API에서바꾸지않았고,호출하지않으면출력에영향없는읽기함수입니다.
- 기존효과가드변경도같은커밋에보존: srww_parts_impl.h/hd_core.py의effect_part명시분류. 이를기반으로Claude가2번윈도우마스크·3번단색수집조건을수정하고기본DLL을빌드하시면됩니다. **GPU.cpp,위헤더/exports,hd_core.py 모두Codex작업점유해제.**
- 당시기록: 효과가드전용DLL이었으나, 현재기본DLL은Claude d98c4226의a6d80b29로교체되어cachedOBJ API포함. EXE만이전번들입니다. 별도진단DLL은`test_current/parts/effect_22163/fill_completion/desmume_cached_obj_debug.dll`. 계약/사용법/기존대조자료는동폴더`HANDOFF_COMPLETE24_AND_API.md`.
- 22163중앙fill정확계약은같은폴더`complete24_contract.json`의뒤8개입니다. 2팔레트×4크기이며renderedcache로확보. 이전directVRAM계약은다음프레임메모리여서사용금지. 코드작업때일반단색UI가unknown으로넘치지않도록이계약을사용할수있습니다.
- Claude의컷인자기페이드수정 `95ba46f0` 인수. GPU경로수정완료라는상태로갱신하며동시앞효과/원본뒤배경이중혼합/소프트웨어표시미수정한계는Claude검증큐에남깁니다. Codex는추가검증을하지않습니다.

## 당시 병렬 작업 (종료된 기록; 현재는 _4.md)

1. **next_shape_art**: 합체공격+179에서 남은 마징카이저 한 자세의 실제 OAM/팔레트/원본 계약을 분리하고 한 벌 제작. 그레이트/진겟타 혼입 금지.
2. **next_key_art**: getter_cutin의 IMG21869/PAT21870 별빛·수직섬광12사각형 한 벌. 처음 후보10개가 가늘어 형태/빈영역 검사에 걸려 폐기, 원본 선폭으로 재제작 중.
3. **effect_live_palette**: 22163 중앙 단색fill4개의 정확한 rendered 계약 확보. 현재 VRAM은 다음 게임상태여서 임시 directVRAM 계약은 폐기. 읽기 전용 cachedOBJ API를 별도진단DLL에 추가·검증 중(아래).
4. **root**: 라이브 설치·대상만 굽기·커밋·검증대기열 인계. 독립 검증은사용자지시로Claude전담. 다른agent는 라이브 그림/라이브러리/DB를 쓰지 않습니다. 공유코드 변경은 예약한 agent만.

## 검증된 설치 묶음

모든 그림은 실제 팔레트/해시로 연결. 다른 기체·다른 색변형 그림 재색칠로 빈곳을 메우지 않았습니다. 원본 RGB/알파를 덧찍지 않았습니다. prefix5263 불변.

|묶음|binding/atlas|연결·굽기·실재생과 한계|
|---|---|---|
|파워드레드99/415|91747–91755, powered_red_pose_reviewed|9개한벌, 굽기오류0, 팔레트/키0,90프레임vanish/loading/held0. 초록가로선은HDdisabled원본에도있어새그림원인아님. 폭발등장면전체미완료|
|22378효과2팔레트|91756–91771, reviewed_effect_22378_bank0/1|16개모두실제HD등장,오류0,wrong_colour최대.0038,키0. unit413weapon1610frame1320/180프레임vanish/loading0. 다른파츠held49남음|
|데스사이즈7108|64213/64207/64200, deathscythe_7108_continuous|[-32,-1]offscreen날개포함한벌. lostopaque0,녹색눈교정,3개재굽기0. 실제300프레임전부HD/vanish/loading0. 팔·봉·날개연결/기체뒤·캐릭터앞·UI맨앞확인. 64207명암영역경고는남음|
|그레이트첫자세17|great_mazinger_observed_pose|실제unit297weapon1213frame300+3의17개. oldindexed11proxy보존.7340/7353색영역교정후재굽기0. 분리조립draw17/누락0,120재생vanish/loading/held0.7340은아래후속새그림으로갱신.82798/91777명암경고남음|
|코다르c전신2|91684/91685|실제회색/회녹색장갑+작은빨강센서로다시그림. 형광초록/자홍잔여해소,IoU.958/.883,재굽기0|
|코다르c중앙14|codarl_central_observed_pose|91686/91688/91689/91111/91682/91114/91232/91690 +91789/91790/91792/91793/91794/91796. 실제14개전부HD,180프레임vanish/loading0. 양쪽분신은별도원본남아HD.757/held32/전체INCOMPLETE|
|민트에너지38|91797–91834, observed_energy_mint|실제흰/민트/비취그림. 11개흰핵밝기오류재제작·재굽기0. 공식quality/palette/key0. 3fixture×180에서2371등장/2222HD/149미준비원본,준비후held0/vanish/loading0. 순수원본15쌍중6검토,긴흰핵/작은흰핵·UI가림정상. 큰burst/원형/BG는미완료|
|진겟타1 19고유그림|7255–7273, getter1_observed_pose|20OAM중7264동일그림2회. 머리7255/6/7을연속재제작v4로교정,뿔·녹색홈·목접합정상. 3개공식경고0,다른16개픽셀보존. 2상태×300프레임전부HD/vanish/loading0. getter_cutin.state의캐릭터페이드차이별도발견(아래),전체장면완료아님|
|19645관측7|91854–91860, observed_effect_19645_seven|실제RGB7개각팔레트새그림,static/effect. 506/506HD,held/vanish/loading0. +46색/위치확인. +28/+32윈도우플래시무시로전체장면정상아님|
|22163관측16|91861–91876, observed_effect_22163_sixteen|실제2팔레트각연속한벌후분할,static/effect. 2708/2708HD,준비후held0/vanish/loading0. 중앙원본flatfill4개사각이음매발견해다음작업. 전체효과정상아님|
|그레이트후속18|great_mazinger_running179_pose|새91877–91881/91886–91893,기존82809/7352/7346/7351/7340. indexed4proxy보존. 얼굴13/헬멧14눈중복해소,기존좋은14보존. tiny연결편15는IoU.6818거부후새그림.905로교정(기준낮추지않음).18개굽기0. 실제300프레임전부HD/vanish/loading0/held2.179/190/220눈·목·손·뿔연결확인.7340은222회중218HD이나+3은컷인가림으로시각확인불가. 마징카이저는별도미완료|

처음진겟타오프라인조립의거대한가로선은OAM오름차순오류였습니다. priority/OAM역순으로교정. 런타임compose는원래reverse=True여서공유레이어수정불필요. 지원영역7.6%손실역투영실험은폐기.
source/provenance는각graphics/rework_*와test_current/parts의개별HANDOFF에보존. 원천주소가확정되지않은관측효과는resource=None·actualRGB로제한(19600/19645/22163이미지번호는모양/bytes대조와원천주소추적을구분).

## 최신 공식 검사와 캐시

- `scripts/verify/verify_art_batches.py`로설치report들과명시binding을선택. `test_current/parts/combined_repair/latest/summary.json`.
- 최신선택133개: **baked키누락0,팔레트규칙위반0,검사오류0,quality colour경고3**(64207/82798/91777). 기타flags0. 이것은전체ROM/전체장면검사가아님.
- 초기새검사에서sync renderer.baked가빈것을누락으로오판한결과는폐기. 최종은disk_cache의실제texture_key존재직접대조.
- native_materials/material_slots는라이브러리변경후재생성. 현재133검사후재생성완료(library91893개, SHA256 bc1913168fc8332a52d7ef133d662eec0b6641a035f5fa89166ef812a0228f08). 캐시메타데이터library_sha256과실제library를대조해야함.
- 직전전체키색검사87289/초록508/자홍568은마지막여러교정전수치라최종수치로쓰지않음.
- 전체누락295주장은폐기(TIM215/PLT40/PAT31/IMG9). 롬전체11,358종누락/다중IMG21%판정불가는아직대부분남음. 설치수와고유누락감소를동일시하지않음.

## 효과용 기체 폴백 수정 — 기본DLL 반영됨

기본10%팔레트슬롯기체가드가효과20개까지계속원본으로보류하던원인확인. 알려진effect_part만집계/강제기체폴백에서제외,미준비native폴백/기체보호/레이어/재색칠유지.

- 변경: hd_core.py +코어srww_parts_impl.h/srww_hd.h/libretro.cpp. `retro_srw_register_effect_parts`,명시태그및유효source_binding별칭상속.
- 검증코어SHA256 `b1e8c2134fc71181863e63e1015f9305dd5aadbb04d1b81aea72c0bcf71be27c`,기본DLL과build/frozen_update번들에같은SHA반영.
- 동일DLL·고정baked-ready91843로162상태×90프레임A/B: 효과판정1095개변경,태그없는기체판정차0,ID/OBJ속성동일. `effect_guard_review/unit_sweep/unit_decision_comparison.json`. 162장면화질전체검증아님.
- 실제unready효과1249회에서원본잘못숨김0. 기체가드전역0으로완화안함.
- 준비후민트38held0,19645관측7held0,22163관측16held0확인.

## 공통 런타임 결함 — Claude 진행 상태

`docs/REVIEW_CUTIN_FADE_FLASH.md`에4상태실측과최소수정위치정리. 그림알파/색으로숨기면안됨.

1. **겟타/고라이온 자기 컷인페이드**: Claude가95ba46f0에서GPU자기blend경로수정. SRWW_SELF_BLEND=0으로끄기. 동시앞BG효과·뒤배경이중혼합가능성과소프트웨어경로는남은한계. Codex가다시검증완료로표시하지않음.
2. **unit333전역플래시누락**: MASTER/BLDY는측정상0. 실제윈도우가BG1/2/3/OBJ를금지하는데HD가빈backdrop에다시그림. 코어의행별_didPassWindowTestNative/_enableColorEffectNative를모든HD draw에전달해야함. 레이어ID5일괄차단은HD외곽선을잘라금지. frame32윈도우끝레지스터복구도래스터시점과달라끝값만복사하면틀림.
3. **22163flatfill 검사누락**: colors>=3 unknown필터가단색중앙fill4개를목록에서빼고있음. native중앙색과HD주변차이가사각patch로보임. known등록은단색에도가능.

### 완료·소스 해제된 별도 진단용 읽기API

- effect_live_palette만srww_texture_cache.h/srww_hd.h/libretro.cpp에cachedOBJ복사API좁게추가. 이미rendered시점indices/palette/hash/w/h를저장한SRWWObjTextures를읽기만함. 현재VRAM/OAM은다음상태여서임시direct계약폐기.
- 별도 `effect_22163/fill_completion/desmume_cached_obj_debug.dll` 빌드완료·코어소스해제. 기본DLL/EXE에는아직미반영. 기존known8snapshot·invalid5·normal2상태240frame차0자료확보. 추가검증은Claude담당.
- draw/unknown필터/knownlookup/폴백조건은바꾸지않음. 그후정확한4fill그림계약확보.

## 코드·EXE·배포 상태

- `verify_runtime_path.py --pure-native`추가. 별도HD-disabled프로세스에서동일상태/offset재생. 예전native쪽은HDsuppression후framebuffer라순수원본아님을report.picture_left에명시. 90프레임63/65쌍실제검증완료. 새그림검사는순수원본사용.
- `capture_native_reference.py`추가. 진단출력은test_current안으로제한,verifier삭제대상도resolved runtime_path내검증.
- 설치기 genericobserved계약/--effect/--static-palette지원, `bake_parts.py --bindings`로대상만굽기. offscreen연속pose canvas_origin지원.
- 최신프로그램 `build/frozen_update/SRW_W_HD/SRW_W_HD.exe` 빌드·workspace지정자체검사통과:폰트2407,패드별도프로세스,코어,1920×1080합성,ready91843,컷인6. 이검사당시보다그림이추가됐음. 연결패드0이라물리진동검증아님.
- **dist배포팩은아직미갱신**. PNG→WebP가atlas내용해시/구운키를바꾸는위험미검증. workspace자체검사만으로배포완료주장안함. DB는현재약2.58GB로이전키잔여가능,배포전valid키별정리/크기검토필요(아직삭제안함).
- Git HEAD d98c4226. Codex코어/읽기API/인계첫커밋046a9701,Claude95ba46f0/d98c4226 인수. 그림·제작도구는별도선택커밋진행중,푸시는아직. 자동git add .금지. parts_baked.sqlite는미추적·LFS미지정이라큰파일무작정추가금지. 새그림LFS규칙정리도필요.
- Git credential helper는프로젝트밖D:경로라푸시전정리. 비밀정보출력금지.
- `verify_edge_palette.py`/`verify_palette_render_cache.py`기존실패는미해결. 정답그림을바꿔통과시키지않음.
- 실제진단렌더23~48fps측정에는검사·저장비용포함. 실제플레이어60fps달성으로보고하지않음.

## 다음 root 인수 순서

1. 현재3agent결과를인수하되실제계약/시각검토후만라이브설치.
2. 21869별빛12개,마징카이저한자세,22163중앙fill한벌완성후대상굽기/순수원본재생.
3. 공통컷인fade/window문제는위문서기준공유코드담당과분리조율. 임시그림보정으로감추지않음.
4. 최종캐시해시/그림키/실제EXE팩검증→ROM/세이브제외선택커밋·푸시. 전체HD완료라고보고하지않음.

## 구운DB 정리 후보 생성 예약
live DB175177행/약2.58GB로이전키잔여가있을수있어root가현재라이브러리키에해당하는BLOB만별도candidate.sqlite로복사해크기·키·무결성·샘플바이트를측정합니다. liveDB삭제/교체안함,재인코딩없음. 새그림agent는DB쓰지않고root도복사완료전추가설치안함. 실제유효그림개수와빠진그림개수로오해하지않을것.


## 구운DB 정리 후보 결과
`test_current/parts/baked_store_compaction/candidate.sqlite`와candidate.json. 현재키87348개전부보존,175177행중과거키87829개만제외. 2,581,123,072→1,283,616,768바이트(약50.3%감소),재인코딩없음,quick_check정상,64샘플BLOB·크기·stats원본동일. liveDB미교체/미삭제. 이정리는그림자체화질변경이나누락기체완료가아님. 후속그림추가후배포시최신키로다시생성·키존재검증필요.

## 별빛/세로섬광 관측2단계 설치 예약
21869전체12후보는미완료. 실제getter_cutin +234별빛10등장/+258~259세로광선4등장두종만완결단계후보. 공식128alpha IoU.636/.720와설치기BOX64 .818/.800을분리기록(기준변경X). root원본/후보시각검토후actualRGB/static/effect태그2개설치·대상굽기예정. nativeRGB/알파복사없음,별빛1.04배기하정렬만. 이후순수원본300재생검증.


## 사용자 담당 변경 — 최신 지시
이후Codex는그림제작·연결·굽기·커밋에집중하고,새공식audit/독립실재생검증은Claude가담당합니다. 진행중3agent에전달했고모두인수. 공유코드추가수정도중단(cachedOBJ기존3파일작업종료). `docs/CLAUDE_VERIFICATION_QUEUE.md`에제작중/반영완료/장면·프레임/알려진문제/코어·EXE상태를모아작업중과반영후갱신합니다. 이전Codex검사결과는이력참고이며새그림에검증완료를승계하지않음.

## 제작 반영 진행(Claude검증대기)
마징카이저22OAM/20고유RGB 최종그림과22163기존16+신규fill8=24개기본후보를연결·대상굽기합니다. 22163 retry는선택비교파일로만보존,동시라이브설치안함. 새그림검증은Claude전담이며Codex는실제입력hash/팔레트/크기·중복및굽기오류만확인. core작업추가없음. 컷인페이드95ba46f0·윈도우/단색d98c4226와새기본DLL인수,새그림검증명령은그코어기준으로큐갱신예정.


## Claude21:25런타임수정 인수 / 제작반영
Claude가95ba46f0/d98c4226으로자기페이드·윈도우·flat수집옵션을처리하고기본DLL a6d80b29119f7c18447725acc4e0e5c8fb88cdda07d8cef6ccb106e936b64fe0로교체했음을인수. cachedOBJ읽기API도기본포함. Codex는코어추가수정없음. build/frozen_update번들은별도재묶기필요. 신규135+도끼1+마징카이저20+fill8(겹침제외164선택binding)은Claude검증대기이며독립검사완료로표시하지않음.
마징카이저slot51/91913형태경고.564748을검증큐에명시하고--defer-shape-review로작업초안연결. 사용자지시로검증판정은Claude에게넘겼으며기준값.70이나측정값을낮추지않음.

## 55개 추가연결·굽기완료(미검증)
21798연출29 + 겟타22053파편8 + 마징카이저초기18 =55개. 생산manifest는production_batch_55/handoff_manifest.json,굽기오류0. 새형태경고는검증큐에binding별명시했고측정기준이나값을바꾸지않음. 이전44개도굽기완료/오류0. 코어046a9701·도구5b5cfb7c선택커밋완료,그림묶음커밋과새기본DLL을포함한EXE재묶기진행. 사용자지시대로추가독립검증은Claude담당. credential helper를저장소밖C:private경로로복사하고해당Git설정만변경해D:의존성을제거(비밀값출력/커밋없음).
