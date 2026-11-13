# root 보조 그림용 실제 에너지 패널4종 원본

기계원종 unit348 weapon1400의 실제관측 binding0 큰 자홍색 에너지 패널4종이다. 본체로 분류하지 않는다. 이 폴더 source_pose.state를 load하고 Core.run1회한offset0이 rendered_contract_all.json/cached계약과 같다. 메뉴생성frame120에서state를저장하고다음1frame의cache를계약으로확보했다. source선정은isolated RAM메뉴fixture이며 실제ROM/세이브/DLL은변경하지않았다.

공통helper계약/실제palette/index/hash는rendered_contract_all.json에있다. core_path와실제SHA는capture_meta.json. 원본셀4개 oam_0_native.png~oam_3_native.png,2×2 rawnative128×144는native_atlas.png,원본확대grid_native_context.png,각셀atlas좌표포함grid_contract.json.

전체원본4개를OAM역순으로조립한whole_native_extended.png와bbox표시whole_native_bbox_context.png는y+128px확장캔버스다. 실제y=-4인상단부분을보존한문맥이며계약좌표는변경하지않았다. 일부OAM사각형은겹치므로각파츠숨은부분을큰그림하나로임의덮지않는다. 공식QA/독립재생검증이아니라제작원본추출이다.

framebuffer_hd_enabled.png는HD-enabled Core.native이므로pure-native증거가아니다. root가패널4종그림을담당하며본인은중복제작하지않는다.
