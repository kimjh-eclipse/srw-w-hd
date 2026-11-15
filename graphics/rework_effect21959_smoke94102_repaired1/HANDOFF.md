## 94102 추가 재제작(현재 후보)

- root가94102의이전후보를도트경계확대에가까운그림으로판단하여중앙미설치보류했습니다. 해당불합격근거를 rejected_94102_blocky_*에보존하고94102만다시그렸습니다.
- **이번추가설치대상은94102 하나**입니다. 독립flat계약은 94102_flat_contract.json, 현재전체candidate_atlas.png SHA는 ca3b79adc522a46a8e5e1451946cc9bed750dbc5fa9b01990622b2d5e98f9e3e 입니다. 앞선94099/94101그림은이전후보와byte일치하며바꾸지않았습니다(production_report.json previous94099_94101_preserved).
- 94102의큰2성분과작은4고유성분을각각내장도구로다시생성했습니다. 기존평평한검정도형/둥근모서리아이콘대신roll된black smoke의내부결·미세한낮은명암·새billowed곡선경계를그렸습니다. 실제회색영역외에는검정위주를유지하고외부haze/new branches/white rims를금지했습니다.
- 1px검정재질점3개는기존자체생성재질을보존하며HD이득으로계수하지않습니다. 작은4고유형상도소스마스크로자르지않고 generated_component_94102small.png의자체생성RGBA를crop/resize했습니다. 큰새원천은 generated_component_8.png/9.png입니다.
- 최종94102 native-grid 연결성분9개와모든성분bbox가원본과같습니다(94102_component_presence.json). 칠면적은원본246→후보283(+15%)이며분리조각/가지는남아있습니다. 과도한팽창여부는독립시각검증위험으로남깁니다.
- 후보·prepare사전검사모두flags=[],IoU .840/미칠0/밖0입니다(94102_candidate_geometry.json,94102_prepare_geometry.json). 실제6개prepare원본입력일치/nonempty는유지합니다. 자동통과를정식QA로쓰지않습니다.
- 94102_native_rejected_smooth_prepare.png는원본/이전94102불합격/새94102/prepare입니다. 회색RGBA합성에서새연기결/외곽곡선/원래자리·폭을확인했습니다.
- 원본mask/RGB/alpha전사,threshold삭제,morphology,색변환없음. 정상3개와앞선2후보를보존했습니다. 설치·굽기·공식QA·게임검증미실시.

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
