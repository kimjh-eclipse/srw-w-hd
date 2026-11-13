# 소드 계열 후속 실제 자세 131_300

현재: 그림 제작·설치 입력 준비. QA는 Claude 담당, 독립 HD 재생검증 미실행.

- 최종 candidate_atlas.png / native_atlas.png(정확4배) / install_contract.json 6 actual 계약 / provenance.json.
- 원본 fixture `test_current\parts\native_weapon_source_131_548\unit131_weapon548_source.state` +300, OAM [5, 9, 10, 12, 17, 18]. 전체 원본문맥 test_current/parts/actual_mechanical_pose_131_300/whole_native_context.png.
- 다른 부품은 preserved_existing_pose.json대로 보존. 원본과 생성 개별 intrinsic alpha, source bbox 기하정렬만 수행. 원본 RGB/alpha stamp 및 이웃wholeposecrop 없음.
- actual prepare_texture 메모리 NullCache nonempty 확인만. 라이브/코어/DB 변경 없음.
- 원본 바이트/실사용색이 같은19/42 공통 칼1조각은 cross_unit_exact_aliases.json대로19생성 그림 공유(다른기체 재색칠 아님). 전체18계약=17고유RGB 예상.
- 알려진 위험: 생성 모델이 손/갑옷 면을 과하게 각지게 바꾸거나 절단면에 외곽선을 추가했을 수 있어 Claude가 연결과 실제색을 판정해야 함. 새 자세 전체 무장 완료라고 기록하지 않음.
- 해당프레임 계약중 잔여 미분류 source 0종은 remaining_source.json.
