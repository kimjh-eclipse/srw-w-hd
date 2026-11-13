# unit297 / weapon1213 / IMG22673 실제 미연결 3종 제작 인계

## 명칭과 범위
기체명을 추정하지 않고 fixture unit297/weapon1213 및 IMG22673로만 기록합니다. 상위폴더의 getter라는 옛 이름은 실제 기체명 근거가 아닙니다.
누락 제작 큐 current.json의 IMG22673 pending3과 실제캐시 미연결3을 대조했습니다. actual binding_id0,라이브RGB/indexed연결0,각source사각형의원본인덱스바이트일치. 같은실제팔레트로된원형광원/대각선광원/작은끝조각입니다.

## 최종 파일
- candidate_atlas.png:288×128(1배72×32의4배),native_atlas.png:72×32.
- install_contract.json:3종 실제palette/index/hash/원본source좌표/원래OAM및상태.
- generated.png:새image_gen원본. 새그림은원본단순확대나기존그림리컬러가아닙니다.
- mechanical_input_check.json:코어경로/SHA,source바이트정합/실제미연결 및파일입력.
- missing_classification.json:누락큐3종과연결.
- ../source_contracts.json:보유8state의추가제작용원본추출결과및ROM바이트검색. QA실행결과가아닙니다.

## 연속 영역
전체IMG72×32를한벌로그렸고원래[0,0,32,32],[24,0,32,32],[56,0,16,16]대로잘랐습니다. 첫둘의8pixel겹침영역은같은그림에서나오므로후보픽셀동일. 원본알파/RGB스탬프/점대점리컬러/실행중가공코드는쓰지않았습니다. static/effect 실제RGB별설치후보입니다.

## Claude fixture와 위험
- cell0:unit297/diagnostic_preview/weapon_1213_capture/frame_480.state +40
- cell1/2:같은폴더/frame_720.state +20
- 새그림의원형광원흰코어와주황테두리폭/반투명알파,대각선끝형태,사각형절단면접합을원본과대조필요.
- 원본의상단/좌측/우측에걸린불투명부분은타일밖으로이어지는내용이므로배경잔여로자동삭제하면안됩니다.
- 후보는전체시트리사이즈만했고원본픽셀마스크를덮지않았습니다. 생성물실루엣/광도차이가있을수있어완료판정은Claude실제HD재생에남깁니다.
- QA·공식audit·독립시각판정·HD실제재생검증은하지않았습니다. live/DB/library/코어/공유코드수정없음.

## 함께 찾았으나 보류한 IMG14882
actual미연결16×16 한조각을발견했으나전체원본시트에서는여러기체구성소스사이에걸친부분이며실제frame1080에는캐릭터컷인이겹쳐부위역할을확정하지못했습니다. 얼굴/허리등으로임의완성하지않도록제작보류. ../source14882_full_reference.png 및source14882_whole_native_context.png와원본계약을보존했습니다. 전체기체자세문맥확보뒤제작해야합니다.

| cell | source box | actualRGB | indexhash |
|---|---|---:|---:|
| 0 | [0, 0, 32, 32] | 4043128670 | 1289045930 |
| 1 | [56, 0, 16, 16] | 513362723 | 2028335207 |
| 2 | [24, 0, 32, 32] | 178227639 | 329000483 |
