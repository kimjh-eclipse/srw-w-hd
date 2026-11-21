# Codex → Claude 20 — 기체별 통합 시트 재작화 (2026-11-15)

이전 기록: HANDOFF_FROM_CODEX_19.md. 사용자가 승인한 방향은 **한 기체의 여러 조합 자세를 한판에 함께 그리는 방식**, 쨍한 원본색과 매끈한 금속 셀 명암입니다. 서펜트 unit9는 HANDOFF_TO_CODEX_7.md에 Claude의 설치·재생 확인 기록이 있습니다. 아래 다른 시트는 그림 후보 전달이며 합격이나 설치 완료를 뜻하지 않습니다.

## 역할

Codex는 내장 이미지 생성과 원출력 보존·전달에 집중합니다. Claude가 정합·분할·연결·굽기·검증·게임 재생을 맡습니다. 다른 팔레트 그림 재색칠 금지. 각 기체 자신의 조합 원본으로 새로 그립니다. 생성 알파/RGB를 코드로 지우거나 원본 알파마스크를 씌우지 않았습니다. 규정 크기가 있으면 전체 캔버스만 리사이즈합니다.

## 즉시 전달한 시트

모든 경로는 `test_current/parts/pose_packets/` 기준입니다. 각 폴더의 HANDOFF와 프롬프트에 자세한 검증 항목이 있습니다.

| 기체 | 자세 수 | 전달 경로 | 상태 및 주의 |
|---|---:|---|---|
| unit0 윙제로 | 32 | unit_0/robot_set/unified_sheet/candidate_sheet.png | 원출력1593×987. 6×6의 마지막4칸 빈칸. source_layout은 입력6120×3792 좌표. pose23 작은 원본 조각 보존 여부, 궤적과 외곽 잔색 확인 필요. |
| unit2 헤비암즈 | 25 | unit_2/robot_set/COMBINED/candidate_combined.png | **Claude가 지정한 COMBINED 원본으로 새 생성**. 전체 캔버스만2464×2072로 조정. generated_combined.png는 원출력. 이전 unified_sheet 배치와 혼용 금지. |
| unit3 샌드록 | 43 | unit_3/robot_set/unified_sheet/candidate_sheet.png | 원출력1795×876. 7×7 마지막6칸 빈칸. 기체가 작아 얼굴·손·가슴 세부는 확정할 수 없는 초안. 원본9408×4592는 도구400거부 후4096폭 전송용 전체축소 입력. |
| unit4 알트론 | 23 | unit_4/robot_set/unified_sheet/candidate_sheet.png | 원출력1441×1091 및 전체캔버스 조정 후보2880×2180. 검정 실루엣12/17 유지 여부와00 잔상 주변 색테두리 확인. |
| unit5 톨기스III | 24 | unit_5/robot_set/unified_sheet/candidate_sheet.png | 5×5 마지막1칸 빈칸. 원출력 그대로. 입력4220×3180/전송4096폭. 은색 궤적과 청록·회색 외곽 잔여 확인. |

## Claude 검증 항목

- 모든 자세에서 얼굴·가슴·어깨·손·발·무장 설계가 같은지, 원본 자세·가려짐·두 팔/두 손/두 다리와 관절 접합이 맞는지 확인하십시오. 생성 도구가 원본 장갑을 손으로 해석한 이전 문제가 있었습니다.
- 각 시트의 입력/출력 해상도가 다릅니다. source_layout 좌표를 원출력에 그대로 적용하지 말고 위치·크기를 정합하십시오. 전체캔버스 리사이즈는 자세별 정합을 보장하지 않습니다.
- 외곽/효과 주변 반투명 회색·원색 점 및 색테두리가 여러 출력에 보입니다. Codex는 증거를 보존하고 임의 삭제하지 않았습니다.
- 헤비암즈: 01/04/11/18 연기·주황 사격광, 13 양측 은색궤적,17 교차청색궤적. 가슴 장갑을 추가 주먹으로 잘못 해석하지 않았는지 확인하십시오.
- 샌드록: 얼굴·쇼텔·실드·가슴·다리·뒷모습을 원본과 비교하십시오. 출력의 세부 해상도가 부족하면 재작화 대상 자세/영역을 특정해 주십시오. 이 초안은 상세 검수 완료 그림이 아닙니다.

## 다음 진행

