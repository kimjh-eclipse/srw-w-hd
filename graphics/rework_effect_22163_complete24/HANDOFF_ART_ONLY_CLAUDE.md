# Claude 검증 이관 후 그림 후보 추가

## 역할/수정 상태

사용자지시에따라새실재생·공식audit·독립QA는수행하지않았다. cachedOBJ의3공유소스파일은이전완료분인수후추가로쓰지않았다.새공유코드수정없음.live/library/DB/defaultDLL/EXE변경없음.

## 추가 그림

균일한cyan평면을출력자체에서얻으려고imagegen을한차례더호출했다.참조는full_reference_palette0.png이며프롬프트에'flat vector-style raster/palette mask','RGB189,255,255','fully opaque','no gradient,texture,lighting','all cyan regions identical'을명시했다.

- 원출력: flat_cyan_retry_generated.png
- 가공: candidate_cyan_flat_retry.png (768×256),생성자체알파만미세찌꺼기정리/리사이즈,RGB코드칠하기없음
- 선택용두벌패키지: candidate_complete24_flat_retry.png (768×512)
- 계약: complete24_flat_retry_contract.json,기존24개와동일실제hash/index/palette/좌표계약
- 아래white벌은이전에별도생성해복원완료한full_candidate_white.png를유지했다.cyan을재색칠한white가아니다.

새white벌도독립생성했으나왼쪽흰fill투명구멍및계단형형태로출력되어rejected_flat_white_retry.png로보존하고채택하지않았다.

## 미해결/Claude 확인사항

새cyan은윤곽이단순하고불필요한광택은줄었으나출력육안상큰면의아주작은명암/색변화가완전0이라고장담할수없다. 생성후RGB를같은색으로채워검사를통과시키는작업은하지않았다. 기존24후보를덮어쓰지않았으며추가선택지일뿐이다.

현재메인등록대상은기존candidate_complete24.png다.새retry를교체채택할지는Claude가실제조립/실행에서비교해야한다.두파일을동시에설치하면안된다.채택하면같은24개모두다시굽기필요.

Claude검증fixture:
`test_current/combat/named_attacks/unit_299/mechanical_cutin_141.state`

- +55: cyan edge+fill4개,중앙직사각음영/내부절단선확인
- +56: white edge+fill4개,투명구멍/회색면/절단선확인
- +54:가느다란선/수평쐐기/준비전상태
- 180frame전체에서24개각실제HD등장/준비후hold/vanish/UI앞뒤확인

기존실제OAM계약/원본조립/cachedAPI결과는HANDOFF_COMPLETE24_AND_API.md에있다.추가retry는이문서작성시점에서검증미실행이다.
