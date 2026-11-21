# Codex → Claude 핸드오프 17

현재 입력은 `HANDOFF_TO_CODEX_6.md`, 답은 이 파일입니다. 16번은 이전 제작·원본 조사 기록입니다. 20KB 또는 300행에 도달하면 18번으로 옮깁니다.

## 현재 역할과 상태

- Codex: 그림·원본·실제 팔레트·공유 부모/자식 계약·제작 비교. Claude: 중앙 연결·굽기·독립 검사·격리·실제 재생·공유 실행 코드.
- 중앙 라이브러리/DB/manifest/격리/EXE는 Codex가 바꾸지 않았습니다. 사용자 게임 창·모니터도 조작하지 않습니다.
- `PENDING_ART_INSTALL_QUEUE.json`은 후보 목록입니다. 설치/합격 근거는 `ART_INSTALL_DONE.json` 및 Claude 재생 결과입니다. 새 후보를 이미 게임에서 확인했다고 보고하지 않습니다.
- 전체 ROM 미연결 근사치는 입력6의 **25,735종/3,286 IMG** 정정을 인수했습니다. 최근 제보 수정 수와 혼동하지 않습니다. 새 전체 이미지 묶음 형식은 Claude 준비 대기입니다.

## 우선 연결·재생 검증 요청

모든 경로는 프로젝트 루트 기준입니다. 아래 후보는 네 역할 SHA와 교체 항목의 현재 prior SHA를 root가 확인한 뒤 큐에 넣었습니다.

| 제보 | 후보 | 현재 한계 / 검증 요청 |
|---|---|---|
|브레스 컷인 원본 도트|`test_current/parts/bless_cutin_user_report/candidate_packet.json` 및 `remaining_family_packet_index.json`|IMG25328~25347의 서로 다른20프레임 제작 완료. 실제 연결/재생 미확인. 제보는25340/PLT25320/SCR25360.|
|샌드록 쇼텔·가슴·다리·뒷모습|`test_current/parts/sandrock_user_report/agent_repair/delivery_index.json`|총63종: 기본머리1+연결편6+실드2+공격54. 입력6 01:13 설치 결과가 최신입니다. D 교체8 동일 source 그림 충돌, E 새4 가늚 및90612 되돌림은 재작업 중입니다. 설치된 항목 재큐잉 금지.  세 자세360/480/600의 조립·반전·피격/플래시 확인.|
|데스사이즈 하체·복부|`test_current/parts/deathscythe_user_report/lower_body_repair/expanded_candidate_packet.json`|342 설치 뒤 형태불합격54는 disabled 유지. 새 held54_source_islands는 검토 전용이며 53 윤곽 개선/37502 미해결입니다. 정적 조립 접합·스타일 결함도 남아 완료 아님.|
|데스사이즈 노란 효과|`test_current/parts/deathscythe_user_report/yellow_lightning_bg/candidate_packet.json`, `yellow_lightning_bg_phase2/candidate_packet.json`, `rock_ring_bg/candidate_packet.json`|번개2교대 프레임+암석 별도960×480. 원래 혼합·스크롤·대사창 우선순위 유지.|
|오른쪽 시작 메뉴 패널|`test_current/ui/start_menu_user_repair/candidate_packet.json`|6교체. 선택판 윗변33% 과대 수정, 단어·반복선 보존. 새 로고 제작0.|
|타이틀 로고 미적용|`test_current/parts/title_logo_hd/candidate_packet.json`|기존 HD 그림 SHA 유효. 현재 참조 연결을 찾지 못함. 기존 그림을 원래 로고 레이어에 연결하고 실제 일본어 획/합성을 확인해 주세요.|
|미사일·궤적|`test_current/parts/missile_trails_user_report/final_packet_index.json`|whole IMG20224/20225 두 타일 재료+95343 정상 교체1. 전체 시트는 실제 OBJ 관측 아님. 아래 설치 제한 참조.|
|민트 효과 소실|`test_current/parts/rejected_effects_source_ready/mint_repair/final_packet_index.json`|95468_corrected/95470 두 후보. 생성 알파 그대로. 끝점·성분·블렌드 검증.|
|주황/연두 입자 소실|`test_current/parts/quarantine_four_source/particle_redraw_two/94016/ready_candidate.json`, `94080/ready_candidate.json`|원본43/17성분. 94016 저알파 잔여3픽셀은 보존·기록. 자동 격리 해제하지 않음.|

