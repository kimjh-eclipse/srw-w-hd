# Codex → Claude 추가 인계 46

이전 전체 진행: HANDOFF_FROM_CODEX_45.md. 이번 문서는 이후 도착한 실제 결과와 최신 포인터를 우선합니다. 전체 이미지 완료·사용자 승인·게임 검증 완료를 뜻하지 않습니다.

## 사용자 지적 unit279 네 자세
최신 목록: test_current/parts/pose_packets/unit_279/robot_set/qa_user_anatomy_20261117/DELIVERY_PARTIAL_REVIEW_20261117.json.
25/27/28/29는 원본 조합 자세별 새 그림입니다. 반려된 옛 sheet04 네 칸은 그대로 설치 제외.
27 최신 qa_confirmed_hand SHA c69157d6…: source contract/OAM 재합성 RGBA 0차이로 진짜 손 OAM16 가시62pixel을 분리. 이전 손 ROI에 섞였던 허리 흰 삼각형(OAM4)과 발(OAM10)은 정당한 별도 부품이므로 삭제하지 않음. 큰 규칙 은색패드를 작은 불규칙 청회색 손·어두운 연결로 국소 작화.
28 최신 qa_independent_source_planes_20261118 SHA772401ca…: 큰 밝은 허리 덩어리를 작고 각진 회청색 연결면으로 수정.
29 같은 이름 폴더 SHAbd08cdeb…: 큰 주먹/입처럼 생긴 가슴 겹침을 작은 손과 평평한 어두운 전완으로 수정. 전면 빨강은 세 점.
25 qa_one_red_dot SHAbfd4f478…: 공중 자세 각진 허리·다리 연결 및 원본의 측면 빨강 한 점.
Claude 검증: 네 자세 원본과 정상화 위치/크기, 어깨-팔-손 소속, 허리/무릎/발 가림 순서, 손의 실제 작은 돌출, 불투명 검정과 진짜 alpha0 틈. 생산자의 개선 관찰을 정확 픽셀 합격으로 쓰지 마세요.

## 새 도착 결과
- ROBOT_320_SINGLE_POSE02_DELIVERY_20261118.json: 원본 단독 새 1회. source_single_alpha_window_20261118/candidate_sheet.png SHA363dce78…; 미사일 주위 직사각 alpha0 창 복구 관찰, 원본 alpha0 여섯 표본 모두 새 RGBA0000. 창 전체 경계·분리 섬·미사일 비율·정합 검증은 남음. 02만 override, 예전 실패3개 제외.
- unit401/robot_set/DELIVERY_EYE_STRUCTURE_401_443_20261118.json: 새 원본판11/25고유대상, 40908 국소+단독 포함 실제13회. 40908 최신 pose08_source_flat SHA45807665…는 금속 얼음판 대신 평면 무테 회백색 스침. 원본 밀도/폭/틈 검증. 42208/23 topology/오른 hardcut, 417/420/421/427 구조 목록은 개별 맵 참조. 비교칸 설치 제외.
- ROBOT_211_213_DELIVERY_20261117.json: 32자세8선호(새4+기존4), 실제6회. 213 qa_alpha_clear SHA21ec6b73… 우선; 최초 실제 A19 안개/금속깃털 RAW 설치 제외. 21114 가는 흔적은 너무 옅을 가능성 QA.
- QA_343_344_347_352_DELIVERY_20261118.json: 4선호/6실제. 343 fine_grey_strands_delivery,347 native_small_mark_delivery 우선. 344 원본 mintgray,352 은청색 날개. 35202는 원본/contract 모두 불투명 BLACK runtime 근거, 흰색 변형 아님. 01 기존 partial 유지.
- QA_300_398_CONTINUATION_BATCH_20261118.json: 해당 연속 범위 29선호판/37실제 RAW의 통합 위치. root358 추가1회는 아래 실패 별도이며 성공 합계에 더하지 않음.

## 불확실성 정정 / 중복 생성 방지
- ROBOT_44_RESIDUAL_RESOLVED_EVIDENCE_20261118.json: 최신 EYE 11/18 00:13 verdict ok/6자세,03 회색 톱니·주황 줄·보라 외피 실제 RAW 확인. 이전 '미해결 가능'을 해결 근거로 정정. 신규0회.
- unit240/robot_set/qa_source_legs_20261117/source_ownership_20261118/HANDOFF_SOURCE_TIPS.md: 원본3자세 재합성 RGBA0차이. 노란 끝은 네 개 별도 sprite 소속, 기존 후보에도 각 끝 존재. 01 아래끝은77중8pixel만 가시. 계약에 다리/엄니 명칭 없으므로 '발 누락'이라 단정해 숨은 팔다리 생성하지 않음. 가림·정합 검증은 남음.
- 19604/06 효과와 실물 클로 소속은 ROBOT_196_SOURCE_RESIDUAL_DELIVERY_20261117.json 및 SOURCE_OWNERSHIP_EVIDENCE로 구분 완료. 아래 진짜 클로를 지우지 말 것.
- 정확 원본 일치/역공유는 HD 품질 합격 증거가 아닙니다. 130/135/451 새 가는 모션 그림이 최신이며 예전 번개판 공유로 대체하지 마세요.

## 실제 미해결
- 35812: 원본 불투명 검정 가림의 비직사각 경계/작은 파랑흰 부분/오렌지 팬을 함께 보존하지 못함. root style-only 실제1회도 source 모양과 거리가 남아 설치 제외. qa_smooth_carrier/PRODUCER_HELD.json에 RAW/SHA/이유 저장. 기존3실패도 보존, 미완.
- 26512: 단독 원본 비교 후보는 가시 부품/고리 검정 개선 관찰이나 숨은 머리·몸통 소유/과장 띠/노랑버튼 미확인으로 HELD 유지.
- 386: 기존 moderation 실패 이후 재시도·우회 없음.
- 모든 신규 후보의 정확 정합·분할·설치·실게임 검증은 Claude 담당. RAW/alpha 수정하지 않고 보존. 원본 prep만 실제4xBRZ/복사; HD 후보 재색칠/코드 리사이즈/강제 알파수정 없음.
