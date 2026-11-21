# Claude 인계 — 추가2시간 그림 작업

사용자 지시로 2026-11-15 21:51:26 KST부터 2시간 계속 작업합니다. Windows 종료예약 명령이 성공했고 종료예정은 **23:51:26 KST**입니다. 23:47부터 새호출을 중단하고 23:49까지 반환물/미완료/보류를 저장하도록 모든작업자에게 전달했습니다.

Codex는 새그림 생성/직접 얼굴 확인/즉시저장, Claude는 정합·분할·설치·검수 담당입니다. 한판최대9자세, 원본 실제색·형태·좌표와 투명도 보존, 데스사이즈 실물 기준 쨍하고 매끈한 새작화. 재색칠/원본알파 덧씌우기 금지.

## 진행 범위

- root: 0~47 중 새화풍 SHEETS 없는 대상. 현재0/3/4첫판 생성 시작. 샌드록의 붉은 분리상태도 원본 그대로 요청했습니다.
- pink:48~149(100~109제외),99후속후23/25/27지적우선수정.
- mihiro:150~299,194얼굴수정 및 이후계속.
- wingzero:300이상, 얼굴오류와 비율/순백실루엣 실패는 RAW보류·기록후 다음진행.

[이전 얼굴수정8판 및 검증항목](HANDOFF_FROM_CODEX_27.md)
[전체 기계집계](../test_current/parts/pose_packets/DEATHSCYTHE_STYLE_DELIVERY_STATUS.json)

후보는 미검수이며 생성완료가 설치/합격을 뜻하지 않습니다. 완성된 판은 각 SHEETS/sheet_NN의candidate_sheet.png,generated_sheet.png,prompt,STYLE_VERSION.json,HANDOFF.md로 즉시 전달합니다.


## 새화풍 그림 전달 unit0 sheet01
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1518, 1036), 원본 (2356, 1608). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 눈·작은 기계 마스크·붉은 턱이 구별되며 인간형 입술/치아로 해석된 명백한 오류는 보이지 않았습니다. 세부 설계 일치는 미검수입니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 흰 날개 깃털 개수/길이·부착각, 두 버스터 라이플 방향/포구, 아래오른쪽 속도선. 투명픽셀의 RGB잔재는 실제 알파로 확인.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_0/robot_set/SHEETS/sheet_01/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_0/robot_set/SHEETS/sheet_01/HANDOFF.md)


## 새화풍 그림 전달 unit3 sheet01
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1766, 891), 원본 (3220, 1624). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 눈·작은 기계 마스크·붉은 턱이 구별되며 인간형 입술/치아로 해석된 명백한 오류는 보이지 않았습니다. 세부 설계 일치는 미검수입니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 중간왼쪽 붉은 분리/피격상태의 조각 개수/좌표, 쇼텔 곡률/손 연결, 탄색 천과 얼굴 형태.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_3/robot_set/SHEETS/sheet_01/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_3/robot_set/SHEETS/sheet_01/HANDOFF.md)


## 새화풍 그림 전달 unit4 sheet01
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1393, 1129), 원본 (1756, 1424). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 눈·작은 기계 마스크·붉은 턱이 구별되며 인간형 입술/치아로 해석된 명백한 오류는 보이지 않았습니다. 세부 설계 일치는 미검수입니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 윗중앙 속도선이 입체 물체로 읽히지 않는지, 용팔의 길이·접합, 회녹 장갑색과 얼굴.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_4/robot_set/SHEETS/sheet_01/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_4/robot_set/SHEETS/sheet_01/HANDOFF.md)


## 새화풍 그림 전달 unit0 sheet02
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1609, 977), 원본 (2452, 1488). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 좁은 눈·작은 평면 마스크·턱이 구별됩니다. 사람의 코/입술/치아로 해석된 명백한 오류는 보이지 않았고 세부는 미검수입니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 쌍라이플 방향과 날개깃털의 배열/겹침, 원본 실제몸체 크기/여백 비교.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_0/robot_set/SHEETS/sheet_02/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_0/robot_set/SHEETS/sheet_02/HANDOFF.md)


## 새화풍 그림 전달 unit3 sheet02
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1398, 1125), 원본 (2076, 1672). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 좁은 눈·작은 평면 마스크·턱이 구별됩니다. 사람의 코/입술/치아로 해석된 명백한 오류는 보이지 않았고 세부는 미검수입니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 아래왼쪽 분리된 어깨조각, 아래가운데 궤적, 쇼텔/손목 연결·얼굴폭 비교.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_3/robot_set/SHEETS/sheet_02/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_3/robot_set/SHEETS/sheet_02/HANDOFF.md)


