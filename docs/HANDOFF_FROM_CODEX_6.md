# Codex → Claude 핸드오프 6

**현재 교환 파일입니다.** 이전 상세 제작 기록은 HANDOFF_FROM_CODEX_5.md의 역사 기록이며 현재 상태는 이 파일을 우선합니다. 정확한 바인딩/그림SHA/원본 계약은 PRODUCTION_ART_BATCH_CURRENT.json, 검증 안내는 CLAUDE_VERIFICATION_QUEUE.md입니다.

## 현재 상태

- **1,845개 고유 작업 대상 연결·대상 굽기 완료**. 새 연결뿐 아니라 기존 그림 교체와 actual 팔레트 변형을 포함합니다. 기체 수/전체 누락 감소 수/실제 HD 재생 검증 완료 수가 아닙니다.
- **1,845개까지 3f63b817로 GitHub 푸시 완료**. 후속기체별packed와새effects후보인수중이며아직현재완료수에미포함.
- 전체 ROM 누락은 마지막 독립 감사11,358종 이후 재집계하지 않았습니다. 다중IMG21%미판정·BG는 그감사 밖입니다. 위 작업 대상 수를 빼서 잔여를 만들지 마세요.
- Codex는 그림 제작·실제 원본 계약·연결·굽기·커밋, Claude는 독립 그림/색/레이어/실제 HD 재생 검증 담당입니다. CRC·메모리 nonempty·굽기 오류0은 품질 판정이 아닙니다.
- **최신 EXE 번들은 미갱신, 열린 사용자 게임 창은 유지**했습니다. C: 소스/에셋/저장소 반영이 실행 중인 구EXE에 보였다고 주장하지 않습니다. 컴퓨터를 끄지 않습니다.
- ROM·세이브·설정·로그·자격증명·구운sqlite은 공개Git에서 제외합니다. source와그림/생산계약/캐시/핸드오프만 커밋합니다.

## 진행 중 분담

- next_key_art: 윙제로0/w2·헤비암즈2/w8 실제 일반색9 후보 인수/연결중. 이후 다른 큰 기체/무장 원본을 채집·제작. source 이름만으로 합체장면의 기체 소유를 단정하지 않음.
- next_shape_art: 캐릭터컷인 native 입력을 분류했지만 오공비 외 확정된 새캐릭터 후보가 없어 마징카이저295/1192+330 actual 기계11고유/16OAM 한벌 제작중. 머리32+16 연속/오른쪽 반전, 나머지10OAM 기존의존 보존.
- effect_live_palette:19678 첫노랑58+다른5actual팔레트18=76계약/64shape 제작·연결·굽기완료. 다음21721/22048 actualFX 제작. 같은그림 다른색으로 빈곳을 메우지 않음.
- root만 라이브 메타·DB에 씁니다. 후보 인수→원본/중복 계약 확인→연결→명시 대상 굽기→manifest/문서→캐시SHA동기화→커밋/푸시. 미설치·실패·보류는 완료수 제외.

## 설치 보류: 오공비 눈6 / 기존fullcutin17

실제+210/+225/+240 OBJ 눈6은 exact/indexed0으로 확인됐지만, 기존 pilot_bg_22825(fullcutin17)의 왼쪽 닫힌눈이 native OBJ x120..136보다 왼쪽에 그려져 있습니다. 새 눈을 정확한 좌표에 올리면 닫힌눈이 별도로 남고 피부 사각형 경계도 보입니다.

얼굴교정 imagegen2회와 생성얼굴 영역[440,32,684,228]만 기존HD에 넣는 시도를 했습니다. 좌석/팔/의상 등 영역밖RGBA불변은 face_only_preservation.json에 보존했으나 최종 제작 조립에도 정합/피부경계가 남아 **설치금지 유지**합니다. 공유runtime·라이브fullcutin17 파일은 건드리지 않았습니다.

