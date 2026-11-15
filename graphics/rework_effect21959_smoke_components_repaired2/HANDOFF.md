# phase21959 실제문제3개 후보 인계

- 대상94099/94101/94102의고정판정및현재live atlas observed_effect_phase_21959 일치를확인했습니다. 전체6개중정상94097/94098/94100 3개는기존자체RGBA/metadata를byte비교보존했습니다(preserved_normal3.json). 정상부모와동일child의임의교체없음. 순수단색파츠교체를새그림수로세지않습니다.
- 최종입력 final_flat_contract.json,native_atlas.png(128×128),candidate_atlas.png(512×512)입니다. 후보SHA256=a7288b9ae79e83f976cfad57dabe4ac04c64894dbf23c0254125302fdb35d06a. sha256.json에원본/계약/생성원천SHA를기록했습니다.
- 실제원자료 actual_observed_contract.json은 next_confirmed_fx_source/art_phase_21959/source_contract.json 그대로입니다. 전체16색BGR555/RGB와raw index/관측state/frame/OAM을유지했습니다. finalflat에source_box와atlas_box를따로적었습니다. 미관측추정추가없음.
- unit314_weapon1279_source.state의94099 +309,94101 +318,94102 +322 실제관측계약입니다. state경로는 true_missing_19898 폴더지만이파츠의실제리소스는21959이며기존계약그대로유지했습니다.
- 3개모두단색이아닌검정+회색연기입니다. 실제사용색은index1 검정불투명,2 #313131,3 #525252,4 #737373입니다. index0만투명입니다. 전체16색팔레트의사용하지않는주황/파랑을연기에사용하지않았습니다.
- 기존연기는검정넓은채움과회색infill이가는고리/수염으로줄어있었습니다. 새그림은원래위치의불투명검정덩어리와회색채움을유지하고미세픽셀계단/디더링을새연속lobed cloud경계로해석했습니다. 다른팔레트그림이나기존RGBA의재색칠이아닙니다.
- 원본연결성분94099=6,94101=2,94102=9를각각분리참조했습니다(components.json). 주요6성분은각각신규builtin image_gen,작은8고유성분은별도생성시트로제작했습니다. 동일1px검정재질은동일자체생성셀의불투명내부RGBA를공유합니다. 이는별도완성파츠로계수하지않습니다.
- 모든생성자체RGBA만crop/resize하여각원래성분bbox에놓았습니다(geometry_registration.json). 원본마스크/RGB/알파전사,색변환,생성알파문턱삭제,morphology없음. 겹친bbox안에다른조각을한꺼번에재배치하지않도록성분별원천을독립생성했습니다.
- component_presence_check.json: 최종native-grid 연결성분수가6/2/9로원본과같고모든성분bbox도원래자리입니다. 94101의주성분native-grid칠면적은358→451로증가했습니다. 거친빈격자를연속그림으로해석한차이이며독립시각QA에서과도한팽창인지확인할위험으로남깁니다.
- 후보및NullCache prepare preflight3개모두flags=[]입니다(candidate_geometry.json,prepare_geometry.json). IoU .864/.773/.976,미칠최대.037,밖최대.012입니다. 정식QA완료가아닙니다.
- NullCache PartsRenderer.prepare_texture 최종6개모두nonempty/sourceindexalphaRGB일치(production_report.json)입니다. 원본채움/성분삭제등prepare통계도모두0입니다.
- manual_native_before_candidate_prepare.png는원본/기존live/새후보/prepare의회색RGBA합성입니다. 불투명검정과회색위치,작은조각과넓은채움을수동확인했습니다. 검정배경에서안보이던black재질을회색에서확인했으며alpha0RGB잔여를실색으로오인하지않았습니다.
- 라이브러리/sqlite/공유코드/코어/EXE/배포/푸시/모니터/게임창미수정. 중앙설치·굽기·동일도구검사및Claude독립시각/실제게임검증이남았습니다.
