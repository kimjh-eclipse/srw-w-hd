# IMG12077 문제 연출87 교체 후보 최종 인계

## 대상과 유지 범위

- Claude `docs/HANDOFF_TO_CODEX_3.md`의 최우선 대상 `observed_effect_12077_new95`95개 중 classified87을 재제작했다. 신규 누락87개 추가가 아니라 기존 바인딩87개의 그림 교체다.
- `normalized_installer_contract87.json`/`install_contract.json`은 installer 형식이다. atlas_box/output_size/slot/spec/actual_palette_rgb/actual_palette_bgr555/기존binding·replacement_of_existing_binding을 모두 보존했다. 후보는 candidate_atlas.png/native_atlas.png이며 원본atlas ID와 크기는 유지한다.
- 정상8개와 대상87 사각형 밖은 live_before_4x.png의 기존HD RGBA를 비트 단위로 보존했다. unflagged_overlap8.json의93073만93074와겹쳐 그 교집합도정상8우선으로보존. 정상8 재판정/다시그리기아님.

## 원본 근거: 역산 팔레트를 설치에 쓰지 않음

- 정규화 입력은 기존 `test_current/parts/true_missing_12077/v2/install_contract.json`107계약에서동일hash/indexbytes/크기/source좌표로복구했다.
- 87중18은 실제 rendered_obj_cache개별관측이며 해당raw bytes/전체16palette/크기/RGBhash까지동일assert했다. 나머지69는개별재생미관측이다. 이69는ROM IMG12077 raw가계약과같고 PLT12076 bank0 전체16값이보존된 실제cached팔레트증거와같다는기존계약의근거를유지했다. 관측으로위장하지않는다.
- 설치 actual_palette_bgr555는 `source_palette_confirmation.actual_proof.palette_15bit` 또는 개별실제cached계약에서읽었다. RGB역산이나기본PLT추측값을설치에넣지않았다. cached palette proof는 unit214/mechanical_cutin_144.state+10/+70 등을기존계약에포함한다.
- source_cached_palette_ROM_integrity87.json:87모두ROMraw/원계약/actualfull16/hash정합,18개별cachedraw추가정합. source_index_palette_integrity95.json은native기준95전체복원일치의참고표다.

## 새 그림과 조립

- 원본전체256x80에는172개연결성분/76고유RGBA형태가있다. 각형태를크게보여주는5개의4x4참조패널을만들어builtinimagegen으로새로생성했다. 원래한벌을단순resize해성분위치가달라지는방식을폐기했다.
- 같은원본성분이반복되는경우동일자체생성모티프를같은색으로재사용한다. 다른기체/다른팔레트그림재색칠이아니다. group53만별도재생성해한칸누락을교정했다.
- 자체생성RGBA를각원본성분bbox의위치/크기에affine등록해원래시트좌표로조립한다. 원본RGB/alpha를출력에전사하지않는다. 알파threshold/morphology/Min/Max로성분을삭제하지않았다. A>=16은생성그림의기하bbox측정에만사용하며출력alpha값을threshold로바꾸지않는다. 각성분의기하사각캔버스경계에서클립되는한계는있다.
- 172는전체시트성분수다. 이번87대상과실제교차하는것은98성분/550native texel/45고유생성모티프다. 이대상안에제작비교상성분소실0. 나머지전체시트영역은기존HD를보존했으므로172개를새로완료했다고세지않는다.

## 제작 중 원본 비교 결과와 한계

- 최종87개의native격자평균alpha128 support 비교:IoU1/면적비1/미도색0. target_component_presence_production.json은98대상성분위치의paint존재를보는생산진단이며독립QA나완료판정이아니다. 원본참조mask는비교에만쓰고출력에는붙이지않았다.
- 색상은원본색배치유지목표로생성했지만완전히동일하지않다. source_colour_production_comparison87.json의원본paint픽셀RGB평균차이중앙값6.10/255,최악binding93009평균12.53/255/최악채널31. 밝은white/pink/red의부드러운명암/AA차이로성분하위색영역이바뀔수있다.
- 비정수AA/4배보간/실제레이어·회전·축척·원본상태별palette phase는공식판정전이다. 실제HD재생과 verify_new_art/classify_new_art를여기서돌리지않았다. Claude가87대상같은방법으로검증해야한다.
- 원본/이전/교체3행비교 native_before_candidate_comparison.png,성분기하component_geometry.json/component_groups.json,생성원본panel*_generated.png와group53_generated.png,수정전v1후보/보고서보존.

## root 설치 주의

- root는새 `effect12077_components_repaired87` atlas를만들어기존87ID만새파일을가리키게분기한다. 정상8의기존binding·옛atlas이미지·텍스처키는모두불변이다. 새후보fullcanvas안의공유교집합도기존8픽셀과같이보존했다. **root분기설치에서는기존87개만굽고95전체재굽기는하지않는다.** 새ID87추가/다른정상대상변경금지.
- 이작업은후보·계약·생산원본대조만이다. 라이브/DB/core/공유실행코드/EXE/Git/공식QA/물리입력/플레이어창을변경하지않았다.

## 연결 계약의 좌표 복원 기록

정규화 계약을 hash만으로 원본107계약에 매칭한 제 실수가 있었다. 같은 해시의 다른 원본사각형(완전동일raw·사용색별칭)이선택되면서candidate atlas_box까지그별칭좌표로바뀌었다. candidate PNG는처음source_live_bindings95의옛좌표로만들어졌으므로실제굽기4개(92988/93006/93018/93034)가빈그림으로판정됐다. 그림/알파의결함이아닌연결계약의좌표혼동이었다.

최종normalized/install87의 atlas_box와spec x/y는모두source_live_bindings95의기존live x/y로복원했고sourceproof별칭좌표는source_box/source_proof_alias_box로분리했다. source_candidate_coordinate_space_proof87.json에잘못된좌표/옛live후보좌표/별도원본증거좌표/원본index·fullpalette재구성일치를모두남겼다. root가87live좌표복원/다시굽기를한다. candidate PNG/SHA/자체alpha변경없음. 다른그림에서도hash만보고후보좌표를정하지않아야한다.
