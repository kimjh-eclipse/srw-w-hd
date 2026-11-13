# 게이츠 익스텐셔널 어레스터 와이어·클로 6종 — 미검증 후보

- 실제 unit74/weapon313 메뉴300. `source_mechanical_fixed_74_313_300/source_pose.state` +0. 팔레트0 실제 물리적 와이어/클로6 OAM 전부 exact0/indexed0 미연결. 다른 palette 기체/연출은 별도 의존으로 보존.
- IMG8872 source (200,0)32×8, (160,16)8×16, (168,0)32×32, (56,48)32×16, (144,0)16×32, (168,48)32×8. actual cached bytes/팔레트 확인. 원본 source 사각형 면적교차 없음.
- ROM PLT 사용색 일치 후보는 없음. 실제 cached palette는 계약에 전부 저장했으므로 그 값을 사용하며 ROM palette 소유자는 미확정(None)으로 둠. IMG source 바이트 일치와 별개이다.
- actual flip_y가 cell1/2/4에 있고 raw 방향 그대로 그림을 제작한 뒤 OAM에서 반전. affine 없음. 작은 클로를 손/얼굴로 완성하지 않고 연녹회색 물리와이어 곡률을 참조.
- cell5의 screen x229+32=261은 화면 밖5px를 포함하지만 계약과 그림 원래32폭 모두 보존. 288폭 제작 조립도 별도 저장하여 화면밖 지원이 사라진 것으로 오해하지 않도록 함. 실제게임은 코어의 256폭클리핑을 따름.
- 생성 raw 보존. 자체 alpha<64만 RGBA0/고알파 불변. 원본RGB/alpha 스탬프 없음. 후보4배/native CRC·팔레트·크기/각후보 존재 기계적 체크.
- SHA256 7cc5d5d1dc27ed046fa2c2a6aaa3adcdf82f546e44da5c6ed8b929244f9eeae9
- 설치 입력 installation_map.json/candidate_atlas.png/native_atlas.png. 공식 QA/실제HD재생 아님.
- Claude 위험: 분할선 끝의 접합/굵기, cell1 짧은 갈고리 곡선이 원본보다 넓어지지 않는지, cell4 S곡선 반전연결, 생성된 작은 직선부 마디/테두리와 원래 wire 질감, 클로모양. wire는FX빔으로 오인하지 말 것. 시각/실재생 미검증.
- 라이브/DB/코어 수정 없음, headless/모니터 off 유지.
