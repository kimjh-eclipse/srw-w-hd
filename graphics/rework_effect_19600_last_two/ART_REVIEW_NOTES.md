# IMG19600 실제 관측 후속 / 신규2개 그림

## 제작 범위와 설치용
- candidate_last_two.png: native32×32의4배128×128 RGBA. 위32×16은jade색hash3200377898, 아래32×16은white/mint색hash3705564854.
- new_candidate_contract.json2개만설치. atlas observed_effect_19600_last_two, exactRGB/static/effect_part=True/resource=None.
- source19600의jade(128,48,32,16)와white(0,48,32,16)이며실제그림형태가다르므로한팔레트그림을재색칠하지않고두참조로새로생성했다.

## 원본 제작 계약
capture_19600_next.py가공통capture_rendered_obj_contracts로실제캐시와renderedOAM을수집했다. unit413 weapon1610 frame360/600,1613 frame600/840,1614 frame360 및unit19 mechanical168/unit299 mechanical141 총7보유fixture의각180프레임을제작입력수집으로읽었다. **후보HD재생검증은아니다.**
source19600의8grid사각형을indexhash로찾은뒤rawindexbytes까지대조했다.3실제팔레트75개관측. 현재라이브대조에서73개는기존연결이고2개만신규다. 큰그룹의기존그림을다시덮어쓰지않는다. 이결과가ROM전장면또는그림품질완료를뜻하지않는다.

observed_contract.json75행및new_observed_contract.json2행에source좌표,현재actualpalette_15bit/RGB,index_pixels/hash,renderedOAMattrs/좌표/affine/flip/engine/state/firstframe기록. bound는cachedhash==partsactualhash와attrs일치필수. unbound는캐시. 현재MMU VRAM/obj_debug픽셀사용없음. 원ROM주소까지추적하지않았으므로resourceNone.

2개모두source/current계약팔레트가해당실제프레임에서동일. jade의사용색은mint[123,222,189]부터darkjade[32,139,106]로흰색이없다. white변형은[255,255,255]흰핵과[213,246,238]/[164,238,213]/mint주변색을갖는다. 등록그림이모든실제색을픽셀단위로정확히보존하는지는Claude판정대상이다.

## 기존73개 보존 근거
existing_overlap_proof.json에모두w/h+rawindexbytes+사용비투명palette슬롯색을대조했다.73/73일치.
- 저장index_pixels가있는바인딩은바이트직접대조.
- 구형extra 및sourcealias에는저장index가없어원참조를선언native_size로읽고고유source_palette_rgb사용색으로index를역복원했다. 원본참조색복원이실제배열과동일하고현재palette의사용슬롯색도같았다. 이는등록계약증거이며HD그림품질합격증거가아니다.
- 기존73개그림/library는변경하지않았다.

## 새 그림과 제한
built-inimagegen2회. rejected_pixel_steps.png는원본계단을확대해부적합하므로미사용. generated_two.png는각팔레트/영역을새로생성해기존계단을부드러운곡선/대각선band로바꾼출력. 생성알파저농도fringe를정리한뒤각패널의자체큰connectedcomponent를원본bbox위치에등록. nativealpha찍기/nativeRGBfill/다른효과재색칠없음. registration.json참조.

생성곡선은원본의계단과직선들보다유기적으로굴곡졌고옅은gradient가있다. white꼬리뾰족점의수/위치,원본crop과연속되는내부band차이가남을수있다. 기존다른조각과연결할때검은절단면을추가하지는않았지만밝기/윤곽줄이생기지않는지는미검증이다. 이미지가생성됐다는것을실재생완료로보고하지않는다.

## Claude 검증 큐
state:test_current/combat/named_attacks/unit_413/native_reference/diagnostic_preview/weapon_1610_capture/frame_360.state
- +112 OAM13 jade3200377898
- +114 OAM16 white3705564854
new_observed_contract.json에정확좌표/변환포함. 신규2개실제HD등장,기존73계약그림보존,준비후held/소실,현재색영역,절단면밝기,효과앞뒤/UI순서를검증할것.

라이브그림/library/DB/core/EXE/설정변경없음. 공식audit/독립QA/후보실재생없음. root설치·굽기후Claude확인대기후보이다.
