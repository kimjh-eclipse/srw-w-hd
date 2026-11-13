# 이지스 변형 공격 350프레임 10종 — 미검증 후보

- 실제 unit52/weapon236 메뉴350, `source_mechanical_fixed_52_236_350/source_pose.state` +0. 팔레트0의 변형 비행 기체 OAM13개 중 새 실제 RGB10, 기존 exact3 보존.
- 실제 미연결7종 / 기존 indexed 다른 색 의존3종(cell0/1/6) 재제작. 신규 누락10으로 세지 않음.
- 모두 ROM IMG8352 실제 원본 bytes 일치, PLT1357 bank0 사용색 일치. source_identity_and_connection.json 및 raw 계약 참조. 같은 원본 crop 첫 일치이므로 고유 소유자 추정하지 않음.
- 자홍/진분홍·노랑/주황·회청색·어두운 청회색 기계부품. whole native 문맥으로 변형 기체 부품임을 확인하고 얼굴/눈을 새로 발명하지 않음.
- 원본 시트에서 맞닿는 cell4/3과 cell0/8/7은 생성 그룹으로 제작 후 분할. 첫 그룹은 실제 원본도 3개 분리 섬. 생성 결과의 3개 섬을 독립 사각형에 정렬하여 OAM 지원 밖 잘림을 제거함(생성 그림 정렬이며 native RGB/알파 스탬프 아님).
- 연속 그룹 분할 재조립 RGBA 일치, OAM 지원 밖 생성 내용 0. 나머지 원본끼리 양의 면적 겹침 없음. 140프레임의 기존 생성1과도 source 사각형 겹침 없음.
- 실제 flip_y인 cell0/1/6은 원본 raw 방향으로 제작하고 OAM 속성으로 뒤집음. affine 없음. native/candidate_pose_production은 제작 조립이며 공식 QA/실제 HD 재생 아님.
- 생성 raw 보존, 자체 알파64 미만만 RGBA0, 고알파 불변. 크기4배/native CRC·원본 팔레트/후보 존재 기계적 확인 완료.
- 후보 SHA256: b070e3aeb62ca8b0121b1d81f1e7ecb23734d0331a8b08624f38001b7be5ef2e
- 설치 입력 installation_map.json / candidate_atlas.png / native_atlas.png.
- Claude 위험: 셀1 둥근 연결부·셀9 원형 관절의 볼륨 해석, 셀5 회색 가로 구조와 주변 자홍 절단 경계, 실제 뒤집힌 부품의 기체 연결, 첫 그룹 3개 섬의 두께/미세 위치. 숫자/분할 일치가 그림 정답을 뜻하지 않으며 시각/실재생 미검증.
- 공유 라이브/DB/코어 수정 없음. 모니터 꺼진 상태에서 headless 제작.
