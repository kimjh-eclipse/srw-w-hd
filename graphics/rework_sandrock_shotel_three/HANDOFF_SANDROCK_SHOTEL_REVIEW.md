# 샌드록 쇼텔 실제 미연결 3종 제작 인계

미검증 후보. 공식 시각/실제 HD 재생 판정은 Claude 담당이며 수행하지 않았다. 공유 runtime/라이브/DB/코어 수정 없음.

unit3 weapon14 정상 네이티브 메뉴 +250의 source state 다음1프레임 cachedOBJ에서 전체23 OAM 중 고유미연결3을 확보했다.20개 기존 의존은 유지한다. 세 raw bytes 모두 IMG7240과 일치하고 실제 사용 palette는1181/7311 bank0이다. exact0/indexed0/core0.

큰32×32 하나는 머리 뒤/어깨의 좁은 계단 장갑 연결편으로 새로운 머리/얼굴/눈을 만들어 넣지 않았다. 작은16×16 둘은 좌우의 작은 팔·장갑 연결편이다. native 전체 bbox와 회색 배경 참조로 실제 검정 연결대를 확인했다. 큰0의 original224 opaque texel은 하나의 연결체라 초기 분리 생성은 채택하지 않았고 imagegen으로 연결대를 교정했다.

## 설치 입력

candidate_atlas.png/native_atlas.png/installation_map.json.4배. 후보 SHA25641fae7769b14e4d37d27fbfc5251845b39748333ffa7e1c464462ce7f0a4ba92. mechanical_contract_checks.json에 raw index SHA/actualpalette RGB/크기/후보 존재 확인. parts_generated.png는최종 생성알파 정리본, parts_generated_original.png 및 parts_generated_connected_with_glow.png가 편집전 생성 원본이다.

## 생성 알파만 정리

imagegen이 후광제거 요청 후에도 저알파 후광을 남겨 producer 규칙에 따라 생성자체alpha<64의 RGBA만0으로 정리했다. 원본 이미지/마스크/실루엣은 사용하지 않았다. >=64의 RGBA는 모두 완전 불변이고 그 SHA를 generated_alpha_cleanup_proof.json에 남겼다. 제거한 nonzero-alpha pixel은8667, 투명RGB까지0으로 정리한 전체수1413209.각 생성셀의 alpha>=64 영역은 하나의 연결체(87673/36050/35932 픽셀)이며 가는 검은 지지대가 연결된 상태다. alpha160보다10픽셀 이상 떨어진 alpha64..159 잔여는0.

이것은 source마스크로 도트 실루엣을 찍은 것이 아니다. 후보4배 정렬 과정의 LANCZOS 재표본화는 별개이며, 가는 안티앨리어싱 선이 원래 생성본보다 잘릴 가능성은 Claude가 확인해야 한다. native 알파/색을 억지로 복사하지 않았다.

native_pose_production.png/candidate_pose_production.png는 실제좌표/priority·OAM 역순/반전으로 새3+기존native20을 조립한 제작용 그림이며 실제 게임 전체 HD 화면이나 공식 재생검사가 아니다.

Claude 장면: source_mechanical_3_14/source_pose.state +0 이후.큰0의 좁은 검은 지지대/흰면 위치와 머리뒤 접합, 작은1/2의 팔과 어깨 연결, 원래 얇은 선의 유지 및 후광 잔여를 확인 요청.처음 모델이 상단 은색면 개수/판금두께를 조금 구체화한 부분은 형태정확성이 미판정이다.
