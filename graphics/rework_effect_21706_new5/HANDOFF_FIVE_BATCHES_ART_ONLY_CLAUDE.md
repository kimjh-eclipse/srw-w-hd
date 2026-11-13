# 후속 5개 그림 묶음19계약 — Claude 검증 대기

## root 설치/굽기 대상
|canonical IMG|계약|native크기|PNG크기|후보|
|---|---:|---|---|---|
|22530|5|56×64|224×256|candidate_22530.png|
|22618|1|32×64|128×256|candidate_22618.png|
|21706|5|184×64|736×256|candidate_21706.png|
|21758|3|192×32|768×128|candidate_21758.png|
|21006|5|72×80|288×320|candidate_21006.png|

각 `new_candidate_<IMG>_contract.json`. 합계19개 고유cached RGB 계약이다. 새그림5묶음이며alias리소스까지중복계산하지않는다. 현재19개모두live exact에없음(`existing_at_handoff.json`생성시점).

- actual cached OBJ의 index_pixels, indices_sha256, actual16색팔레트, RGB/indexhash, OAM속성/좌표/변형/engine, state/frame을보존했다.
-19/19모두rawindex+actual15bitpalette에서RGB/indexhash를독립재계산하여캐시해시와같음. 이는제작입력정합이지그림품질판정아님.
- 각candidate4배와native크기/maxA≥16/근접빈그림배제 확인. 기존공유 `prepare_texture`를메모리atlas+NullCache로19개모두실제로호출해준비후그림유지. 성분제거모두0,최소준비지원면적비0.740. `prepared_presence_report.json`. live/DB/cache쓰기없음.

## source alias7개 취급 — 소유IMG 단정 금지
-22530 신규5개와22496 신규5개는w/h/raw index bytes/실제사용palette색/actual RGBhash가모두같은계약이다.
-21706중2개와21855신규2개도같은관계다.
- root지시대로같은실제계약에는동일한자체새그림을한번만그렸다. 다른기체의색변형그림을재사용·재색칠한것이아니다.
-7개에는 **resource=None, source_owner_confirmed=false, source_candidate_matches, source_owner_note**를명시. source_x/y및canonical IMG는원본그림제작참조위치일뿐실행중업로드IMG소유의증거로해석하면안된다.
- `source_alias_equivalence_proof.json`: 두원본후보의동일근거. 실제색이같아한RGB binding으로모두연결되므로22530/22496또는21706/21855양쪽을별도중복등록하지않는다.
- 단일source로새로확정된나머지는22618=1,21706=3,21758=3,21006비평면=5,총12개다.

## exact state/frame
계약별frame이최종근거다. 대략다음원본재생입력에서채집했다.
-22530/22496: unit413 weapon1613 frame1560.state 부근의자주/검정작은먼지조각.
-22618: unit413 weapon1613 frame1080.state 부근의흰색/민트가장자리큰곡면조각.
-21706/21855: unit140 mechanical_cutin168.state 및같은그룹unit141/142/143/145/146,황금타격광/빨강먼지/회색연기조각.
-21758: unit413 weapon1610/1613 frame360.state 부근의흰핵·옅은청록빔section.
-21006: unit232 mechanical_cutin133.state의황색beam조각.

## fade54와미제작평면 보류
-20966/19887에서나온54신규계약은양쪽이같은계약이며actual팔레트46종이다. **고유index모양은4종**이고각44/4/4/2색단계계약이다. 앞서2형태라고잠정말한것은틀렸으며4종으로정정한다.
- `fade_20966_19887_contracts.json`에actualstate/frame/팔레트/index모두보존. 그림54개를억지로반복생성하지않았고,기존4형태와의연결·밝기팔레트처리는Claude런타임검증큐로넘긴다. source소유IMG는단정하지않는다. 이54를이번19완료숫자에더하지않는다.
-22618/21758의각2평면및21006의13평면은uniform index배열이거나원본소유를구분할수없는평면이라제작대상에서뺐다. 원본알파/색으로코드채우지않았다. flatfill을조용히해결완료로세지않으며별도nativefallback/소유확정이필요하다.
-19999actual1개는기존연결이므로보존. 보유한실제fixtures밖의무장/자세가완료됐다는주장없음.

## 그림위험 / Claude 확인
-22530작은먼지는원본보다곡면/문양이과장되었고작은점은둥글게생성됨. alias두source모두실제색과맥락확인.
-22618 민트edge폭과커다란whitecore곡률이원본과정확한지확인. 원본cut면에생성선이추가되지않았는지도확인.
-21706 황금star의spike수가원본보다늘어난부분과연기hole/회색면의변형. native색위치는실제팔레트기준이지만그림품질정상판정아님.
-21758 큰빔의가장자리/흰면밴드와두section이맞닿는절단면에선이생기는지확인.
-21006 첫출력이금속장식같아사용하지않고flat2D로다시생성했다. 최종도약간의노랑gradient/edgeband가남아원본의단순한면과다를수있다. 개별crop의연속면을확인해야한다.
- 전체준비성분제거0과alpha존재는실제전투의레이어/가림/로딩/진동/색변형/화질을보증하지않는다. 실제후보재생/독립QA는하지않았다.

## 생성·후처리
Built-in imagegen transparent mode. native reference를입력으로각효과별새로그렸다. 공통프롬프트는원본좌표/형태/큰빈공간유지,black투명,밝은핵불투명,원본색영역유지,cut면선금지,추가particles/glow/mist금지,도트계단은smooth연속선으로이다.21006은금속/3D/bevel/윤곽선금지와flatpale-yellow면을추가했다. 원출력파일은 `generated_<IMG>_0.png`,생성파일명은`prepare_candidates.py`에있다.

생성RGB/alpha만사용했고native RGB/alpha stamp나실행필터수정은없다. 자체생성alphathreshold/min3/max3와nativebbox위치/크기맞춤만했다. sourcealias7개의메타데이터보존은`annotate_provenance.py`후처리에서이루어지므로producer재실행시반드시다시실행한다.
