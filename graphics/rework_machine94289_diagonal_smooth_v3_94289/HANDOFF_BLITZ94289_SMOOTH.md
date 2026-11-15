# 94289 주황 대각획 새 HD 후보

상태: 같은 ID 교체 그림 후보. 연결·굽기·공식 판정은 Claude 담당입니다.

- `queue_entry.json`에 네 파일 SHA와 실제 작업 시점 prior spec SHA가 있습니다. contract/drawing/native/generated 모두 제공했습니다.
- `contract.json`, `candidate_atlas.png`, `native_atlas.png`, `generated_raw.png`, `native_prior_new_comparison.png`.
- 그림 SHA `b0f2c446ca946eb2add0d2d850c3a343e7069d58f9232be74f8e4ee634580492`, native8×16/HD32×64.
- 실제 원본: `source_mechanical_53_241/source_pose.state` +0/OAM3, 화면(101,70), RGB807414989/index2237994330. 실제 cached index/full16을 현재 spec과 대조하고 RGB를 재계산했습니다. 기존 소스 기록은 IMG8438(176,16)이며 이번 그림도 같은 실제 색을 기준으로 합니다. 같은 raw/full16 완전 포함 파츠는 없습니다.

기존의 오른쪽 가장자리에 몰린 가는 빨강 선 대신, 원본의 넓은 윗중앙 꺾임과 아래 주황 면을 그렸습니다. 사각색면 초안은 설치 금지로 보존했습니다. 다음 매끄러운 초안도 가운데 폭이 좁아 추가 생성으로 넓혔고, 그 전 그림은 `generated_thin_smooth_before_width_fix.png`로 보존했습니다. 최종은 사각 픽셀색면을 복제하지 않은 연속 곡면입니다.

원본에는 검정 재료가 없으므로 검정 외곽선·받침은 추가하지 않았습니다. 원본 RGB/알파 전사·native mask·코드 재색칠·알파 삭제는 없습니다. 원본의 작은 굽은 획을 매끄럽게 해석했으므로 윗중앙 폭과 원본 중심선·인접부 위치는 Claude 실제 판정 대기입니다. 자동 합격으로 적지 않습니다.

중앙 데이터·코어·DB를 변경하지 않았으며 prepare/굽기/공식 QA/HD 재생을 하지 않았습니다.
