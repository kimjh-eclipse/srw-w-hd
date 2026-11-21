# Codex → Claude: 2026-11-20 全기체 재작화 재개

최신 TO9 11/19 요청에 따라 unit5전체를 최우선, unit3/4전체도 병렬 재작화. 기존179자세 수령과별개인 신규요청. 원본색·구조·actual4xBRZ 전처리·쨍하고매끈한style, 생성RAW바이트보존. 분할·정합·설치·게임검수는Claude. 기존SHEETS/candidate/ROM/library/queue 변경없음.

해상도부족 재발방지로 원본native4x크기는유지하고 SOURCE만최대4칸 소판으로배열. 각새layout/pose계약과함께인계. 생성픽셀편집없음. 비교용base도기체당한번은실제타깃으로새로그림.

## unit5 실제 새 RAW 수령

plate_01~07 각 폴더 RAW_imagegen.png와 DELIVERY_ROOT_20261118.json에 SHA/실제크기/요청프롬프트/새layout 저장. 전체24normal+3affine 생성. 경로 C:/Emul/Workshop/SRW_W_HD/test_current/parts/full_robot_redraw_20261120/unit_5/. gate통과는분할/손·얼굴구조/설치합격아님.

- plate02는 aspect상대오차7.8%로gate실패.03원본겹친머리도확인되어03제외한04/05/06만 plate_02_valid_04_06으로원본재배열/새생성중. 기존판삭제·픽셀정규화없음.
- pose03은원본 native부터 머리같은조각이겹침. 계약15OAM재조립과픽셀완전일치/NN4정확. 화면원점[122,44],OAM영역x130..202,y52..130은화면내부라 화면경계클리핑으로단정불가. 원작순간잔상인지 캡처OAM문제인지미확정.03새RAW설치승인보류.
- Claude: C:/Emul/Workshop/SRW_W_HD/test_current/gui/unit_review/attack_starts/unit_5_weapon_22.state 원본OBJ로frame688..700,특히694 재생확인. 출처weapon22/pose103/obj029, OAM10·11·12·19 머리조각/분리조각 실제동시표시 여부(window/affine/전환포함). nativeSHA8323541314470639434e311337ad4cc411e90f3e4800f46e7fae28c5416b0829. 잘못된원본에서머리를추정수정하지않음.
-00/02는weapon23,01은weapon21출처. 반복회색형태가모두히트로드/새물리발톱이라는단정금지. 원본반복윤곽·부품소유/범위에따라검수. pose23연결된긴로드/방패와원래손모양유지여부중점.


## unit4 FULL 2026-11-20 새 RAW 수령 — 23 normal +3 affine

기존 RAW 재사용 없이 built-in image_gen 7회 실제 새 생성. 일반 pose00..22(기본 pose02 포함) + sheet_a01 pose_a00..a02 전부 그렸습니다. SOURCE만 <=4칸 소판으로 재배열했고 모든 새 layout_snapshot.json에 original_contract_locations를 보존했습니다. 생성 RAW는 byte 그대로 복사했으며 resize/crop/mask/recolor/composite하지 않았습니다. sourceNN4/실제 xBRZ 입력·정식화풍 참조 직접 열람, 원본/참조/계약 SHA 재확인. candidate/ROM/library/queue 변경 없음.

전체 인덱스: C:\Emul\Workshop\SRW_W_HD\test_current\parts\full_robot_redraw_20261120\unit_4\UNIT4_FULL_REDRAW_INDEX.json

