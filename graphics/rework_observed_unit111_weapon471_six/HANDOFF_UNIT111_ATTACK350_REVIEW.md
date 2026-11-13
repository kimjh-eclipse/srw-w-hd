# 실제 unit111 / weapon471 +350 미연결 6종 후보

상태 `CACHED_OBJ_ARTWORK_CANDIDATE_UNVERIFIED`. 공식 검사·실제 HD 재생은 Claude 대기. 공유 코드/라이브/DB/코어 변경 없음.

- 설치 입력: installation_map.json, candidate_atlas.png, native_atlas.png, contract.json.
- 후보 SHA256: `bcd759bb5a1e53b258f4f643b9911f1dff95fb8f21430999cc6276abfca32f20`.
- 실제 fixture: `source_mechanical_fixed_111_471_350/source_pose.state` +0. 메뉴350 actual cached OBJ/OAM/팔레트와 코어 SHA는 계약 보존.
- binding0 13개라는 숫자를 누락13으로 세지 않았다. 원본이 빈 OBJ를 먼저 제외했고 유효8종 중2종 indexed proxy도 제외했다. 이번6종만 exact0/indexed0이다. 원래 셀1..6을 최종0..5로 재번호했고 전체8 원본은 *_complete_source.json에 보존했다.
- 원본 IMG9834 4종/9871 2종의 실제 인덱스 바이트가 일치한다. 대상 원본 사각형끼리 교집합 없음. 다른 기존 파츠/팔레트/실제 OAM 좌표와 priority는 whole_pose_dependencies로 보존.
- 전체16색 PLT1665 bank0 일치 여부는 full_palette_phase_proof.json. 실제 회백/회보라/검정 면만 생성했고 색있는 눈/장식/발광을 넣지 않았다. 작은 조각을 완성된 얼굴/무장으로 자동완성하지 않고 원본에 보이는 잘린 형태를 그렸다.
- 생성원본 보존, 자체 alpha<64 정리와 고알파RGBA 불변. 원본 RGB/알파 찍기 없음. candidate_pose_production은 제작 참고이며 실제 HD 재생 결과가 아니다.

Claude 위험: 좁고 구부러진 셀2 연결편이 실제 기계 선인지 다른 연출인지, 작은 조각의 두께/밝은선/검정 빈틈, 셀3 복합 기계면의 모델 해석과 아래 돌기, 기존 몸체와의 절단 경계·명암을 확인해야 한다. 실제 native에서 보이는 부분의 신규 그림 후보이며 전체기체/기술 완료가 아니다.
