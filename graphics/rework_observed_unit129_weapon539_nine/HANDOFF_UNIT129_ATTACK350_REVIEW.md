# 실제 unit129 / weapon539 메뉴350 미연결9 후보

상태 `CACHED_OBJ_ARTWORK_CANDIDATE_UNVERIFIED`. 라이브/코어/공유 코드/DB 변경 없음. 공식 검사·실제 HD 재생은 Claude 대기.

- 설치 입력: installation_map.json/candidate_atlas.png/native_atlas.png/contract.json.
- 최종 후보 SHA256: `beebdcced069773da572be85ca226b34a206570f373b761d759bff4f8a2d9de7`.
- fixture: source_mechanical_fixed_129_539_350/source_pose.state +0. 메뉴350 actual cached OBJ/OAM/전체16색/코어SHA 보존.
- 원래12 후보 중 indexed proxy3은 제외하고 actual exact0/indexed0인9종만 제작했다. 원래0/1/4/5/6/8/9/10/11을 최종0..8로 재번호. 전체 actor17의 나머지기존 의존 보존. 원본 IMG10459 4종/10442 5종의 실제 인덱스 바이트 일치. 전체16색은 PLT1781 bank0 일치.
- 작은7texel 조각도 실제 원본/화면 연속을 확인해 함께 제작했다. 최종셀4 큰32×16 source(168,16)/화면(188,76), 셀3 작은8×8 source(200,16)/화면(220,76), 같은 IMG10442/full16/반전없음. 한40×16 새그림 master를 나눠 끝의 작은지지영역을 보존했다(tiny_support_continuity.json).
- 첫 생성은 팔그룹 끝이 작은8×8사각형 아래로 내려가63HD픽셀이 지원밖으로 남았다. 원본알파로 자르거나 수치기준을 낮추지 않았다. 다른7조각 RGBA를 그대로 보존한 채 이 팔그룹만 별도 imagegen 원화로 다시 그려, 마지막끝의작은흰지지부와하단투명빈틈을 수정했다. 새그림파일 group_3_regenerated_raw.png. 회전등록시도는 채택하지 않았다. 최종8그룹 전부재조립RGBA같음/지원밖누락0. preserved_seven_source_crops_proof.json의7crop SHA불변.
- 생성원본/첫실패/새팔그림/자체alpha<64정리근거 보존, 고알파RGBA 불변. native RGB/alpha/mask 복사·스탬프 없음.
- 검정/남보라 복합실루엣과 실제초록카메라가있는큰무장도 원본색/빈틈을참조했다. 해부학적이름이나 카탈로그의기체정체만으로부분역할을발명하지않았다.
- candidate_pose_production은 제작참고이며 실제 HD 게임결과가 아니다. 9조각모두비어있지않고최대alpha255는기계적확인이지모양/색/재생통과판정이아니다.

Claude 위험: 새팔끝의작은지지부가너무밝거나단순해졌는지, 큰무장/검정연결실루엣의기계구멍·선형태를모델이발명했는지, 파랑/회백부품과작은주황·빨강·초록면의위치/밝기, 기존몸체·proxy머리와의경계/명암을실제재생에서확인해야한다. 전체기체/무장완료로세지않는다.
