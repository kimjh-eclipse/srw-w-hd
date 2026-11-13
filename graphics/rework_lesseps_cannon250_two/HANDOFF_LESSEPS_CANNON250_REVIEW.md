# 레셉스 40센티포 연속 함체 2종 — 미검증 후보

- 실제 unit67/weapon294 메뉴250. `source_mechanical_fixed_67_294_250/source_pose.state` +0. 팔레트0 기계 OAM7 중 실제 미연결2(exact0/indexed0), 기존 exact5 의존 보존.
- IMG8796(32,0)/(0,0) 각32×16 actual raw 일치. 두 조각 palette16 완전동일. 실제 화면 (146,80)/(114,80), flip/affine 없음으로 source와 screen 양쪽32px 맞닿음 확정.
- 두조각을 연속64×16 원본으로 조립하여 한 생성 그림으로 만들고32경계로분할. 같은 생성 RGBA 재조립 완전일치. 중앙 함체/회청색두포신이 경계에서 끊기지 않도록 공유. 원본의 잘린 상하/우측 면을 전체함체로 임의완성하지 않음.
- 내장 imagegen 새그림 원본 보존. 자체 alpha<64만 RGBA0/고알파 불변, 원본RGB/alpha스탬프 없음. 4배 크기/native CRC/원본팔레트/후보 존재 기계적확인.
- SHA256 a3907bc3ca2ebdc539f46250b6e049601c8aeee7e8a6553ebbcfd481ba5b9c52
- 설치 입력 installation_map.json/candidate_atlas.png/native_atlas.png. 연속원본 continuous_native/continuous_generated 및 분할증거 포함.
- Claude 위험: 함체 띠 상하절단면이 기존5개파트와 맞는지, 포신 길이/두께와 실제 발사위치, 생성된 둥근 포신 볼륨과 올리브색 배치. production 조립만 저장, 공식 QA/실제HD재생 미검증.
- 공유 라이브/DB/코어 수정 없음, 모니터 off/headless 유지.
