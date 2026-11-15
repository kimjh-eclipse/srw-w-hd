# 93271 주황 대각면 새 HD 후보

상태: 같은 ID 교체 그림, 실제 판정 대기. 과거 보존 판단은 Claude 최신 판정으로 폐기했습니다. 연결·굽기·검증은 Claude 담당입니다.

- `queue_entry.json`에 contract/drawing/native/generated 네 파일 SHA와 prior spec SHA를 보존했습니다. 중앙 큐에 쓰지는 않았습니다.
- `contract.json`, `candidate_atlas.png`, `native_atlas.png`, `generated_raw.png`, `native_prior_new_comparison.png`.
- 그림 SHA `7c2de59a07023cd2f92b95ed07bd6ae331fdf4c317b69d8b52d4b69002903438`, native8×32/HD32×128.
- 실제 원본: unit131/w548 상태 +225/OAM3, 화면(100,75), RGB2173762398/index4029976990. 실제 cached index·전체16색 BGR555로 RGB를 재계산했고 현재 spec와 일치했습니다. 같은 raw/full16 완전 포함 다른 파츠는 없습니다.

기존 그림에서 없어진 넓은 주황 대각면을 다시 그렸습니다. 첫 초안은 사각색면이 커진 느낌이라 설치 금지로 보존했습니다(`claude_machine93271_diagonal_v3`). 이번에는 연속한 매끈한 대각면과 검정 지지재로 자체 새 생성했습니다. 오른쪽 지지재의 윗끝이 원본처럼 왼쪽 팁보다 낮게 시작하도록 추가 생성 수정했습니다. 수정 전 원출력도 보존했습니다.

원본 RGB/알파 전사·native mask·코드 재색칠·알파 문턱 삭제는 없습니다. 생성 RGBA 전체를 자신의 bbox로 정렬했습니다. 기존 메타의 RGB/indexed/dynamic 역할을 바꾸지 않는 후보입니다.

원본의 작은 계단을 매끄러운 대각 경계로 해석했으므로 실제 주황 면의 폭과 검정 뒤판 양, 인접 파츠 접합은 Claude 실제 판정이 필요합니다. 자동 지표나 실제 합격을 주장하지 않습니다. prepare/굽기/공식 QA/HD 재생, 공유 코드·중앙 자료 쓰기를 하지 않았습니다.
