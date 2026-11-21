# Codex → Claude 38 — 2026-11-17 오전 종료 전 인계

사용자 지시: 오늘 오전 9시(KST)에 PC 종료. Windows 종료 예약은 07:38경 성공했고 그대로 유지 중. 종료 전 가능한 준비·파일 점검을 수행하고 이 문서에 계속 저장한다. 전체 이미지 작업은 미완료.

## 생성 상태

- 이미지 생성 한도 오류 `usage_limit_reached`가 해소되는 도구 안내 시각: **2026-11-17 19:43:14 KST**. 오전에는 새 이미지 생성 호출을 하지 않았다. API/CLI 우회 없음.
- 기존 성공 RAW는 모두 프로젝트에 저장되어 있고 실행 중·미회수 생성 호출은 없다. 지난밤 root 추가 9판 상세는 `test_current/parts/ROOT_LAST_NINE_DELIVERY_20261116.json`.
- 현재 수신 문서는 `docs/HANDOFF_TO_CODEX_9.md`. 8번은 이전 검수 원문으로 유지. 최신 기체별 검수는 각 `robot_set/EYE_REVIEW.json`도 대조할 것.

## 오전에 수행한 일

- 최근 전달 **38판 / 고유 파일 365개**를 읽기 점검. RAW·candidate·generated 해시, 참조 저장 해시, layout 해시 및 2.5px 해상도 기준 기술 오류 **0건**. 시각 검수·정합·분할·설치·게임 실행은 수행하지 않음.
- 결과: `test_current/parts/MORNING_DELIVERY_AUDIT_20261117.md` 및 `.json`.
- root 잔여 12폴더의 원본·실제4xBRZ·layout·슬롯/pose·기본 자세·기존 요청/후보·미제출 프롬프트 초안 목록: `test_current/parts/MORNING_ROOT_SOURCE_QUEUE_20261117.md` 및 `.json`.
- 새 QA 접수: 8번 23:38 이후와 9번 전체를 합쳐 **222기체**, 원문 중복0·SHA 검증 통과. 분류는 전체 재작화10 / 경미수정157 / 명시 승인·즉시 재작화 불필요55. `test_current/parts/MORNING_QA_INTAKE_20261117.json` 및 `.md`. 이는 해당 범위의 접수 분류이며 전체 프로젝트 미완료 수와 같지 않음. 이전 8번 전체 재작화 요청은 별도로 남아 있음.
- 없던 unit338 sheet02 `reference_4xbrz.png` 및 메타데이터만 기존 실제 xBRZ 도구로 신규 생성. native/layout/후보 수정 없음. 해당 큐를 갱신 중.
- 338 참조 갱신 후 잔여12폴더 모두 native/layout/실제4xBRZ 준비 완료. SHA 검증 추가11건 오류0. 새 참조 SHA `5d57293f3812c1d760d5c756100e5532ed783d3c31344a3256ce68819d8345a5`.
- **그림이 없다고 지목된 368s06·366s05·378s05·396s02·403s02는 기존 ALT9판으로 해당 자세 전부 커버됨**. 원본30슬롯 RGBA 동일/누락0/기술오류0. `test_current/parts/MORNING_EXISTING_ALT_RECONCILIATION_20261117.json`과 `.md`에 실제 candidate·layout·pose 대응 수록. Claude가 이 ALT들을 먼저 분할·독립검수할 것. 이미지 승인 의미는 아님. 403 공식 sheet02 반려본은 설치 금지 유지, PREFERRED의 대체3판만 검수. 366/378은 외부 도구 RAW 경로 메타가 없어 candidate=로컬 generated 증명까지만 가능.
- 구조 우선 9기체(236·237·444·209·403·361·367·416·417), 30시트 원본 메타데이터 준비: `test_current/parts/MORNING_PRIORITY_SOURCE_BRIEF_20261117.json`. 원본1x→4x 픽셀 복사 일치 확인, 각 슬롯의 실제 크기·알파 bbox·원본 색 빈도·참조 SHA 저장. 생성 요청을 실행한 결과가 아님.
- unit361 sheet03의 잘못된 자세 복사를 피하기 위한 **원본 전용 ALT2×2 3판** 준비: `unit_361/robot_set/morning_prepared_20261117/sheet_03/SOURCE_PREPARATION_MANIFEST.json`. base34+대상16~23, 원본9pose/공식 슬롯 RGBA·NN4 동일 검증. 실제4xBRZ·별도layout·미제출 프롬프트 저장. 잘못된 HD sheet02 참조 없음. candidate/generated 없음.
- unit416 검정 실루엣·모은 손 구조 수정용 **원본 전용 2×2 1판** 준비: `unit_416/robot_set/morning_prepared_20261117/silhouette_hand_selected/PREPARATION_ONLY.json`. base01+10/12/13. V자 팔 사이 진짜 투명 틈·하단 둥근 덩어리·벌어지지 않은 쐐기형 손이 핵심. 원본/공식slot 동일 증명, 4xBRZ와 불투명 검정 구별용 회색 검토본 및 미제출 초안만 있음. candidate/generated 없음.
- 전체 재작화 요청 15기체의 별도 수정 후보 대조: `test_current/parts/MORNING_REDRAW_RECONCILIATION_20261117.json` 및 `.md`. **83·127·362는 별도 수정 후보8판으로 각각 전체 자세 커버**(RAW SHA·해상도 확인), 먼저 그 후보를 Claude가 검수. 224는 비HOLD ALT3판이 있으나 효과HOLD·색 문제는 미해결. 나머지11기체는 별도 전달 수정 후보 없음. EYE_REVIEW에 검수 시트 경로/SHA 결속 정보가 없어 과거 판정을 낡았다고 단정하지 않았으며 mtime으로 승인 여부를 판단하지 않음.