## 설치 실수 방지

1. 브레스25328/25330/25332는 `*_corrected.json`만 선택.25340/25341의 기본 이미지 지문이 충돌합니다.25340은 map512window1265223264도 확인,25341은 origin_8192 지문143590503. 빈 map prefix만 쓰지 않습니다.
2. 샌드록 머리는 `head_candidate_preserved_alpha_4x.png`만. 옛 임계값 알파 초안은 철회했습니다. 공격 A그룹 cell0/1은 `head360_continuous`40×40 마스터로 대체한 최신7묶음만. 실제 빨강 투구/보라 몸/노랑 V자는 원본 색이 맞습니다.
3. 샌드록 실드 원본은 IMG1190/PLT1191(full16=실제cached=독립HD-off MMU bank14). 다른 팔레트 indexed fallback은 덮지 않습니다.
4. 번개27956/27958는 tilebase128,27957/27959는 tilebase576, 둘 다 PLT27953/bank10/BG1. 두 IMG가 동시에 VRAM에 있으므로 현재 map/base/window로 구분해야 합니다. 검정 중심은 원래 BG 혼합용 바탕이므로 삭제하지 않았습니다. 암석은24640/24639/24641, BG2 tilebase512/bank8~9. 효과512entry window만 처리해 대사창을 보존해야 합니다.
5. 미사일 whole2는 `tile_source_only=true`, `actual_observed=false`, `adapter_required=true`이며 ready_screen_candidates입니다. 직접 큰 OBJ처럼 렌더링하지 않습니다. 기존 좋은 타일 우선순위를 유지하고 새로 빠진53+13위치 재료로 적용한 뒤 타일 DB를 다시 만드세요.95343은 ready_candidates의 별도 정상 교체입니다.20225 하단은 raw/full16같은 기존95351 **부모 전체**를 동일 좌표로 공유했습니다.
6. `quarantine_four_source/repair92544`, `_v2`, `_v4`, `parent_whole_draft`, `parent_cells_draft`는 미제출 초안입니다. 얇은 획/원본보다 넓은 획/3D 과장/매트 문제로 선택하지 않았습니다.92544는 실제3성분이며 y5가 비어 있습니다.93510은 부모93493과 경계를 넘어 이어지므로 부모 전체를 재제작 중입니다.

## Claude 설치 판정 인수

입력6 20:15~20:20: 펼친 날개37485, 닫힌 날개89913/89946/89504, 발스토크8607~8612, 샌드록90602, 연기95459가 설치·그림판정 통과. 19818의7계약도 통과. 전체 무장 실제 재생 완료라는 뜻은 아닙니다.

발호크 총·발/토라스 머리·어깨는 현재8바인딩과 설치된 그림 SHA가 이미 수정본과 일치합니다. `test_current/parts/reported_valhawk_taurus_current_audit/HANDOFF.md` 참조. 중복 생성0. 옛 형태가 실제로 계속 보인다면 활성 그림/캐시/런타임 경로 확인이 필요합니다.

## 진행 중

- 미히로: 기존24924는 다른 공통 컷인군이었습니다. 고양이귀 장식·주황 캐주얼복의 IMG25224~25237, PLT25210~25223, MAP25238~25254의 별도17표정군을 새로 찾았습니다. 예전 inventory가 같은 MAP를 잘못 붙여 후반을 모자이크처럼 보여주던 문제도 원본 준비 단계에서 발견했습니다. 정확한 조립·지문 대조를 마쳤고 누락 그림 제작 중이며 새 후보 아직 미제출입니다. IMG25230/25231/25233에는 각각 두 MAP가 있어14 IMG=14표정 가정도 정정했습니다. 실제 사용 state/frame은 아직 관측하지 못했으므로 새17개 모두 실제 공격 호출이 확인된 것으로 주장하지 않습니다. `correct_variant_family/native_correct_all17_contact.png` 및 `source_index.json` 참조.
- 격리92544는 아래 정확3성분 후보를 제출했습니다.93493/93510도 아래 부모 한벌 후보로 제출했습니다. 미흡 초안은 큐에 올리지 않습니다.

## 공통 검증 요청

원본 raw/index/full16, 공유 부모/자식 crop, 실제 색·뿔·눈, 성분 개수/굵기/끝점, 파츠 접합, 반전/회전/확대, 컷인·빔·기체·대사창 순서, 페이드/피격/플래시, 냉/온 캐시 로딩을 확인해 주세요. 원본 최근접 확대나 제작 조립 비교를 실제 HD 재생 합격으로 세지 않습니다.


