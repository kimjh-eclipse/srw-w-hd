# 실제 unit93 / weapon385 +370 미연결 2종 후보

상태 `CACHED_OBJ_ARTWORK_CANDIDATE_UNVERIFIED`. 그림 제작·원본 계약만 완료했고 실제 HD 재생/공식 검사는 Claude 대기다.

- 설치 입력: `installation_map.json`, `candidate_atlas.png`, `native_atlas.png`, `contract.json`.
- 후보 SHA256: `48c055ceeb3e6f5d8f186307627c20532c939b5c4c823ac3b07f1b71e441b611`.
- 실제 상태: `source_mechanical_fixed_93_385_350/source_pose.state` +0. 요청 최소350 뒤 실제 캡처된 메뉴 프레임은370이다. 원본계약에 actual cached OBJ/팔레트/OAM/코어 SHA 보존.
- hash4177950 32×64의 흰 긴 뿔/녹회색 머리, hash3364155657 32×16의 녹회색 기계 접합편. 두 조각 모두 정확 RGB 및 indexed 연결 없음. 원본 인덱스는 IMG8871의 기록된 사각형과 일치.
- 전체 actor11 OAM 중 다른8개의 indexed proxy 그림은 이번에 재제작하지 않고 의존관계로 보존한다. 원래 10종 전체 추출은 `*_all10_source.json`과 원본 시트로 보존했다. 전체 몸체 HD 완료라고 세지 않는다.
- 실제 시점220과370의 전체16색이 동일하다(`observed_palette_stability.json`). ROM 팔레트와 사용색 검색은 일치 후보가 없으므로 특정 PLT나 기본/페이드 소유를 임의로 넣지 않았다. 관측된 실제 녹회색/흰회색/작은 주황 눈 슬릿과 작은 붉은 네모 위치를 그대로 생성했다.
- 상단 뿔과 머리는 하나의 실제32×64 그림으로 제작했고 다른 파츠의 숨긴 내용을 덮지 않았다. 셀1 접합편은 독립 원본형태로 제작했다.
- 화면 오른쪽으로 잘린 관측 자세다. 계약의 전체 cached 원본 payload와 생성 캔버스는 보존했으나 화면 밖 부분까지 실제 재생에서 보였다고 주장하지 않는다.
- 생성 원본을 보존했고 자체 alpha<64만 투명화했다. 고알파 RGBA는 불변이며 원본 RGB/알파를 찍지 않았다.
- `candidate_pose_production.png`는 제작 참고이며 실제 HD 재생 검사가 아니다.

Claude 위험: 길고 흰 뿔의 실제 머리 각도·주황 눈 위치, 작은 붉은 네모 색, 기존 indexed 몸체와의 녹회색 면/목 이음새, 생성 AA 외곽의 밝은 선, 관측 화면 밖으로 잘린 원본지원, 다른 시점에서 머리와 접합편의 연결을 확인해야 한다. 팔레트 소유 미확정은 유지한다. 라이브/공유 코드/DB 변경 없음.
