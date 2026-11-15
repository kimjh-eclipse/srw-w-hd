# 그레이트 68884 실제 어두운 팔레트 master 후보

상태: 새 그림과 공유 계약만 준비. Claude 연결·굽기·실제 판정 대기. 과거 보존 판단은 최신 Claude 판정으로 폐기했으며, 정상 색 경고 전체를 다시 그리지는 않았습니다.

## 입력 및 파일

- `queue_entry.json`: 교환 큐에 넣을 항목. contract/drawing/native/generated 네 파일 SHA와 현재 prior spec SHA를 모두 담았습니다. 중앙 큐는 root가 직렬 인계합니다.
- `contract.json`, `candidate_atlas.png`, `native_atlas.png`, `generated_raw.png`, `prior_specs.json`, `drawing_provenance.json`.
- 후보32×32 원본/4배128×128. 그림 SHA `014a41e8618186fa5c2eb6c4eca58cd0af2c5766d2a05124550bd40a7af7481f`.
- `native_prior_new_comparison.png`에서 실제 원본·현재 그림·새 후보를 비교할 수 있습니다.
- 원본은 `test_current/combat/mazinger_combination/frame_1560.state` +0/OAM18, 화면(212,96). cached RGB53746234/index2534254743, 실제16색과 현재 spec이 일치하며 실제 index+BGR555로 RGB를 재계산했습니다.

## 바뀐 그림

기존 그림은 평상시 파랑·흰색으로 그려졌습니다. 새 그림은 원본의 보라·자주색 장갑, 빨간 V/등날개, 어두운 청색 부츠·팔, 노란 눈·뺨뿔, 보라 회색 마스크를 맞춰 다시 그렸습니다. 실제 원본 형태를 기준으로 왼팔의 잘린 부분, 양발 벌린 자세와 오른손을 유지하도록 했습니다.

원본을 재색칠하거나 RGB/알파를 찍지 않았습니다. imagegen 자체 새 그림의 전체 RGBA를 원래 bbox에 정렬했으며 native mask를 씌우지 않았습니다. 매끈한 셀 음영을 사용했습니다. 가슴·뿔·팔·부츠의 실제 위치와 보라 명암 구획이 완전히 맞는지는 Claude 판정 대기입니다.

## 반드시 함께 보는 공유 관계

- 68884: RGB 활성, indexed 비활성. 새32×32 master 전체(0,0).
- 68885: 같은 실제 full16/index가 68884의 (16,0,16,16)에 완전히 포함됩니다. 새 master의 동일64×64 RGBA 영역을 직접 공유합니다. 별도 그림을 만들지 않았습니다. child 단독 OAM 사용은 독립 관측하지 않았습니다.
- 93353: 68884와 원본32×32/index/full16 전부 동일합니다. 새 master 전체를 공유하되 **원래 rgb_enabled=False/indexed_safe=True**인 fallback 역할을 그대로 유지해야 합니다. 임의 RGB 활성화 금지.
- 68895는 이번 actual full16/index 포함 관계가 없어 변경하지 않았습니다.

이들은 실제 원본 포함/동일 관계이며 다른 기체·다른 색 그림을 빌려 쓰는 것이 아닙니다. 네이티브 bytes와 전체 palette 검산·현재 spec SHA는 계약/생성 스크립트에 보존했습니다. 겹치는 영역은 같은 master의 같은 좌표를 쓰므로 생성 RGBA도 동일합니다.

## 미수행

공유 코드·코어·중앙 라이브러리·DB·캐시·manifest를 수정하지 않았습니다. prepare/굽기/공식 QA/HD 재생을 수행하지 않았고 자동 검사 통과나 실제 해결로 기록하지 않습니다.