## 격리92544 정확3성분 후보 제출

`test_current/parts/quarantine_four_source/repair92544_three/ready_candidate.json`을 root 회색 원본/후보 시각 비교·4역할SHA·현재 prior 확인 후 ready_candidates에 추가했습니다. 원본64텍셀은 윗4/긴44/짧은16의3성분이며, 세 성분을 각각 새 생성한 동일 시트의 자기 RGBA에서 bbox로 기하 배치했습니다. 원본의 y5 빈 줄은 정확히 alpha0으로 남고 전체 끝점 bbox도 일치합니다. 그림 SHA `7b615ca1fe523a05218f28e15f86c9b0a3c8375154024a80aefe49a3a1b531aa`.

가시 alpha>8부터3성분, alpha>16 면적64.0625 원본환산. 생성 알파를 삭제하지 않아 최대4/255의 잔여14성분79고해상도픽셀이 남습니다. 전체 alpha>0은17성분이며, 이를3성분이라고 숨겨서 보고하지 않습니다. `metrics.json`과 `HANDOFF.md`에 개별 AA끝점0.25~0.5원본픽셀 차이도 기록했습니다. 검증 요청: 분리된 윗 조각 소실/붙음, 끝점·굵기·흰/노랑/주황색, 저알파잔여, 실제 재생 블렌드. 격리 해제/설치/재생은 아직 수행하지 않았습니다. root의 thin/v2/v4 초안은 계속 설치 금지입니다.


## 격리93510 / 부모93493 한벌 후보 제출

`test_current/parts/quarantine_four_source/repair93510_parent93493/candidate_packet.json`을 root 회색 비교·4역할SHA·두 현재prior 확인 후 ready_candidates에 추가했습니다. 선택한 두 번째 평면 생성 master는 `candidate.png`/`generated.png`입니다. 부모32×8 전체 한 장에서 왼쪽16×8 child를 잘라 쓰며, 부모47/자식14 원본환산 면적과 일곱8연결 성분·bbox가 유지됩니다. source(175,61)의 child끝점이 오른쪽 parent(176,60)/(176,61)로 이어집니다. 다른full16인93523은 제외했습니다.

임계값으로 alpha를 삭제하지 않았습니다. 배경 alpha>8은0이며 alpha1~3의 미세155픽셀은 그대로 기록했습니다. 기존 dynamic_palette/lookup/effect mode는 보존합니다. drawing SHA `02c10017df0b41c9ec595e45b0b14b640b10a4ec1cbf618115395caad9c45cb9`. 검증 요청: 부모/자식 접합·성분/명암·확대시 자연스러움·실제 블렌드/재색칠, 이전 격리 해제. 생성 직후의 정확숫자를 게임합격으로 보지 않습니다.


## 2026-11-15 작업 재개 / 최신 입력6 인수

21:35 얼룩 감사와21:00 이후 설치/보류를 인수했습니다. 데스사이즈342계약 중54개는 형태 불합격 disabled로 유지되어 미완료입니다. 샌드록 새27개/메뉴6/95343/94016/94080/92544 설치는 실제 전체 장면 재생 합격과 구별합니다.

**설치 불가 패키지 수정:** `test_current/parts/candidate_packaging_repair/candidate_packet_index.json`. C/D/E를 new/replace 전용6폴더, 민트를 각독립2폴더로 나누고 기존 HD/생성 그림은 byte-identical로 유지했습니다. 작업 중 DONE20261115_011415가 갱신돼 C/E를 포함한5묶음은 이미 설치됐음을 확인했습니다. 따라서 ready_packets의 **D교체8 + 민트2, 총3패킷**만 root4역할SHA·현재10prior 확인 후 큐에 넣었습니다. 설치된 새16개를 재등록하지 않습니다. obsolete_queue_entries의 옛혼합3/민트2만 정확source/contract/drawingSHA 일치 조건으로 큐에서 뺐고 원본 파일은 보존했습니다.

민트 native는 계약 index/full16에서 재생성했습니다. 다만 현재 기존 native도 알파차이0/불투명RGB차이0라 예전 실패는 현재 파일로 재현하지 못했다고 기록합니다. 8개 분리 패키지 read-only installer check/matte 검사는 통과했으나 설치·굽기는 실행하지 않았습니다. E새4/교체90612의 형태 flag는 패키지 분리만으로 해결된 것이 아니므로 별도 그림 QA가 필요합니다.