병렬로 unit1 데스사이즈16, unit10 알트론23, unit471 윙제로28 통합 시트 생성 진행. 뒤이어 토러스 계열(unit6/7/8), 스트라이크·에일스트라이크(unit11/12), 소드·런처(unit14/15)를 각자의 원본으로 생성합니다. 완료되는 순서대로 이 문서에 갱신합니다. 기존 개별 자세 대량 생성 후보의 보류는 유지합니다.

## 추가 즉시 인계

- **unit1 데스사이즈16자세**: `unit_1/robot_set/unified_sheet/candidate_sheet.png`, 원출력1452×1083. `HANDOFF.md`에 날개뿌리~몸통, 다리, 낫 그립, 얼굴/가슴 통일성, 효과를 금속장갑으로 오해했는지, 파랑/자홍/회색 경계 잔재를 대조 요청했습니다. pose10 검정실루엣 보존 여부 포함. 게임 정합·검수 전 후보입니다.
- **unit10 알트론23자세**: `unit_10/robot_set/unified_sheet/candidate_sheet.png`, 원출력1441×1091→전체canvas 후보2880×2180. unit4 그림 복사나 재색칠이 아니라 unit10 자신의 native로 새로 생성. 00 잔상 주변 초록/노랑 점, 04 상단 빨강 점, 외곽 halo 검수 요청.
- unit471 첫 출력은 완전 투명 영역이 없는 알파 오류라 후보로 발행하지 않았습니다. 원출력 보존 후 내장 이미지 도구로 배경 투명화 수정 중이며, 코드 배경 삭제는 하지 않았습니다.
- root는 unit21 라이트닝6자세, unit22 IWSP15슬롯(원본02는 빈 칸) 한판 생성 중입니다.

- **unit11 스트라이크12자세**: `unit_11/robot_set/unified_sheet/candidate_sheet.png`, 원출력1540×1021→입력동일1648×1092. pose04 잔상과 머리 위 빨강 점/외곽 회색·파랑 점 확인 요청.
- **unit6 토러스SK11자세**: `unit_6/robot_set/unified_sheet/candidate_sheet.png`, 원출력1399×1124. 03/05/08 잔상의 금속 입체화가 원본 의도와 맞는지, 흰/파랑/빨강 외곽잔재·센서/다리/라이플 확인 요청.
- **unit21 라이트닝6자세**: `unit_21/robot_set/unified_sheet/candidate_sheet.png`, 원출력1798×875. 좌하단은 원본부터 분리 장비만 있습니다. 02 병렬궤적 개수·틈과 보라 장비/얼굴/몸통/관절 검수 요청.
- **unit22 IWSP15슬롯**: `unit_22/robot_set/unified_sheet/candidate_sheet.png`, 원출력1403×1121. 원본pose02와 마지막16번째칸은 빈칸으로 유지. 실제점유는14칸. 쌍포·날개·곡도·얼굴/어깨/관절 및 경계잔여 확인 요청.
- unit471은 도구의 배경 투명화 재시도도 실패했습니다. `generated_all_poses.png`와 `generated_background_repair.png`만 보존, candidate 미발행·적용보류. 알파에 완전투명 영역이 없는 첫 출력과 회색잔여를 자체 HANDOFF에 기록했습니다. 이 기체는 생성완료 전달 수에 넣지 않습니다.

- **unit7 토러스SK MA1자세**: `unit_7/robot_set/unified_sheet/candidate_sheet.png`, 원출력1402×1122. 자신의 흰색/적황 원본으로 신규생성, 캐논/폴딩기하·정렬·각도·외곽확장 검수 요청.
- **unit8 진회색 토러스5자세**: `unit_8/robot_set/unified_sheet/candidate_sheet.png`, 원출력1445×1089. unit6 흰그림 재색칠이 아니라 자신의 원본으로 새생성. 04 원본부분절단 유지·센서/주먹/골반/부츠·정렬 대조 요청.
- **unit12 에일스트라이크15자세**: `unit_12/robot_set/unified_sheet/candidate_sheet.png`, 원출력1702×924→전체캔버스2100×1140. 날개 주변 빨강 점/halo, 날개접합/양손/다리/얼굴/slot배치 검수 요청.
- **unit14 소드스트라이크14자세**: `unit_14/robot_set/unified_sheet/candidate_sheet.png`, 원출력1270×1239. 4×4 마지막2칸빈칸. 공통얼굴/장갑·관절·원본기하·색잔여 테두리 대조 요청.
- **unit15 런처스트라이크10자세**: `unit_15/robot_set/unified_sheet/candidate_sheet.png`, 원출력1475×1066. 4×3 마지막2칸빈칸. 올리브 장비/등 접합·눈센서색·팔다리·외곽잔색 대조 요청.

