# 코덱스 → 클로드 인계 33

이 문서가 현재 인계입니다. 이전 작업 기록은 HANDOFF_FROM_CODEX_32.md에 있습니다. 그림은 Codex, 정합·조각 분할·설치·게임 검증은 Claude가 담당합니다. 후보 생성은 설치나 검수 통과를 뜻하지 않습니다.

## 사용자 승인: 가오파이가(unit403) 금색 pose24

- 사용자가 `exec-b929a731-cef7-4ccb-9f56-34327b12aa5b.png`에 **굳**이라고 승인했습니다.
- 정확한 전달 파일: `test_current/parts/pose_packets/unit_403/robot_set/pose_24/candidate_identity_structure.png`.
- 원본 RAW와 동일 바이트이며 USER_APPROVED_ART.json에 SHA와 승인 범위를 기록했습니다. 승인 범위는 이 금색 그림의 형태와 스타일입니다. 다른 자세, 정합, 분할, 설치 완료를 뜻하지 않습니다.
- target 원본 + 실제4xBRZ + 같은 기체의 다른 원본 자세18/02 구조 참조 + 데스사이즈 스타일로 새로 그렸습니다. 다른 색 그림 재색칠이 아닙니다.
- 얼굴·가슴·팔 연결과 양쪽 무릎 원뿔이 살아 있는 이 그림을 같은 기체의 구조 기준으로 사용합니다. 다른 자세의 색은 각각 원본대로 새로 그립니다.
- 예전 `gold_fresh_redraw.png`, `source_structure_redraw.png`, 옛 sheet02/alternate 그림은 승인본이 아닙니다. 섞어 사용하지 마세요.

## 가슴·팔 구조 수정 후보

`unit_403/robot_set/pose_11`, `pose_14`, `pose_15`의 `candidate_identity_structure.png`를 전달했습니다. 실제 생성 요청/참조 SHA는 각 `identity_structure_redraw_request.json`에 있습니다.

- 같은 기체의 다른 원본 각도와 승인된 금색 그림을 구조 참조로 사용했습니다. 파란 자세를 금색 그림에서 재색칠하지 않았습니다.
- 얼굴은 작은 기계 마스크로, 가슴·팔·허리는 연결된 구조로 다시 그렸습니다. 픽셀의 작은 명암을 큰 얼굴/이빨/깃털 갑옷/공중에 뜬 금속 덩어리로 해석하지 않도록 수정했습니다.
- Claude 검증: 실제 원본 앞쪽 은색 부품의 소속/겹침, 가슴과 팔의 연결, 얼굴 가림, 무릎 원뿔과 발 형태, 캔버스 위치·배율·알파. 금색 사용자 승인을 파란 자세에도 확대 적용하지 마세요.
- 새로운 공식9칸 재작화와 3자세 조합을 생성 중입니다. 공식sheet02의 `identity_whole_sheet.png`는 중앙 주먹/가슴 형태가 다시 과장될 여지가 보여 producer HOLD입니다. 단독 수정 후보를 우선 대조해 주세요. 이전 `assembled_corrected.png`도 옛 literal 시안 기반이므로 설치 대상이 아닙니다.

## 그 외 전달

- unit404: 공식 sheet01~05 후보 파일이 있습니다. sheet01은 이전 사용자 사자발 수정/합성본, sheet02~05는 실제4xBRZ 참조 후 생성한 후보입니다. 03~05 추가 전달했습니다. 팔의 좌우와 사자발/손 구분, 부분 파츠 슬롯, 속도선과 어두운 연출 자세를 각 HANDOFF에 검증 항목으로 적었습니다.
- unit405: 공식sheet01 + sheet02/ALT4/part01~03 + 공식sheet03 후보를 전달했습니다. sheet02는 **ALT4 각 폴더의 별도 layout만** 적용해야 합니다. 보라 괴수 얼굴·이빨·왕관, 분홍 빔의 원본 잘린 경계와 투명 구멍을 검증해 주세요.
- unit406: 새 후보 생성 중입니다.
- 트로와: incoming8에서 기존 user_report 그림 설치 완료 확인했습니다. 새 cutin_redraw 후보는 중복이며 자동 대체할 필요 없습니다.

## 병행 작업

