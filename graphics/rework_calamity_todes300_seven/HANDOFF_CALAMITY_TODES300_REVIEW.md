# 카라미티 토데스 블록 실제 자세 큰7종 — 미검증 후보, tiny1 보류

- 실제 unit80/weapon338 메뉴300. `source_mechanical_fixed_80_338_300/source_pose.state` +0. palette0 기체16 OAM 중 큰7종 후보(미연결4+indexed actual색 재제작3),9texel tiny1보류. 기존exact8의존보존. 전체자세완료주장하지않음.
- 큰7원본전부IMG9034 raw일치. 실제팔레트원본/CRC/크기확정. indexed 메타41688/41665/41667은각다른색의존,새그림actualRGB연결을신규미연결로세지않음. 최신activeactualRGB대조는final_live_exact_dependency_check.json(현재교체대상없음).
- 미확정tiny hash365017408은청록단색9texel. IMG1526첫바이트일치만있고소유자/역할미확정이라그림발명하지않음. held_tiny_contract.json,원래contract_all8_source/각source_all8파일보존,설치지도에서는제외. 최종contract7행에서마지막cell6은원래cell7이며original_source_cell=7로명시.
- 중요무장배치정정: 원래cell2/1 source9034(64,32)/(96,32)는raw좌우인접이나실제화면(171,51)/(203,67)로y가16다르다. raw64×32그림은최종미사용. 실제동일palette16·flip/affinefalse검산후(0,0)/(32,16)의64×48native문맥을별도생성해원래각32×32사각으로나눔. actual화면16px차그대로유지,기하를강제로일자연결안함.
- 처음6그룹시트중무장그룹1만별도생성으로교체,나머지5그룹은기존생성그림보존. 실제64×48생성master의사각지원밖13HDpixel은생성그림전체를오른쪽3HDpixel(.75native)정렬하여교정. pixel삭제/원본alpha스탬프없이비제로클리핑0/고알파RGBA순서완전불변. 최종분할재조립RGBA일치/사각지원밖내용0.
- 자체생성alpha<64만RGBA0/고알파불변. 다른셀에원본RGB/alpha찍기없음. 4배크기/native CRC·팔레트/후보존재기계적확인. 공식QA/실제HD재생은실행하지않음.
- 최종SHA256 36cf24fd159e728d6159c77c07e9e3155997340071740bb4e371d645625310eb
- 설치 입력 installation_map.json/candidate_atlas.png/native_atlas.png. actual64×48원본/분할/정렬근거및원본·제작조립포함.
- Claude 위험: 긴무장의16px계단OAM분할접합과실제손위치,헬멧주황노랑장식/원래녹색눈/마스크형태,잘린암부장갑과하부연결,작은주황패널색영역. 생성머리와부품의과한부피/외곽캡여부는시각·실재생미검증. tiny1은별도미완료큐유지.
- 라이브/DB/코어공유코드수정없음,모니터off/headless유지.
