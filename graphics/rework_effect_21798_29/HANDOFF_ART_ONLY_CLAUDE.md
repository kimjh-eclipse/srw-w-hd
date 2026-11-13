# 효과21798 실제 관측29개 새 그림 인수 (검증은Claude담당)

## 파일

- candidate_21798_29.png:768×512 RGBA,상하2실제팔레트각192×64의4배.
- candidate_contract.json:29개exactRGB/static/effect_part=True/resource=None. x/y는후보좌표,source_x/source_y는원본IMG좌표,실제팔레트/index/OAM/priority/fixture/frame포함.
- native_21798_29.png / native_candidate_comparison.png:실제원본색과새그림나란히보기.
- generated_palette0.png / generated_palette1.png:독립imagegen원출력.
- mechanical_production_checks.json:hash/크기/범위/원본index일치같은제작확인만.

공식audit/실제후보재생/독립QA는실행하지않았다. live/library/DB/defaultDLL/EXE/플레이어설정/공유소스변경없음.

## 실제 계약과 선정

fixture:
`test_current/combat/named_attacks/unit_19/mechanical_cutin_168.state`

기본코어cachedOBJ읽기API로렌더된OAM의정확index/palette/hash를직접수집했다.동일OAM의활성여부/화면내범위/캐시크기와실제OAM크기일치를확인해이전프레임cache혼입을피했다. 현재MMU의미래VRAM으로색을추정하지않았고PLT도추정하지않았다.

29고유RGB변형,실제팔레트2개(19개+10개). 최초보인offset은12,14,16,20,22,24,26,28,32,34,38,66,70,72. 모두rawindex가원본IMG21798의해당crop과일치했다. CAPI RGBhash와indexhash를기록rawindex/actualpalette로재계산해서일치assert했다.등록권장resource=None,actualRGBhash전용.

내용은분홍광선/가는직선궤적과노랑/주황타격광·폭발연속시트다.같은시트의29개를두실제팔레트한벌로묶어제작했다.다른기체/다른효과그림을빌려쓴것이아니다.

## 새 그림 방법

imagegen스킬built-in2회호출로두실제팔레트를각각새로그렸다. 1번은pale pink/ivory-yellow코어,2번은hot magenta/orange-yellow코어를직접참조했다.1번을재색칠해2번을만들지않았다.

프롬프트공통요구:3:1원본시트전체레이아웃동일,가는직선길이/각도동일,폭발/불꽃색영역동일,내부타일절단면외곽선금지,검은윤곽선금지,새분기/입자추가금지,실제투명알파.

prepare_candidate.py는생성원출력자체alpha만Min3/Max3으로미세찌꺼기정리한뒤4배해상도에리사이즈했다. **최종리사이즈후추가Min/Max정리는하지않는다.** 그렇게하면정상가는직선이없어지는것을제작미리보기에서발견해제거했다.원본알파찍기/원본색codefill/다른팔레트재사용없음.

## 알려진 차이 / Claude 확인 큐

완성판정이아닌그림후보다.폭발구름의둥근소용돌이가원본보다세밀하고각불꽃뾰족점개수·가는광선위치가약간다를수있다.폭발밝은영역크기와분홍광선외곽의알파프린지를특히확인해야한다. magenta는이효과의정상색이므로색이분홍이라는이유만으로키잔여로오인하면안된다.실제sourcepalette영역밖에튀는고채도잔여는별도로봐야한다.

Claude검증state:위unit19/mechanical_cutin_168.state
- +12/+14/+16:첫가는광선/초기두팔레트변화
- +20/+22/+24/+26/+28/+32/+34/+38:중간광선·불꽃조각
- +66/+70/+72:후반폭발연결과두팔레트밝은영역
- 전체180frame:29개각HD실제등장/원본유지·준비후held/소실/UI침범/전역flash보존검사

provenance_native_first_*.png는계약수집시원본화면이다.후보를실제로렌더한검증이미지가아니다.

## 인수 절차

root만29개라이브일괄등록→exact29재굽기.그다음Claude가재생/공식검사.이child는새실재생이나audit을하지않는다.
