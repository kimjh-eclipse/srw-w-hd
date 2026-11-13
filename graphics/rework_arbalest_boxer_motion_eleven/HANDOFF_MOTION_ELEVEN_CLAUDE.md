# 아바레스트 boxer 실제 미연결11효과 — 그림 제작 인계

## root 설치/굽기 후보
- `candidate_motion_eleven.png`, **768×1152**, 원본native atlas **192×288**. 원본파일실제크기를그대로4배로썼다.
- SHA256: `751b6e27749a5d02cec6fd60ab8be50f33d73bcc92485a9def411f81a397a1e6`.
- `new_motion_eleven_contract.json`,11개. atlas_id=`observed_arbalest_boxer_motion_eleven`.
- 참조native는기존`native_atlas.png`. 기존`contract.json`의각`atlas_box`좌표를바꾸지않았다. 판정없는원본context는`native_cells_context.png`, `unit265_native_context.png`, `whole_native_bbox_context.png`.

## 제작입력과후처리
- 부모/shape담당이제공한rendered cached OBJ 11개rawindex/실제16색palette/hash/OAM속성/좌표/변형/engine/state/frame을보존했다. rawindex+actualpalette로cachedRGBhash11/11재계산일치.
- 원본source state는 `test_current/parts/borrowed_shape_rework/source_mechanical_265_1096/source_pose.state`. load후1run에서제공된원본계약(frame0)이다. 새HD후보의실제재생검사는하지않았다.
- resource=None,owner_confirmed=false/source_owner_confirmed=false. 실제캐시원본은확정이지만IMG리소스소유를임의로단정하지않았다. effect_part=true/static actualpalette.
- built-in imagegen으로11조각을한벌새로그렸다. 처음생성은검정금속칼같은재질이되어사용하지않고,다시원본의옅은회청/흰색영역으로생성편집했다. 최종원출력은`generated_pale_eleven.png`.
- 전체sheet bbox를한번에맞추지않고각cell을분리하여자체생성alpha220threshold/min3/max3후해당nativebbox의위치/크기에맞췄다. 원본RGB/alpha를복사하거나원본mask로찍지않음. tiny조각을빈그림이나점으로대체하지않음.
- `prepare_motion_eleven.py`가재현절차와최종원출력파일명을보존한다.

## 준비후생산존재 확인
- 기존공유`PartsRenderer.prepare_texture`를메모리atlas/NullCache에서실제로호출,**11/11준비후그림유지**.
- maxA≥16,최소지원면적비0.573,분리성분제거모두0,referencefill0/cutink0.
- `motion_eleven_production.json`에각조각숫자/원본bbox/생성bbox/준비스탯/PNG SHA. `prepared_motion_00.png`~`10.png`는준비산출물이며live baked DB에쓴것이아니다.
- 이확인은빈그림/위치실수로생성이삭제되는것을막는생산입력검사다. 독립QA/실제게임HD재생/무기정상판정이아니다.

## Claude후속확인
- unit265 무장1096source_pose를동일하게불러11효과가실제기체/무장연출과맞는지확인.
- 원본속도선의쪼개진갈래와끝점방향은유지하도록그렸으나,생성본에반짝임/가는외곽선/자잘한갈래가추가되었을가능성. 작은조각의두께와원본색영역위치도실제확인필요.
- 기체분류가아니라효과분류로인계받았지만전체공격context에서물체부품이나효과인지재확인해야한다. 이미지가있다는것만으로기체전체HD완료나컷인/가림순서정상으로세지말것.
- 라이브library/DB/코어/EXE/사용자창/설정변경없음.

## 최종생성프롬프트
Image1(초기생성11조각)을Image2(native색/형태reference)와같은옅은색으로교정:11개grid위치/각도유지,검정outline/shadow/bevel/금속칼재질제거,shadow#8BA4AC/middle#A4BDCD/light#D5DEE6/bright#EEEEEE만사용,어두운외부영역은투명,실제원본의회청하단면+흰상단면단순band,3Dgloss/추가조각금지,tiny11조각누락금지,갈라진끝/절단면윤곽선추가금지,3:4transparentcanvas. 도구built-in image_gen,transparent_background=true.
