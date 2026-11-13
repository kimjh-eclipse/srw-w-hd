# 샌드록 서브 엔진 입력 계약 조사

그림 제작 전 원본 입력의 기계적 정합 확인이며 공식 시각/실재생 QA 아님. 라이브/DB/코어/공유 추출 helper 수정 없음.

- capture_engine1_contract_private.py는 공통 helper의 producer 전용 사본이다. core.sub_oam/sub_parts와 cachedOBJ engine1을 읽으며, 공통 target selector가engine0인 경우만 허용한다. 즉 다른 엔진을 임의로 읽어 본체 계약으로 오인하지 않는다.
- 각 source 캡처 전후 video_epoch 동일, cached 사각 크기/원본 OAM attrs/바인딩 hash가 일치해야 채택한다. 실제 index bytes+palette15bit로 CRC32 RGB hash와 index hash를 별도로 재계산해 모든 채택 OAM과 같음을 확인했다. 상세 engine1_source_identity_connections.json.
- sandrock_forecast_engine1_source:18 OAM 중 기체는16/17 두64×64이며 exact/indexed가 각각 있다. secondary_unit_6089 및secondary_unit_6253.0..15는 작은 UI/글자 사각형으로 기계 그림 누락으로 세지 않는다.
- sandrock_weapons_engine1_source:17 OAM 모두 최신 sandrock_cached_pose의 exact 그림이 있다. 미연결0이므로 중복 생성하지 않았다. 원본 재색칠 문제/서브 렌더 미반영은 이 source 연결 조사로 완료를 주장할 수 없으며 Claude의 공통 runtime 판정 영역이다.
- Core.binding_id는1-based, metadata 배열 인덱스는binding_id-1이다. 연결 분류에는 실제 hash+크기 exact 검색 결과를 사용했다.
