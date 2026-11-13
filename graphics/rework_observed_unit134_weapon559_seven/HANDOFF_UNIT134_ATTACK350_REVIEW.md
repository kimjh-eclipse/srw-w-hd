# 실제 unit134 / weapon559 메뉴350 기계7 후보

상태 `CACHED_OBJ_ARTWORK_CANDIDATE_UNVERIFIED`. 라이브/공유 코드/코어/DB 변경 없음. 공식 검사·실제 HD 재생은 Claude 대기.

- 설치 입력: installation_map.json/candidate_atlas.png/native_atlas.png/contract.json.
- 후보 SHA256: `40e7ffe8ce4076a49c716547e580788afbe0e0902289b94c90d50884cdea3a3e`.
- fixture: source_mechanical_fixed_134_559_350/source_pose.state +0. 실제 메뉴350 cached OBJ/OAM/팔레트/코어SHA 보존.
- 원래9후보 중 실제 미연결6을 새로 만들었다. 이중1조각과 실제 source를공유하는 indexed proxy44278을 같은그림으로분할하기위해추가해 최종7=미연결6+proxy교체1. 다른머리/하체proxy2는기존의존보존. 원래0/1/2/5/6/7/8을 최종0..6으로재번호.
- 원본 IMG10442 4종/10459 3종의actual인덱스바이트 일치. 전체16색 PLT1781 bank0 일치. 기존unit129와같은기체색팔레트여도같은그림으로가정하지않고새actual조각을선정했다.
- 최종셀2 source(168,0)32×16과셀0 source(192,0)32×16은같은 IMG10442의8×16을공유한다. raw/full16일치를검산해 한56×16 생성master에서분할했고 두분리조각의투명간격도보존했다(source_partial_overlap_proof.json). raw위치로같은물체라고합친것이아니다.
- 무장3조각(최종5 총열32×16/4 세로기계16×32/3 작은끝16×8)은 실제화면(55,70)/(87,57)/(71,86)에서조립되는형태를먼저원본으로확인했다. 원본source의세로접함과다른실제화면의13px/29px계단오프셋을유지한48×37공통native문맥으로그린뒤각OAM사각형으로분할했다(actual_weapon_context_proof.json). 작은36texel도그룹의원래위치에서새그림을갖는다.
- 네생성그룹 모두분할재조립RGBA동일/사각지원밖누락0. 생성원본보존,생성자체alpha<64정리·고알파RGBA불변. native RGB/alpha/mask 복사·스탬프없음. 실제좌표/반전/OAM/priority·기존의존보존.
- candidate_pose_production은제작참고이고실제HD게임검사가아니다.

Claude 위험: 무장새그림이원본보다총구/구멍/그립을또렷하게발명했는지,13px/29px계단조립이음새와작은끝,공유두조각의색/위치/투명간격,작은주황면/초록무장판/파랑회백장갑의명암과기존몸체연결을확인해야한다. 전체기체/무장완료로세지않는다.