**데스사이즈 보류54:** `held54_review/contact_00~04.png`를 root가 전부 보았습니다. 작은 사각형에 새 그림의 끝점만 남거나 빈곳이 채워지는 실제 형태 문제를 확인했습니다. 공유RGBA 일치만으로 하위 형태도 맞는다고 판단했던 것을 정정합니다. `held54_review/PRODUCER_FINDINGS.md`에 기록하고 부모1164/7086 원본배치에서 재제작 중입니다. disabled만 풀거나54개를 독립 조각으로 덧대지 않습니다.

**재색칠 신규 그림:** 2,213쌍/2,070바인딩의 실제 팔레트 별도 그림 요청을 인수했습니다. runtime smoothing으로 전부 해결됐다고 하지 않습니다. 새RGB키로 그려 연결해야 하며 코드 재색칠로 후보를 채우지 않습니다. 현재 미히로17표정/설치계약 수정/데스사이즈54를 병행합니다.


## 미히로17표정 중 마지막6개 새 후보 제출

`test_current/parts/mihiro_full_cutin_source/agent_repair/correct_variant_family/last_six_candidate_index.json`의6개(25233_MAP25249/25250,25234_MAP25251,25235_MAP25252,25236_MAP25253,25237_MAP25254)를 root4역할SHA·packetSHA 검증 및 회색 원본/후보6쌍 눈 확인 후 ready_screen_candidates에 추가했습니다. 각자 원본 표정·확대·클립을 별도 새 생성한960² 후보입니다. 남은11개와 혼동하지 않습니다.

표시 도구에서 일부 유사 프레임이 얼굴 패치처럼 보이는 현상 때문에 원본 파일 불일치를 의심했으나, 이6개는 soleROM 원시4bpp/SCR800entry/flip/bank를 독립 재조립해 native.png RGBA와byte-exact,4배reference도pixel-exact임을 확인했습니다. `last_six_fresh_ROM_proof/proof.json` 참조.25249와25250은 얼굴 패치가 아니라 몸이 동일하고 입 주변317픽셀이 다른 전체 프레임입니다. root가 앞서 채팅에서 말한 파일불일치는 정정합니다. 최초11개 쪽도 독립 재조립 확인 중입니다.

각 생성 알파는 보존했고 bbox측정용alpha16을 그림삭제에 쓰지 않았습니다. 저알파 먼지/far background 소수픽셀도 삭제하지 않았습니다. 실제state/frame은 관측하지 못했으며, ROM 조립 확인을 실제 게임 연결 합격으로 세지 않습니다. 검증 요청: 올바른 미히로표정 호출·줌/스크롤·MAP512가드·원래오렌지/초록/보라색·페이드·대사창가림·저알파먼지.


## 이미 설치된 샌드록16개 타일 원천 metadata 증명

설치된95851~95866의 resource/source_x/source_y가 모두 비어 있음을 발견했습니다. 정확 RGB lookup만으로는 보이더라도 타일 라이브러리 재료 구성에 빠질 수 있으므로 `test_current/parts/candidate_packaging_repair/source_metadata_amendments_for_Claude.json`을 준비했습니다.

16개 모두 이전 indexed dependency의 실제 ROM IMG/source좌표를 읽어 raw 인덱스가 byte-exact이고, target의 실제 cached full16으로 RGBhash도 일치함을 확인했습니다. `prove_installed_source_metadata.py`는 soleROM/source계약/currentlibrary 읽기만 합니다. 이것은 **정확 raw를 가진 IMG 별칭 증명**이지 유일한 기체/원본 소유자 확정이 아닙니다. aliases 중 검증된 resource/source좌표로 설치 metadata를 채우고 타일 라이브러리를 갱신할지 Claude가 판단해 주세요. 원본 팔레트는 그대로 유지해야 합니다. 중앙 라이브러리·DB는 수정하지 않았습니다.


## 미히로17표정 전체 후보 인수 완료

추가 첫11개의44역할SHA+11packetSHA와 원본/후보contact를 root가 확인했습니다. 이미 인수한6개와 합친 `test_current/parts/mihiro_full_cutin_source/agent_repair/correct_variant_family/all17_delivery_index.json` 기준17개 모두 ready_screen_candidates에 있습니다. 새로 추가한 것은11개이며 앞선6개를 중복 큐 등록하지 않았습니다.17개 이미지지문+MAP512guard 조합은 서로 충돌하지 않습니다.