- 보류 근거/최종 후보를 **graphics/review_pending/wufei_eye_animation/**에 보존했습니다. STATUS.json은 install_allowed=false/linked_in_runtime=false/counted_as_completed=false입니다.
- 해당폴더는 라이브parts/cutins 라이브러리에 연결되지 않았고 완료6으로 세지 않습니다. 재생품질을 통과한 그림으로 배포하지 마세요.
- 원래 작업자료: test_current/parts/borrowed_shape_rework/wufei_eye_animation_missing/. 제작조립은 실제HD재생증거가 아닙니다. 얼굴 정합과 눈모션/피부경계가 해결된 뒤에만 함께 반영해야 합니다.

## 최근 제작에서 반드시 확인할 것

- 합체1920 그레이트10/마징카이저17,1560 마징카이저3/그레이트3은 기존 그림 교체입니다. 새 누락33종 감소로 세지 않습니다. 연속 머리/단일 작은기체를 원래 비겹침OAM으로 나눈 근거·반전·기존의존을 보존했습니다. 마징카이저1560 윙끝10HD경계pixel,Great1560 alpha>0경계7HDpixel은 시각판정 대기입니다.
- 마징가Z머리2는ROM14723/팔레트2636 bank0 actual새연결. 몸통11의존 유지,32+16 연속머리/오른쪽역반전. native몸체+후보머리 제작조립을 실제HD재생으로 세지 않음.
- 알트론4/w18 녹색은 원래 기체색으로 확인해 조명가능성 보류를 정정했습니다. 드래곤헤드/늘어난팔/대형몸체8 추가,기존1보존. 큰crop 안의 팔·다리 구조 발명 위험은 Claude 확인 필요.
- 격룡신374/1488 +90/145/150 6은 actual 주황상태 전용이며 일반 녹청 기본색 완성이 아닙니다. index형태 기존매칭0, +145 실제가시84픽셀 조각 포함. phase를 일반색으로 잘못 판정하지 마세요.
- 소드 스트라이크/루즈 첫18계약→15고유,후속18→17고유. 같은rawbytes/w/h/실사용색의 동일칼/조각만 공유. 다른기체의 그림 재색칠이 아닙니다.19/42의미분류5픽셀OAM8은보류로남아 자세전체완료아님.
- 천룡신/테카맨12 중 **247/1009+150 OAM10은 cached source확정이나 native가시면적0**. 라이브메타에 source_native_visible_area=0/source_native_visible=false/source_rendered_cache_observed=true,manifest.cached_only_source_bindings로 구분. 그림이 화면에서 보였다고 주장하지 않습니다.
- 373/1483 FX8의 cell0 극박화이트/시안흔적은 지원면적1.684배라 두꺼울 위험.368/1462 FX14는 첫 금속판형 음영 출력폐기후 재제작했지만 흰6의 계단선/희미한gray외곽이 남습니다. actual초록2는 키잔여가 아님.
- 21954는 초기파랑/백색 라벨을정정:actual노랑주황11/민트청록11.22186은밝은17/암색16 방전.19678은노랑58+다른actual5팔레트18,고유64shape. 색별 독립그림이며76새형태라는뜻아님.
- FX의 작은분리성분 제거·얇은선·생성rim·직각절단경계·구멍/분리영역·원래단색fill은 각 graphics/HANDOFF와production_report의 위험을 실제장면에서 확인해야 합니다.
- 앞선12077 별/파편95 중 빈출력17 복구,22410/92493대각선,22030파편v2,jade6참조캔버스,21819반원/점선,21080단색fill,Getter2/3독립분리v2,Behemoth투명홈교정은 이전이력5/검증큐 참조. 옛 실패후보를 설치본으로 보지 마세요.

## 공통 제작 / 출처 규칙

실제 rendered cachedOBJ+같은프레임OAM의 indexbytes/actual팔레트/hash/attr/크기와 전체native문맥을 사용합니다. end-frame VRAM·기체이름만으로 추정하지 않습니다. 실제캐시원본이 확정되면 소유ROMIMG를몰라도resource=None으로제작가능하나 첫raw일치후보를단독소유확정으로바꾸지않습니다. 미관측 확장은 단일IMG/PAT+actual16팔레트 근거/observed=false를 보존합니다.

생성자체RGBA만 사용하고 원본RGB/alpha를HD에찍지않습니다. 다른기체재색칠금지,이웃파츠가사각crop에섞인master후보폐기,원래떨어진홈/레일/절단면보존. 첫5,263바인딩불변. 아틀라스를 바꾸면 해당전체바인딩 재굽기. source계약과같은raw/실사용색중복만보존하고완료수에서중복제외.

## 런타임 / 코어 소유권

**코어 소스 해제**. Codex는 이 제작에서 공유 runtime/코어를 수정하지 않았습니다. 마지막 확인 DLL SHA256은 a6d80b29119f7c18447725acc4e0e5c8fb88cdda07d8cef6ccb106e936b64fe0,Claude95ba46f0/d98c4226 cachedOBJ 경로입니다.

- 설치도구만 Windows atomic replace 일시 읽기잠금의 최대3초 재시도와 source가시성출처필드 보존을 추가했습니다.
- 빔/폭발의기체앞뒤,컷인의기체앞/대사창뒤,윈도우/플래시/자기페이드/sub/UI/폰트/맵은 Claude의 공통 runtime 검토 대상입니다. BLDY/MASTER_BRIGHT 등 기존한계를 임의해결했다고하지않음.
- 코다르273/1120의4조명계약(채널거의+3),20966/19887의기본4외50fade,22378late65,21774/21775섬광45는 새 기본형태로 무한재제작하지 않고 source_contract_extensions/기존인계로 넘겼습니다.
- 최신EXE재묶기·실제HD재생·60fps/입력/패드 검증은 미실행. 구compact1.28GB는최신그림없어live교체금지. 현재sqlite에는oldkeys가남아있으며공개Git제외.

## 기록 운영

작업 시작/방향변경/인수/완료 모두 이 파일 갱신. 오래된현재상태삭제.300행또는20KB넘으면 HANDOFF_FROM_CODEX_7.md로이동안내. Git/이전파일은역사기록이며새후보에옛검증합격을승계하지않습니다.

## 새 제작 입력 검사: 원본 포함영역의 생성그림 공유

동일 confirmed IMG/actual전체팔레트에서작은raw사각형이큰raw사각형에포함되면해당생성HD도동일영역을공유해야합니다. Z2v1이이조건을위반했음을제작계약검사로확인, v2후보는작은셀만큰셀의동일생성그림으로교체/밖RGBA불변. 기존Z2 두ID그림교체·전체2재굽기완료이며완료수+2아님. 연결도구에새작성계약내raw포함/생성RGBA일치검사를추가했습니다. 원본RGB/alpha찍기가아니며전수HD품질검사도아닙니다. resource/팔레트/소유불명 또는이미연결보존된계약끼리는검사범위밖. 앞으로확정된공유영역이서로다르면라이브쓰기전에중단합니다. 옛Z2후보를거부한음성사례생산검사기록도보존. 기존전역의유사문제는Claude별도검토요청.

## 최신32신규 / Z2동일ID2 v2 완료

마징카이저295/1192+330의26OAM 중16미연결OAM→11고유를새제작/연결(IMG14749 9/14723 2),기존10의존보존. source포함2쌍은동일생성HD공유.21721 FX11의source포함2쌍도공유일치통과,22048 FX8과윙제로속도줄2도추가. Z2v1은새생산guard에서차단됐고v2는1공유쌍통과/작은셀밖RGBA불변/기존2ID수정,새2로세지않음. 총34대상굽기오류0/6.1초,manifest Z2 SHA갱신. 실제HD재생품질은Claude대기. 원본소유불명/이미연결보존계약은이guard범위밖임을유지.

## 최신114 제작 완료

알트론/베스나차량8·진하이메뉴버17·진겟타공격세부5·FX21995(20)/20050(10)/21632(15)/21737(5)/19999(34),총114굽기오류0/6.4초. actual반복OAM은raw/크기/사용색으로동일그림공유,역할미확정tiny와속도줄/충격광은기계완료수에서제외. 21632source포함1쌍/19999의6쌍생성공유guard통과. 소립자제거/곡선두께/내부질감/큰몸체의구조발명위험은각HANDOFF로Claude판정대기. 설치도구가source_engine원본필드도보존하게했으며공유runtime변경없음.

## engine1 원본 연결 자료 / 역할 정정

샌드록forecast기체2·weapons17,데스사이즈forecast기체3·weapons17은cachedOBJ1+subOAM/parts와같은epoch의actual바이트/팔레트로CRC재검산후기존exact연결확인. 그림누락0으로중복그림제작안함. **graphics/source_contract_extensions/engine1_named_units/**에계약/원본그림/인계보존. 이것은기존그림품질/실제서브렌더정상판정아니며미표시는Claude공통runtime/상태검토요청. helper는producer전용,공유코어미수정.

104/w437붉은파트를key담당이코우지/마징가로잘못불렀던명명은폐기. 실제초상화는가이이고source9416 raw/실제AR팔레트1592/1613/9436근거로**붉은아스트레이합체관측4**후보를shape담당이제작. 세부owner_unit=None,104청색본체나마징가로명명/그림재사용하지않음. 이4는아직연결예정이므로현재완료수미포함.

## 다음 연결 / source 부분교차 검사

톨기스III13은기존다른색indexed그림을actual RGB로새제작하는색기준rework이며미연결13종감소로세지않음. source1200/PLT1201 bank0유일일치,source부분교차4쌍은동일생성HD공유. 새연결guard를포함뿐아니라부분교차전체로확장. 기존Z2v1거부/v2통과1쌍·터보11의3쌍·21721의2쌍을제작입력기능사례로확인(전수HDQA아님). resource/actualfullpalette가불명확하거나이미연결보존된부분은범위밖. source계약의IMG교집합rawbytes가다르거나생성HD교집합이달라지면live쓰기전중단.

후속실제SOURCE에서픽셀계단원형21737·불투명cream배경21427·격자침범22198은첫출력폐기/생성도구재교정한최종본만인수. 빛/파편/단색면의두께·추가명암·작은성분제거위험은각HANDOFF로Claude에게남김.

## engine1 도구 설명 정정 / 다음 생산

위4source의capture_meta 설명문이공통helper명으로남은것만실제producer privatehelper경로로정정해archive에도동기화했습니다. 원본hash/bytes/palette/epoch불변. MobiusZero본체/건배럴12(9관측단계)후보인수,전함포탑9생성의중복포구2는그대로인수하지않고imagegen교정중. 같은한기체의여러작은source를픽셀불변packedatlas로합쳐한번에연결하는제작입력최적화를key담당에게요청(다른기체/FX혼합X,원래source별계약/HDnativeSHA보존).

## 최신134 제작 완료

톨기스III actual색13 rework·붉은아스트레이합체관측4·SEED구아즈/칼라미티/금색기체16·FX21284기본26/22439(15)/22390(13)/21836(11)/21427(22)/22198(13)/진하이메뉴버충격광1 총134대상굽기오류0/6.6초. 원본source부분교차공유검사Tall4쌍/21284 7/22390 4/21836 1/21427 9/22198 10통과. shape/색/알파·입자제거·순서의실제게임판정아님. 21284 ring밝기변형2는fade_two_contract.json에보존/완료수제외. 파일명위치차이로일부패킷인수가중단됐던것은실제생성파일경로를확인해재개했고,기존인수완료ID를보존해중복ID증가없이134를모두구웠습니다. 설치도구는이제필수입력파일을쓰기전에전부확인합니다.

## 다음 인수 대기

모비우스12·unit50회색전함포탑9·프리덤14·검정금색기체108/457의12는같은기체별무손실packed계약으로받았습니다. 각source와packed의HD/nativecropRGBA SHA동일,원래raw/fixture/frame/attrs/pose의존보존. 다른기체/FX를섞지않고metadata전체쓰기횟수만줄입니다. Sandrock쇼텔3은생성alpha<64만제거/고알파불변과연결대근거보존,Justice/Fatum10은다른색indexed의actual색rework. 아직이후보는현완료수미포함. 전함폴더명dominion은임시명:catalog50은아크엔젤/실제관측회색포탑으로만기록하고도미니온확정소유로부르지않음.

## 알파 전처리 재현 근거 보강

FX담당이최근31 source폴더에ALPHA_PROVENANCE.md를추가했습니다. 필터전generated원본은보존,기존threshold>=220 이진화→Min3→Max3→ownbbox등록은연광/가는선손실위험이있습니다. 기존candidate그림/라이브를몰래바꾸지않고이정책과원본을해당graphics폴더에복사해Claude우선검증항목으로전달합니다. 앞으로생성alpha보존기본이며개별정리만명시합니다. 잘못된기존FX가전부해결됐다는뜻아님.

Sandrock w15+270 actual색rework6은생성2회가좁은연결편을손/장갑으로부풀리고후광이남아설치보류. source원본/실패gen/PRODUCTION_HELD.md 보존,원본stencil/색맵으로억지통과시키지않음. 이6도완료수제외.


## 최신 273 제작 연결 / 후속 생산 중

같은 actor별 packed12묶음137계약, Sandrock쇼텔3·Justice12·SwordStrike8·Deathscythe4·Altron15·dragonhead1, actual FX19600/20498/21673/21748/22060/21869를 인수했습니다. 입력274 중 중복1 제외 **273개** 연결·굽기 오류0/7.4초. 누적 **2,118 작업 대상**이며 전체 ROM 누락 감소 수가 아닙니다. 정확한 ID/source/atlas SHA는 PRODUCTION_ART_BATCH_CURRENT.json. 실제 HD재생/색/절단면/레이어 판정은 Claude 대기입니다. Providence77_665 OAM2는 native visible10픽셀뿐인 계약, source 전체 보유와 가시 확인을 구분합니다. Forbidden31픽셀 암부 보존, LauncherRouge 상하몸체 source32와관측32.296875의 반올림차이 보존.

Sandrockheated270 6은 graphics/review_pending/sandrock_heated270에 실패그림/원본/계약/STATUS 보존, 라이브 연결·완료수 제외. Wufei6도 기존 보류 유지.

현재3에이전트는 각각 후속 실제기체/무장, 형태·실제색 재제작, 실제팔레트 효과를 생산 중입니다. FXphase21959/22303/22044/21324/21774와21758 발사광6의 후속연결 진행 중. IMG12281 46은 중앙면 투명구멍 때문에 아직 인수금지, 다른 실제팔레트 생성alpha와의 구조동일성 근거를 요구했습니다. EXE재빌드/사용자게임재시작/독립QA는 하지 않았습니다.


## 후속60 연결·굽기 완료 / 12281 보류

phase21959(6)/22303(7)/22044(7)/21324(7)/21774(2)와21758발사광6 총35, 굽기오류0/6.5초. 런처스트라이크Agni260 10(새8·actual색교체2),런처루주초기15 추가25 굽기오류0/5.7초. 누적 **2,178 작업대상**. 작은연결편·포구·공유접합·alpha64정리·FX광원과얇은선은Claude판정대기. phase fade168은완료수제외.

12281효과46 후보는별도청록생성RGB와정상민트alpha공유이나두형상IoU .92855,RGB연장19,667px으로자동설치보류했습니다. 원본mask스탬프없어도다른생성형상alpha공유가정합을보장하지않으므로imagegen재교정요청. 아직46개live아님/완료수제외. 현재3에이전트계속생산중. 사용자EXE/열린게임은변경하지않음.
