# 기계 부품 후보 256_130

현재 상태: 새 그림 제작 및 설치 입력 준비. 검증은 Claude 담당이며 실제 HD 재생/품질 판정은 하지 않음.

- 최종 그림: `test_current\parts\mechanical_rework_three\256_130/candidate_atlas.png` (원본 아틀라스 정확 4배).
- 원본 참조: `test_current\parts\mechanical_rework_three\256_130/native_atlas.png`.
- 설치 계약: `test_current\parts\mechanical_rework_three\256_130/install_contract.json`, 3개 actual cached RGB.
- 원본 전체 문맥: `test_current\parts\actual_mechanical_pose_256_130/whole_native_context.png` 및 `all_rendered_obj_contracts.json`.
- 생성 원본: 상위 `generated_isolated_grid.png`, 각 부품 자체 투명도 생성. 원본 RGB/알파 복사나 wholepose 사각 crop 아님.
- Claude 확인 fixture: `test_current\combat\named_attacks\unit_256\mechanical_cutin_160.state` +130, 관련 OAM [3, 4, 13].
- 메모리 prepare nonempty 확인만 수행, DB/코어/라이브 변경 없음.
- 알려진 위험: 생성 과정에서 기계 세부면/절단면을 발명했을 수 있음. 개별 생성이라 원본 기하와 이웃 연결/실색은 Claude가 판정해야 함. 미확정 소유 ROM IMG는 None으로 유지.
- 원래 5개 중 cell2/OAM12 및 cell4/OAM15는 준비 도중 현재 라이브 RGB/indexed 연결이 확인되어 설치 계약에서 제외. 원본 계약은 all_five_source_contracts.json에 보존. 나머지 원본 자세 부품도 그대로 보존.
