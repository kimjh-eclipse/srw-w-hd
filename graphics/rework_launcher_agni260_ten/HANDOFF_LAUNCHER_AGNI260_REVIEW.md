# 런처 스트라이크 +260 한 자세 10종 미검증 제작 후보

- 실제 native 메뉴 unit15/w52 +260, source_mechanical_15_52/source_pose.state +0의 cachedOBJ/actual 팔레트/OAM 계약입니다. palette0 전체13 OAM 중 기존3개를 유지하고 10종을 제작했습니다. 실제미연결8종과 기존 indexed proxy 실제색교체2종(머리/녹색장갑)을 구분합니다.
- 실제 index와 ROM IMG7822/7651/7777 bytes가 동일합니다. 모든 실제색을 원본 계약에서 확보했으며 녹색장갑·빨강노랑 끝판·머리 실제 눈/뿔색을 키색으로 삭제하지 않았습니다. ROM 첫 byte일치는유일소유증명은 아닙니다.
- source IMG7822 cell1/6은8열이 겹칩니다. 원본 bytes/팔레트 일치검산 후 생성HD만 동일 source 좌표로 공유하고 교차밖 생성RGBA는 유지했습니다. shared_source_intersection_proof와 source별 generated_master 보존.
- imagegen 내장 도구로 생성했고 가장자리 색잡티 제거를 한번 추가 요청했습니다. 최종 생성본 자체 alpha<64만 RGBA0 정리했고 >=64 RGBA는 전부 불변(증거 SHA/제거수는 generated_alpha_cleanup_proof.json). 원본 mask/원본RGB/색상기반 강제절단을 사용하지 않았습니다. 초기/교정 생성본 보존했습니다.
- 위험: 얇은 AA 경계 손실, 생성에서 구체화된 손가락/몸통 면/머리옆면, source cell6 왼쪽 경계의 분리 장갑섬과 오른쪽 무장판 접합, 기존3개와의 표면연속성은 Claude 판단이 필요합니다. cell4 실제3texel은 작은암부 sliver로만 제작했으며 정체이름을단정하지않았습니다.
- 모든10개가 비어있지 않고 alpha최대160 이상, raw/palette/size/공유 기계적일치만 확인했습니다. 공식 audit와 실제 HD 재생은하지않았습니다. native/candidate_pose_production은 OAM 우선순위/역순/반전을 적용한 제작조립이며 전체HD 완료/실제게임HD 검증결과가 아닙니다.
- 라이브/DB/코어/공유runtime 변경없음. root 직렬 연결 후 Claude 확인 대기입니다.
