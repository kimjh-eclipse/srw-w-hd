# 소드카라미티 슈베르트게베이르 실제 자세5종 — 미검증 후보

- 실제 unit131/weapon546 메뉴300. `source_mechanical_fixed_131_546_300/source_pose.state` +0. palette0 기체16 OAM 중 actual exact0/indexed0 미연결5종, 기존exact11 의존 보존. IMG10555 원본bytes/PLT1793 bank0사용색일치. 일반청록카라미티와다른기체의붉은기본색이므로팔레트fade색교체로취급하지않음.
- 원래cell2 오른칼64×32 screen(141,93),끝cell1 16×16 screen(205,109). 동일palette16/flip·affinefalse 검산후 actual(0,0)/(64,16)80×32 문맥으로한생성그림제작,각원래사각으로추출. source좌표10555(0,32)/(160,64)는서로맞닿지않으므로raw시트인접이라고설명하지않음.
- 왼칼cell4는source(64,32)64×32,actualflip_x=True. raw방향별도원본을그대로새로그리고actual반전으로조립. 오른칼과같은native라고가정해복제하지않음. 손cell0(144,80)/3(128,80)은각16×16별도형상으로제작,source인접만으로연속손발명없음.
- 전체4생성그룹→5OAM. 분할재조립RGBA완전일치,사각지원밖생성내용0. 자체alpha<64만RGBA0/고알파불변,원본RGB/alpha스탬프없음. 4배크기/nativeCRC·팔레트/후보존재기계적확인.
- 최종SHA256 6bc67b194b81416c436152dea2f8c143f3b7224da3e69f389c129e463a18e0ee
- installation_map.json/candidate_atlas.png/native_atlas.png가설치입력. 원본/생성raw/actual80×32문맥·분할근거/제작조립포함. 기존activeactualRGB교체대상없음(모두새actualRGB).
- Claude위험: 오른칼끝80×32계단분할과손접합,왼칼반전각도/길이,원본검은틈대비생성된새구멍·리벳세부,양손손끝수/모양·붉은색영역. 공식시각/실제HD재생미검증,이자세외모든무장완료주장없음.
- 라이브/DB/코어수정없음,headless/모니터off유지.
