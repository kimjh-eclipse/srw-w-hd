# 프로비던스 대형빔샤벨 자세 기계4종 — 미검증 후보

- 실제 unit77/weapon327 메뉴450. `source_mechanical_fixed_77_327_450/source_pose.state` +0. palette0 기체 OAM21 중 exact0/indexed0 실제미연결4, 기존exact17 의존 보존. 빔FX/상대palette는그림목록에혼입하지않음.
- 전부 IMG8909 actual bytes일치: cell0(216,0)32×16,1(80,48)16×16,2(96,32)16×32,3(176,32)16×16. source사각형면적교차없음. 원본팔레트사용색/CRC/크기기계적확인.
- source/whole문맥은하부발쪽연결부0,작은회청색부분1,위로들린팔의세로부재2,파랑회색교차조각3. 캐릭터얼굴/손가락으로임의완성안함. 실제cell3 flip_x=True,나머지False,affine없음.
- 생성raw보존. 자체alpha<64만RGBA0/고알파불변. nativeRGB/alpha스탬프없음. 4배크기/후보존재기계적체크. 기존actualRGB활성binding교체대상없음,신규exact연결대상4.
- SHA256 2d3b776b045735ef5b12b812f26868cc8dce356c99297349ebe77928cee734f8
- installation_map.json/candidate_atlas.png/native_atlas.png가설치입력. 원본/제작조립은공식QA/실제HD재생아님.
- Claude 위험: 작은cell1의생성반사면이원본회청색보다밝아보이는정도, cell0붉은커프면적/흰패널, cell2팔의홈깊이/끝접합, cell3파랑슬리버의각진지원과반전. 그림이원본에맞는지시각/실재생미검증이며색보정런타임으로정답처리하지말것.
- 라이브/DB/코어수정없음,모니터off/headless유지.
