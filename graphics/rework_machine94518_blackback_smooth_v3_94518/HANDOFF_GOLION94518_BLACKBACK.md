# 94518 불투명 검정 뒤판과 곡면 패널 후보

상태: 같은 ID 교체 그림. 연결·굽기·검증은 Claude 담당입니다.

- `queue_entry.json`에 네 필수 파일 SHA와 prior spec SHA를 보존했습니다.
- `contract.json`, `candidate_atlas.png`, `native_atlas.png`, `generated_raw.png`, `native_prior_new_comparison.png`.
- 그림 SHA `5825400e1d4f2ea8ee50257913b0f8caed3da7addb78df8c0a87e55e2c1cab59`, native16×16/HD64×64.
- 실제 원본: unit404/w1591 상태 +610/OAM1, 화면(136,72), RGB1498162686/index2594634152. cached 원본·실제16색·현재 spec을 대조하고 RGB 재계산 일치를 확인했습니다. 같은 raw/full16 완전 포함 다른 파츠는 없습니다. IMG 소유 미확정 상태를 유지합니다.

원본 왼쪽의 검정은 빈 공간이 아닌 불투명 재질입니다. 기존 그림은 이를 없애 초록 막대처럼 보였습니다. 새 그림은 넓은 불투명 검정 뒤판을 복원하면서 오른쪽 흰색·초록·파랑·빨강 패널을 연속한 매끄러운 곡면으로 그렸습니다. 사각색면을 키운 첫 초안은 설치 금지로 보존했습니다(`claude_machine94518_blackback_v2`).

검정 뒤판은 자체 생성의 실제 불투명 면입니다. 원본 RGB나 알파를 덮어찍거나 원본 마스크로 자르지 않았고, 코드 재색칠·알파 문턱 삭제도 없습니다. 실제 원본의 평평한 색 경계는 곡면 음영으로 해석했으므로 초록/흰 띠의 광택 밝기와 폭, 외곽 접합은 Claude 실제 판정이 필요합니다. 검정 면 복원 후보라는 사실을 전체 색·형태 합격으로 쓰지 않습니다.

중앙 라이브러리·DB·캐시·manifest·코어에 쓰지 않았습니다. prepare/굽기/공식 QA/HD 재생을 하지 않았습니다.
