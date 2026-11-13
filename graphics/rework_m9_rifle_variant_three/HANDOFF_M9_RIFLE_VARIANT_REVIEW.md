# M9 다른 저격/라이플 자세 실제미연결3종 후보

상태: 미검증 후보·연결 준비 완료. Claude 시각/재생검증 담당. 라이브·DB·코어변경없음.

source_mechanical_262_1076/source_pose.state (M9 unit262/저격1076,메뉴frame420저장)와 source_mechanical_261_1063/source_pose.state (M9 unit261/라이플1063,메뉴frame240저장). 로드후1회run의 실제 cachedOBJ+renderedOAM기준. 둘모두격리RAM진단메뉴원본이며 기력/비용/지형완화·ROM/사용자저장불변은capture_meta참조. 캠페인합법성QA아님.

본체palette0 전체26OAM 중새3종3OAM, 기존23OAM 의존 whole_pose_dependencies.json 보존. 앞서새로그린m9_sniper_boxer7 및root작업중m9_smoothbore2의actualRGB는제작선정에서명시적으로제외했다. 새3종은최신exact/indexed0(source_identity_and_connection.json). 캐시actualpalette사용색은3종모두ROM후보일치. 원본indexbytes는ROM13663/13662 실제동일영역완전일치(rom_indices_identity.json), 소유리소스의유일성은별도미확정.

설치installation_map.json + candidate_atlas.png768×288/native_atlas.png192×72, 정확4배. mechanical_contract_checks.json은원본RGB/alpha/indexSHA/크기확인, candidate_presence.json은빈/nearalpha max16미만=0. 품질QA아님. SHA `c4416fa4cc47c4ea2216921214e36d97bc1f8b02f8ca2a265969a1a812544c15`.

parts_generated.png는imagegen exec-e212c134원본. 기체전체bbox문맥과3원본셀을참조해새로그림. 원본RGB/alpha스탬프없고 생성알파bbox정렬만. cell0은머리뒤에솟은부분연결편이며얼굴/머리라고하지않는다. cell1은좌우두분리조각을보존. cell2는짙은중앙영역이있는부분연결편이다. 임의로포구/손/입으로완성하지않도록프롬프트에명시했다. 접합cap/두분리영역지원·회색밝은면범위는Claude판정대기. unit*_production_assembly.png는원본기존파트를조합한제작문맥이며HD재생증거아님.

Claude재생:
```powershell
python scripts/verify/verify_runtime_path.py --state test_current/parts/borrowed_shape_rework/source_mechanical_262_1076/source_pose.state --frames 120 --save-frames 0 15 30 60 --track-atlas m9_rifle_variant_missing --name m9_other_sniper
python scripts/verify/verify_runtime_path.py --state test_current/parts/borrowed_shape_rework/source_mechanical_261_1063/source_pose.state --frames 120 --save-frames 0 15 30 60 --track-atlas m9_rifle_variant_missing --name m9_rifle
```