- 124~149 담당은 132~144 등의 후속 후보를 계속 저장하고 `test_current/parts/pink_xbrz_progress.jsonl`에 즉시 기록합니다. 14101의 원본 없는 작은 분홍 빛 추가는 수정 필요 사항입니다.
- 215~299 담당은 224~230 등을 전달하고 231부터 계속 진행합니다. 224 큰 흰 효과의 구멍 메움은 별도 HOLD이며, 원본의 알파 구멍을 코드로 억지 복원하지 않았습니다. 진행 표는 담당 영역의 XBRZ215_299_PROGRESS.json입니다.
- 380~399 및430~472 담당은 380~390 후보/보류를 기록하고 391의 큰 판을 원본 픽셀 무축소의 2×2 별도판으로 작업 중입니다. 380 마지막 partial-body 판의 틈 메움은 HOLD입니다. 각 ROBOT_XBRZ_RESUME_FINAL_STATUS.json과 개별 HANDOFF 우선.
- 모든 RAW는 저장 직후 원본 요청/참조 SHA와 함께 전달합니다. 원본 native/native4x/layout은 보존합니다. 실제 원본 픽셀당 생성2.5 이상만 후보로 내보냅니다.

## 최신 수신과 앞으로의 규칙

현재 확인한 최신 incoming은 HANDOFF_TO_CODEX_8.md(11/16 20:26 수정)입니다. 미작화519장에 실제4xBRZ 참조 준비, 기존 포함547장이라는 인계를 반영했습니다. 더 최신 인계가 생기면 읽고 추가 작업에 반영하겠습니다.

4xBRZ는 윤곽 참조이며 최종 HD 그림이 아닙니다. 작은 부품과 경계·색의 권위는 원본입니다. 부품 정체가 모호하면 같은 기체의 다른 **원본 각도**를 함께 보고 연결 구조를 파악합니다. 재색칠로 빈 파츠를 메우지 않습니다. 색이 변하는 순간은 incoming8의 런타임 원본 표시 결정에 따르며 별도 색변형 그림을 추가 생성하지 않습니다.

unit406 sheet01 전함4자세 RAW후보 전달: 3.697px/native. 포신변화·벤트구획/노즐·원본DARK밝기/정합 검증은 개별HANDOFF.

unit403 공식sheet03/04/05 구조재작화 RAW후보 전달. 각 STYLE_VERSION prompt/refs SHA + HANDOFF. 승인gold개별을같은기체정체성참조로사용, source각색독립작화. 04중우머리없는원본상태/05하좌cyan원본상태/03효과개수와알파 검증요청. 단독gold승인≠전체판승인.

unit403 sheet02/user_structure_redraw_alt4/part03 새조합 candidate_sheet.png 전달(RAW assembled_identity_corrected.png), 5.495px/native. 승인gold24+수정blue14/15 실제개별원천을같이참조해조합. 이폴더 별도layout만적용. 개별원천우선, 새보드도Claude정밀QA대상. 옛반려REVIEW_STATUS는 새후보로대체표시했고 반려원천은별도보존.

unit408→406 전체4자세 원본 native/native4x RGBA·차원·순서·공식layout·합성원본·실제4xBRZ 일치검증 후 RAW그림공유. SOURCE_IDENTITY.json 증거. 재색칠없음. 실제바인딩/공유부품/원본정합 Claude검수대상.

## 새 일감 수신: 11/16 20:26 눈 검수

사용자 추가 작업 요청에 따라 새 검수 수정도 병행합니다. 원본/설치본은 보존하며 수정 후보 그림만 넘깁니다.

- root: unit20 sheet01 기준pose07 총구+pose02 연두/주황 파편선·붉은사선. 같은기체 sheet02의 정상총구를 실제참조에 포함해 국소그림수정 중.
- root: unit24 하부가 얇은rail로 바뀐 문제. 원본의 두꺼운회색덩어리와 짙은둥근부품을 원래발자국 안에 다시그리는 중.
- root: unit48 pose01 원본빈중앙검정채움 제거+흰빔왼쪽수직경계. pose06 은색칼날로해석된잔상을 무외곽선 반투명회청streak로 바꾸며 아래의 실제머리/뿔/청록blade를 원본참조로 복원 중. 실제4xBRZ참조도 각원본에서 추가준비.
- 124~149 담당: 132~149 신규44판/전체동일공유증거 기록을 마쳤으며 141원본없는분홍빛도단일수정완료. 최신검수 unit70/71/72를 우선수정하도록 배정(잔상칼날/누락/검정얼룩·71오른팔/원본DARKslate색). 오래된5/100~106은 그뒤 상태확인.
- 215~299 담당: 224 흰효과단독3RAW 추가시도했으나 내부구멍메움 실패로HOLD, 원본/실제필터/요청/매핑 보존. 대비색읽기전용참조로추가시도1회고려. 그뒤 최신검수 unit74/75의2~3갈래hook과 원본회녹/청회색 팔레트 복원우선 배정. 코드재색칠/알파마스크편집없음.
- 380~399/430~472 담당: 392까지전달진행, 393계속. 새검수근거는 다른담당과겹치지않게처리.

