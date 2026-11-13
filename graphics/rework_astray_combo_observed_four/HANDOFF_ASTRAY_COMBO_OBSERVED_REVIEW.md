# 붉은 아스트레이계 합체 관측 파츠 4종 인계

미검증 후보. 공식 QA/실재생 판정은 Claude 담당이며 수행하지 않았다. 공유 runtime/라이브/DB/코어 수정 없음.

- 다른 담당의 actual_mechanical_pose_104_420을 넘겨받고 동일 state+420을 현재 cachedOBJ API로 다시 추출했다. 새 astray_combo420_cached_source의 실제4 hash/attrs/팔레트가 원계약과 일치했다.
- 해당 fixture는 unit104(아스트레이BSL) weapon437 합체 공격이다. 화면의 말하는 인물은 코우지 아닌 가이이고, 보이는 붉은 기체는 합체 참여 아스트레이계다. 마징가라고 명명하지 않았다. 정확한 참여 기체 unit 세부형은 source_owner=None으로 남긴다.
- 네 기계 파츠의 raw bytes는 모두 IMG9416/PAT9417과 일치한다. 본체3의 실제 사용 palette는1592(아스트레이R 기본색)/1613(파워드 레드)/9436 bank0 후보와 같고 좁은4번째 조각은 실제별도palette다. pattern 표의 palette9415만 보고 임의 재색칠하지 않았다. 실제팔레트 우선. source_identity_and_connection.json.
- 전체10 OAM 중 실제미연결 고유4를 모두 새로 그렸다. 기존6은 의존 관계다. exact0/indexed0/core0. candidate_atlas.png/native_atlas.png/installation_map.json 설치 입력. SHA25670fe99f79247675d7504857be1f97c1edca7c57a33827f177a69420ba14a81f7.4배. raw SHA/크기/실제palette RGB/후보 존재는 mechanical_contract_checks.json.
- 큰32×32 붉은/회색 장갑2, 작은16×16 연결편, 좁은16×32 흰/빨강/노랑 슬리버. 얼굴/눈을 만들어 넣지 않고 실제 whole-native 위치를 참조했다. 원본 RGB/alpha stamp, 다른캐릭터 그림 재색칠 없음.
- native_pose_production.png / candidate_pose_production.png는 실제 priority/OAM 역순/반전을 적용한 제작용 조립. 기존6은 native로 남기므로 게임 전체 HD 결과가 아니다.
- Claude 장면: test_current/parts/native_weapon_source_104_437/unit104_weapon437_source.state +420. 장갑0/1의 실제 열린 절단면/관절 접합, 작은2의 지원영역/손가락 문맥, 슬리버3의 상단노랑/흰면과 뒤쪽 본체 사이 연결을 확인 요청. 생성 도구가 회색 장갑의 외곽 림과 손가락을 원본보다 상세화했으므로 형태 정확성은 미판정이다.
