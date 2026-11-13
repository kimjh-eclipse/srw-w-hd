# 실제 unit86 / weapon366 +300 기계 6종 미검증 후보

상태 `CACHED_OBJ_ARTWORK_CANDIDATE_UNVERIFIED`. 라이브·코어·DB 변경 없음, 공식 검사와 실제 HD 재생은 Claude 대기.

- 입력: `installation_map.json`, `candidate_atlas.png`, `native_atlas.png`, `contract.json`.
- SHA256: `54ad9ec1e84a45c05aa9036930eb06e5bdb23b7eef9180ff9486856fb01ab4ed`.
- 실제 fixture: `source_mechanical_fixed_86_366_300/source_pose.state` +0. 메뉴 캡처 시점 300, actual cached OBJ/팔레트/OAM 및 코어 SHA는 계약에 보존했다.
- 미연결 5종 + indexed proxy 재제작 1종(셀3, 메타5485/6049). 전체 actor palette0 OAM17 중 나머지 기존 exact 그림은 의존관계로 보존한다. 다른 실제 RGB를 기존 연결로 무시하지 않는다.
- 외관은 실제 원본의 흰뿔 회청색 기체/기계 무장이다. 카탈로그 unit 이름으로 소유 기체를 단정하거나 별도 설정색을 넣지 않았다. 6종 전체16색은 ROM PLT1403 bank0와 일치한다.
- 셀0/1/2/4/5의 원본 인덱스는 IMG8695의 기록된 사각형과 완전히 일치한다. 셀3의 작은 관절 단면은 최초검색 IMG1415와 바이트 일치하지만 단일 소유 이미지 근거가 아니므로 설치 계약의 resource/source좌표는 null이며 `source_candidate_matches`에만 기록했다. cached 실제 RGB/크기 계약은 확정이다.
- 각 원본 사각형은 서로 겹치지 않는다. 화면상 겹침은 OAM/priority/반전 그대로 제작 조립했고, 화면이 겹친다는 이유로 뒤 조각에 앞 조각 그림을 덮지 않았다.
- 셀2/3/4는 actual flip_x=true이며 생성 원화는 뒤집기 전 원본 방향이다. 나머지는 flip 없음.
- 생성 시트 상단 가운데 총열이 정규 셀 폭 밖으로 약간 나와 세 상단 crop을 x=0..420/420..1100/1100..1536으로 분리했다. 다른 조각 포함/총구 자름 없음. 최종 각 원본 캔버스로 생성 그림만 등록했다.
- `parts_generated_raw.png` 보존, alpha<64만 정리·고알파 RGBA 불변. 원본 알파/색을 찍지 않았다.
- `candidate_pose_production.png`는 제작 참고 조립이며 실제 HD 게임 화면이 아니다.

Claude 위험: 회청색 총 표면 명암이 원본보다 밝을 수 있음, 원본 작은 디테일을 모델이 둥근 관절/리벳으로 해석했을 수 있음, 셀0 연결편과 큰 무장 셀1의 화면 겹침, 셀3 작은 관절 가장자리, 어두운 셀2/5의 검정 면과 기존 팔 접합을 실제 재생에서 확인해야 한다. 전체 무장 완료를 주장하지 않는다.