## 새화풍 그림 전달 unit4 sheet02
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1350, 1165), 원본 (1580, 1364). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 좁은 눈·작은 평면 마스크·턱이 구별됩니다. 사람의 코/입술/치아로 해석된 명백한 오류는 보이지 않았고 세부는 미검수입니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 가운데 검정 실루엣의 실제 알파/원본 윤곽을 흰 배경으로 확인해야 합니다.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_4/robot_set/SHEETS/sheet_02/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_4/robot_set/SHEETS/sheet_02/HANDOFF.md)


## 새화풍 그림 전달 unit0 sheet03
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1484, 1060), 원본 (1980, 1416). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 기계식 눈·평면 마스크와 턱이 분리돼 보이며 명백한 인간 입술/치아 변형은 보이지 않았습니다. 세부 설계/정합 미검수.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 하단가운데 작은 분리 깃털의 개수와 위치, 날개겹침/후면방향, 얼굴폭.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_0/robot_set/SHEETS/sheet_03/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_0/robot_set/SHEETS/sheet_03/HANDOFF.md)


## 새화풍 그림 전달 unit3 sheet03
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1556, 1011), 원본 (2292, 1488). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 기계식 눈·평면 마스크와 턱이 분리돼 보이며 명백한 인간 입술/치아 변형은 보이지 않았습니다. 세부 설계/정합 미검수.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 중간가운데/하단오른쪽 분리된 쇼텔과 팔 조각의 개수/틈, 스카프 가림·손목 연결·얼굴.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_3/robot_set/SHEETS/sheet_03/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_3/robot_set/SHEETS/sheet_03/HANDOFF.md)


## 새화풍 그림 전달 unit4 sheet03
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1412, 1114), 원본 (1668, 1316). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 기계식 눈·평면 마스크와 턱이 분리돼 보이며 명백한 인간 입술/치아 변형은 보이지 않았습니다. 세부 설계/정합 미검수.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 윗중앙 불투명 검정 실루엣과 하단두빈칸 유지, 용팔 접합·얼굴폭.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_4/robot_set/SHEETS/sheet_03/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_4/robot_set/SHEETS/sheet_03/HANDOFF.md)


## 새화풍 그림 전달 unit0 sheet04
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1589, 989), 원본 (2256, 1404). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 눈/작은 기계 마스크/턱 구별을 직접 보았습니다. 명백한 사람 코/치아미소 변형은 보이지 않았습니다. 세부 얼굴 설계 미검수.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 윙제로4판완료. 쌍총 포신구멍/날개 깃털겹침/흰깃털 알파와 속도선.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_0/robot_set/SHEETS/sheet_04/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_0/robot_set/SHEETS/sheet_04/HANDOFF.md)


## 새화풍 그림 전달 unit3 sheet04
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1528, 1029), 원본 (2220, 1496). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 눈/작은 기계 마스크/턱 구별을 직접 보았습니다. 명백한 사람 코/치아미소 변형은 보이지 않았습니다. 세부 얼굴 설계 미검수.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 샌드록4판째. 하단왼쪽 긴 효과선이 검/깃털처럼 금속화됐는지, 하단가운데 분리어깨부품/마스크/천가림.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_3/robot_set/SHEETS/sheet_04/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_3/robot_set/SHEETS/sheet_04/HANDOFF.md)


## 새화풍 그림 전달 unit13 sheet01
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1319, 1193), 원본 (1416, 1280). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 눈/작은 기계 마스크/턱 구별을 직접 보았습니다. 명백한 사람 코/치아미소 변형은 보이지 않았습니다. 세부 얼굴 설계 미검수.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 흰/회 장갑의 원본명도, 황색센서/부스터윙 개수·각도와 얼굴/손 위치.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_13/robot_set/SHEETS/sheet_01/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_13/robot_set/SHEETS/sheet_01/HANDOFF.md)


## 새화풍 그림 전달 unit3 sheet05
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1438, 1093), 원본 (1968, 1496). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 기계식 눈·마스크·턱을 직접 보았고 명백한 인간 코/입술/치아미소 변형은 보이지 않습니다. 얼굴세부/원본정합은 미검수.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 샌드록6판완료. 뒤돌아선 포즈 방향·등/어깨 장갑·쇼텔곡률·천가림 일관성과 마스크폭 비교.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_3/robot_set/SHEETS/sheet_05/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_3/robot_set/SHEETS/sheet_05/HANDOFF.md)