unit403 공식sheet01 수정후보 전달 3.13px/native. 승인gold를각색새작화의같은기체구조참조로사용. 전체판검수전이며 원본partial/분리uppercomponent/회색잔상/cyan상태와 실제가슴-팔접합 대조요청. 이전후보별도보존.

신규검수수정 전달: unit24 sheet01 candidate_sheet.png 하부수정 RAW. unit48 pose01/06 candidate_effect_correction.png RAW단독후보(원래candidate/fit/설치미변경). 01 중앙검정덩어리제거/빔왼쪽수직cut, 불투명검정0·중앙3샘플A0. 06 칼날금속외곽선→반투명회청streak 및밑머리/청록blade복원. 각 HANDOFF_EFFECT_CORRECTION.md의 원본4배캔버스 크기로전체비례정규화 후정합/검수부탁. 74/75도담당agent가전4판후보전달(미검수).

unit20 sheet01 candidate_sheet.png 총구/색효과선수정 RAW 전달, 3.801px/native. sheet02정상base총구참조. 효과색/자리와나머지기체변형 검증요청. 20/24 편집입력HD는 before_* 파일에동일바이트보존하고 STYLE실제참조검증경로를그보존파일로기록(원래제출경로는request preserved_reference_paths).

unit407 sheet01 단독전투기 RAW후보 전달 13.106px/native. red/gold/purple 실제원본색, 관절/구멍/돌출수/정합/alpha는개별HANDOFF.

unit403 sheet02 별도part02 4자세 구조수정후보 전달 4.124px/native. gold+blue11/12+4폭발별. 원본BLUE팔레트유지. part01첫시도는다른3자세까지gold로되어반려, source팔레트독립재작화로BLUE복원후 잘못된base만 승인원천으로교체조합 중. 색변형을후처리/코드재색칠하지않음.


## 추가 전달 및 신규20:40 요청 분담

- unit403: PREFERRED_DELIVERY.json 작성. 공식01/03/04/05 + sheet02 대체2x2 3판을 우선 검수. part01 금색 재배치와 파란3자세 후보 저장. 이전 전체9칸02 및 literal drafts 제외. 금색 원화 한 장만 사용자 승인, 합성판·파란 자세는 미승인.
- unit409/410 sheet01 새 후보 저장. 부분 결손/잔상/무기와 눈·손·발수 및 배치 검수 필요.
- 딘70~72 수정6판: test_current/parts/pink_dinn_repair_20261116_handoff.md. 잔상 opacity가 진할 가능성/70pose09 yellow-tipped appendage 원본 대조 항목 포함.
- incoming8 20:40 신규77/78/79/80/81/83/84 확인. 담당124가 원본색·잔상·팔·포드·선체를 수정. 담당215는30/37연기,38/39잔상 진행. 담당380은397이후 신규 기체 진행. root는409/410이후 이어감.


## 다음 후보 즉시 전달

- unit409/410: 공식sheet01·02 모두 candidate_sheet.png 및 STYLE_VERSION/HANDOFF 저장. RAW==candidate. 409s2 잔상 끝이 금속처럼 보일 가능성과 source원형/투명도 정밀검수 항목 명시.
- unit411/412: sheet01 후보 저장. 411 상우 partial/dark 상태의 실제검정영역과 alpha0 구분/조각 위치 확인필수. 411s2 생성중. 412 전8자세/sheet01 완료 후보.
- unit78 포드stripe/khakigrey,80s2 muzzle불꽃제거 후보: 각 robot_set/user_report_repair_20261116_2040/sheet_SS. Claude검수전.
- unit30/37/38/39 효과수정 전4판: 각 robot_set/CORRECTION_20261116_EFFECTS/ 후보 및 layout_alt.json. 연기/팬/핑크가는선 수정. 기존 공식layout 직접적용 금지. 각 HANDOFF 참고, 독립검수미실시.
- unit413/414 첫판 생성 진행.


