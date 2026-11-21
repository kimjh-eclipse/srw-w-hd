# Codex → Claude 23 — 최대9자세 시트 전달 현황

갱신: 2026-11-15T19:30:04+09:00

사용자가 확정한 새 규칙: **한 판 최대9자세, 첫 칸 공통 기본 자세.** Claude의 SHEETS 입력/layout 그대로 사용하고, 첫판을 후속판 스타일 참고로 넣습니다. 원본색/배치/실루엣/가려짐 유지, 다른 팔레트 재색칠 금지. Codex는 그림/원출력 전달, Claude는 정합·분할·연결·굽기·검증 담당입니다.

**새 형식 후보 25장 / 준비 입력 737장 / 후보 미발행 초안 4장.** 검수/설치 완료 수가 아닙니다. 기존 unified 제출과 원본공유 근거는 이 숫자에 합산하지 않았습니다.

이전 작업·룰 전환과 톨기스III/IWSP 수정 사항: [HANDOFF_FROM_CODEX_22.md](HANDOFF_FROM_CODEX_22.md). 기존 대형시트 현황은20/21번 문서. 각 그림 폴더 HANDOFF에 기하·색·효과·외곽잔여 검증 항목을 기록했습니다.

## 현재 전달된 판

| 기체 | 판 | 항목 | 공통 기본 자세 | 그림 |
|---|---|---:|---|---|
| 5 | sheet_01 | 9 | pose_09 | [후보](../test_current/parts/pose_packets/unit_5/robot_set/SHEETS/sheet_01/candidate_sheet.png) |
| 5 | sheet_02 | 9 | pose_09 | [후보](../test_current/parts/pose_packets/unit_5/robot_set/SHEETS/sheet_02/candidate_sheet.png) |
| 5 | sheet_03 | 8 | pose_09 | [후보](../test_current/parts/pose_packets/unit_5/robot_set/SHEETS/sheet_03/candidate_sheet.png) |
| 55 | sheet_01 | 9 | pose_06 | [후보](../test_current/parts/pose_packets/unit_55/robot_set/SHEETS/sheet_01/candidate_sheet.png) |
| 55 | sheet_02 | 9 | pose_06 | [후보](../test_current/parts/pose_packets/unit_55/robot_set/SHEETS/sheet_02/candidate_sheet.png) |
| 57 | sheet_01 | 9 | pose_02 | [후보](../test_current/parts/pose_packets/unit_57/robot_set/SHEETS/sheet_01/candidate_sheet.png) |
| 57 | sheet_02 | 8 | pose_02 | [후보](../test_current/parts/pose_packets/unit_57/robot_set/SHEETS/sheet_02/candidate_sheet.png) |
| 58 | sheet_01 | 9 | pose_04 | [후보](../test_current/parts/pose_packets/unit_58/robot_set/SHEETS/sheet_01/candidate_sheet.png) |
| 58 | sheet_02 | 4 | pose_04 | [후보](../test_current/parts/pose_packets/unit_58/robot_set/SHEETS/sheet_02/candidate_sheet.png) |
| 103 | sheet_01 | 9 | pose_11 | [후보](../test_current/parts/pose_packets/unit_103/robot_set/SHEETS/sheet_01/candidate_sheet.png) |
| 104 | sheet_01 | 9 | pose_06 | [후보](../test_current/parts/pose_packets/unit_104/robot_set/SHEETS/sheet_01/candidate_sheet.png) |
| 105 | sheet_01 | 9 | pose_10 | [후보](../test_current/parts/pose_packets/unit_105/robot_set/SHEETS/sheet_01/candidate_sheet.png) |
| 155 | sheet_01 | 9 | pose_05 | [후보](../test_current/parts/pose_packets/unit_155/robot_set/SHEETS/sheet_01/candidate_sheet.png) |
| 155 | sheet_02 | 9 | pose_05 | [후보](../test_current/parts/pose_packets/unit_155/robot_set/SHEETS/sheet_02/candidate_sheet.png) |
| 156 | sheet_01 | 9 | pose_13 | [후보](../test_current/parts/pose_packets/unit_156/robot_set/SHEETS/sheet_01/candidate_sheet.png) |
| 156 | sheet_02 | 9 | pose_13 | [후보](../test_current/parts/pose_packets/unit_156/robot_set/SHEETS/sheet_02/candidate_sheet.png) |
| 157 | sheet_01 | 7 | pose_04 | [후보](../test_current/parts/pose_packets/unit_157/robot_set/SHEETS/sheet_01/candidate_sheet.png) |
| 158 | sheet_01 | 7 | pose_04 | [후보](../test_current/parts/pose_packets/unit_158/robot_set/SHEETS/sheet_01/candidate_sheet.png) |
| 313 | sheet_01 | 2 | pose_00 | [후보](../test_current/parts/pose_packets/unit_313/robot_set/SHEETS/sheet_01/candidate_sheet.png) |
| 314 | sheet_01 | 9 | pose_00 | [후보](../test_current/parts/pose_packets/unit_314/robot_set/SHEETS/sheet_01/candidate_sheet.png) |
| 314 | sheet_02 | 3 | pose_00 | [후보](../test_current/parts/pose_packets/unit_314/robot_set/SHEETS/sheet_02/candidate_sheet.png) |
| 315 | sheet_01 | 4 | pose_02 | [후보](../test_current/parts/pose_packets/unit_315/robot_set/SHEETS/sheet_01/candidate_sheet.png) |
| 316 | sheet_01 | 8 | pose_04 | [후보](../test_current/parts/pose_packets/unit_316/robot_set/SHEETS/sheet_01/candidate_sheet.png) |
| 317 | sheet_01 | 5 | pose_01 | [후보](../test_current/parts/pose_packets/unit_317/robot_set/SHEETS/sheet_01/candidate_sheet.png) |
| 318 | sheet_01 | 5 | pose_02 | [후보](../test_current/parts/pose_packets/unit_318/robot_set/SHEETS/sheet_01/candidate_sheet.png) |

## 적용 보류

명백한 배경/전체비율 실패는 정식 후보로 발행하지 않고 원출력과 사유를 보존합니다. 같은 원본으로 도구 재시도는 한 번만 합니다. 코드를 통한 알파삭제/원본마스크/재색칠/분할은 하지 않습니다.
- unit55/sheet_03: 후보 미발행. 해당 폴더 HANDOFF/실패 기록 참조.
- unit59/sheet_01: 후보 미발행. 해당 폴더 HANDOFF/실패 기록 참조.
- unit60/sheet_01: 후보 미발행. 해당 폴더 HANDOFF/실패 기록 참조.
- unit312/sheet_01: 후보 미발행. 해당 폴더 HANDOFF/실패 기록 참조.

## 계속 진행

root: unit5 수정·22 실루엣 보완 및100~109. pink:48~149(100~109 제외). mihiro:150~299. wing:300 이상. 이전 unified 완성본은 재요청 전 유지하며, 새 생성은 모두 SHEETS 형식입니다. 준비 입력 파일 수는 Claude의 추가 자료 생성에 따라 달라질 수 있습니다.
