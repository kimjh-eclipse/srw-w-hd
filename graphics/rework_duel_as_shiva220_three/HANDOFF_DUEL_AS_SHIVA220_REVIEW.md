# 듀얼 AS 시바 초기 자세 3종 — 미검증 후보

- 실제 unit55/weapon250 메뉴220. `source_mechanical_55_250/source_pose.state` +0. 팔레트0 전체19 OAM.
- 새 실제 RGB3: 미연결1(파랑 슬리버 cell2) + indexed 다른색 재제작2(cell0 41442, 머리cell1 41476). 기존 초기 미연결 레일/작은회청판2종은 앞 duel_grenade420_missing hash1571128644/1677208175과 raw/actual palette/크기 동일이므로 재생성하지 않고 의존관계에 기록. 전체5로 중복 세지 않음.
- cell0 IMG8467(64,0), cell1 IMG8468(32,0), cell2 IMG8468(224,16) 원본 bytes 일치. 실제 PLT1380 bank0 사용색 일치. 바이트 첫 일치와 유일 리소스 소유자 확정은 구분.
- 생성 초안은 확대 도트처럼 남아 폐기(rejected_pixelated_draft.png). 2차 매끄러운 셀화 최종본 parts_generated_raw.png 사용. 원본의 흰회색 뿔/헬멧, 녹색 두 점, 주황 이마/하늘색 턱 위치를 참조. 자체 alpha<64만 정리하고 고알파 불변, 원본 RGB/alpha 스탬프 없음.
- 후보 SHA256 bf552948f6f3fa7eab9054fa38875861682e99d2d5c1b6ca8591732a63e8ef0c
- 연결 입력 installation_map.json/candidate_atlas.png/native_atlas.png. native CRC/팔레트·4배 크기·후보 존재 기계적 검사 완료.
- production 조립은 제작 자료이며 공식 QA/HD 실재생 아님. 실제 whole 의존에는 앞 단계 후보2종이 들어갈 예정이므로 root가 먼저 duel_grenade420을 연결하면 해당 raw가 자연스럽게 공유됨.
- Claude 위험: 실제 녹색 두 점의 역할과 새 그림 눈 위치 해석, 매끄러운 그림이 원본 각진 마스크를 너무 둥글게 해석했는지, 세로 얇은 조각 두께/잘린경계. 시각/실재생 미검증.
- 공유 라이브/DB/코어 수정 없음, 모니터 깨우지 않는 headless 제작.
