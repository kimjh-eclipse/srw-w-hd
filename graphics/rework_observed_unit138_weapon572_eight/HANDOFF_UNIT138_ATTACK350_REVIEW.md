# 실제 unit138 / weapon572 메뉴350 미연결8 후보

상태 `CACHED_OBJ_ARTWORK_CANDIDATE_UNVERIFIED`. 공식 검사·실제 HD 재생은 Claude 대기. 라이브/공유 코드/코어/DB 변경 없음.

- 설치 입력: installation_map.json/candidate_atlas.png/native_atlas.png/contract.json.
- 후보 SHA256: `45ac11fab8db1ad362a1c4ff4063304a06ef551b48dbf754c04188d731ae65ad`.
- fixture: source_mechanical_fixed_138_572_350/source_pose.state +0. actual cached OBJ/OAM/팔레트/코어SHA 보존. 실제 메뉴350의 기체는 화면밖으로 돌진해 일부만 보인다. raw cached 전체와 상대 OAM좌표를 bbox로옮긴 whole_native_bbox_context.png는 제작용 역할자료이며 실제게임에서전체가보였다는뜻이아니다(bbox_context_provenance.json).
- 원래9후보중 머리 indexed proxy1은제외하고 actual exact0/indexed0인8종만 제작. 원래0/1/2/3/5/6/7/8을 최종0..7로 재번호. 원본 IMG10618 6종/10629 2종 actual 인덱스바이트 일치, 전체16색 PLT1808 bank0일치. 대상 원본사각형 교집합없음. raw에서닿은별도팔조각들은 실제위치가달라 임의로한물체로잇지않았다.
- 원래8×8/29texel 작은조각은 실제몸체접합위치와 full bbox문맥을 확인해 새그림에포함했다. 완성된손/눈/얼굴로해석하지않고 짧은남색/검정연결면만생성. 관측원본이작다는이유로누락시키지않았다. 다른여러큰팔/다리/검정장갑/칼조각은원본각도와분리빈틈대로그렸다.
- native 메뉴200은16OBJ모두기존연결,메뉴300의8×8같은hash는새후보의존으로덮이지만칼은palette1의다른RGB단계이므로이번palette0칼과혼동하지않는다. 메뉴350+20에서는OBJ없음. 전체무장완료로세지않는다.
- 생성원본/자체alpha<64정리근거보존, 고알파RGBA불변. native RGB/alpha/mask 복사·스탬프없음. candidate_pose_production은화면크기내제작참고, bbox_candidate_pose_production은화면밖cached부품까지좌표이동해본제작참고이며 실제HD검사가아니다.

Claude 위험: 칼의얇은흰경계/새AA,작은8×8접합부두께/색,회백복합부품의모델이임의로추가한장식·관절선여부,검정갑옷의불투명영역과다른팔/다리의이음새·명암을실제재생에서확인해야한다. 머리proxy는그대로라새몸체와의색/스타일차이도미확정이다. 화면밖부품전체의실제게임표시완료를주장하지않는다.