## 설치 제외 및 원본 해석 주의

- **unit276 sheet02 중앙(slot4)**: 실제 복합 곡선 무장 누락 의심. 해당 슬롯 설치 제외. sheet05 원본과 대조해 실제 무장을 보존하며 다시 그릴 것. 회색 곡선이라고 모두 잔상으로 지우지 말 것.
- **unit50 QA sheet03 첫 칸 base06**: LEFT 갑판포 누락으로 설치 제외 유지. 같은 QA sheet01 공통 기준과 비교. 나머지 8칸은 별도 검수.
- **unit279 sheet01 top-middle partial**: 원본의 불투명 검정 블록과 대각 띠 누락으로 설치 제외 유지. `literal_partial_repair_20261116/`는 원본·4xBRZ·별도 layout·프롬프트까지 준비됐으나 미생성.
- 109·110의 잔상, 362 새 시트의 초록 잔상 폭·농도·갈퀴처럼 보이는 모양은 기술 검사로 해결된 것이 아니다. Claude가 원본과 시각 비교해야 함.
- **236 base01과 444 base03의 native RGBA가 완전히 동일**: SHA `77b3cbc4e8f7b16f03fc4c933717d558d155830a6d4457ba606a3004bc479b38`. 하지만 EYE_REVIEW의 색 설명은 서로 달라 보임. `test_current/parts/MORNING_236_237_444_SOURCE_COLOUR_NOTE_20261117.json`에 원본 경로·색 빈도·근거를 저장. 원본 회색/빨강/주황 픽셀의 부품 소유관계를 우선하고, 서술만 따라 전체 흰색·빨강으로 바꾸지 말 것. 원본 자료가 잘못 공유된 것인지 검수 서술 차이인지 Claude가 확인 필요.

## 재개 순서와 역할

1. 새 검수 목록과 기존 수정 ALT를 먼저 대조해 이미 전달한 그림의 중복 생성 방지.
2. 사용자 반려 구조 및 전체 재작화: 403은 반려 공식 sheet02 대신 기존 PREFERRED ALT3판부터 검수하고 미통과 부분만 새 작화. 209 전체 크기·잘림, 361 sheet03 다른 자세, 367 sheet01 사람 얼굴 수정. 236·237·444는 위 원본 색 대응 확인 후 진행.
3. root 미완료: 279 부분 패치·sheet02/03/04 → 280 ALT part02/03·sheet02/03 → 281 sheet02/03 → 276 실제 무장 수정 → 338 sheet02 경미 여백.
4. 193·194·204·205·206 수정용 9판은 준비 완료/미생성. `unit_150/robot_set/SHEETS/QA_193_194_204_205_206_PENDING.json`. 이후 266~274, 284~299 및 기존 기체별 QA 큐.

Codex는 실제 새 작화 및 RAW 즉시 저장, Claude는 시각 검수·정합·분할·설치·실제 게임 확인. 한 판 최대9·공통 기본 자세·원본 자리/크기/색·투명 여백·검정 하드컷 유지. 4xBRZ는 윤곽 보조이고 원본 작은 부품 해석을 대체하지 않는다. 순수 색변형 페이드/섬광 순간은 런타임 원본을 사용하며 새 재색칠로 메우지 않는다.

이전 후보별 상세 인계: `docs/HANDOFF_FROM_CODEX_37.md` 및 이전 문서. 기술 검사는 이미지 승인이나 전체 완료를 의미하지 않는다.
