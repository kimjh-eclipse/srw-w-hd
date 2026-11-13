# 카라미티 슈라크 수평무장·손4종 — 미검증 후보

- 실제 unit80/weapon339 메뉴300. `source_mechanical_fixed_80_339_300/source_pose.state` +0. palette0 기체OAM15. 새4종=실제미연결3+indexed actual색재제작1(원래cell2/현재2,메타41685). 앞todes300의머리/몸통/작은주황패널/하부4종은같은hash·raw·palette라다시그리지않고의존관계에기록. 앞보류tiny1도그대로보류. 따라서전체자세미완료유지.
- 새4모두 IMG9034 actual bytes: 원래0(184,0)32×16,1(32,32)32×32,2(0,32)32×32,8(160,0)32×16. 실제 cached 팔레트 및 ROM 사용색 후보는 source_identity_and_connection.json에 기록. source_owner첫일치/유일소유자판정구분.
- 이번무장2/1은source와실제screen양쪽32px수평연속: raw(0,32)/(32,32),screen(136,65)/(168,65),같은palette16/flip·affinefalse. 64×32native로새그림한개제작후32경계분할. 앞todes300의y16차사선무장과혼동하지않음.
- 손은원래8/0 source x160/184,y0,폭32씩부분교차8×16. native indices/actualpalette16동일검산후56×16master에원래서로분리된두손을그려각32사각형분할. 실제screen의x/y배치가source와다르므로screen으로기하를바꾸지않음. 공유교차영역생성HD RGBA완전일치.
- 첫생성오른손4손끝은원본3개와달라imagegen으로3개교정. 교정시왼쪽무장과왼손은기존생성픽셀불변으로보존하고오른쪽생성영역만합성. 원본RGB/alpha스탬프없음. 생성raw/교정raw/합성본/불변SHA증거보존.
- 자체alpha<64만RGBA0/고알파불변. 최종분할재조립RGBA완전일치/사각지원밖0. 4배크기/rawCRC·palette/각후보존재기계적확인. actual활성RGB교체대상은latest_exact_check.json에기록(현재없음).
- 최종SHA256 27fbf16cb81c10f14d31faaaa7c83ff5b94b81d86f0cd636cec4bf9af828ad7f
- installation_map/candidate_atlas/native_atlas가설치입력. 최종contract4행의cell3은원래8,original_source_cell명시. 전체원본9행은contract_all9_source.json에보존.
- Claude위험: 수평무장접합/실발사위치, 손의분리간격/실제3손끝과청록커프, 원래공유8×16이애니메이션에서다른배치로등장할때의지원형태. 밝기/검은cap·과한볼륨도미검증. production조립은공식QA/실제HD재생아님.
- 라이브/DB/코어수정없음,모니터off/headless.