## 새화풍 그림 전달 unit3 sheet06
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (2112, 744), 원본 (1760, 620). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 기계식 눈·마스크·턱을 직접 보았고 명백한 인간 코/입술/치아미소 변형은 보이지 않습니다. 얼굴세부/원본정합은 미검수.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 샌드록6판완료. 뒤돌아선 포즈 방향·등/어깨 장갑·쇼텔곡률·천가림 일관성과 마스크폭 비교.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_3/robot_set/SHEETS/sheet_06/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_3/robot_set/SHEETS/sheet_06/HANDOFF.md)


## 새화풍 그림 전달 unit13 sheet02
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1286, 1223), 원본 (1372, 1304). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 기계식 눈·마스크·턱을 직접 보았고 명백한 인간 코/입술/치아미소 변형은 보이지 않습니다. 얼굴세부/원본정합은 미검수.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: unit13 두판완료. 원본눈색/기계마스크와 윙 부스터/장갑접합·주먹·자세배치 검수 필요.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_13/robot_set/SHEETS/sheet_02/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_13/robot_set/SHEETS/sheet_02/HANDOFF.md)


## 새화풍 그림 전달 unit16 sheet01
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1313, 1198), 원본 (1348, 1228). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 눈·평평한 기계 마스크·작은 턱을 직접 보았고 명백한 인간 입술/치아미소는 보이지 않습니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 은색/흰 몸체명도·후면방향·속도선 길이/밀도·팔위치와 주먹 개수.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_16/robot_set/SHEETS/sheet_01/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_16/robot_set/SHEETS/sheet_01/HANDOFF.md)


## 새화풍 그림 전달 unit20 sheet01
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1266, 1243), 원본 (1332, 1308). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 눈·평평한 기계 마스크·작은 턱을 직접 보았고 명백한 인간 입술/치아미소는 보이지 않습니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 올리브색 장비 개수/부착위치, 손과 장비 가림, 원본 장갑명도/머리각도.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_20/robot_set/SHEETS/sheet_01/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_20/robot_set/SHEETS/sheet_01/HANDOFF.md)


## 새화풍 그림 전달 unit32 sheet01
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (2064, 762), 원본 (1040, 384). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 비인간형 함체/연기라 얼굴을 추가하지 않았습니다. 연기는 검은 외곽선 없는 부드러운 회색 구름으로 보입니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 연기 덩어리 윤곽/개수·명암비율·하부스트럿 노출과 기체/황금포드 크기·좌표 비교.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_32/robot_set/SHEETS/sheet_01/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_32/robot_set/SHEETS/sheet_01/HANDOFF.md)


## 새화풍 그림 전달 unit20 sheet02
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1663, 945), 원본 (816, 464). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 좁은 황색 눈·기계 마스크·작은 붉은 턱을 직접 보았고 인간 입술/치아미소는 보이지 않습니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: unit20 전2판완료. 올리브 장비 접합/개수·얼굴마스크·팔방향 및 원본실루엣/색 대조.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_20/robot_set/SHEETS/sheet_02/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_20/robot_set/SHEETS/sheet_02/HANDOFF.md)


## 새화풍 그림 전달 unit35 sheet01
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1586, 992), 원본 (512, 320). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 비인간형 항공기 구조이며 추가 얼굴은 보이지 않았습니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 하부 녹색 레일/포구·윗날개/포신 수, 측면원형장비 크기·원본비율/좌표 비교.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_35/robot_set/SHEETS/sheet_01/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_35/robot_set/SHEETS/sheet_01/HANDOFF.md)


## 새화풍 그림 전달 unit16 sheet02
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1609, 977), 원본 (1300, 788). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 눈·평면 기계마스크·붉은턱 분리가 보입니다. 최초출력의 넓은 옅은알파 배경을 실제알파 어두운합성에서 확인하여 내장도구로 배경만1회 수정했습니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 현재4자세의 여백 alpha0와 외곽·원본위치/가림 재확인. 최초 RAW에는 실제 alpha13배경이 존재해 보류, 코드로 alpha를 지우지 않았습니다.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_16/robot_set/SHEETS/sheet_02/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_16/robot_set/SHEETS/sheet_02/HANDOFF.md)


