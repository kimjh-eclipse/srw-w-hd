# unit368 weapon1462 실제소실3개 후보

- 대상93450/93451/93452는고정판정과현재live observed_unit368_weapon1462_fx_fourteen이같습니다. 실제그림은기계가아닌노랑/주황/빨강작은파편열입니다. 모양이나이름으로기체를추정하지않았습니다.
- 최종입력 final_flat_contract.json,native_atlas.png(256×256),candidate_atlas.png(1024×1024)입니다. SHA256=178e941174039f02ca8c49d06490d04330905e9361d820d9dcefa47ae8ad5b59. sha256.json에원본/계약/생성SHA를보존했습니다.
- atlas총14개중정상11개의기존자체RGBA/metadata를byte비교보존했습니다(preserved_normal11.json). 순수단색독립파츠를새그림수로추가하지않습니다.
- actual_observed_contract.json은 native_weapon_source_368_1462/fx_actual/source_contract.json 원자료그대로입니다. unit368_weapon1462_source.state +590의실제렌더관측/OAM/rawindex/full16BGR555/RGB계약을보존했습니다. 미관측추정추가없음.
- **ROM source owner는여전히미확정입니다. resource=None/source_owner_confirmed=false를유지합니다.** 이source_box는기존관측원본아틀라스의배치좌표이며ROMIMG좌표라고주장하지않습니다(source_box_kind=observed_source_atlas_layout_not_ROM). atlas_box는새candidate의설치좌표입니다.
- 실제원본위치의노랑/황토/주황/깊은빨강재질을각각새로생성했습니다. source조각의양방향색을흰색/주황단색으로몰지않았습니다. 원본위치는맞지만알파가약해작아보이던기존조각대신불투명한filled core와새매끈painted contour를그렸습니다.
- source성분수는93450=6/93451=8/93452=7입니다. 각생성성분자체RGBA bbox만crop/resize하여원래bbox에등록했습니다(geometry_registration.json). 93451첫생성에서3개의bent chips가갈라져 rejected_93451_split_components.png로보존하고다시연결된형태로생성했습니다.
- 원본RGB/alpha전사,originalmask사용,알파문턱삭제,morphology/재색칠/타팔레트alpha차용없음. 작은단색점은부모의원래성분일뿐별도완성파츠로계수하지않습니다.
- 후보및NullCache prepare preflight3개모두 flags=[]이고IoU1/1/1,미칠0,밖0입니다(candidate_geometry.json,prepare_geometry.json). source가작은도트라native-grid mask가같다는뜻이며정식HD시각QA완료가아닙니다.
- final PartsRenderer.prepare_texture14개전부nonempty/sourceindexalphaRGB일치입니다(production_report.json). 정상11개메타/RGBA는보존했습니다.
- manual_native_before_candidate_prepare.png는원본/기존/새후보/prepare를회색RGBA로비교합니다. 채워진폭과개수·위치·실제색계열을수동확인했습니다. 작은도트들은HD형태이득이제한적이며새paint재질/경계와opacity개선이주요차이입니다. alpha0RGB ghosts를실색으로오인하지않았습니다.
- 라이브러리/sqlite/공유코드/코어/EXE/배포/푸시/모니터/게임창미수정. 중앙설치·굽기·동일도구검사및Claude독립시각/실제게임검증대기입니다.
