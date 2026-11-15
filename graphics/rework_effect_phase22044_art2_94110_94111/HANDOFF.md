# phase22044 그림2개 인계

- 대상94110/94111은latest현재분류와live observed_effect_phase_22044가같고미설치후보목록에없음을확인해제작했습니다. 정상부모공유영역은없습니다. 전체7개중정상5개RGBA/metadata를byte비교보존했습니다(preserved_normal5_metadata.json).
- 최종그림/계약 final_flat_contract.json,native_atlas.png(128×64),candidate_atlas.png(512×256)입니다. 후보SHA256=d562144c952028958ef492081c77cd35d467bebb2d5b606f1c11f5eaba2013cb. sha256.json에원본/계약/생성원천SHA를보존했습니다.
- actual_observed_contract.json은 next_confirmed_fx_source/art_phase_22044/source_contract.json의실제원본raw/full16BGR555/RGB/state/frame/OAM원자료복사입니다. finalflat에source_box와atlas_box를분리하고actual/미관측구분을유지했습니다. 관측되지않은팔레트추정없음.
- 94110은사용색4~7중index7 #5A5A4A가197/297로진한회갈색주재질입니다. 94111은index2~6의중간베이지이며밝기가다릅니다. 같은전체팔레트라도동일밝기그림으로재색칠하지않고각각독립생성했습니다.
- 새그림은원래넓은filled dust mass,큰구멍/가지/꺾임/분리조각의위치를유지하면서연속rolling cloud외곽과내부먼지결을새로그렸습니다. 기존그림의가는불꽃/wisp로의축소를반복하지않았습니다. source94110=2성분/94111=3성분입니다.
- 94111첫생성에서안쪽곡선이작게떨어져main을분리참조로재생성했습니다. 최종안쪽조각은같은main생성원천의자체RGBA crop을원래source rows15~17의3×3범위로resize/정렬하여연결했습니다(own_geometry_registration.json). 원본mask/RGB/alpha를옮기지않았습니다.
- 원래작은2조각은 generated_94111_initial.png의해당생성성분자체RGBA만사용했고,나머지초안큰덩어리를최종에쓰지않았습니다. 94110원천은generated_94110.png,94111큰원천은generated_94111_main.png입니다. 원천은builtin image_gen입니다.
- authoring_component_layout.json은그림좌표배치중native-grid 연결성분을2/3으로확인한저작근거일뿐공식QA가아닙니다. 생성alpha>=128은bbox/배치측정에만쓰고출력alpha값을삭제/이진화하지않았습니다.
- manual_native_before_new_art.png는원본/기존live/새그림을회색RGBA로합성한수동대조입니다. 실제두단계밝기와넓은채움/큰구멍/조각위치를확인했습니다. alpha0RGB잔여를불투명외곽으로오인하지않았습니다.
- 역할변경에따라PartsRenderer.prepare/기하검사도구/전체검사/설치/연결/굽기를실행하지않았습니다. 중앙library/DB/materialcache/manifest미수정. Claude가실제prepared좌표/팔레트·색면적/성분폭/게임재생을검증해야합니다. source의미세격자윤곽과새유기적먼지경계의차이는남아있습니다.