- group_01 pose_00,pose_01,pose_02,pose_03 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\full_robot_redraw_20261120\unit_4\group_01\RAW_imagegen.png` SHA256 `20f3b7a80fbf5a10390ebe36df70c7722ba7a85d6967b38eb40b54fbde3d4add` [1526, 1030] vs request [1280, 864]; pixels/native 4.769, aspect error 0.0000, gate True; alpha [0, 255].
- group_02 pose_04,pose_05,pose_06,pose_07 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\full_robot_redraw_20261120\unit_4\group_02\RAW_imagegen.png` SHA256 `df85b50c4dc0cdbe9ba984bbf937a06e532dbe2ce33e24844c568d03ae76589f` [1295, 1215] vs request [1048, 984]; pixels/native 4.939, aspect error 0.0008, gate True; alpha [0, 255].
- group_03 pose_08,pose_09,pose_10,pose_11 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\full_robot_redraw_20261120\unit_4\group_03\RAW_imagegen.png` SHA256 `d48b6719a1d2022d0592314e8e3ce16254aad9927056f5623471a0b2b02a5644` [1274, 1234] vs request [1032, 1000]; pixels/native 4.936, aspect error 0.0004, gate True; alpha [0, 255].
- group_04 pose_12,pose_13,pose_14,pose_15 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\full_robot_redraw_20261120\unit_4\group_04\RAW_imagegen.png` SHA256 `c264727eb3577f7beefc6bd8b95fc8fa945f485a340c0464885b793f30111e48` [1321, 1191] vs request [1136, 968]; pixels/native 4.651, aspect error 0.0549, gate True; alpha [0, 255].
- group_05 pose_16,pose_17,pose_18,pose_19 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\full_robot_redraw_20261120\unit_4\group_05\RAW_imagegen.png` SHA256 `622513e455459ad22fb05bb0f13d47117f53987031b98a3b3668baddff507618` [1382, 1138] vs request [1136, 936]; pixels/native 4.863, aspect error 0.0006, gate True; alpha [0, 255].
- group_06 pose_20,pose_21,pose_22 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\full_robot_redraw_20261120\unit_4\group_06\RAW_imagegen.png` SHA256 `4d5e25882f365ac54fe4f1d5415bb731c4cfc5ce5d7adc44b158d1db101b8cf6` [1437, 1095] vs request [1112, 848]; pixels/native 5.165, aspect error 0.0008, gate True; alpha [0, 255].
- group_07 pose_a00,pose_a01,pose_a02 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\full_robot_redraw_20261120\unit_4\group_07\RAW_imagegen.png` SHA256 `9f0626b87b1396f30bd1abf5cebfa759e417f7813f1c8903282e73dc77f22bf2` [1531, 1027] vs request [1168, 784]; pixels/native 5.240, aspect error 0.0006, gate True; alpha [0, 255].

QA 한계: gate 전부 통과는 구조/설치 합격이 아닙니다. group04 aspect 오차 약5.5%로 제한 근처라 Claude 원본 정합 검수 필요. pose12/17은 원본처럼 단색 near-black 실루엣이며 생성 결과 경계가 다소 부드러워져 정확한 외곽/구멍 유지 확인 필요. pose00 속도선 위치/길이, pose08 분리된 흰 타원, pose22 낮은 웅크림, a01 분리된 용발톱 2개/a02 겹친 부품의 소유·겹침·알파를 원본 계약으로 확인 바랍니다. 모든 슬롯 그림 수와 포즈 방향은 직접 확인. Claude 분할/정합/게임 검증/설치 대기.


### unit4 alpha QA 주의 — RAW 설치 승인 아님

7장 모두 생성 interior alpha가 주로253/252이며255는약400~1100픽셀뿐입니다. 외곽에도alpha1프린지가있습니다(group02좌상단corner alpha1). 따라서 alpha extrema[0,255]와해상도gate통과만으로요청된 interior완전불투명/exterior완전0 충족이라판정하면안됩니다. tool RAW 그대로보존했고 금지된mask/threshold/alpha편집안했습니다. 정식alpha요건미충족상태로 Claude검수대기.

## 실시간 신규목록과 검증 주의

C:/Emul/Workshop/SRW_W_HD/test_current/parts/full_robot_redraw_20261120/FULL_ROBOT_REDRAW_PROGRESS.json 에 RAW/SHA/새layout/크기/요청파일별프롬프트/진행목록. 신규expected99타깃(unit3normal43+affine3,unit4normal23+affine3,unit5normal24+affine3). 비교용base도target으로포함. 이전179반려세트와중복합산금지. RAW수령과resolution/aspect gate·실제구조/알파/설치승인은서로다름.

unit5 회색전개부 해석 정정: 로컬named_attacks report/menu/context에서weapon21=히트로드,22=빔사벨,23=메가캐논 확정. weapon23 +720/+840 두긴회색구조가유지되고+960사이에서빔발사. 초기prompt가전개부를motiontrace로부른것은정정.00/16/18/a01새RAW는실제긴회색물리패널이보이나원본대조필요.02/07/10/20은불확정전개전환윤곽을연기/희미한잔상으로흐리면안되므로 별도 plate_cannon_transition_fix 생성중. 원본의겹친윤곽그대로보존하고숨은부품수추정금지. 기존모든RAW그대로보존.

unit4 내부alpha 대부분252/253,외부alpha1 잔여가있음. extrema0..255만으로완전불투명/깨끗한외곽합격으로세지말것. 임계치/마스크로코덱스가픽셀편집하지않음. group04비율오차5.49%와실루엣12/17 source핏 별도검수. unit3 aspect실패판은원본소판으로다시생성중.

## unit5 후속 RAW 저장 완료 / 분할 출처 맵

plate_02_valid_04_06 새 RAW 1295×1215, SHA 780f50e89a13151cbf1d86109ff5bc96960a6923768e9027fd91e4bc7df3766b, aspect/resolution gate 통과. pose04/05/06은 이 새판을 우선 검수.
plate_cannon_transition_fix 새 RAW 1254×1254, SHA a12209037fde1ac4c6c939f35192cca41fcdc4d9a8cad32099f811440d40f719, gate 통과. pose02/07/10/20 전개부를 불투명한 원본 회색 전환윤곽으로 다시 생성. 구조 검수 대기.
unit_5/UNIT5_PREFERRED_TARGET_MAP.json은 24normal+3affine 각 자세에 RAW/SHA/해당 새 layout/프롬프트를 연결. 새판에 예전 SHEETS 좌표를 적용하지 말 것. pose03은 source hold 유지. 모든 RAW 원본 바이트 보존, 설치/게임 합격 아님.

진행 인덱스의 unit3/4 상대경로를 프로젝트 절대경로로 해석하도록 수정하여 실제 수령을 표시하도록 고쳤음. 08시경 중간집계: unit3 42/46 RAW(비율 실패판 재생성 진행), unit4 26/26, unit5 27/27. 수령 총95/99와 검증합격을 혼동하지 말 것.

## unit3 샌드록 전체 신규 RAW 46타깃 / 11월20일

`test_current/parts/full_robot_redraw_20261120/unit_3/`에 normal pose00..42 43개와 affine a00..a02 3개를 모두 실제 새로 그렸다. 기본 pose22도 plate08의 실제 새 대상이다. 이전 2.19 해상도 RAW를 재사용하거나 재색칠하지 않았다. source-only 3대상 소판과 actual xBRZ DLL scale4를 사용했으며 공식 native/SHEETS는 그대로다. 각 새 layout_snapshot.json은 원본 계약과 공식 SHEETS 좌표를 SHA와 함께 연결한다.

초기 gate통과 plate01,02,03,06,07,09,15,16. plate04,05,08,10,11,12,13은 비율 불일치여서 다른 담당자가 새 source2x2판으로 재생성 중. plate14는 원본 RAW를 보존하고 `plate_14_retry_square/RAW_imagegen.png`로 다시 생성: 1394×1128, 요청1088×880, native당 최소5.12px, SHA276f9d66049ae3166c9b94ac2ab18cd6d3d3f69a15afec86959e8f997193ca67. pose39/40/41은 이 square판을 우선 검수한다.

`DELIVERY_INDEX_UNIT3.json`은 RAW·SHA·layout·프롬프트 요청파일 목록. `RAW_ALPHA_DIAGNOSTIC.json`은 생성 픽셀을 편집하지 않은 읽기 전용 alpha통계. alpha0은 있으나 대부분 그림 내부가252/253 등 부분알파다. 예: plate01 완전불투명1196픽셀, 부분알파390848픽셀. extrema0..255와 해상도 gate만으로 구조/알파 완성으로 판정하지 말 것. 코덱스는 임계치/마스크/재색칠/리사이즈/크롭/합성으로 RAW를 손대지 않았다. Claude가 분할·원본위치 정렬·얼굴/가슴/다리/쇼텔/방패/후면 이음매와 A0/opaque BLACK을 검사하고 설치한다. ROM/library/queue 변경 없음.

사용자 지적 확인: exec-c3f120d4-f68b-4daa-a027-09b078f5fa2e.png = unit5 plate02 좌상단 pose03. 생성본에서 머리·안테나가 여러 개 겹쳐 잘못된 형태로 보임. 원본 native4x에도 머리같은 겹친 조각이 있으나 정당한 잔상이라고 확정되지 않았음. 이 RAW는 설치 대상에서 제외하는 source hold 유지. 이미 별도 plate_02_valid_04_06으로 정상 나머지 세 자세를 재생성했고 pose03은 실제 frame694 확인 후 정상 원본을 받아 새로 그려야 함.

## unit5 캐논 명암 후속 / 최종 우선 검수 RAW

- 첫 cannon_transition_fix는 source 겹침구조를 단색 번개선처럼 단순화한 잔여문제 확인. detail_retry는 명암은 개선했으나1111×1415로 요청1296×1304의비율실패. 둘다보존, 우선분할대상아님.
- SOURCE만 두자세씩가로로재배열하고다시생성. plate_cannon_pair_02_07 RAW 1768×889 SHA3e8e1765b5dd1c5bc73c4ac183fd813a862cbbb1a2f6d2b2ab9a14994b342901. plate_cannon_pair_10_20 RAW1808×870 SHAea32c0162c4639844e9df70da1de16febc873388be58a0d3a3edd4d459990bfc. 둘다비율/해상도gate통과, 내부회색명암과잉크윤곽이생겼음. 원본변환순간의형상보존/새blade추정여부는Claude대조검수대기.
- UNIT5_PREFERRED_TARGET_MAP.json의02/07/10/20을이두판으로갱신. 각해당새layout사용필수. 생성픽셀변형없음.
- unit3/4와같이 RAW의부분알파문제가있을수있으며 alpha extrema만으로합격아님. cannon_transition_fix의밝은/시안alpha1..8 픽셀14364개는숨은RGB만은아님. 실제알파합성으로검수하고Claude가처리판단. 코덱스임계치/마스크수정없음.

### unit5 전환 형상 검증 요청 구체화

pair02/07/10/20은 명암·연결은 개선됐으나 회색 반복윤곽을 실제 금속blade처럼 확정한 해석이 남아 있음. 최종 설치승인 아님. Claude: unit_5_weapon_23.state에서612~616및646 전후의 원본OBJ/블렌딩으로 전환형상의 동시표시/잔상/클리핑을 확인할것. pose02=frame616 obj005(origin58,-26),07=646 obj047(origin34,-24),10=612 obj059(origin39,6),20=614 obj086(origin46,-10). 실제 source.json/frames.json 근거. 정상 전환 의미가 정해지기 전 blind 재생성으로 임의 blade수를 더 만들지 않음. 조합 원본이 수정되면 이 네자세를 새자료로 재작화.


## unit3 aspect 실패7판 재생성 — 04/05/08/10/11/12/13

source-only 3타깃+empty 2x2 새배열로 각 native local4x 크기를 유지. 기존 세로판/RAW/metadata를 덮어쓰지 않았으며 실제 built-in 새 생성7회, 생성픽셀 변형없음. 각 retry_source2x2/layout_snapshot.json에 이전plate좌표와 official_mapping 보존. 인덱스/preferred_target_map: C:\Emul\Workshop\SRW_W_HD\test_current\parts\full_robot_redraw_20261120\unit_3\RETRY7_DELIVERY_INDEX.json

- plate_04_retry_source2x2 pose_09,pose_10,pose_11 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\full_robot_redraw_20261120\unit_3\plate_04_retry_source2x2\RAW_imagegen.png` SHA256 `a4156086bb722e63cfa4b6106577bf15da461604c52bf636227c605d62ec270f` [1564, 1006] vs [1424, 916]; aspect 0.0001, pixels/native 4.393, gate True.
- plate_05_retry_source2x2 pose_12,pose_13,pose_14 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\full_robot_redraw_20261120\unit_3\plate_05_retry_source2x2\RAW_imagegen.png` SHA256 `12797be46414c92b4fd807c7ed31f86a81cab5d134ce52ba6ae6c84f3091d7c9` [1369, 1149] vs [1120, 940]; aspect 0.0000, pixels/native 4.889, gate True.
- plate_08_retry_source2x2 pose_21,pose_22,pose_23 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\full_robot_redraw_20261120\unit_3\plate_08_retry_source2x2\RAW_imagegen.png` SHA256 `ae0ee38e001e5fc63641c9f551c96a72c3b0e8ed87842e6fc2c14ea2793ccb03` [1254, 1254] vs [960, 976]; aspect 0.0167, pixels/native 5.139, gate True.
- plate_10_retry_source2x2 pose_27,pose_28,pose_29 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\full_robot_redraw_20261120\unit_3\plate_10_retry_source2x2\RAW_imagegen.png` SHA256 `a9c12625635df8400b74068ce054d9d03eb9ea6dcb8bb5f5f96e4e8d2e2de8a8` [1549, 1015] vs [1220, 800]; aspect 0.0007, pixels/native 5.075, gate True.
- plate_11_retry_source2x2 pose_30,pose_31,pose_32 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\full_robot_redraw_20261120\unit_3\plate_11_retry_source2x2\RAW_imagegen.png` SHA256 `56540a4af9be892cfb7806296b7c6daf0b3e90f3ae1cfbac51fe6b8c7daa1d09` [1654, 951] vs [1608, 924]; aspect 0.0006, pixels/native 4.114, gate True.
- plate_12_retry_source2x2 pose_33,pose_34,pose_35 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\full_robot_redraw_20261120\unit_3\plate_12_retry_source2x2\RAW_imagegen.png` SHA256 `e6c0d11066e33b02675052d765088133f83e645cb858771e9711648df3595eba` [1375, 1144] vs [956, 796]; aspect 0.0008, pixels/native 5.749, gate True.
- plate_13_retry_source2x2 pose_36,pose_37,pose_38 RAW `C:\Emul\Workshop\SRW_W_HD\test_current\parts\full_robot_redraw_20261120\unit_3\plate_13_retry_source2x2\RAW_imagegen.png` SHA256 `c732788aba3482fae8bfa0ea9c7ccbac2010ddcb3d3b3db66afad58ff824cd73` [1320, 1192] vs [948, 856]; aspect 0.0001, pixels/native 5.570, gate True.

입력NN4/actual4xBRZ/canonical STYLEONLY 직접검수, SHA재확인. 모든3타깃과하단우측빈칸을출력에서확인. 12 detached sword,13/31 detached armor plates,14 horizontal speed streaks,30 diagonal slash groups,29 right-edge partial clipping를프롬프트에명시·결과눈검수. 구조정합/무기손잡이접합은Claude최종검수. RAWalpha는주로252/253, exterior1프린지존재해완전불투명/알파0계약미충족; threshold/mask등수정안함. gate통과는설치승인아님. candidate/ROM/library/queue변경없음.

## 2026-11-20 08:07 최종 수령 집계 — 신규요청99자세

unit3 46/46 새RAW,unit4 26/26 새RAW,unit5 27/27 새RAW 저장. unit3 마지막비율오류7판21타깃도재생성완료했고 최소비율/해상도46/46통과. unit3 UNIT3_PREFERRED_TARGET_MAP.json / DELIVERY_INDEX_UNIT3.json 재빌드완료. unit4 UNIT4_FULL_REDRAW_INDEX.json,unit5 UNIT5_PREFERRED_TARGET_MAP.json이 Claude우선검수출처. 전체43개RAW파일 SHA재확인일치(반려중간본도보존포함).

아직전체작업완료/설치승인아님: unit5 pose03 원본겹친머리1자세 확인대기,02/07/10/20 캐논전환해석4자세 검수조건. 나머지도 Claude원본정합/분할/게임검수대기. unit3/4 RAW내부alpha252/253가많아alpha정식요건미충족,외곽alpha1잔여도주의. 코덱스생성픽셀편집/threshold/mask/합성/ROM/library/queue변경없음.

이번99자세의신규미생성0. 원본확인후재작화가능성5자세+Claude실제검수피드백에따른수정은남아있음. 이전53의sourcepacket대기/정책hold는별도이며이번99와완료합산하지말것. 최신TO9추가원본이오면그원본으로계속재작화.

## 사용자 요청 재확인 / 이전 수량 설명 정정

docs/IMAGE_WORK_RECHECK_20261120.md 참조. 최신99는생성RAW수령이지전역완성수가아님.99타깃원본crop/매핑/실파일/SHA대조완료(누락중복0),preferredRAW33장,중간실패보존포함43장. 전부부분알파존재/A255비중0.049~0.565%라내부불투명요건미충족. unit5 5자세별도hold. 기존unit386affine15자세+unit23pose01=최소16미생성보류도남아있고,수량미확정원본요청/기존교정미해결은별도. 전체남은그림0으로세지말것.

추가확인:95pose01도23pose01과native/contract/candidateSHA동일한도구거부보류. 기존미생성은17개unit-pose항목/동일원본합친16개독립그림으로정정.131a02는전체A0빈원본검증대기이며RAW판존재만으로완료세지말것. affine252판RAW+짝SHA252/252재검증완료.

## 11/20 사용자 지시: 오전11시까지 진행 후 종료

Windows작업 Codex_ImageWork_Shutdown_20261120_1100 등록/NextRunTime 2026-11-20 11:00 확인. shutdown.exe /s /t 0,강제/f없음. 새Claude핸드오프/원본을계속확인하고그릴수있는새요청부터진행. docs/IMAGE_WORKLIST_LIVE.md 및 .json을새작업수신/그림전달/검증대기로갱신. 원본대기와정책hold를임의생성/중복재생성으로채우지않음. 종료전최신인계저장.

## 추가 전역 실파일 감사 / 수신 계속

473robot_set/native7753자세/기본SHEETS1239개 실물조사. 개별pose에그림없는일반65중64는다른layout/RAW수령,125pose11은빈원본/runtime_original명시. affine894중미수령은기존386a00..a14 정책hold15뿐. 기존없음기록9시트도실파일수령확인. 이감사는품질승인/설치완료가아님. 새로즉시생성할유효미수령패킷발견0.

수신담당 /root/redraw_sandrock_full 가10:50KST까지신규Claude핸드오프/패킷변화를60초간격관찰. 새유효요청이오면입력직접열람/원본SHA검증/actualBRZ+STYLE/built-in생성/RAW바이트저장/새layout/프롬프트/SHA를자율진행하고본인계와IMAGE_WORKLIST_LIVE.json갱신. 10:50이후새호출시작금지,남은일/진행저장후종료준비. Windows11시shutdown작업Ready및/s /t0확인. 원본부족/정책hold/429를억지생성으로채우지않음.

## 11/20 09:20대 — 새수신 unit265 누락8자세 실제 생성

TO9의 새 `11/20 09:09` 절에서 unit265 pose08/15/16/17/19/27/35/40 미납 요청을 확인. 기존 PREFERRED_DELIVERY/ROOT_260_263_265 납품에는 없는 대상이고각pose candidate도없음. 원본색을먼저확인하여08/17은순백flash,나머지6은아주어두운charcoal청회색고유원본으로구분. 기존밝은Arbalest HD를재색칠하지않았다.

납품목록 `test_current/parts/incoming_redraw_20261120/unit_265/INCOMING_UNIT265_DELIVERY.json` 에모든RAW/SHA/새layout/contract/sourceSHA/실제prompt/알파통계. 총8타깃,실제4호출(white2target source-only교정1회포함),모든RAW그대로보존. new2x2 source-only배치이므로옛SHEETS좌표적용금지.

- `plate_02_dark/RAW_imagegen.png`: pose15/16/19,1254×1254,SHA050d24bd26cb635c72754c6d94d82fd54bc93a81f0ccd297794b547507d4e0c5. 본래짙은팔레트와작은cyan눈/yellow핀유지. 원본raised-rifle/후측면/잘린팔의정확가림·연결·크기/알파는Claude검수.
- `plate_03_dark/RAW_imagegen.png`: pose27/35/40,1513×1039,SHAa7fd946b8ec5b529c977e7618e1b9f76e9456938bc893b133b0e68d617bed5b3. 40의교차회색운동선은금속칼날이아닌평면밀집선으로그렸으며정확원본가닥수/범위/불투명밀도는Claude검수.
- white08/17 최초 `plate_01_white/RAW_imagegen.png`와 `plate_01_white_sourceonly_fix/RAW_imagegen.png` 모두보존. source-only추가1회후에도원본A0작은구멍이메워지거나외곽이구름덩어리처럼읽힐수있고RGB247~255미세음영이남아**strict순백/홀보존미해결**,preferred/설치승인안함. 마지막SHA b41068b4d664ca9a1609f749e8163edc320a13b8bd9c0abfbd7085606f2b6511. 도구반환그림마스킹/강제순백/리사이즈로고치지않음.

`docs/IMAGE_WORKLIST_LIVE.json` new_actionable/new_deliveries/new_holds에위항목추가. dark6도대부분alpha252/253이므로gate통과=완성아님. ROM/library/기존queue/candidate변경없음.

## 11/20 오전 — 컷인 신규 일괄요청 G009/G010 얼굴2IMG

TO10 정식일괄요청의 G009/22850(키라 보라눈·갈색머리·teal헬멧),G010/22857(아스란 초록눈·청남머리·burgundy헬멧)을원본canvas실제색으로새HD셀작화. 그룹의두IMG는단순연속프레임이아니라BG2얼굴과BG1피부발광+대사창틀의서로다른레이어였다. BG1 22851/22858는HUD가같이들어있어Claude소스분류대기이며임의HUD생성/제거안함.

납품 `test_current/parts/cutin_batch_redraw_20261120/G009_G010_DELIVERY.json`. 실제4호출,새이미지2개. 첫RAW는fullyopaque원본얼굴사각영역안에A0구멍6042/5908px가생겨preferred아님. source-only32px투명여백을추가한native+actual4xBRZ로각1회다시그려큰내부구멍해결. 두번모든RAW변경없이보존.

- G009/IMG22850_padded_sourceonly_retry/RAW_imagegen.png:1881×836,SHA5a00bcfd7b27b4dd7b113e096ff4868a888c6c577fcbec930f0d4e1dedbc3bac.
- G010/IMG22857_padded_sourceonly_retry/RAW_imagegen.png:1881×836,SHA901c91670e5f6b35b4d443bbb961870c67317b3ddab9a1aeca0c01cdb8862d4b.
- 둘다요청1344×576(각nativecrop320×128의4x=1280×512+32여백),해상도gate최소5.598px/native,비율오차약3.58%. 읽기전용innerROI[112,100,1768,735] A252..254,A0=0,A<200=0. **alpha255완전불투명은아직아님**,외부미세잔여/정확사각경계·눈/피부광선원본위치는Claude검수.

원본은512×512canvas중상단(0,0)-(320,128)만그림이고나머지A0. source-only로A0여백을trim한뒤새32여백을넣었으므로새layout_snapshot.json으로그림부분을원래2048×2048맵원점(0,0)에복원해야함. generated픽셀resize/crop/마스킹/재색칠/합성은Codex에서하지않음. batch원본/ROM/library/기존queue변경없음. docs/IMAGE_WORKLIST_LIVE.json 신규납품/분류hold반영.

## 11/20 오전 추가 — G019 얼굴부분 / G026 보스 얼굴

`test_current/parts/cutin_batch_redraw_20261120/G019_G026_DELIVERY.json` 에2호출신규RAW·SHA·prompt·source/새layout. 생성픽셀변경없음.
- G019/IMG22927_source_crop/RAW_imagegen.png:1954×805,SHAd3d5f9d8d7f513cc1b3f9a20916d4743526e509cb0a4c3f66310aae074e22e0d. 원본자체가저채도회색헬멧·머리/회색눈+옅은분홍피부라그색대로새작화. **얼굴부분만납품**,nativecrop[0,0,256,96],원512²맵의다른영역청록대사창/HUD틀은그리지않고Claude소스분류대기. 전체IMG완료로세지말것. 새그림위양옆모서리cutout은원본사각coverage와독립검수필요.
- G026/IMG23042_source_crop/RAW_imagegen.png:1596×986,SHAca450f61c79f91926af8fc1abc3a1f6fa8374b464ed918db4c886faf464a5b3e. 보스눈썹/큰이빨웃음/두꺼운턱/뺨사선/갈색머리/남색옷을원본과같은구도로새그림. source nativecrop[0,0,256,152] 아래A0만trim+32sourcepadding. 왼쪽암부는원본RGBA(16,16,16,255) 실제불투명영역이라검정배경으로오해해지우지말것. 생성샘플(6,6,8,253),정확원색/불투명coverage/표정·스케일Claude검수.
둘다gatePASS뿐이며alpha252/253부분불투명잔존. 새layout으로원래맵좌표복원Claude담당,RAW강제alpha수정/크기변경/합성없음. liveworklist에납품및G019부분소스hold반영.

## 11/20 오전 추가 — 로봇클로즈업 G001/G003/G007

`test_current/parts/cutin_batch_redraw_20261120/G001_G003_G007_DELIVERY.json`:3IMG실제4호출,모든RAW/SHA/sourcecrop/새layout/prompt저장. 원본A0여백만trim+32sourcepadding,originalcanvas복원좌표각layout기록. 후보/ROM/library/기존queue수정없음.
- G001 IMG22755_source_crop/RAW_imagegen.png:1382×1138,SHA83f9f7c227287ba35a25316bf041074a625ee261cbc1655e070ad2e5f0c4878c. 붉은장갑/회색테두리의긴검정홈클로즈업을새작화. 원본하단분리회색패턴블록도그렸으나오른쪽strip에작은홈처럼새선이생겨정확윤곽·불필요detail검수필요. 이부분이실제화면사용맵인지도Claude분류가능. 원본하단source내용임의생략/합성없음.
- G003 IMG22769_source_crop/RAW_imagegen.png:1723×913,SHA1db05815c957a652106dd5095ae0a800ad20c8752d51c3f75300f846754d18a6. 원본검정/charcoal얼굴,가늘고기운주황노랑눈/작은노랑장식을smooth셀로새그림. 눈길이·facegeometry·원래A255검정면/알파Claude검수.
- G007 IMG22831_source_crop/RAW_imagegen.png 및 IMG22831_whitepanel_sourceonly_retry/RAW_imagegen.png:둘다1723×913,첫SHA7448e204422b2a2bcf4c10fcbaedd3d06c28d33318e12a8d13b99d9b024bfa91,교정SHA183fa665495400a362eceebe49f1667374e537b7d6afa40da0a9555ea9f705d2. 녹/남색머리·보라보석·cyanV·주황목을새로그렸으나원본은흰배경까지불투명사각면. 첫RAW는흰배경제거,source-only1회교정은흰배경일부복구하나왼쪽큰A0구멍발생하여 **opaque white background 미해결hold**,preferred아님. 강제whitefill/마스크/합성으로고치지않고보존.
모두gate통과뿐;이전처럼alpha252/253잔존. liveworklist신규납품및G007hold반영. G007은도구transparenttrue가흰배경을자동제거하는한계로반복호출중단.

## 11/20 오전 — G014 테카맨 컷인5IMG / 고유원본2개

납품 `test_current/parts/cutin_batch_redraw_20261120/G014/G014_DELIVERY.json`. 원256²전체RGBA를직접비교하여22877=22881,22878=22879=22882 완전동일확인. `IDENTICAL_NATIVE_RGBA_PROOF.json`에각원본파일SHA/전체RGBA SHA/size. 고유2원본만각새그림,동일원본alias에는새RAWbyte그대로공유. 기존HD재색칠/크기변경/합성없음.
- 22877/22881 우선검수: IMG22877_sourceonly_eye_correction/RAW_imagegen.png,1394×1128,SHA는해당request/DELIVERY. 첫RAW의녹색눈은native22877에없는색(원본green픽셀0개)이라제외. 같은native+actualBRZ만써서**새로그려**흰/짙은visor눈으로교정했다. 첫RAW도보존. 긴흰headfin·붉은가슴/금장·넓은어깨·허리의세갈래claw·하단hardcrop 원본위치검수.
- 22878/22879/22882 우선검수: IMG22878_source_crop/RAW_imagegen.png,1576×998,SHA158ef886c599f9038d936dafa11f9eb1bfaf8c3756fd1e667bd75daf9c35dd3e. 양어깨녹색원형pod와두주먹포함새작화. 정확pod구멍수/위치·손가락포즈·fin/torso폭·원본색검수필요.
총실제3호출,새5IMG매핑. 새layout은source alphaBBoxtrim+32padding에서original1024²맵에복원하는좌표포함. alpha252/253미완전불투명및외부미세잔여계속QA. 설치/승인아님. liveworklist납품반영.

## 11/20 오전 — G015/G016/G020 신규4IMG

`test_current/parts/cutin_batch_redraw_20261120/G015_G016_G020_DELIVERY.json` 에3호출4IMG RAW/SHA/source/새layout/prompt/alpha통계. G02022934=22935는256²전체RGBA완전동일하여동일새RAWbyte공유(각source proof포함),색변환없음.
- G015 IMG22895_source_crop/RAW_imagegen.png:1479×1063,SHA3eac33e96495a5d5465126fd8bb9cbd4c0cab8ef7b5b2d9692dce7a16ee84113. 갈색기계머리,큰양옆뾰족lobe,빨강후면fin/목,흰긴faceplate,작은turquoise원형모듈을원본pose로새HD.
- G016 IMG22896_source_crop/RAW_imagegen.png:1396×1127,SHAb10e126250165e61a3ba8908a9e8788de4b31052ce417ecaa5caa14d1c32e696. 다른nativepose/자기색으로별도새작화,큰가운데삼각horn/흰brow/작은facewhite부분/후면길게뻗은fin. source오른쪽맵경계에서잘린horn끝을완성하지않고hardcut유지.
- G020 IMG22934_source_crop/RAW_imagegen.png:1723×913,SHA40f7b336fb1656e41e8fd5b3a206b12a48d20aff948553b01761942bdc481791. 회백/검정로봇얼굴과green눈,앞가로기계rail새HD. 눈과rail의원본상대위치/scale가정확한지독립검수. 검정왼쪽면은source불투명paint라제거하지말것.
원본A0여백만crop+32sourcepadding,원래canvas복원좌표새layout포함. 모두gate통과뿐,alpha252/253미해결·shape/색/정합/설치Claude검수. RAW픽셀수정없음. liveworklist납품반영.

## 11/20 오전 — G059/G061 얼굴component2개

`test_current/parts/cutin_batch_redraw_20261120/G059_G061_DELIVERY.json`:새2호출2얼굴부분RAW·SHA·source/새layout·actualprompt·alpha통계. **BG1전체IMG완료아님**:원512²canvas에서top[0,0,256,144]인물부분만원본그대로crop+32padding하여새로그렸고,다른곳의cyan대사창/HUD틀은Claude소스분류대기.
- G059 IMG23496_face_component/RAW_imagegen.png:1635×962,SHA7ef131b817eeec9c6a53828889ca61acb807be108f0e1af73891bfe37b84b7c9. 회백헬멧노년pilot의주름·뾰족코·비대칭작은갈색동공/흰눈·웃음과이빨을원래색/표정으로새HD. 임의젊게만들거나blueeye추가하지않음.
- G061 IMG23542_face_component/RAW_imagegen.png:1635×962,SHA는request/DELIVERY. 금빛각진헬멧/주황머리/오른blueeye/왼green렌즈+눈/외치는입을원본색으로새HD. 전체사각영역원래opaque,검정틈도불투명paint검수.
G04823249 원본canvas는빈검정cockpit배경만있고OVERVIEW여성얼굴은다른OBJ이므로얼굴그림발명안함,priority3배경대상으로남김. G06223543/44는원본RGBA동일하지만used_in에unit386이있어부모386hold범위확인전호출안함(별도BG인물컷인인것과기존blockedaffine동일성은불명,우회아님). 이둘을수령완료로세지않음. sourceclassification notes/liveworklist반영. 모든RAW그대로,라이브러리/큐/ROM변경없음.


## 11/20 10:06 KST — G004/G044 new cutin RAW
4 actual builtin calls / 5 IMG:22791/22792 own night/warm palettes one source2panel plate;23180/23181/23182 separate fresh frames. Index `C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G004_G044_DELIVERY.json`. All source/native4x/actual4xBRZ viewed; original maps unchanged, exact source-only crop/restore map in layout. All dimension gates pass but not acceptance: RAW alpha252/253 and border speckles/edge clipping/face expression require Claude QA. Black original panel is paint, never erase; G04423182 wholly mechanical internal robot face. No RAW transformations/candidate/ROM/library/queue edits.
[22791, 22792] RAW C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G004\IMG22791_22792_source_plate\RAW_imagegen.png SHA256 267c39d10e416a9ecc4a19377a60e32c4c185f9ce95f9b2d356d5f523a8f6f5a
[23180] RAW C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G044\IMG23180_source_crop\RAW_imagegen.png SHA256 d12bd64aa907f5184e1469af535f76eebede4e065b3b2e047ce991887635b0a0
[23181] RAW C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G044\IMG23181_source_crop\RAW_imagegen.png SHA256 f4b1820bcac8d225eaa1426486c371f662d7a5db08b09bb48189d014ed4174ab
[23182] RAW C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G044\IMG23182_source_crop\RAW_imagegen.png SHA256 6b29897cb293d1a45c1a2189bbd1176edf002807460ad00ae732e1b2e4745cfe


## 11/20 10:11 KST — G063/G071/G072 3 new cutin RAW
3 actual builtin calls:23547 teal-lit pilot;23617 blue robot huge fist foreground;23618 own amber robot state. Each viewed native4x+actual4xBRZ+canonical STYLE, exact source-only crop/restore maps. Index `C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G063_G071_G072_DELIVERY.json`. All dimension gates pass, alpha252/253 and native boundaries/fist-to-face scale/expression require Claude QA; no install approval. No RAW transforms or candidate/ROM/library/queue changes.
23547 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G063\IMG23547_source_crop\RAW_imagegen.png SHA256 4a15deb454ddfaa8c6cc2b87ba7454eb74c8d12c42d7412674f6df3a8ccbfa78
23617 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G071\IMG23617_source_crop\RAW_imagegen.png SHA256 a7216c7239938ff97832f5168ea607b155d7f2bc5aa3a961699d4866ba1466ae
23618 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G072\IMG23618_source_crop\RAW_imagegen.png SHA256 3998e538b00ff1907a89b1c08e061601475e8f803abc1cb3ce0fb55d975ea202


## 11/20 10:14 KST — G07623893/G081/G082 new RAW
3 actual builtin calls,3IMG.23893 blue-helmet pilot;23957/23958 separate smooth/wrinkled green villain expressions newly drawn from own native. Index `C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G076_G081_G082_DELIVERY.json`. All dimension gates pass, alpha252/253, source boundary/clipping/eye/mouth contour still QA.23894/23896 not called (native contains HUD or baked dialogue), classification pending. No RAW transforms/candidate/ROM/library/queue changes.
23893 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G076\IMG23893_source_crop\RAW_imagegen.png SHA256 01fcdeee3aeab2b799ec1fc2cc35bf4fbf029544a315687092af49559e89d8bf
23957 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G081\IMG23957_source_crop\RAW_imagegen.png SHA256 65504d293f01333733ed47bf353f907c1aabe982770f285417e0541ca72cdd7b
23958 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G082\IMG23958_source_crop\RAW_imagegen.png SHA256 d8e496b304a40333b1d575cdcb2ee58f2d1d7ee02ccbe0929f74a411f95a107b


## 11/20 10:18 KST — G085/G086/G087 new RAW
3 actual builtin calls /3IMG:23994 teal pilot left profile;24092/24093 blue-white-red robots, native-specific foreground mechanical assemblies. Index `C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G085_G086_G087_DELIVERY.json`. Source/native4x/actual4xBRZ/STYLE viewed. All dimension gates pass; alpha252/253, native joins, mechanical front block/circular hole counts and boundary QA remain; no accepted/install claim. G087 actualprompt corrected beforecall to machinery from generic fists, sourcegeometry remains authority. No RAW transforms/candidate/ROM/library/queue edits.
23994 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G085\IMG23994_source_crop\RAW_imagegen.png SHA256 8ddad8a63241a4767b1308a9512c6fc4420643148f85959bf6f0336d84d35ddd
24092 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G086\IMG24092_source_crop\RAW_imagegen.png SHA256 7e36f9e3b233431d11d10d0dc458f203c1687826ff3cc71c7c12f5f5d11fb478
24093 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G087\IMG24093_source_crop\RAW_imagegen.png SHA256 f5d33cc01c4f805575d70289a3d1f58793b7650824ba8976af3b3f4b67bb5a24


## 11/20 10:24 KST — G088/G089/G090 5 new RAW
5 actual builtin calls /5IMG:24115,24116,24117,24119,24120 each freshly drawn own native palette; no generated donor colors. Index `C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G088_G089_G090_DELIVERY.json`. All dimension gates pass. IMPORTANT 24115/16/19/20 have unrequested white/colored blade halos/speckles and are install-HOLD, no generated pixel repair.24117 dark base state cleaner but exact mechanical contours/joins/alpha QA pending. G09024121FX not called. Source/native4x/actual4xBRZ/STYLE viewed; no candidate/ROM/library/queue edits.
24115 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G088\IMG24115_source_crop\RAW_imagegen.png SHA256 fc4e6f360864583fe3c76927ce36b8dff1a21859007bc4c2e2c0e0aba866bd17
24116 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G089\IMG24116_source_crop\RAW_imagegen.png SHA256 85c9e37e43ac0a387e4324cdb4911564efa3784e1fff7415be3493efcac6689c
24117 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G090\IMG24117_source_crop\RAW_imagegen.png SHA256 a08690ff5434196ec6e61bccd74dbdeeb67acbab14442d90a4740c01ea238247
24119 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G090\IMG24119_source_crop\RAW_imagegen.png SHA256 4d2cbd3243dc2bc78bc6a87d54b2ed56162bbfa21216690c733b9a287d296606
24120 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G090\IMG24120_source_crop\RAW_imagegen.png SHA256 c5a4005468ee5fc5e2874cb1367a7f5ab9e8dab8d7c2166522a62701a4487c11


## 11/20 10:28 KST — G022/G023/G024 3 new RAW
3 actual builtin calls/3IMG:23000 neutral grey robot upperbody smooth blank face,23019 armsraised,23020 armsdown/red fins. Index `C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G022_G023_G024_DELIVERY.json`.23019/23020 UPPERROBOT COMPONENT ONLY, native dialogue HUD below not drawn; not full IMG completion. All dimension gates pass but alpha252/253, exact pose/joins/bottomcrop (especially23020 bottomedge) QA remain. Source/native4x/actual4xBRZ/STYLE viewed, no RAW transforms/candidate/ROM/library/queue edits.
23000 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G022\IMG23000_source_crop\RAW_imagegen.png SHA256 3c5c058f54dce5132a456a62a5667924a72bc6c2e69f18063bf21ba1e26ec695
23019 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G023\IMG23019_source_crop\RAW_imagegen.png SHA256 9f92cac1c8c0bcdcf461dcf8033bc98089e99d6024a3222d6b1c07f86ce41810
23020 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G024\IMG23020_source_crop\RAW_imagegen.png SHA256 5bd3ef1cda0bbc4151616e253dc9cc9aa4eb56a897e6a77c0a307aa800ca2606


## 11/20 10:32 KST — 3 new BG RAW, framing/opacity HOLD
3 builtin transparenttrue calls:24453 cyanpillar,24510 bluevortex,24517 space tile. Index `C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\BG3_DELIVERY.json`. All dimension gates pass BUT G106/G112 ignored32transparentpadding and paint fullbleed; source-fit not accepted. G113 erased fullyopaque native tile corners into transparency, cannot tilewrap/opacity pass. G116 preparednotcalled. No generated pixelrepair or candidates changed. Source/native4x/actual4xBRZ/STYLE viewed.
24453 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G106\IMG24453_source_crop\RAW_imagegen.png SHA256 31e7c8dadf2f44f4d2bb7985281264220e17dc067374e1e3cddbdd2746f92507
24510 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G112\IMG24510_source_crop\RAW_imagegen.png SHA256 10d07c4cbba258c6172361ec1a66541c8a8b75f72d8b7a010c4d5982f5007003
24517 C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G113\IMG24517_source_crop\RAW_imagegen.png SHA256 ab5e8694801ed99711ff0d8e8e2817578e94315c9ed8dea083c89c0f0fb9a2fc


## 11/20 10:37 KST — G000/G006/G017 4newRAW/5IMG
4 builtin calls,5IMG:22701=22702 nativeRGBAidentical proof and one RAWaliases;22813 swordrobot;22903/22904 separate native basic/unfolded states. Index `C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G000_G006_G017_DELIVERY.json`. G017 upperrobot component only/HUD classification pending. All dimension gates pass, strict alpha252/253 and native hole boundaries/rootlight counts/swordgrip QA remain. G000 central native alpha0 cutout preserved but small edge speckles, no hidden body invention. No RAW transforms/candidate/ROM/library/queue edits.
[22701, 22702] C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G000\IMG22701_source_crop\RAW_imagegen.png SHA256 fa9b42a5d0cc033e3016aba7ae3ddf31b0f94d49c03e62bfb4097e763cbf5af2
[22813] C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G006\IMG22813_source_crop\RAW_imagegen.png SHA256 557f6ecb7582192f7eef2f37b3ff839dde38c0042f045b4eacb7ca8cc9622cc9
[22903] C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G017\IMG22903_source_crop\RAW_imagegen.png SHA256 f4895ac76b5d9ff8badd3d9a65baef566bc0a39ddaea0bd6f2d2b8589b7a4092
[22904] C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G017\IMG22904_source_crop\RAW_imagegen.png SHA256 f6aeb948a85585e24a03e88983fd57466b6e01b206657741d5087d46ebf26077


## 11/20 10:41 KST — G021 3newRAW/5IMG
3 builtin calls for5IMG.22977=22978=22981 exact nativeRGBAproof sharing one newlydrawn RAW;22979/22980 each separate new source glowstate. Index `C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G021_DELIVERY.json`. All dimensions gates pass,22980 aspect deviation borderline5.9percent. Native shoulder edge clipping, original3lobe/glow topologies, alpha252/253 and source exactalignment QA remain. No RAW transform/recolor/candidate/ROM/library/queue edits.
[22977, 22978, 22981] C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G021\IMG22977_source_crop\RAW_imagegen.png SHA256 59d5544d20aed9a58b2f0213060ba15d00f71989b19300b98ecca9f1e673315a
[22979] C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G021\IMG22979_source_crop\RAW_imagegen.png SHA256 4026c75edff578487a44cbe0b67f9f11d9d07047333a4ad8d029eba783d8a46b
[22980] C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G021\IMG22980_source_crop\RAW_imagegen.png SHA256 6152ec238447e9a47b419120e390d6553561936609553689b13b5ce365cda9e8


## 11/20 10:45 KST — G002/G028 final 2newRAW/4IMG
2builtin calls:22758 spearheldoverhead robot;23095=23096=23097 exactnativeRGBAproof upperrobot component. Index `C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G002_G028_DELIVERY.json`. G028 sourceHUD below not drawn/fullIMGincomplete;G00222759 uncalled. All dimension gates pass, exact blade grip/hardcrop/alpha252/253 QA pending. No RAW transforms/candidate/ROM/library/queue edits.
[22758] C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G002\IMG22758_source_crop\RAW_imagegen.png SHA256 44027e920aed809c338d003dc8be995063a48ab2c0efee888f36b9e66c30d1c7
[23095, 23096, 23097] C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\G028\IMG23095_source_crop\RAW_imagegen.png SHA256 d01b108ed8688b30ca66793dcda62d072483c74e93cfa2c85cd5549eade61214


## 11/20 10:46 KST — Incoming cutin consolidated audit
Master `C:\Emul\Workshop\SRW_W_HD\test_current\parts\cutin_batch_redraw_20261120\CUTIN_INCOMING_MASTER_DELIVERY.json` includes every RAW call/SHA, preferred target map with exact alias/component/hold flags, source/native/reference/contract/layout SHA checks, prepareduncalled and untouchedbythisroot IMGIDs. Summary:{"updated": "2026-11-20T10:45:35.601679+09:00", "scope": "ONLY this 11/20 incoming cutin batch redraw output root; not global campaign installed progress", "actual_new_raw_calls": 51, "unique_raw_sha256": 51, "image_ids_with_new_raw": 57, "full_layer_target_ids_with_new_raw": 47, "component_only_target_ids_with_new_raw": 10, "known_visual_hold_target_ids": 8, "prepared_uncalled_requests": 1, "raw_sha_failures": [], "source_or_reference_or_contract_changed": [], "total_incoming_image_ids": 693, "not_touched_by_this_output_root": 636, "all_pending_Claude_visual_sourcefit_opacity_QA": true, "accepted_or_installed": false, "notes": ["Counts of untouched IDs are NOT globally RAWmissing: preexisting11/18 RAW/existingHD hooks and policy/source holds must be reconciled separately.", "All RAW preserved unchanged. Common alpha252/253 remains strict opacity limitation. Dimension gate alone is not QA.", "G009/G010 padded source retry and G014 eye correction preferred; G007 whitepanel retry remains HOLD. All first RAW remain in rows.", "No generated resize/crop/mask/recolor/composite, no candidate/ROM/library/queue modifications.", "G116 preparednotcalled. Known23/95/386 hold content not retried. No429/moderation error this incoming run."]}
Cutin new imagegen calls have ended at10:45; observer remains until10:50. TO10 latest unchanged atthis check. Original693IMG request not completed; untouched count is not global missing count because oldRAW/hookedHD exist. All new art remains Claude QA, not installed.


## 11/20 10:50 KST — Incoming observer ended / all RAW saved
DOC_WATCH_END and PACKET_WATCH_END exit0 confirmed. No new incoming doc request afterTO10; _scan/scan_new.json alone continued progressing, no finalized newsourcepacket observed. In-flight imagegen0, unsavedRAW0. Morningnew55builtin calls/55RAW SHAverified → cutin57IMG(10componentonly)+unit2658poses=65requestedtargets including nativeRGBAaliases. All ClaudeQA, accepted/installed0. Master `test_current/parts/INCOMING_MORNING_DELIVERY_20261120.json`; detail `test_current/parts/cutin_batch_redraw_20261120/CUTIN_INCOMING_MASTER_DELIVERY.json`.
Remaining: unit26508/17 strictwhite/holeprecisionhold,8cutinvisualholds,10componentHUDsourceclassification; commonalpha252/253/sourcefitQA across others.693IMGbatch incomplete;636IDs untouchedbythisroot is NOT globalRAWmissing because preexistingRAW/hooks exist. G116sourcepreparednotcalled.23/95/386existingholds untouched. No429/moderationerrors in incomingrun. Candidate/ROM/library/queue untouched, generatedpixeltransforms0. Windows11:00shutdown reservation remains parent-owned, not changed.