## 원본이 완전히 같은 묶음 — 재색칠 없이 기존 새그림 공유 요청

unit13/17/18은 각각15자세 native_4x 전체의 RGBA 바이트·크기·포즈순서가 unit12와 같습니다. 각 `robot_set/unified_sheet/SOURCE_IDENTITY.json`에 개별 원본 파일 SHA/원시RGBA SHA/크기/비교대상 증거가 있습니다. **새그림을 추가로 그린 수에 포함하지 않았습니다.** Claude가 unit12 새그림의 공유 적용 가능성을 판단해 주십시오. 이름만 같거나 색이 다른 묶음을 복사하지 않습니다.

unit16은12자세 중04가 unit11과 달라 별도의 통합 시트 새생성을 진행합니다. 나머지11자세 동일근거도 자체 문서에 남겼습니다.

## 후속 즉시 인계·보류

- **unit16 스트라이크12자세**: `unit_16/robot_set/unified_sheet/candidate_sheet.png`, 원출력1540×1021→전체canvas1648×1092。04 원본차이로 독립신규생성. 잔상 주변 파랑/cyan 점·머리 위 빨강 점·halo 검수 요청.
- **unit25 에일 스카이그래스퍼2슬롯**: `unit_25/robot_set/unified_sheet/candidate_sheet.png`, 원출력 그대로. 왼쪽은 원본부터 어두운 분리장비 조각과 주황궤적만 있습니다. 생성의 금속판 해석과 오른쪽 기체·장비/연장선/콕핏/포구·외곽잔색 검수 요청. **unit26/32/33은 unit25 전체 원본과 RGBA·크기·순서가 같음**. 각 SOURCE_IDENTITY.json의 증거로 Claude 공유 적용 판단 요청, 중복 신규생성 수에는 미포함.
- **unit27 소드 스카이그래스퍼3슬롯**: `unit_27/robot_set/unified_sheet/candidate_sheet.png`, 원출력1653×951. 2×2 마지막칸빈칸. 01 분리조각·02 장비없는 변형을 원본 그대로 보존하도록 요청한 새작화. **unit34 원본이 unit27과 완전히 같다는 증거**도 기록했습니다.
- **unit28 런처 스카이그래스퍼1자세**: `unit_28/robot_set/unified_sheet/candidate_sheet.png`, 원출력1637×960. 녹색 하부레일·분리 세로조각/포드/쌍수직익 검수 요청. **unit35=28, unit36=29** 전체 원본 동일 근거를 각각 SOURCE_IDENTITY.json에 기록했습니다. unit29 그림은 아직 생성 중입니다.
- **unit30 IWSP 스카이그래스퍼5슬롯**: `unit_30/robot_set/unified_sheet/candidate_sheet.png`, 원출력1942×809. 02 검정 패치와 포신/원본잘림/생성이 채운 부분 차이·청록/회색잔재 검수 요청.
- **unit19 소드13자세 첫 출력은 명백한 전체 비율 오류라 정식후보에서 제외**했습니다. candidate_sheet_draft01.png/generated_draft01 보존·적용금지 표시, 원본만 참조해 한 번 재시도할 예정입니다.
- **unit24 스카이그래스퍼는 배경/halo 실패로 후보 미발행**. unit_24/robot_set/unified_sheet/에 최초 그림과 배경수정 시도만 보존하고 APPLY_PROHIBITED.txt 기록. 2회 모두 배경 잔여가 보여 추가 반복은 멈추고 다른 기체를 진행합니다.
- **unit23 뫼비우스 제로 원본 pose01의 분리·절단된 조합을 Claude가 확인해 주십시오.** 실제 완성 자세를 추정해 채우지 않고 이 기체 생성은 보류했습니다. 다른 원본 자세와 조립 상태가 달라 현재 자료만으로 완성기체 기하를 확정할 수 없습니다.

## 계속 생성·인계

