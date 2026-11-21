# Codex 이미지 작업 인계41 — 계속 생성 / 279 사용자 반려 구분

이전 상세: HANDOFF_FROM_CODEX_40.md 및39. 최신입력 HANDOFF_TO_CODEX_9.md. 실제builtin imagegen, RAW=candidate bytes/alpha보존. 원본재색칠/다른팔레트대체/HDresize/코드alpha정리없음. 설치·ROM·원본/공식layout불변. 후보납품은 독립검수/사용자승인과다름.

## 279 최신 사용자반려4자세

- 기존sheet04/qa_alpha의25/27/28/29 4슬롯 계속사용금지. STYLE와DELIVERY_MAPPING_20261117_XBRZ.json 및root목록에slot_holds명시.
- 새 **부분개선 검토후보4개**: unit_279/robot_set/qa_user_anatomy_20261117/DELIVERY_PARTIAL_REVIEW_20261117.json. 각target-onlylayout 사용/신base14참고전용설치제외. RAW원본과생성요청/참조SHA/독립검토메모가각폴더에있음. 사용자반려완전해결아님.
-25 pose25_source_planes/qa_smooth_planes (SHA5286ffa4…) 및28 pose28_source_planes/qa_smooth_planes (SHA93d3a289…): 원본에서새로각진light/darkplane을그리고실제smooth편집. 큰원형cup명암감소는독립관찰됨. 좁은darkgap/겹친leg/손이Cclamp로일반화된부분은source대조남음.
-29 pose29_source_only/qa_marks_hand (SHA7c211988…): 큰oval가슴cavity/입술rim을flatdark면으로새로그리고작은뒤손열린형태수정. 전면4red-dot를3으로고치는추가실제편집2회는실패해RAW설치금지보존. native14/29는top1+front3삼각배치pixelmark,정확source위치40문서/독립메모. Claude source표식대조필수.
-27 pose27_source_only/qa_patch_topology (SHA56f7334c…): 세모glyph→round3dots,source손dark면/lightstubs추가. C형rim/alpha접합미해결. 회색source/target지원추가edit qa_source_opaque SHA2617f08e…은원본ROI수치일부가까워졌으나형태복구증명못해비교RAW/설치금지. opaque원본78.95%vs새68.98%,정합한계/semantic손mask아님.

## root새전달

- **107 선택2자세**: unit_107/robot_set/PREFERRED_DELIVERY_20261117_EYE.json. qa_guard_hand_20261117 gate8.1376/SHA c2b79d95….00 얼굴LEFT 밝은회색가드주먹·lowerfist복구,02등orange/green파편/무테gray연기·손목. source주먹위치/조각수/연기범위/작은손형태와발끝정확도ClaudeQA.
- **108 선택4targets+base** 2판: unit_108/robot_set/PREFERRED_DELIVERY_20261117_EYE.json. qa_motion_20261117/plate01 gate3.8944/SHA12d03156…,plate02 gate7.3306/SHA28ca35f8….00/04/15 grey모션무테/분리/부분투명,01짙은뭉게연기+partial bodysource가림. 실제redorangeweapon은solid유지. 회색RGB검토완료,가닥수/농도/원본partialhardcut·모든body구조/좌표·palette정확도검수.
- **114팔높이2entry**: unit_114/robot_set/PREFERRED_DELIVERY_20261117_EYE.json. qa_arm_height_20261117 gate7.5812/SHA c47e8998….실제INDEXはJanM1Astray, EYE notes의Deathscythe기체명은잘못됐으므로nativewhite/bluegrey/redorange기준그림.10 SCREENLEFTforearm sourcechest/shoulderheight와연결맞춤.정확높이/기울기·어깨/다른팔/발끝/원본색면적QA.
- **110 effect추가작업**: 기존user_report_repair_20261116_2204/sheet01 smoke02·파편후보와sheet90 thin27을재사용검토하고,00/07넓은metal면만실제편집. qa_motion_topology_20261117 gate4.6286/SHA8ff041c7…에서metalbevel은줄었으나회색합성에서어두운backing면남음. qa_sparse_lines 실제추가생성중,완료판정아님.
- 이전root97/176/181/261262/276/279/460/465/462/463 등39/40과 ROOT_RESUME_DELIVERIES_20261117.json 참조. root현재24선호판집계는전체완료/설치수아님,279위4부분검토후보별도.

## 새agent전달

- 452/75 전체32자세 preferred4판: unit452/robot_set/SHEETS/REDRAW_452_75_RESUME_20261117.json.각기체PREFERRED_DELIVERY 및SHEETS/DELIVERY_NATIVE_REDRAW/HANDOFF.45204/09한팔만머리옆/반대팔가로 source복구,05opaque검정block,09무테반투명잔상.75은백면복구.45202/7501 A1외곽샘플기록/코드정리없음.
-225229232 전체45원본=44HD후보+1검정flash원본,선호10판: ROBOT_225_229_232_DELIVERY_20261117.json/HANDOFF.232누락4번째mintC고리실제복구.225선폭/229균열/232반지름·파편exactClaudeQA.
-379392393394399 선택9판: QA_379_392_393_394_399_DELIVERY_20261117.json/HANDOFF.399는fist_delivery최종.39208 blackbar strictalpha255는미충족가능,393tinycream particles/394반투명redpink호가닥 검수.
- 이전agent270274/266269283/236237444/193194204/205206/361367416/357359365371/448453454455457/445446447/224231238249380/459464468선호경로39/40및rootmanifest.latest_agent_delivery_manifests참조.

## 계속진행중 / 겹치지말것