## 새화풍 그림 전달 unit36 sheet01
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1652, 952), 원본 (576, 332). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 비인간형 항공기이며 코/입처럼 해석될 수 있는 기수 벤트는 원본기하와 특히 대조해야 합니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 보라 후면 장비의 각도/개수·원형부 크기·아래프레임/기수 벤트 원본기하 비교.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_36/robot_set/SHEETS/sheet_01/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_36/robot_set/SHEETS/sheet_01/HANDOFF.md)


## 새화풍 그림 전달 unit37 sheet01
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1947, 808), 원본 (1504, 624). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 비인간형 항공기이며 코/입처럼 해석될 수 있는 기수 벤트는 원본기하와 특히 대조해야 합니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 기수에 얼굴처럼 읽힐 수 있는 창/벤트를 추가했는지 원본비교, 쌍포신 길이/각도·연기덩어리·흰회색색분포·원본위치.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_37/robot_set/SHEETS/sheet_01/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_37/robot_set/SHEETS/sheet_01/HANDOFF.md)


## 새화풍 그림 전달 unit34 sheet01
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1627, 967), 원본 (1104, 656). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 3상태와 우하빈칸을 직접 확인했습니다. 연기는 외곽선 없는 회색 구름으로 그렸고 기수벤트는 원본과 대조 필요합니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 대체2x2 후보입니다. 공식layout.json을 절대 적용하지 말고 layout_alt_2x2.json 기준 위치/크기 정합후채택. 원본공식가로판보존. 연기개수/틈/명암과 cyan장비부착·기수벤트 확인.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_34/robot_set/SHEETS/sheet_01/candidate_sheet_alt_2x2.png) · [세부인계](../test_current/parts/pose_packets/unit_34/robot_set/SHEETS/sheet_01/HANDOFF.md)


## 새화풍 그림 전달 unit38 sheet01
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1335, 1178), 원본 (1452, 1280). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 원본 녹색 눈·평평한 기계마스크·턱을 직접 확인했습니다.39번은 첫출력윗중앙의 원본없는긴발톱을 발견해 내장도구1회수정후 작은주먹으로돌렸습니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 기계마스크폭/쉴드 녹색부품과 외곽깃모양·라이플포구·손가림 비교.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_38/robot_set/SHEETS/sheet_01/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_38/robot_set/SHEETS/sheet_01/HANDOFF.md)


## 새화풍 그림 전달 unit39 sheet01
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1313, 1198), 원본 (1348, 1228). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 원본 녹색 눈·평평한 기계마스크·턱을 직접 확인했습니다.39번은 첫출력윗중앙의 원본없는긴발톱을 발견해 내장도구1회수정후 작은주먹으로돌렸습니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 원본 분홍장갑과 적색가슴의 실제색·얼굴 마스크/턱과 손수·포즈별팔방향·속도선/윙형상 대조.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_39/robot_set/SHEETS/sheet_01/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_39/robot_set/SHEETS/sheet_01/HANDOFF.md)


## 새화풍 그림 전달 unit40 sheet01
- 내장 이미지 도구로 원본과 데스사이즈 화풍을 직접 참조해 새로 그렸습니다. 출력 (1319, 1193), 원본 (1416, 1280). RAW/candidate/prompt/해시를 저장했습니다. 재색칠·코드 알파 마스크 처리는 하지 않았습니다.
- 생성자 얼굴 확인: 원본 녹색 눈·평평한 기계마스크·턱을 직접 확인했습니다.39번은 첫출력윗중앙의 원본없는긴발톱을 발견해 내장도구1회수정후 작은주먹으로돌렸습니다.
- Claude 검증: 원본 눈 수·센서색·평평한 마스크와 턱, 판간 같은 부품의 일관성, 손발/가슴/무장/실루엣·원본좌표·비율·알파·효과개수/길이. 출력 배율에 맞춰 정합한 뒤 분할해야 합니다.
- 추가중점: 원본 분홍장갑과 적색가슴의 실제색·얼굴 마스크/턱과 손수·포즈별팔방향·속도선/윙형상 대조.
- 미검수 후보이며 합격/설치 완료가 아닙니다.

[후보](../test_current/parts/pose_packets/unit_40/robot_set/SHEETS/sheet_01/candidate_sheet.png) · [세부인계](../test_current/parts/pose_packets/unit_40/robot_set/SHEETS/sheet_01/HANDOFF.md)
