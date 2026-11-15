# 95247 실제 어두운 올리브 지지면 후보

상태: 같은 ID 95247 교체용, Claude 연결·실제 장면 판정 대기. 신규 누락 해소 수에는 추가하지 않습니다.

- 설치 입력 `installation_map.json` / `contract.json` / `candidate_atlas.png` / `native_atlas.png`.
- 실제 상태 `test_current/parts/native_weapon_source_424_1650/unit424_weapon1650_source.state` +390, OAM8, 화면(76,73), 8×8, 불투명7texel. 기존 제작 폴더의390 식별자는 실제 unit424 소유를 의미하지 않습니다. 반전·아핀 없음. RGB1688207606을 cached index+실제 BGR555 16색으로 재계산해 확인했습니다.
- 실제는 어두운 올리브 [32,32,24]의 넓은 불투명 계단 면과 맨 아래 오른쪽 [65,57,49] 한 칸입니다. 기존 그림은 가는 곡선이 되어 고형면을 잃었습니다. 새 그림은 자체 생성한 평평한 두 재료면이고, 장식·금색·곡선·절단면 윤곽은 추가하지 않았습니다.
- 4배32×32 후보 SHA `1a517946762024eedd111d4bbcb3fd153de6feb86eafb49e697531ec39efea5b`.
- 후보/NullCache prepare 기하 IoU1/미칠0/외부0/flags0. 이 수치는 실제 화질이나 레이어 합격을 뜻하지 않습니다. 원본 RGB/알파 전사, 재색칠 코드, 알파 문턱 삭제는 하지 않았습니다. 생성 원본·정렬 근거를 보존했습니다.
- 같은 atlas 정상7개는 `preserved_normal7.json` 그대로입니다. 실제 미세 부품 역할은 어두운 기계 접합면 수준까지만 확정하며 해부학적 명칭은 추정하지 않습니다.

## 기존 큰 그림과의 관계: 연결 판단 필요

전체 팔레트·index가 같은 원본 영역은 legacy `full_attack_070`의 #64028(16,16), #64029(8,16), #64030(0,16)에 포함됩니다. 그러나 그 원천 HD crop은 노란/금색이고 새 actual source의 어두운 올리브 면과 다르며, 현재95247과도 RGBA 동일하지 않습니다. `legacy_parent_RGBA_comparison.json` 참조.

이 부모 셋은 `registered_attack_bank=False`인 legacy여서 원천 crop만으로 런타임 결과를 확정할 수 없습니다. **정상 부모로 검증된 자료가 아니므로 틀린 노란 crop을 복사하지 않았습니다.** 부모는 변경하지 않았고, 부모의 실제 동시 사용과 접합은 미확정입니다. root 지시에 따라 actual 올리브 단독 후보를 준비했으며 연속 경계·같은 원본의 두 그림 충돌 위험을 Claude에 넘깁니다. 실제 장면 판정 전 최종 해결로 세지 않습니다.

공유 코드·라이브·DB·코어 변경, 공식 QA, HD 재생은 수행하지 않았습니다.
