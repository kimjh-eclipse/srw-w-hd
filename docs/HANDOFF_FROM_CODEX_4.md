# Codex → Claude 핸드오프 4

현재 교환 파일입니다. 이전 제작 기록은 HANDOFF_FROM_CODEX_3.md에 보존합니다. 현재 상태는 이 파일을 우선합니다.

## 현재 상태

**수량 구분:** 이전 ROM 전수집계의 HD누락11,358종은 전체기준이며 아직 재집계하지 않았습니다. 이 문서의 작업묶음 수에는 기존그림교체·실제팔레트변형이 포함돼 전체누락에서 단순차감할 수 없습니다. 전체완료율은 보고하지 않습니다.

- **코어 소스 해제**. Codex는 코어와 공유 그리기 코드를 수정하지 않습니다.
- Claude의 95ba46f0 / d98c4226 반영 완료. 기본 DLL SHA256 a6d80b29119f7c18447725acc4e0e5c8fb88cdda07d8cef6ccb106e936b64fe0. cachedOBJ API도 포함합니다. EXE 번들은 아직 이전 DLL이므로 재묶기 필요.
- Codex는 그림 제작·정확 계약 연결·대상 굽기 담당, 독립 색/키/실제 재생 검증은 Claude 담당. 기계적 입력 검사만 Codex가 수행합니다.
- 현재 이번 작업묶음146개고유타깃 연결·대상굽기완료,굽기오류0. 기존그림교체와팔레트별새계약이포함되므로전체누락감소146이라는의미가아닙니다. 넓은 전수 굽기는 아닙니다. 라이브러리·저장소 쓰기는 root 한 명만 수행합니다.
- next_shape_art: 샌드록 실제 팔레트 자세 재제작. next_key_art: 데스사이즈 다음 무장 자세. effect_live_palette: 20498 다음 효과 그룹. 모두 라이브 파일과 코어는 수정하지 않습니다.
- 컴퓨터 종료 금지, 사용자 테스트 창 유지, ROM/세이브/사용자 설정/로그 푸시 제외.

## 이번 제작 묶음 (연결·굽기 완료, Claude 독립 검증 대기)

|묶음|수|제작 위치|Claude 확인 대상|
|---|---:|---|---|
|겟타 무장 shaft|2|test_current/parts/getter_remaining_effects/next_effect_source/pole_forms|getter_cutin +56/57/59/90/110/126/207/234. 절단 이음매·잔상·도끼 축. effect 태그 없음|
|21948 효과 새 계약|17|test_current/parts/effect_21948|unit413 weapon1610 frame360+112~128 및 frame600+31/63~94. 기존 exact14개 보존; 새17개만 연결. 흰 중심/민트 가장자리 접합|
|코다르 분신 cached14|14|test_current/parts/borrowed_shape_rework/codarl_clones90_cached_pose|unit280 mechanical_cutin_168+90. 26 OAM/14 unique. 이전17 입력의 phantom3개 폐기·미설치. 칼과 양쪽 분신 연결|
|데스사이즈 일반7086|20|test_current/parts/deathscythe_normal_pose|duo_map_attack.state+120. v1 폐기, continuous 후보 사용. 뿔 금색/눈 초록/회색 장갑·날개/팔/몸통 이음매|
|20498 회색 곡선|2|test_current/parts/effect_20498_gray|unit413 weapon1610 frame600+31 OAM3/4. 연속 상하 두 조각. 전체20498 완성이라는 의미 아님|
|데스사이즈 접힌날개 자세|14|test_current/parts/deathscythe_next_pose|duo_cutin.state+180. 15 OAM 중 기존7086 1개 재사용,14개 연결. 얼굴을 가리는 날개는 원본 문맥. 작은 연결부·색·키 잔여 확인|

각 폴더 install_report.json에 실제 binding 및 IoU 경고를 기록합니다. --defer-shape-review는 통과 판정이 아니라 독립 검증 대기 표시입니다. 굽기 후 아래 결과를 갱신합니다.

## 이번 반영 결과

- 첫67종: bake_parts 오류0, 6.0초. 샌드록16종: 오류0, 5.4초. 이는 제작 굽기 시간이며 게임 FPS 측정이 아닙니다.
- 21948의 회색2종은20498과 실제RGB/크기/인덱스가 같은 계약이라 binding91986/91987을 공유합니다. 최종그림은 연속곡선20498 atlas로 연결됐습니다. 서로 다른 기체 팔레트를 재색칠해 대체한 것이 아닙니다.
- 샌드록16:90624/23931/90626/90638/90622/90611/23523/90640/90602/90608/90605/90629/23914/90612/90596/23925. 기존RGB 정확일치 항목의 그림교체입니다.
- 정확한 전체번호·atlas해시는 `docs/PRODUCTION_ART_BATCH_CURRENT.json`. 각 `graphics/rework_*/pose_contract.json`, `installation_report.json`, `ART_REVIEW_NOTES.md`도 저장해 Git에서 원본계약과 제작검토점을 추적할 수 있게 했습니다.
- `shape_review_required` 경고: 겟타pole slot8,21948 slot8/3/4,20498 slot3/4. 나머지 입력겹침기준은.70 이상이지만 시각적완료 판정은 아닙니다. 키색·색번호·실제재생 수치는 Claude 미측정입니다.
- native_materials/material_slots 캐시는 이번 라이브러리에 맞춰 재생성합니다. EXE 재묶기는 Claude 그림/재생검증 완료 뒤로 남겨둡니다. 실행 중인 사용자창은 건드리지 않았습니다.

## 후속 연결·굽기 결과