root110 qa_sparse_lines 실제생성,118/119 선택QA source패킷4판실제생성중. agent280=111기존postEYE QA재생성제외/112기존준비packet재개/113분리몸통및white속도선/117sheet0203크기팔레트실제4판생성. agent281=1099targets모션/연기/source12등짐. agent361=373374375미해결조사/작화와381..390후보조사.

스타일기준unit1/pose00/generated.png SHA77bc2d7c… 유지확인. 모든후보source정합·분할·게임확인·독립승인은Claude에게남음.

## 110 최종 현재 후보 전달

- unit_110/robot_set/PREFERRED_DELIVERY_20261117_EYE.json. qa_motion_topology_20261117/**qa_sparse_lines/candidate_sheet.png** SHA05539eccc1ed1a49eecf1b04324f0a12c1ae3a2e011f73c31a67f20b9fcd4155 gate4.6286가선호. 회색합성에서00/07이전어두운막/metal면이사라지고분리palegreyline사이실제투명공간확인. 원본가닥수/경로/범위·density/sourcealpha/기존body가림은독립QA. 부모8ff041…은superseded.
- 기존11/16실제source sheet01 smoke02/작은debris후보는새로재생성하지않고 **layout_legacy_smoke02_only.json**으로02만검토재사용. 원본layout편집없음. root현재25선호판(전체완료/설치수아님),279부분검토후보4별도.

## 118/119 선택QA4판 전달

- 각 unit118/119 robot_set/PREFERRED_DELIVERY_20261117_EYE.json.1186targets+rollingbase10 qa_pose_scale_20261117/plate01/02 SHA caf6f271…/555013b0…,gate4.7863.18/20팔source어깨높이·19자체굽힘·14/17각원본openhand·21backview,두어깨blade/orangetips/full여백복구관찰. exact손끝/visor/greyheadblade/bounds/판별색·파트소유관계QA.
-1195targets+base14 qa_motion_scale_20261117/plate01/02 SHA5533c50b…/96330727…,gate4.3542.09회색RGBA에서white/palecyan모션무테/부분투명,03sourcechestarm/02·04·07원본크기fullfeet/binders. exact왼작은줄수/RIGHT3가닥/큰호폭·fade/path·solidbody구분·mint빛면적·자리·크기Claude검수.
- root선호29판(전체완료/설치수아님),279별도부분검토후보4.
-109新4판완료: ROBOT_109_DELIVERY_20261117.json/HANDOFF.전체26자세8선호판(새4+기존선별4),9모션targets+12등짐 source개선.01smoke하단hardcut/07·14·23잔상폭·밀도·수QA.
-111재생성제외proof/112113117新4판완료: unit113/robot_set/qa_source_20261117/DELIVERY_111_112_113_117_20261117.json.분리01 tinyV/partialbody·white속도선exact/13openhand·4graytips/117registeredscale·source색QA.
-3733743754판완료: QA_373_374_375_DELIVERY_20261117.json/HANDOFF,최종375두판포함.자체layout sheet_origin [x,y]로정규화완료;공식layout/RAW불변.次381382386390실제4판생성,root141144146148149조사예정/agent123124126·131132136137139진행.

## 追加 전달 및 현재 작업 갱신

- 123/124/126: test_current/parts/ROBOT_123_124_126_DELIVERY_20261117.json 및 HANDOFF. 83원본=81HD후보+2순색원본 runtime, 선호15판(새5+기존10).12327 이중머리 구조가 단일helmet처럼 읽힐 가능성은 남은 검수.12417 white diagonal/18redtip POD/20greyarm/27face,12605회전blur 새작화.12603/06은 실제원본에 대형FX없음, 임의추가안함.
- 131/132/136/137/139: unit131/robot_set/qa_source_20261117/DELIVERY_131_132_136_137_139_20261117.json. 실제11회/RAW11/선호10판/63fresh target poses.13608은 전체검정 원본 runtime 증거별도.131은 qa_streak_shape SHA89e6e5b9… gate4.0024 최종선호: 흰core감소/얇은pinkred분리가닥으로추가수정, 정확수·경로검수남음.137원본grey-green/opaqueBLACK05/white09,139작은warmredorange돔색,132자체copperpalette/greyhand 복구.
- 381/382/386/390: QA_381_382_386_390_DELIVERY_20261117.json 및 HANDOFF. 4선호판 gate4.427..7.926.386 parallel_lines_delivery는12얇은줄전달가능/00원본3tiny enclosed alpha holes중2개만남아00held.추가구멍편집은HTTP400 moderation_blocked로반환없어우회하지않고실패JSON보존.390 layout_safe_delivery 실제새소스하단여백후새생성(HDresize없음),큰tipgap유지/원본1nativepixel tinygap하나누락.386/390blackalpha median254/253으로strict255미보장, 원본대조필수.
- 224두QA판 자체layout 좌표8곳을[x,y]로정규화하고 embedded mapping6곳과각SHA도갱신. LAYOUT_ORIGIN_AUDIT_20261117.json/단위정규화증거참조. 공식layout/RAW불변. 오래된 ALT layout_alt 대신 QA layout사용.

현재 root=141전체2판+144/146/148/149각선택1판, native+실제4xBRZ+canonicalstyle의 실제 builtin6호출진행(cell158/159). agent281=120/121/122선택3판(120새후보이미저장); agent280=150/156/166/171/178/179미해결source확인후새작화; agent361=389원본밝기/크기검토후필요범위작화. 모든후보는사용자승인/설치완료아님.279사용자반려4자세는앞선부분검토상태계속유효.
