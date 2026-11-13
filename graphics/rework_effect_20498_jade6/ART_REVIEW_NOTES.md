# IMG20498 jade 실제 그룹 / 신규6개 후보

## 설치용과 기존 보존
- candidate_jade_plume.png: native128×32의4배512×128 RGBA. 실제관측jade그룹의미연결6개를모두포함하는연속plume두개한벌이다.
- new_candidate_contract.json: 신규6개만. atlas observed_effect_20498_jade_plume / exactRGB / resource=None / dynamic_palette=False / effect_part=True.
- hash:3751420720,4202208232,3659430972,4005213723,1491087823,3181635244.
- 기존4개는keep_existing_contract.json에기록하고유지. 전체10개계약인observed_contract.json은문맥이며4개는새아틀라스범위밖에도있으므로통째등록금지.
- existing_overlap_proof.json:4/4 w/h,index배열,사용한비투명팔레트슬롯RGB일치.3개는저장index_pixels직접대조.4721 alias는source_binding4463(extra참조원본)의고유source_palette_rgb로인덱스를역복원한뒤실제배열과일치,alias의palette_rgb도실제사용슬롯과일치했다.4개를새그림으로덮지않는다.

## 제작 원본 / 실제 팔레트
capture_20498_jade.py는새공통capture_rendered_obj_contracts로unit413 weapon1610 frame360/600 두state각180frame의원본제작계약을재수집했다. 10개모두현재cachedOBJ와renderedOAM에서관측. bound라면cachedhash==core.parts actualhash와attrs일치를요구. unbound는cached계약. VRAM/obj_debug픽셀사용없음.

observed_contract.json의palette_15bit 및original_palette_rgb가실제현재팔레트다. 각행마다원본index_pixels,hash,index_hash,source_x/source_y,w/h,engine/OAMattrs/좌표/변환/firstframe/state를기록했다. 임의PLT추정과재색칠없음. native_full_plume.png는ROM IMG20498의연속128×32영역을이실제팔레트로표시한제작참조이며,각등록crop의rawindex는실제캐시와일치. 원ROM주소까지추적한것은아니므로resourceNone.

paletteRGB 사용색은[123,222,189],[74,213,164],[65,189,148],[49,164,123],[32,139,106],[24,123,90],[16,115,82],[16,98,65]. **흰색핵이없는실제녹색변형**이며white/mint그림을재색칠해만들지않았다. source와현재palette계약은동일하다.

## 새 그림 / 알려진 차이
built-inimagegen을실제jade참조로별도2회생성했다. generated_first.png와generated_flat_retry.png. flat_retry를후보로사용. 두plume를연속한그림으로그려overlap사각형을공유좌표에서사용하고절단면검은윤곽을추가하지않는다. 생성자체알파의미세분리찌꺼기만정리하고각plume의생성자체큰connectedcomponent를원본bbox위치에등록했다. nativealpha stamping, nativeRGBfill,코드재색칠없음. registration.json참조.

**남은제작한계:** interior를단색으로요청했지만생성본은옅은명암변화를남겼다. 원본에서단일색인3751420720(source32,16,16,16)도누락하지않고같은연속그림crop으로계약에포함했으나,후보가원본처럼완전균일하다는보장은없다. 단색코드채우기로검사를속이지않았다. 원본보다곡선band가두껍고꼬리갈라짐형태가달라졌다. Claude는특히단색crop과주변그림간밝기/접합줄을판정해야한다. 품질합격또는완료선언아니다.

## Claude 확인 장면
state1:test_current/combat/named_attacks/unit_413/native_reference/diagnostic_preview/weapon_1610_capture/frame_360.state
신규6개모두첫관측+112. 각OAM/좌표는observed_contract.json. 기존4721/91982등도같은프레임문맥에기록돼있어새그림과기존그림의연결·스타일차이점검필요.
state2:동일weapon_1610_capture/frame_600.state +72/+74는이미기존연결된ray/대각선부분문맥.
신규6개HD등장·기존4보존·민트현재색유지·단색내부·절단선·가림/UI·준비후소실여부를Claude가검증할것.

## 변경 경계
gray2/21948새17/20498white새7/live그림/library/DB/core/EXE/설정변경없음. 공식audit/독립QA/후보HD재생검사없음. 원본제작계약수집과기계적hash/크기만확인했다.
