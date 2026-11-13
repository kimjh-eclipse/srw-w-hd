# 알트론 드래곤행 +320 한 자세 15종 미검증 제작 후보

- 실제 메뉴 unit4/w19 +320의 cachedOBJ/실제 OAM16개 중 실제 exact0인15개를 새로 그렸습니다. 기존1개 의존 유지. 15종 중 indexed도 없는6종과 다른 actual palette인 기존 indexed 교체9종을 구분했습니다. 신규 누락15로 세지 마십시오.
- 실제 palette0 사용색을 그대로 계약에 보존했습니다. 청록 장갑, 회백색, 검정/빨강/노랑 패널 및 머리 눈·카메라 색은 실제 도트 기준입니다. 다른 기체 색 구성으로 재색칠한 것이 아닙니다.
- 원본 인덱스 bytes는 ROM IMG7454/7415/1192의 사각형과 동일합니다. 검색은 첫 일치 증거일 뿐 유일 소유 IMG를 증명하지 않으므로 source_owner_unit=None와 match_scope를 명시했습니다. 실제 cachedRGB/indices/팔레트/크기는 확정입니다.
- IMG1192의 두 사각형은8열이 겹칩니다. 실제 원본 인덱스/팔레트 동일을 검산하고 생성 HD만 실제 source 좌표로 공유해 나눴습니다. shared_source_intersection_proof.json 및 resource별 generated_master 보존. 원본 RGB/알파를 찍지 않았고 교차 밖 생성 RGBA는 불변입니다.
- imagegen 내장 도구의 3열5행 새 그림으로 제작, 생성 알파 bbox 위치/크기 정렬만 수행했습니다. 원본 마스크로 실루엣을 덮지 않았습니다.
- 위험: 좁은 옆면 조각(cell0/4)은 생성자가 금속 면을 더 구체화했습니다. 잘린 머리 cell5의 얼굴 면·노랑 뿔/눈 위치, 드래곤장갑 cell2/14 손가락/패널 형태와 접합은 Claude 판단이 필요합니다. cell13은 실제6texel의 극소 청록 연결끝이라 역할 이름을 단정하지 않고 raw형태 작은 sliver로만 생성했습니다. 별도 source 소유를 추정하지 않았습니다.
- 모든15 후보가 비어있지 않고 alpha최대160 이상이며 실제 source raw/palette/크기 기계적 확인만 했습니다. 공식 형태/색 audit나 실제 HD 재생은 수행하지 않았습니다. native/candidate_pose_production은 OAM 우선순위·역순·반전을 적용한 제작 조립 비교입니다.
- Claude 상태: source_mechanical_4_19/source_pose.state +0, 원래 실제 메뉴 +320. 전체 원본/계약/후보 조립을 함께 확인하십시오. core/live/library/DB는 변경하지 않았습니다.
