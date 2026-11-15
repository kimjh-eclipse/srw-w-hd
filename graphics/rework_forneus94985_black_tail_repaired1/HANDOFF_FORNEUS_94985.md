# 포르네우스 꼬리 검정 가장자리 #94985 후보

같은 ID 교체1개 후보, 신규 누락 증가0. 정상22개 유지. 공식 QA/HD재생·라이브/코어/DB 쓰기 없음.

- 실제 source: native_weapon_source_346_1395/unit346_weapon1395_source.state +235/OAM22/screen178,85/8×16/22texel. flip_x=True이므로 후보는 원래 raw 방향이고 런타임 반전을 바꾸지 않았습니다. 전체문맥 actual_mechanical_pose_346_235/whole_native_context.png의 꼬리 끝 가장자리입니다.
- 원래 cached index/actualfull16/RGB CRC가 현재 spec과 같음을 확인했습니다. current key로 mode=ro SQLite SELECT에서 실제 baked를 읽었습니다. 현재는 원본의 넓은 검정 실루엣을 얇은 광택 호로 바꾸어 미칠27.3%가 남았습니다.
- generated_raw.png는 imagegen 새 출력 exec-2193acf1-1c80-4d3a-9daa-3bdbc103eec6.png 보존. 실제 원본은 무늬 없는 고형 검정 재질이므로 광택/홈/질감/밝은 선/장갑 장식을 발명하지 않고 넓은 지지형상과 단조로운 검정을 유지했습니다.
- 도트이미지를 키운 것이 아니라 새 고해상도 실루엣을 생성해 자체 RGBA bbox 기하 정렬만 했습니다. source RGB/alpha 전사·native mask/문턱삭제·침식/팽창 없음.
- installation_map.json 같은#94985만 교체. 원래 hash/index/fullpal/lookupflags/source속성 유지. contract.json/native_atlas.png 같이 사용.
- candidate_atlas.png SHA `3d8f70fa476a39a92199a192748fba691486f2798972e3a9fc42c459d2790c35`.4배32×64. 후보/NullCache prepare 사전기하 flags0, IoU .909/미칠0/외부0. 숫자를 실제 화질 합격으로 부르지 않습니다.
- 같은fullpal 다른 큰 raw의 완전포함 결과 0개(same_source_parent_matches.json). 정상22 spec 불변은 preserved_normal22_latest.json.
- replacement_comparison.png는 source/current baked/new candidate. 실제 단색부품을 불필요한 세부묘사 없이 복원했으므로 미관의 변화는 작을 수 있습니다.

Claude 확인: 꼬리의 인접 정상 파츠와 붙는 상단의 잘린 경계/반전방향, 원래 완전검정과 후보의 미세한 검정 명암·AA 차이, 매끈해진 실루엣이 계단 원본의 지지영역을 유지하는지 실제 장면에서 봐야 합니다. 전체 기체/꼬리 다른 자세 완료가 아닙니다.
