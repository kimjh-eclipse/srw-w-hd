# 듀얼 AS 시바 발사 자세 4종 — 미검증 후보

- 실제 unit55/weapon250 메뉴450, `source_mechanical_fixed_55_250_450/source_pose.state` +0. 팔레트0 기체 OAM16 중 새 실제 RGB4, 기존 exact12 의존 보존.
- 신규 미연결1(파랑 슬리버 cell2) / indexed 다른 색 재제작3(발쪽0 메타75801, 머리1 메타41475, 대각 총3 메타65510).
- IMG8551(0,0), IMG8468(0,0), IMG8550(56,48)/(192,0) 실제 source bytes 일치. PLT1380 bank0 사용색 일치. IMG8468 머리(0,0)는 앞 초기220의 다른 머리(32,0)와 source 겹침 없고 각각 새 그림. 원본 crop 첫 일치를 소유자 고유성으로 오인하지 않음.
- 실제 flip/affine 없음. 녹색 눈/카메라 및 총의 녹색 표시점은 실제 원본 사용색이므로 지우지 않음. source별 사각형 면적 겹침 없음.
- 내장 imagegen 새 셀화, raw 보존. 생성 자체 alpha<64만 RGBA0/고알파 불변. 원본 RGB/알파 스탬프 없음. 4배 크기/native CRC·팔레트/후보 존재 기계적 체크 완료.
- SHA256 83231e7da4b6f56be9b8f3686fb8a0b1c878c4e15ecbdf461ce3a6b272ca19d9
- 연결 입력 installation_map.json/candidate_atlas.png/native_atlas.png. 제작 조립 native/candidate_pose_production 포함, 공식 QA/실제 HD 재생 아님.
- Claude 위험: 대각 총의 긴 내부 레일/투명 홈과 손잡이 부분, 원래 지원영역보다 볼륨이 늘어난 곳, 머리 눈/카메라/뿔 위치와 잘린 목 연결, 발쪽0 장갑선. 모두 시각/실재생 미검증.
- 공유 라이브/코어/DB 수정 없음, 모니터 off 유지.
