# 실제 unit145 / weapon608 메뉴350 미연결 조각1 후보

상태 CACHED_OBJ_ARTWORK_CANDIDATE_UNVERIFIED. 공식 시각 검사 및 실제 HD 재생은 Claude 담당이며 수행하지 않았다. 라이브/공유 코드/코어/DB 변경없음.

- 설치 입력: installation_map.json, candidate_atlas.png, native_atlas.png, contract.json.
- 후보 SHA256: ea67d5e13ad4ee4248fdeb1be92865470e70e0c2d6fd11a295352696fdcf2163.
- 실제 fixture: source_mechanical_fixed_145_608_350/source_pose.state +0. 단일32×16, RGB hash553727985. actual exact/indexed 모두 미연결. 원본IMG10768(56,0)의 index bytes와 일치한다.
- 전체16색은 메뉴200/350에서 동일하지만 ROM 팔레트의 단일 소유자는 확정하지 못했다. owner=None을 유지한다. observed_palette_and_role_trace.json에 비교 보존.
- 청색 기계손/주황분사 혼합 조각이다. 최초 생성 프롬프트에서 독립 발사체로 가정했으나 인접20프레임에서 몸체13파츠 전부와 동일하게 x-79/y0 이동했음을 확인하여 이 해석을 취소했다. 상세 기능/기술명 미확정. 이 정정은 그림 의미 판정의 위험으로 보존한다.
- 생성 출처 exec-c19c2824-0761-45f6-b4d6-60fc63a3a749.png. native RGB/알파/마스크 스탬프 없음. 생성 자체 alpha<64만 RGBA0 정리하고 고알파 원본을 보존했다.
- 기계적 검사: raw SHA/크기/실제 팔레트 원본RGB 일치, 후보 비어있지 않음/maxalpha255. candidate_pose_production.png는 신규1조각+나머지native 조립 제작참고이며 실제HD게임검사가 아니다.

Claude 위험: 회백색 돌출부 개수/손가락 해석, 청색 둥근 면과 검정 뒤쪽 테두리, 주황분사 영역의 형태와 인접 몸체 연결을 확인해야 한다. 독립 발사체라는 초기 잘못된 프롬프트 의미가 그림 형태에 영향을 주었을 수 있다. 전체 무장/기체 완료로 세지 않는다.
