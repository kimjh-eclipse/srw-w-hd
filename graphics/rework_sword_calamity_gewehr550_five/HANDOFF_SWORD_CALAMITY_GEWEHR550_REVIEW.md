# 소드카라미티 슈베르트게베이르 후속550 새5종 — 미검증 후보

- 실제 unit131/weapon546 메뉴550. `source_mechanical_fixed_131_546_550/source_pose.state` +0. palette0 기체OAM16. 앞300 검2/손1은동일hash/원본bytes/사용팔레트로공유의존만재사용(검에는actualflip_y/flip_x변형보존),신규그림5만제작.
- 새5=실제미연결4+indexedactual색재제작1(주황손·회백가드 원래0/최종0 메타44671). 모두IMG10555 actualbytes/PLT1793 bank0사용색일치. 붉은기본색ROM일치로fade단계로분류하지않음. 기존활성actualRGB교체대상없음.
- 머리원래3 뿔끝8×16 screen(163,37),원래4 머리32×32 screen(171,29) 동일palette16/flip·affinefalse검산. actual40×32배치에서(0,8)/(8,0)연속native문맥으로하나의새머리를그린뒤각OAM사각으로분할. native눈은작은청록빛,붉은헬멧/주황노랑뿔/회백마스크를참조하고일반색으로자동교체하지않음.
- 기타주황손/길게뻗은붉은발/작은구부린붉은장갑은각원본형태별새그림. 아래잘린부위를전체신체로임의완성하지않음. 원래3/4의다른source좌표를raw시트인접이라고설명하지않고actual화면연속근거만사용.
- 전체4생성그룹→5사각. 분할재조립RGBA완전일치/사각지원밖0. 자체alpha<64만RGBA0/고알파불변,nativeRGB/alpha스탬프없음. 4배/nativeCRC·palette·후보존재기계적확인.
- 최종SHA256 201440917be7cf12b4aaf71b423f4af6b0ab4f560b04b442c7dbd823caa0f9ba
- 설치 입력 installation_map.json/candidate_atlas.png/native_atlas.png. 최종contract5행은원래0/2/3/4/5를재번호,original_source_cell기록. 전체8행은contract_all8_source로보존.
- Claude위험: 뿔끝/머리접합과눈/뿔정확한색·각도,주황손의손끝수/회백가드,긴발과다리절단면,작은구부린장갑의깊이. 공식시각/실제HD재생미검증이며이외모든기술완료판정아님.
- 라이브/DB/코어수정없음,모니터off/headless유지.
