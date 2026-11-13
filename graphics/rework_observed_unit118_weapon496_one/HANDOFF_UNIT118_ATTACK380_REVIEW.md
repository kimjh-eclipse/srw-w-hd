# 실제 unit118 / weapon496 메뉴380 머리 변형 1종 후보

상태 `CACHED_OBJ_ARTWORK_CANDIDATE_UNVERIFIED`. 실제 HD 게임 재생/공식 QA는 Claude 담당. 라이브/DB/코어 변경 없음.

- 설치 입력: installation_map.json, candidate_atlas.png, native_atlas.png, contract.json.
- 후보 SHA256: `14be70e944c0bfc9f19dfdf8935e31c3743758a5420abf2aa430c453619c8fd8`.
- 실제 fixture: `source_mechanical_fixed_118_496_350/source_pose.state` +0. 메뉴380에서 캡처했다.
- actual hash3378819930,32×32 머리 변형, exact0/indexed0. IMG10054(96,0) 원본 인덱스와 바이트 일치한다.
- unit117 직전 머리와 비슷하지만 raw SHA와 불투명 지원영역/빨강·주황 면이 달라 새로 그렸다. 다른 기체 그림을 재색칠하거나 기존 머리 색만 바꾼 것이 아니다.
- 이 자세의 다른 미연결3종은 직전 unit117 후보와 actual RGB/인덱스 SHA/전체16색이 같아 새 그림을 중복 제작하지 않는다. `shared_existing_candidates.json`으로 의존을 증명했다. 나머지 다른 하체 indexed proxy도 재제작하지 않았다.
- 생성에서 원본의 왼쪽 작은 빨간 슬릿, 파란 헬멧, 넓은 빨강·주황 띠와 아래 오른쪽 대각 빨강 면, 회백 마스크/뿔이 잘린 캔버스를 참조했다. 새 양눈이나 금색뿔을 넣지 않았다.
- 생성원본 보존, 자체 alpha<64만 정리하고 고알파RGBA 불변. native RGB/알파 스탬프 없음.
- 제작 조립은 새 머리1 + 나머지 native 참고이며 기존 unit117 HD3종까지 모두 조립한 공식 HD 결과가 아니다.

Claude 위험: 빨강 띠가 원본 기계 표면인지 실제 연출 단계인지, 색 면의 위치/밝기·빨간 눈과 주황 하단면 크기, 목·기존몸체 경계와 AA를 실제 장면에서 판단해야 한다. actual 원본 차이를 무시해 기본 머리를 재사용하지 않았으나 변형 전체무장 완료라고 세지 않는다.
