# Codex → Claude 34 — 새 후보 및 이어서 할 작업

이전 상세 기록은 HANDOFF_FROM_CODEX_33.md. 모든 후보는 독립 검수·정합·분할·설치·게임 확인 전이며 사용자 승인으로 간주하지 않습니다. 사용자 승인은 unit403 pose24의 b929 원화 한 장에 한정됩니다.

## 즉시 전달

- unit419 전체3판(20자세) 후보 저장. 각 SHEETS/sheet_01~03/candidate_sheet.png, generated_sheet.png, STYLE_VERSION.json, HANDOFF.md, generation_request.json. 원본 작은 yellow 센서/helmet point 수, 팔/무장 귀속 및 raisedhand/back 방향 검수 필요.
- unit420 전체4판(30자세) 후보 저장. 같은 표준경로. 작은 rigid mask/green visor·실제 손과 팔 접속·뒤모습 확인 필요. 특히 sheet02 중우 / sheet03 상중의 얇은 blue parallel 원본 요소가 후보에서 단단한 rack처럼 보일 수 있습니다. 원본 단독 shape/프레임으로 실제 부품인지 잔상인지 먼저 판별해주세요. 잔상이면 무외곽선 반투명 수정 대상이며 해당 자세는 확정 전 설치하지 마세요. longgrey요소도 임의 무기명으로 추정하지 않습니다.
- unit417 전3판,418 전1판은 33 기록 후 모두 후보 저장. 417 black fragmented silhouette와418 whiteflash는 grey review RGB로 실제 alpha 합성 확인. 구멍/파편/크기/개수 source 정밀 검수는 남아 있습니다.
- unit415 전2판,416 전4판. 416sheet01은 beam_correction_request.json/beam_corrected.png, sheet02는 hand_correction_request.json/hand_corrected.png가 현행 RAW입니다. 얇은손끝을 drill로 그렸던 초안은 hand_edit_input.png에 보존. 새손가락 개수/길이·곡률/관절 연결은 원본 단독pose13으로 검수해주세요.
- unit421/422 첫판 후보 저장. 421 나머지2판 생성중,422나머지3판은 아직 미착수.
- 424sheet01 ALT4/part01~03은 원본pixelcopy와 실제4xBRZ/별도layout만 준비. 공식9칸 원본 및layout 보존 SHA 확인. 아직 그림 없음. 생성 후 별도2x2 layout로 받아야 하며 공식9layout 직접 적용 금지.

## 병행 담당

- 담당124: 신규20:40 수정13판 전달. 총괄 test_current/parts/pink_visual_repair_2040_handoff.md. 81 잔상 길이/단단함 QA 보류. 5/100~106 새Deathstyle19판 기존존재 확인해중복생성하지않음. 이후1/11/16 기존눈검수수정 진행,22 blacksilhouette는 이미 별도수정본이 있어 재생성 안 함. 필수스타일원화 unit1pose00/generated.png는 절대 덮어쓰지 않음.
- 담당215: 30/37/38/39 효과별도수정4판 전달후244이후신규기체 진행. 224 내부투명구멍/23801 redsilhouette가 생성에서 왜곡돼 보류. 실패자료 보존, 코드alpha마스크로메우거나지우지않음.
- 담당380: 381~399 및444~449 후보 전달후450이후 진행. 430~443 등 실폴더없는번호는 그림있다고 보고하지않음.

## 적용 규칙

RAW bytes/alpha를 그대로 저장하고 해상도2.5px/native 이상만 후보로 전달합니다. 실제 참조경로·SHA·전문프롬프트는 요청JSON, 후보/RAW/규격은 STYLE_VERSION.json. 단순 비율 차이만으로 재생성을 반복하지 않으며 전체캔버스비율 정규화/정합은 Claude가 수행합니다. 원본위치·크기가 목표입니다.

*_review_rgb.png/jpg는 보기 전용이며 후보/분할 입력이 아닙니다. 검정 viewer에 숨은 불투명 검정실루엣과 alpha0 RGB찌꺼기를 구별하기 위한 자료입니다. 원본·설치·runtime·ROM은 이 작업에서 변경하지 않았습니다.

전체 작업은 아직 진행 중입니다.


## 이번 재개 추가 전달

- unit421 전3판 후보 완료. 02/03 pixels/native=2.914/5.670. 수직 시안 잔상·실제 수직 은색 장치·뒤 원형 기구/패널 및 손/얼굴 센서 원본 대조 요청.
- unit422 전4판 후보 완료. 02/03의 대각 lavender 잔상은 무외곽선 반투명 새그림으로 몸체 비침을 살렸습니다. 02하우 수직 보라선은 원본 단독 shape/frame으로 실제 기구인지 잔상인지 판별 바랍니다. 04우측 모인 손가락/가슴 작은 구조 검수 필요. 요청JSON·RAW·후보·STYLE·각HANDOFF 저장.
- unit424 sheet01/ALT4/part_01 첫4자세 후보 저장(3.75px/native). 별도 layout.json 필수. part_02/03 및 공식02/03 현재 생성 중. dark silhouette·green/grey detached fragments는 각 원본 상태로 요청했고 밝은 금색으로 일괄화하지 않습니다.
- unit425 및427 첫판 생성 중. 425/426 공식원본4x/필터/layout 파일은 동일함을 확인했으며, 공유전 개별native/native4x RGBA도 검증 예정. 아직426 그림 전달 아님.
- 담당124는 unit1 별도2x2 수정5판+11/16 각1판+30702 feather수정 전달. 각 user_report_repair_20261116_2040/와 별도layout 사용. unit1 pose00 필수스타일원화는 보존. 이후301/309/311 등 계속.
- 담당215는244전4판 완료,24501 잔상을 반투명으로 1회국소수정해 저장 후24502 계속. 담당380은450전2/451전1/452전2판 전달 후453 진행.


## 추가 전달 2

- unit424 전체18자세 후보 5판 완료: sheet01은 ALT4/part_01~03 별도2x2(각3.75/3.604/4.131), 공식02=2.667,03=5.936px/native. robot_set/PREFERRED_DELIVERY.json에 정확한 후보/별도layout/SHA 기록. 공식01 원본9칸layout 직접사용 금지. darkbrown 상태/green detached parts·grey연결·집게 이빨과 fin수 검수 필요. 02중좌gold수평잔상은 greyRGB로 실제 반투명 확인했으며 source길이/비침 QA 남음.
- unit425 후보저장(4.114px/native), unit426은 3개 개별native+native4x RGBA 총6검사와 sheet/filter/layout 동일성 검증 후 RAW bytes 공유. SOURCE_IDENTITY.json 증거. 재색칠 없음. whiteflash 정확한 구멍/실루엣/분리흰조각 수, 작은우측기체 크기 및 전체캔버스 비율 정규화 QA 필요.
- unit427 전3판 후보완료. 01 cyanwhite 투사체 사이공간은 greyRGB 합성에서 alpha0 확인. 02중앙/03하중은 source측후면/좁은yellow요소의 해석을 Claude shape/frame으로 확인 후 설치 바랍니다. 출력에서 정면mask처럼 바뀌었는지 불확실해 중요QA표기. 03상중 partialcut 유지. 각 센서·손/팔귀속·뒤투사체 검수 필요.
- 기존 누락목록 점검 후156sheet03,164/167첫판 신규생성중. 165/168은 각각164/167의 개별native/native4x 10파일 RGBA 및 sheet/filter/layout까지 동일해서 SOURCE_IDENTITY.json 증거준비(아직그림공유전).188/189도 동일성검증만완료. 다른팔레트 재색칠은하지않음.
