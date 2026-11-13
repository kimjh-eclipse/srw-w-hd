# IMG20498 미관측 35개 추가 그림 — Claude 검증 대기

## 제작 결과
- `candidate_20498_unobserved_pair.png`: 1024×768, 원본 좌표계 256×192. bank0 y=0, bank1 y=96.
- `new_20498_unobserved_generated_contract.json`: 새 35개. 앞서 인계한 재사용 8개와 별개이며 이미 연결된 42개를 덮지 않는다.
- 원본 IMG20498/PAT20499 단일 이미지 패턴, PLT20497 각 bank의 16개 u16 값이 실제 cached OBJ 팔레트와 완전히 일치한다. `20498_palette_witness.json`에 실제 state/frame/OAM 증거.
- 이 35개 shape 자체는 보유 재생에서 관측하지 않았다. 원본 리소스/패턴/팔레트 확정에 따른 제작 계약이며 실제 등장·그림 품질 판정은 Claude 대기.
- 각 crop maxA≥16, 원본 불투명 픽셀 수 대비 생성 alpha 지원 면적 10% 이상. 이는 거의 빈 그림을 제외하는 제작 무결성 확인뿐이며 형태 일치 QA가 아니다.

## 생성 및 복원
- built-in imagegen으로 두 bank를 각각 새로 그렸다. 기존 다른 효과 재색칠 없음.
- 전체 생성본이 하단의 넓은 불투명 연속면을 투명하게 만들었으므로, 같은 효과의 하단 연속면 두 색을 별도 생성했다.
- `generated_continuation_rgb.png`의 직접 생성 RGB와 `generated_continuation_alpha.png` 오른쪽 bank의 직접 생성 alpha를 사용. 두 bank의 원본 index geometry는 같은 IMG이므로 동일하다. 생성 RGB의 검은 배경만 제외했고, 원본 RGB/alpha를 복사하거나 원본 mask로 찍지 않았다.
- `prepare_new_full_pair.py`에 재현 절차. 원본 bbox조차 강제로 찍지 않는다.
- 전체 시트의 먼지/입자 영역은 생성기가 구슬처럼 과장했지만 이번 35개 crop은 그 영역을 쓰지 않는다. 이미 연결된 파츠는 보존해야 한다.

## 남은 시각적 위험 / Claude 큐
- 하단 연속면과 나머지 새 그림이 만나는 source x64 경계의 색 밴드 높이 차이 가능.
- 긴 빔의 상하 절단면에 생성 외곽선이 일부 생겼을 가능성, 원본 대비 곡선 과장/민트 농도 차이. 후보 저장을 정상 판정으로 해석하면 안 된다.
- 미관측 shape이므로 먼저 해당 PAT pose/record에 대응하는 실제 fixture를 확보한 뒤 재생 판정해야 한다. witness에 적힌 기존 fixture는 팔레트 증거이고 이 35개 전부의 등장 증거가 아니다.
- 라이브 라이브러리/DB/코어 수정 및 실제 HD 재생 검사 없음.
