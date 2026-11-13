# 빔 전경 합성 수정 — 2026-11-13

## 확인한 원인과 변경 범위

발호크 무장 1613의 저장 상태 frame_1320에서 빔 BG와 기체 OBJ가 같은 우선순위를 사용한다. 기존 코드는 이 경우 OBJ를 앞에 두므로 HD 기체가 발광 빔을 가렸다. 하드웨어의 일반 tie 규칙 자체가 오류인 것은 아니다. 사용자가 요청한 에너지 연출 순서를 위해, 가산 발광(EVA>0, EVB=16)이고 OBJ가 두 번째 합성 대상일 때만 동일 우선순위의 빔을 기체 위로 합성한다.

- 기체 ID나 무장 ID별 예외가 없는 공통 처리다.
- 불투명 배경과 일반 알파 효과의 tie 규칙은 유지한다.
- 캐릭터 컷인(BG 대상) 위로 효과를 강제로 승격하지 않는다.
- 살아 있는 앞쪽 OBJ의 가림 마스크를 통과하지 못하면 기체를 다시 드러내지 않는다.
- 기존 전면 BG는 종전의 우선순위/알파 계수를 유지한다.
- 이번 변경은 동순위 가산 발광 문제를 해결한다. 원본에서도 더 뒤의 우선순위인 모든 BG를 무조건 앞으로 보내는 변경이 아니다. 모든 캠페인 장면이 해결됐다고 인증하지 않는다.

## 검증

1. verify_foreground_blend.py: 색 산술, 일반 tie 유지, 발광 tie 승격, BG 컷인 보호, fast/slow 일치, GPU/CPU 일치, 투명도 보존 통과. GPU/CPU 최대 차이 0.
2. verify_beam_order.py: 게임을 90프레임 진행시키며 같은 프레임의 구 경로/수정 경로를 비교. 최대 23,849개 출력 픽셀이 바뀐 24프레임 그림을 직접 확인했다. 이 비교는 동기 준비 미술 진단이며 실제 플레이어 경로 검사를 대체하지 않는다.
3. verify_runtime_path.py: 별도의 실제 비동기 준비/ready 전달 경로로 90프레임 재생. frame_1320은 REVIEW, 소실/로딩/원본 유지 0, 안정 구간 HD 면적 99.1%, 유색 빔 tie 합성 89,780 픽셀 누계. frame_1320_running_24.png에서 기체 위 빔과 그 위 대사창을 직접 확인했다.
4. 추가 8개 보유 상태 회귀: 소실 0. NO_HD_PARTS 3, INCOMPLETE 5. 기존 미연결 HD와 BG 기반 장면의 판정은 별도로 남아 있다. 이 수치는 시각적 정상이나 전 기체 완성의 근거가 아니다.
5. program-only EXE 재빌드 및 배포 폴더 반영 완료. SRW_W_Test.exe의 내장 foreground_blend 모듈에서 ENERGY_TIES가 들어간 것을 확인했다. 실행 중인 이전 프로세스는 자동으로 갱신되지 않는다.

## 증거 위치

- test_current/combat/beam_order_comparison/{before,after,difference}.png
- test_current/combat/runtime_path/beam_order_final/report.json
- test_current/combat/runtime_path/beam_order_final/frame_1320_running_24.png
- test_current/combat/runtime_path/beam_order_regression/report.json

ROM, 저장 상태, 캐시에는 변경하지 않았다. 소스 변경은 emulator/foreground_blend.py, emulator/hd_parts.py 및 검사 도구에 있다.
