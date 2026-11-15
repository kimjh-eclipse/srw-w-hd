# IMG19808 실제 연출결함11 교체 후보

## 범위

- Claude `HANDOFF_TO_CODEX_3.md`에서 `observed_effect_19808_new12`12개 중11개(lost10/empty1)를지정한교정이다. 기존92654–92664 같은11ID의그림교체이며신규누락11완료로세지않는다.
- 정상92653(기존candidate x0,y0,w64,h32)은옛HD RGBA를비트단위로보존했다. 대상11사각형밖도보존. root는새`effect19808_components_repaired11`atlas에11기존ID만분기하고정상1의oldbinding/atlas/image/key는그대로두면된다.
- 후보candidate_atlas.png/native_atlas.png. normalized_installer_contract11.json과install_contract.json은동일한installer형식. ready_replacement11.json에서경로/해시/범위확인.

## 원본과 팔레트 계약

- 기존 `true_missing_19808/install_contract.json`을 hash뿐아니라원본source_box/크기/rawbytes로대조해복구했다. source_live_bindings12.json의옛candidate좌표를atlas_box/spec x/y로고정했고원본source_box와분리했다.
- 대상11중개별실제cached9,ROM IMG19808 raw+actualfull16팔레트확정미관측2. 관측/미관측을그대로보존. actual_palette_bgr555는실제rendered_source_contract.palette_15bit에서직접읽고full16일치를assert했다. RGB에서역산한값을설치에사용하지않음.
- source_candidate_palette_integrity11.json에ROMraw/기존raw/hash/실full16/개별관측여부/실제팔레트증거를보존. fixture는unit141/mechanical_cutin_128.state 등원계약의frame/observations 참조. 새실제재생확인한것은아니다.

## 성분과 자체 그림

- 원본전체256x32에는19개연결성분/17고유형태가있다. 단순전체시트resize대신고유형태큰참조→자체새RGBA→각원본성분bbox의위치/크기에등록해원래좌표로조립했다.
- 첫성분은흰호와회색호가한texel접촉으로묶였는데wholebbox만맞추면내부곡선이어긋났다. 두역할을각각그려원래흰/회색bbox에조립하는방법으로교정. 나머지복잡한7개형태도단독큰참조로다시그려선폭/슬릿/잘린끝을복원했다. 작은단색2texel은imagegen에서새opaque cyan평면을만들어그자체RGBA를사용했다.
- 원본alpha/RGB를출력에전사하지않음. alpha threshold/Min/Max/morphology로성분삭제안함. alpha>=16은생성그림의기하bbox측정에만사용하며전체자체RGBA를affine등록한다. 기하사각형외곽에서클립되는한계는있다.
- 대상11은19원본성분의일부/전체와교차하며982native texel. 해당범위의생산비교상성분소실0. 정상1영역의537texel은새로고쳤다고세지않음.

## 생산 확인: 설치 계약 좌표를 실제 사용

- 최종SHA `43bf8306fe41f5e371ddc70702c43312e2cc7dee52c5646475b8dd91366d8318`,4배1024x128/native256x32.
- 직접원래좌표prepare12와 **normalized installer11의atlas_box/spec좌표를사용한NullCache prepare11**을둘다실행해출력RGBA가일치함을확인. normalized_installer_prepare11.json에각기존ID/candidate crop/spec좌표/출력hash/maxalpha/일치여부보존. 12077의hash별칭좌표혼동재발을차단하기위한제작입력검사다.
- source기하native격자alpha128 비교:11전부IoU1/면적비1/미도색0. target_component_presence_production.json은19대상성분위치의paint존재만본다. 이는공식QA/색상합격/실제HD재생판정이아니다.
- 색차이는남는다. source_colour_production_comparison11.json의원본paint좌표RGB평균차이중앙값4.54/255. 최악평균은92656에서12.04/255,최악한채널차이는92654에서66/255. 주로gray호경계/AA와밝은호내부색배치가원본과다를수있다.

## Claude 확인 위험

- 새그림은원본의의도된단계형cut/두께를유지하려일부외곽계단을남겼다. 이음부분의4배AA/색배치/선두께가실제화면에서자연스러운지는공식판정대기.
- 정상92653과새92654는원본시트x64경계에서서로이어질수있다. 정상1을변경하지않았으므로old/new그림AA/명암경계가실제동시조립에서보이는지확인해야한다. 같은시트의인접이실제동시조립증거라고주장하지않는다. 원계약의같은frame/OAM배치로판정.
- 모든부분/겹침은한조립시트의같은자체그림에서잘라같은영역을공유한다. native_before_candidate_comparison.png는위부터원본/이전/교정후. panel/단독group/흰호/회색호참조와생성원출력/v1,v2후보·보고서를보존.
- root만새atlas분기설치/11굽기. 이agent는라이브/library/DB/core/EXE/Git/공유실행코드/독립audit/실제HD재생/물리입력을변경하지않았다. verify_new_art/실제재생은Claude담당.