## 추가 즉시 전달 (독립 검수 전)

- unit411 sheet02 추가. 기체 2판 후보 저장 완료. 가슴 개구 3단계와 파란 세로/가로 잔상은 개별 HANDOFF 검수 항목 참고.
- unit413 5판과 unit414 1판의 RAW/candidate/STYLE/HANDOFF 저장 완료. 앞뒤 방향, 손/팔/다리 연결, 기준 자세 동일성은 Claude 정밀 검수 필요.
- unit415 sheet01 후보 저장(2.8802px/native). sheet02 생성 중.
- unit416 sheet01: 상우 민트 발광의 불필요한 검정 외곽/금속 테두리를 imagegen 1회 수정한 beam_corrected.png가 현행 후보. RAW 동일 바이트/alpha 유지. sheet02~04 진행.
- unit409 sheet02: effect_corrected.png가 현행 후보. 상중/상우 회색 잔상 아래 기체가 비치도록 1회 수정. 이전본은 effect_edit_input.png 보존. 끝 모양/투명도/원본 위치 검수 필요.
- 신규20:40: unit79 sheet01/02 하늘색 발광·펼친 왼손,84 잔상 수정 후보 저장(담당124).81 추가 구름 오생성은 기록하고 재작화 중.77/83도 진행.
- unit30/37/38/39 CORRECTION_20261116_EFFECTS는 layout_alt.json 필수. 기존 공식layout 직접 적용 금지.
- 담당380 보고: unit444 전2판 후보 저장,381~399 후보47판 RAW/candidate SHA 불일치0. 각 HANDOFF 정밀 검수 항목 참고.

### 투명 그림 표시 주의 (후보 픽셀 수정 금지는 유지)

원본의 불투명 검정 실루엣이 검정 배경 viewer에서 빈칸처럼 보이는 사례416s2/417s1 확인. 검수 전용 회색 배경에 alpha composite한 native_review_rgb.png로 구분하고, 실제 검정 상태를 비우거나 색칠하지 않습니다.
생성RGBA도 viewer에서 alpha253 본체가 안 보이는 경우가 있지만 회색 검수 합성본에서는 정상입니다. *_review_rgb.png는 보기 전용이며 후보·분할 입력으로 사용하지 마세요. 원본/RAW alpha 임계값 처리나 수정은 하지 않았습니다.


## 현행 후보 갱신

- unit415 전2판 후보 저장. unit416 전4판 후보 저장: sheet01 beam_corrected.png, sheet02 hand_corrected.png가현행이며중우의드릴오해를얇은손가락으로1회수정. sheet03/04도바로납품. 모든판개별STYLE/HANDOFF참고.
- unit417 sheet01 및418 sheet01 후보저장. 원본blackfragment/whiteflash실루엣을grey검수RGB로존재확인, 구멍/형태/실제alpha정밀검수필수. 417sheet02/03 생성중.
- unit419/420 sheet01 후보저장(각3.5977/3.2967px per native). 센서수/실제손·무장·가림·partialstate/잔상해석 source대조필수.
- 신규20:40 수정13판 총괄: test_current/parts/pink_visual_repair_2040_handoff.md 및 _status.json. 83전체28자세4판새작화,81최종fresh본효과QA보류. unit5/100~106새Deathstyle19판이이미존재하여중복생성하지않음: pink_5_100_106_status_audit_20261116.json 증거.
- 담당124 다음수정:1/11/22/16 기존눈검수,그뒤301/309/311/305/307/308 미해결. 기존수정중복확인. 필수Deathstyle원화 unit1pose00generated.png는보존.


- unit417 전3판 저장,418 전1판 저장.419/420 첫판저장후나머지생성중.421/422 첫판후보저장(3.0284/3.0950);나머지는아직미착수.
- root 진행상태 test_current/parts/ROBOT_ROOT_RESUME_STATUS.json 참고. 전체작업완료아님.
- 424sheet01은9칸해상도2.5미달예상으로 별도ALT4/part01~03 source pixelcopy+xBRZ입력/각layout만준비. 원본9칸과입력파일보존검증. 아직그림없음.
