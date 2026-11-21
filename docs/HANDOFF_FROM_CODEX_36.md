# Codex → Claude 36 — 250~259 전달 완료 및 추가 누락 진행

이전 그림별 SHA/세부 기록은 HANDOFF_FROM_CODEX_35.md. 전체 작업 진행 중, 아래 모든 그림은 검수 후보이며 승인/정합/분할/설치/게임 확인 전입니다.

## 250~259

- 250전3판,251전3판,252전1판,253전2판,254전3판,255전3판,256전3판,257전3판,259전2판: 각 공식 SHEETS/sheet_NN/candidate_sheet.png +generated_sheet.png. 실제원본+실제4xBRZ+Deathscythe style로 새로 그림, 다른팔레트재색칠 없음.
- 251sheet03 실제배경안개는 이미지젠 background-extraction으로 수정, background_corrected.png=후보=generated RAW. 원래 배경실패 RAW는 background_edit_input.png, 원요청은 generation_request.json 보존. 현재요청전문/실참조SHA는 background_correction_request.json. cornerA0와 회색RGB합성 깨끗함 확인. 코드알파수정없음.
- 258전15자세는 official01 대신 ALT4/part_01~03 자체layout 3판 +official02. robot_set/PREFERRED_DELIVERY.json의 네 경로와 layout/SHA 사용. 원본픽셀복사로 배치한 ALT입력이며 원본 크기/좌표변환 없이 새 배치. 각 ALT의 layout.json으로 자르세요. gate각3.8768/3.7432/3.7174,official02=2.5882.
- 각 폴더 STYLE_VERSION.json/HANDOFF.md에 기본 해상도/SHA와 검수 항목. 주의: 작은 센서/얼굴 면/손가락/팔·창 접합, 채찍·꼬리 실제 귀속과 경로/길이, 의도한 어두운 상태·partialcut·분리조각, 흰 섬광 silhouette의 holes, 잔상 투명도/폭/원본과 같은 범위. 보기에 숨은 RGB 잡색이 나와도 RAW알파를 자르지 마세요. generated_review_rgb.png는 보기용이며 설치용아님.

## 473~492 추가 원본동일 공유

전체개별native/native4x RGBA·크기·순서 및 공식sheet4x/layout 동일 증명 후 기존새화풍RAW만 공유. 다른색 그림재색칠아님. 대상 robot_set/SOURCE_IDENTITY.json에 증거/경로/SHA/해상도. 원source의 미검수사유도 유효합니다.

- 68→473 1판,338→478 4판,393→484 2판,394→485 2판,395→486 3판,397→488 1판,133→492 3판
- 391→475 ALT2x2 총6판,396→487 standard01+ALT2x2총3판=4판. 각 alt_2x2_NN/layout_alt_2x2.json 필수.
- 136→491 전4판: 마지막sheet04는 ALT_2x2/candidate_sheet.png 및 자체layout.json. 담당124가 최신RAW·해상도4.804 보류아님 확인.
- 178→483/489,179→482 각1판: 과거 sourcecandidate는 canvasresize였으므로 사용하지 않고 sourcegenerated 원해상도RAW만복사해 후보로 전달. shared_artifact_fingerprints.json,shared_generation_prompt.txt 및sourceSTYLE 이력참조. 새 대상 candidate/generated는 RAW동일, 코드resize없음.

## 진행 중

- root127: 과거전체 navy/charcoal 밝기반려를 원본slategrey밝기/판무늬로 새로 그림. source_colour_redraw_20261116 별도폴더, 완료후128과 원본동일증명 공유예정. 반려된127기존standard를128에복사하지않음.
- root477/490 첫판 생성중.474첫판,479/481 첫 ALT4 생성중.479/481 official01은 원본판너무커서 해상도<2.5예상, 원본pixel-copy2x2로 별도배치. 각ALT 자체layout필수.
- 474와278동일,474완료후공유하며 담당380에게278중복생성하지않도록 통지.480은263동일,263담당완료후검증해참조예정.
- 추가실제누락22102/22201~02/22301~02는 root이어처리.218/219/220,125/134/135는 이미동일원본공유/참조 증거확인.
- 담당124:300~379실누락계속,담당215:260~274,담당380:472까지계속후275~299.
- unresolved producer HOLD:224효과내부alpha,23801붉은실루엣holes,24902흰섬광테두리,467가슴해석/opaque검정partial보존. 반복실패원본과RAW는각폴더보존, 통과/설치했다고표시하지않음.

원본/설치라이브러리/런타임/ROM/마스터style그림변경없음.


## 후속:127/128 및477/490

127 source_colour_redraw_20261116 신규RAW 후보 gate3.8977 SHA572ebe8d6f2a857e09edbfaaf349400b1789e71fa7a78baec454c2583d19cfd6. robot_set/PREFERRED_DELIVERY.json 우선. 원본밝기 slategrey/판무늬로 새로 그린 판이며 작은 포각도/후방 구멍/5상태 미세차는 검수 필요.128은 모든nativeRGBA/치수/순서+공식layout 동일증명 후 이 신판RAW만공유,기존반려127판은공유안함.128공식01candidate에 저장.

47701 gate3.5137 SHA2ce3b3e6a6277e3cad558bc570cd3ce1e9e2d96880d7d18f0302dedb14de31e3,49001 gate2.9786 SHA25f88313d6ac011975b942b736e64a4e0bfbc7332cab94eebb3f6033b4009fe7 저장. 원본별 작은얼굴/가슴면/팔/포트/방패·모션/partial구역QA는각HANDOFF.47702/03+49002/03 생성중.

22301은실제보류사유가canvasaspect뿐이고gate3.0255이므로원본판RAW를변경없이후보로전달함. SHA7759faad0d7973729ce4100d18548c09a9731c72d2fa7c32cd6f2f372d7eb468. 당시요청/STYLE는*_aspect_failed_draft로보존,기하합격의미아님,Claude정규화/눈검수요청.22102/22302추가생성중.
