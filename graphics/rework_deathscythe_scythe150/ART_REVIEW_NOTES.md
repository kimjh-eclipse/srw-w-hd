# 데스사이즈 낫날 +150 한 단계 제작 인계

## 범위
이전 보고의 "낫날2단계"는 부정확했습니다. duo_cutin +150에서 동시에 이어져 나오는 좌우32×16 조각2개이며, IMG7105의[0,144,32,16]과[32,144,32,16]입니다. 한 연속64×16 그림을 새로 그린 뒤 중앙에서 잘랐습니다.

## 입력
- candidate_atlas.png:256×64(4배). install_contract.json atlas_box는1배64×16 기준.
- generated.png: image_gen 생성 원본.
- native_reference.png/native_sheet.png: 실제 렌더 캐시의 낫날을 연속 배치.
- pose_reference.png/native_pose.png: 손잡이/기체와 연결되는 원본 문맥.
- pose_dependencies.json: 이 프레임 전신15 OAM 중 나머지13개의 기존 normal20/next14 후보 의존. 기존 exact RGB는 새로 바꾸지 않습니다.
- mechanical_input_check.json: 실제hash/캐시크기/source index 바이트 일치,기본DLL경로와SHA.

## Claude 확인 위치와 위험
- fixture test_current/combat/duo_cutin.state, offset150(load후151run).
- 좌우 낫날 조각의 중앙 경계와 손잡이 기점 접합,기체/이펙트/UI 레이어 확인.
- 생성 그림의 둥근 끝과 작은 휘날림이 원본보다 길거나 넓을 수 있습니다. 표면 밝은 띠 폭/위치와 순수녹색 부분도 원본과 대조가 필요합니다.
- 알파는 생성 결과를 보존했습니다. 원본 알파/RGB를 찍지 않았고 키색 일괄 삭제는 하지 않았습니다. 가장자리 반투명 잔여는 Claude가 확인해야 합니다.
- QA·독립 시각 판정·HD 재생 검증은 수행하지 않았습니다. live/DB/library/공유코드는 수정하지 않았습니다.
- 이어서 관측된 나머지 제작 우선순위는 ../OBSERVED_WEAPON_PRIORITY.md 및 observed_weapon_inventory.json에 있습니다.7개 스냅샷에서 이번 재제작 후보50종,아직 이번 후보에 없는10종(IMG7084 8/7085 2)입니다. 이는 전체 무장 완료율이 아닙니다.

## exact 대상
| cell | OAM | actual RGB | index hash |
|---|---:|---:|---:|
| 0 | 24 | 1592824817 | 760394337 |
| 1 | 14 | 3599948006 | 3701720510 |
