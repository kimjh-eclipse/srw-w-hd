# 아바레스트 속도선FX6 동일ID 교체후보

상태: 미검증 그림후보. 실제HD 재생/verify_new_art 공식검사는 Claude 담당. 신규미연결 수/완료수추가없음. 라이브/공유코드/DB수정없음.

- 설치입력 installation_map.json/candidate_atlas.png/native_atlas.png/contract.json/replacement_targets.json.
- 후보 SHA256 e2dfe7025b11012ab64b56e4b941a06500c9733042fdbc25604b2994cfe56a12.
- 동일1-based #92956/#92958/#92960/#92962/#92964/#92965만교체. 현재old_spec와actual cached OBJ계약의hash/index바이트/w/h/전체팔레트기계대조통과. 기존dynamic_palette=False/effect_part=True/resource=None/source_owner미확정속성그대로보존.
- key의 test_current/parts/claude_arbalest_fx_reclassification/exact_fx_source_contracts.json 및 HANDOFF_PRODUCTION.md 역할분류인수. 기계부품으로그리지않고흰속도선·작은날림FX로새로그림. IMG소유를새로추정하지않음.
- 실제source_mechanical_265_1096/source_pose.state +0의OAM1/3/13/17/24/25. #92960 원본은3texel작은성분+12texel긴성분이분리되어있어둘다새그림에포함. 나머지는8connected각1성분,총7성분. 각localbbox/면적은native_component_geometry.json에보존.
- 생성 exec-d5c1cc75-197e-43cc-bf09-87ba82efdbd4.png. 첫생성을imagegen으로편집한새그림이며6개각원래분기·두성분/방향/고형면을유지하도록요청했다. 원본RGB/alpha스탬프/수작업색칠/기계그림재사용없음.
- alpha문턱/팽창·침식없이전체생성RGBA를기하정렬/resize. 160은정렬앵커측정에만사용하며alpha값을0으로만들지않음. 일반원래OAM캔버스scissor외마스크없음. 낮은alpha원본도유지. alpha_and_alignment_provenance.json.
- generated_component_presence.json은제작성분존재확인만: #92960의두성분이각각163/44HD픽셀로분리되어남고다른5개도각1성분. 원본과형태·색·면적이맞는다는공식판정아님.
- raw미리보기에서보인외곽광은대부분alpha0영역의RGB를보여생긴착시였다. 샘플(80,200)RGBA[17,18,19,0]. 실제RGBA를회색배경에합성한 generated_rgba_composited_preview.png에는큰외곽광없음. 알파를지워서그림을깨끗하게만든것이아니다. 앞선실제광추정은취소한다.
- replacement_preview.png는원본/기존/새후보제작참고. 같은묶음11중다른5그림은손대지않았고whole_pose_dependencies보존.

Claude 위험: #92956의갈라진속도선구멍/갈래/외곽두께를새그림이정돈해바꾸었을수있다. 작은4개는층진덩어리를테두리달린리본/갈고리처럼해석했을수있다. #92965의회청색밴드와흰면비중/기울기, #92960의미세성분사이간격·위치·면적을확인해야한다. 성분존재를확인했을뿐원래속도선성분분포가동일하다는주장없음. 실제반영/공식검증완료주장없음.
