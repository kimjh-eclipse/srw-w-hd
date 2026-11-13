# 기계 부품 후보 298_180

현재 상태: 새 그림 제작 및 설치 입력 준비. 검증은 Claude 담당이며 실제 HD 재생/품질 판정은 하지 않음.

- 최종 그림: `test_current\parts\mechanical_rework_three\298_180/candidate_atlas.png` (원본 아틀라스 정확 4배).
- 원본 참조: `test_current\parts\mechanical_rework_three\298_180/native_atlas.png`.
- 설치 계약: `test_current\parts\mechanical_rework_three\298_180/install_contract.json`, 3개 actual cached RGB.
- 원본 전체 문맥: `test_current\parts\actual_mechanical_pose_298_180/whole_native_context.png` 및 `all_rendered_obj_contracts.json`.
- 생성 원본: 상위 `generated_isolated_grid.png`, 각 부품 자체 투명도 생성. 원본 RGB/알파 복사나 wholepose 사각 crop 아님.
- Claude 확인 fixture: `test_current\combat\named_attacks\unit_298\mechanical_cutin_140.state` +180, 관련 OAM [21, 22, 23].
- 메모리 prepare nonempty 확인만 수행, DB/코어/라이브 변경 없음.
- 알려진 위험: 생성 과정에서 기계 세부면/절단면을 발명했을 수 있음. 개별 생성이라 원본 기하와 이웃 연결/실색은 Claude가 판정해야 함. 미확정 소유 ROM IMG는 None으로 유지.
- 기존 graphics/rework_great_thunder168_cached/pose_contract.json 17개와 actual index byte+w/h 비교 시 세 부품 모두 동일 없음. 전체 라이브 동일 바이트 검색도 동일 없음. scene 이름이 비슷해도 같은 원본으로 단정하지 않음. 형제 unit299 동일 source 중복 재생산하지 않음.