데스사이즈 닫힌날개/낫14종(`duo_map_forecast.state +0`)과 20498 흰색·민트 신규7종을 연결·21종 굽기완료(오류0,5.6초). 20498의 기존32 exact는 보존. 별도 실제재생 검증은 하지 않습니다.


- 낫날 좌우2종 추가연결:92083/92084,atlas deathscythe_scythe150_continuous. `duo_cutin.state +150`에서 동시에붙는32×16 두조각이며 애니메이션2단계가 아닙니다. 64×16 연속그림에서분할,기존13OAM 의존은graphics/rework_deathscythe_scythe150/pose_dependencies.json. 접합/끝각도/손잡이·낫색을Claude확인.
- GitHub main에 e837cf4c까지푸시완료(이번83종 및이전누적소스·Claude런타임수정포함). 후속그림은다음커밋/푸시예정. 이동된제작도구18개는97ad6e2c로보존. ROM/세이브/설정/로그제외.
- 설치기가계약과installation_report를graphics제작폴더에자동복사하도록개선. 재제작의원본계약·입력경고가test_current정리로사라지지않게합니다. 공유실행코드변경없음.


## 샌드록 확대공격9 및 낫날2 후속굽기

- 샌드록9종 연결:38668/38635/38649/38647/38622/38652/92091/38633/38628. atlas sandrock_weapon_closeup_cached_pose. 기존8교체+unbound1신규, 일반몸체16과공유없음. `sandrock_closeup_cutin_full.state +0` 원본은플래시로가려지므로원본/HD표시성공은Claude가다른전후프레임으로판정해야합니다. 셀4/6추가생성,원본빈간격·작은몸체조각·V-fin/칼색·대사창가림검토.
- 낫날2+샌드록9,정확11종추가굽기완료(오류0,5.4초). 전체이번묶음115개고유타깃. 모든타깃은 metadata에도 pending_claude / independent_visual_verification=false 명시. 자동입력검사통과를시각완료로승격하지않습니다.

20498 jade 신규6연결·대상굽기완료(92094~92099,오류0,5.4초). 기존exact4보존. 단색3751420720의옅은gradient미해결은Claude판정대기이며단색완료로보고하지않음.

- 누적이번묶음121개고유타깃. 실행용색상캐시도최신 bcc822530c3b5c1185ea435eff6bb4307f6c7a682d402bee58c46ef55787296d 라이브러리로갱신완료. 실제재생/색품질판정은하지않았습니다.


## 데스사이즈 초록궤적10 입력 경고


- 92100~92109, atlas deathscythe_green_arcs_7084_7085. 7084 두actual팔레트각4 +7085가는궤적2.
- slot4(92100)/slot6(92101) 입력alpha IoU .164/.179로낮고다른8개는.95~.997. 이2개는 제작레이아웃/선폭누락가능성을제작담당에돌려보냈습니다. 이후얇은2개새그림기하교정후10개전체굽기완료. 입력IoU.682/.683으로.70미만경고는남아있고실제재생판정없음. 임시연결을완성으로세지않습니다.
- 이부분당시131/121진행상태는종료. 현재전체작업묶음146종모두대상굽기완료,시각검증은대기.

19600 실제관측잔여2종도신규연결예정(기존73exact보존).

가는궤적2교정본을같은atlas에반영하고10개전체굽기완료. 다른8개그림불변,입력기하교정이며Claude시각판정은대기. 19600후속2도함께대상굽기완료(12종오류0,6.6초).


## 사용자최신우선순위: 전체 실제누락 신규제작

- 이미연결된샌드록무장7교체는보류. next_key는 IMG22062/22054 실제미연결4 제작으로전환. shape는진행중그레이트10인계뒤큰미연결기체/무장그룹으로전환. effect는19645새3뒤상위큰미연결효과그룹제작.
- `scripts/assets/plan_missing_art_batches.py`로과거누락계약을현재라이브exact/indexed와대조한제작선정큐 `test_current/parts/missing_production_queue/current.json` 생성. 새ROM감사나전체잔여집계가아님. 옛팔레트/미관측팔레트는실제표시팔레트확정후제작. 등록있음은그림품질합격을뜻하지않음.
- 22378late의새67RGB계약은실제로고유형태2의연속fade팔레트입니다. 67장을재색칠해채우지않고, 두기본그림+실행중fade계약으로분리해Claude에인계. 다른큰효과그룹제작을우선합니다.
- 그레이트10과19645진짜미연결3연결·대상굽기완료(13종오류0,5.3초). 그레이트10의분류는exact1교체/indexed8교정/진짜unbound1추가입니다. 10모두를전체누락감소10으로계산하지않음.


## 최신확인요청과잔여

- 최신라이브러리SHA256 bdc967ee8584372e93b80c2552fad673c9ce5f8ee6f642e0aa4c9a0949b0e212. 실행용색상캐시동기화완료. 이번146타깃모두굽기완료,독립시각검증대기.
- 19645 새3:92122/92123/92124. 첫두가는slash의입력IoU .558/.640 경고. 일반unit본체의분실검사와별개로반투명폭/원본선과위치·베기끝색을Claude가봐야합니다.
- 19600 새2:92110/92111. unit413 weapon1610 frame360+112 OAM13 /+114 OAM16,두실제팔레트신규그림.
- 그레이트신규10:82822/92113~92121. 기존재제작9종의존계약보존. unit299 mechanical_cutin168+0,HD-enabled프레임버퍼는순수원본증거가아님. 머리4/5연속그림분할/기존팔과새다리접합/작은빨강7/가림은Claude확인.
- baked.sqlite은로컬제작산출물이며Git에추가하지않습니다. 낡은1.28GBcompact후보는현재신규그림이없으므로교체금지. EXE·배포팩은Claude검증뒤새코어포함재묶기필요.
