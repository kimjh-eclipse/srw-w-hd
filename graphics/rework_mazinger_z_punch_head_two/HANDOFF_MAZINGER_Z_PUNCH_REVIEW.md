# 마징가 Z 머리 2종 제작 인계

미검증 후보이며 실제 HD 재생 판정은 Claude 담당이다. 라이브/DB/코어를 수정하지 않았다.

- unit294 / 무장1184 로켓 펀치와1185 아이언 커터의 정상 네이티브 메뉴에서 추출한 같은 머리 2종이다. 두 장면 26 OAM 중 고유 미연결 머리 2, 각 자세 몸체 11 OAM은 기존 의존 관계다. 새로운 자세 전체 13종을 제작했다는 뜻이 아니다.
- 실제 exact RGB 연결0 / indexed 연결0 / core binding0을 source_identity_and_connection.json에 기록했다. IMG14723의 전체 indices bytes가 일치하며 팔레트2636 bank0의 실제 사용색도 같다. ROM 첫 일치 witness이므로 유일 소유 증명은 아니다.
- 원본 머리는 화면104,55의32×32와136,55의16×32로 인접한다. 오른쪽16은 flip_x=true다. 표시 상태48×32를 단 한 번 새로 그린 후 원래32/16 경계에서 나누고16을 역반전했다. 원본 알파를 찍지 않았고 내부 절단면 선도 새로 추가하지 않았다.
- candidate_atlas.png / native_atlas.png / installation_map.json이 설치 입력이다. 기계적 raw hash/팔레트/크기/후보 존재 확인은 mechanical_contract_checks.json. 생성 출처는 parts_generated.png, 내장 imagegen 사용.
- 후보 SHA256:1e2ad4f0acb841bd426869559d51447a8708a3840502ea8951d660448716a573
- candidate_pose_production.png는 후보 머리와 native 몸체의 원좌표 제작용 조립이며 게임 재생 또는 기존 몸체 HD 결과가 아니다. 실제 OAM 우선순위/역순/반전을 적용했다.
- Claude 확인 장면: source_mechanical_294_1184/source_pose.state 및 source_mechanical_294_1185/source_pose.state +0 이후. 머리/몸체 하단 접합, 양쪽 뿔과 하늘색 이마 패널, 빨강/노랑 눈, 반전 경계가 움직일 때도 맞는지 확인 요청.
- 알려진 한계: 그림은 연속머리 해석으로 제작했으며 세부 모양/색 배치 및 실재생 가림은 아직 미판정이다.1187은 네이티브 메뉴에서 제공되지 않아 억지로 실행하지 않았다.