`fresh_rom_proof_first11/proof.json`도 soleROM 직접4bpp/SCR 조립이 원본PNG·4배reference·계약 인덱스·팔레트와 일치함을 확인합니다.25245의 '파일불일치' 추정은 표시 결과를 잘못 읽은 것이었고, 원본 파일이 실제로 다르다는 증거가 없어 철회합니다. 잘못 만든 부분 얼굴 초안은 제외하고 새 전체 상반신 그림을 선택했습니다. 나머지 후보도 자기 표정/확대이며 무조건 한 그림을 반복 연결한 것이 아닙니다.

기존24924의 별도 공통컷인과 혼동하지 마세요. IMG25224~37/PLT25210~23/MAP25238~54가 이번17표정입니다. 실제 사용 state/frame은 여전히 미관측이며 '완료'는 그림후보17개 제작·원본대조까지입니다. 일반 파츠 설치기가 아닌 화면 컷인 전용 경로로 연결/굽기/재생해 표정전환·위치·줌·팔레트·fade·대사창가림을 확인해 주세요.

## 11/15 계속 작업: 팔레트 후보2와 데스사이즈 검토 전용

- `test_current/parts/recolour_actual16833/component_candidate_index.json` 2개 네 역할SHA/root 육안 비교 완료, ready_candidates에 등록했습니다. 새 RGB키2571710004/3922471057만이며 기존13890/13891을 덮어쓰지 않습니다. 매우 작은 입자로 HD 이득이 제한적입니다. PAT16834 bank1 범위 부족→effective0 감사 fallback이며 실제 관측 아님. Claude는 실제 장면 팔레트를 먼저 확인해 주세요. 두 후보의 6/7성분·분홍색·끝점 비교를 보았으나 독립 화질/재생 합격은 미확인입니다.
- `test_current/parts/deathscythe_user_report/held54_source_islands/HANDOFF_CLAUDE.md`와 `review_candidate_packet.json`: 공유340계약, 54 중53 윤곽 개선. 37502는 두 재생성 실패로 기존 섬 전체 보존, 미해결입니다. root가 normal/closed 정적 조립을 보니 normal 머리 뒤/날개에 각진 돌출, closed 오른쪽 어깨 위 스타일 불일치가 남아 있습니다. **ready 큐에 넣지 않았고 disabled 해제 요청도 아닙니다.** 정적 조립은 실제 재생이 아닙니다. 이음매가 틀리면 그림 재작업이 필요합니다.
- 미히로는 `correct_variant_family/all17_delivery_index.json`의 서로 다른17프레임 후보가 현재 묶음입니다. 처음11+마지막6 모두 ROM부터 다시 해독한 native와 동일함을 확인했습니다. 앞선 native/reference가 다르다는 의심은 철회했습니다. 설치·실제 표시 검증은 Claude 담당이며 아직 완료 근거 없음.
- 진행 중: 샌드록 D/E 그림 결함, 감사상 다른팔레트에서 얼룩지는 다음 묶음을 각각 서브에이전트가 새 그림으로 제작합니다. 중앙 라이브러리·DB·실행 코드·사용자 화면은 수정하지 않았습니다.

## 11/15 사용자 추가 지시 — 데스사이즈 날개·몸통 접합 재작업 중

- 사용자는 미채택 exec-95d7 초안을 최종인지 문의했고, 원본 형태를 바꿔 버려 미채택임을 답했습니다. 해당 초안을 설치 대상으로 취급하지 마십시오.
- 이번 요청은 접합을 고친 **조립 그림 공개**입니다. 기존 held54 후보의 normal 머리 뒤 각진 조각과 closed 오른쪽 어깨 이음매를 수정 중입니다. 현재 IMG7086의 4개 원본 분리 섬을 원본 경계·실제 색으로 새 생성하고 있습니다.
- 중앙 설치·굽기는 하지 않으며, 새로운 조립 그림도 OAM 계약에 따른 정적 합성임을 명시하겠습니다. Claude 검증: 원본 자세/회전·반전·부모 자식 crop·날개 아래 몸통 가림·대사창 우선순위·연속 프레임에서 접합 및 색 경계. 37502 disabled 임의 해제 금지.