- **unit19 소드13자세 재시도 성공 후보**: `unified_sheet/candidate_sheet.png` 원출력1173×1341로 원본1680×1920의 비율에 가까운4×4/13점유/3빈칸. 첫 실패본은 적용금지 초안으로 보존. 새본도 기하·얼굴·관절·무장·잔색 검수는 필요합니다.
- **unit29 라이트닝 스카이그래스퍼1자세**: `unified_sheet/candidate_sheet.png`,1711×919. 보라색 뒤장비/하부홈/은색포드/앞코·외곽잔색 검수 요청. unit36 동일원본 공유근거 있음.
- **unit31 스카이그래스퍼2 1자세**: `unified_sheet/candidate_sheet.png`,1507×1044. 원본우측 절단선/흰잔재·핀/포드/하부 검수 요청.
- **unit37 IWSP 스카이그래스퍼5슬롯**: `unified_sheet/candidate_sheet.png`, 신규원출력 그대로. 02는 어두운 분리조각, 마지막칸빈칸 보존요청. 쌍포/날개·하부장비·콕핏·외곽잔여 검수 요청.
- **unit38 M1 아스트레이9자세**: `unified_sheet/candidate_sheet.png`, 신규원출력 그대로. 얼굴/흉부/손발·방패와팔겹침·검/라이플방향·센서색·붉은외곽점 검수 요청.
- **unit39 스트라이크루주12자세**: `unified_sheet/candidate_sheet.png`, 자기분홍원본으로 새작화. 정상스트라이크 재색칠 아님. 공통얼굴/몸통/관절/라이플·04가로잔상·외곽잔여 검수 요청.
- **unit40 에일루주15자세**: `unified_sheet/candidate_sheet.png`,1702×924 원출력→2100×1140 후보. 분홍실제색. 넓은 붉은외곽점이 있어 적용 전 해결 필요. **unit41은 unit40과 완전동일원본**이라 SOURCE_IDENTITY.json으로 공유근거만 기록.
- **unit42 소드루주15자세**: `unified_sheet/candidate_sheet.png`,1642×958 원출력→2140×1248 후보. 파랑어깨점·머리/발빨강점·정합 검수 요청.
- **unit44 6자세**: `unified_sheet/candidate_sheet.png`,1786×881. 03 부분장비·02속도선을 원본대로 보존요청, 얼굴·포드/등접합·속도선/잔색 확인 요청.
- **unit45 14항목**: `unified_sheet/candidate_sheet.png`,1399×1124. 02는 빈칸이 아니라 원본검정실루엣. 13일반색+1검정실루엣과 마지막2빈칸. 곡검/등포신·날개·가로선·관절/얼굴 확인 요청.

## 남은 범위 병렬 계속

추가: unit23은 01의 조각/잔상을 임의로 완성기체로 채우지 않고 실제 source에 보이는 형태만 한판 새작화해 후보를 전달했습니다. `unit_23/robot_set/unified_sheet/candidate_sheet.png` 및 자체 HANDOFF 참조. 앞선 생성보류 기록은 이 인계로 갱신하며 원본조합 의도 검증 요청은 유지합니다.

unit100 아스트레이 블루프레임9자세, unit102 FW15슬롯의 새 통합 시트도 `unified_sheet/candidate_sheet.png`에 전달했습니다. 펼친손/손가락과 장갑의 구분, 공통얼굴/몸통/관절,102 큰어깨장비/후면포스트/02회색잔상 검증 요청을 자체 HANDOFF에 적었습니다. unit101은100과 완전히같은 원본이므로 공유근거만 기록할 예정입니다.

`UNIFIED_SOURCE_GROUPS.json`에 준비372기체 묶음의 **323개 고유 원본 시트 그룹**을 기록했습니다. 전체자세 PNG파일 바이트와 순서가 같은 묶음만 공유대상이며, 색이 다른 원본은 공유하지 않습니다. 이 숫자는 ROM 파츠 누락 수나 검수 통과 수가 아닙니다.

기존 담당의 소분량이 끝나면 unit48~149 /150~299 /300이상을 세 에이전트가 나눠 번호순으로 계속 생성합니다. 완료된 시트마다 각 폴더 HANDOFF와 이 문서를 갱신합니다. 한도 오류는 우회하지 않고 그대로 기록합니다.
