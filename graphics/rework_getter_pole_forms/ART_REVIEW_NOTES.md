# 겟타 토마호크 연출의 청보라 막대형 파츠2형태 후보

제작·연결입력만준비했다. **판정/audit/실제HD재생은Claude담당이며이번후보에서실행하지않았다.** 라이브/DB/공유코드변경없음.

## 최종파일

- `candidate_atlas.png`:256×128 RGBA, native64×32의4배.
- `native_reference.png`:64×32, 실제OAM색원본. 후보와같은아틀라스배치.
- `generated.png`: 신규생성원본 `exec-0b2cbfbb-b2ed-46b2-b5cf-1dab70a2a440.png`.
- `install_contract.json`:2개,전체rawOAM기록·16색·hash/index/encodedindices/spec좌표포함.
- `source_candidate_contact.png`:원본/후보자료. `mechanical_input_check.json`:크기·연결입력만점검.
- `pure_native_context_60.png`, `pure_native_context_90.png`:이전에확보된순수원본전체장면참조를복사했다. 이번에새HD재생검증을돌린것이아니다.

## 정확한대상·변경범위

| cell | 실제원본 | index_hash | RGBhash | 후보native좌표 | 원본관측 |
|---|---|---:|---:|---|---|
| 0 | IMG14461/14485 [120,56,8,16] | 1104042560 | 3710864711 | [0,0,8,16] | getter offset56~59,8 appearances |
| 1 | IMG14461/14485 [48,128,32,16] | 3563099472 | 2684431255 | [32,0,32,16] | offset90~126,86 appearances |

두개모두이전rawcapture에서미연결로관측된정확RGB다. 기존91896양날도끼머리와는다른새바인딩대상이다. 21869별빛·22053불꽃·22163과겹치지않는다. 같은IMG전체완료가아닌관측두파츠다.

8×16의indices는IMG14487/14916 [120,88,8,16]에도동일해서source_alternatives에보존했다. 실제업로드원천을한개만단정하지않는다. 원본바이트일치는상위 `source_contracts.json`·`find_sources.py`에서확보했다.

실제16색BGR555는PLT14460 bank2의16칸과동일하다. bank0주황기체팔레트를사용하지않는다. 두개는어두운청보라·연보라하이라이트의같은색한벌이다.

## 역할과제작

전체원본장면과crop를함께참조했다. 겟타가양손을올리고토마호크연출이겹치는구간의가늘고긴청보라막대형그림이다. **토마호크축/축의잔상후보**로기록하며그것이기체얼굴·허리라고가정하지않았다. 실제역할세부는Claude가원본순서와함께판정한다.

처음부터전체무기를새로그리지않고실제두사각형이담는부분만그렸다. 짧은형태는약간휘어진세로막대,긴형태는왼쪽아래→오른쪽위의가는대각선막대다. 끝은다른부분과이어질수있어새화살촉·장식고리·끝캡·불꽃을추가하지않도록요청했다.

생성그림두반쪽을원본지원bbox로배치·4배축소했다. 원본RGB/원본알파를출력에찍지않았고다른그림재색칠도아니다. 두형태는원본이미지에서서로떨어진위치라겹침사각형은없다. 동일팔레트/화풍의한벌이다.

## Claude확인할위험·프레임

- 원본의한두texel짜리밝은점들이새그림에서는길게이어진면으로보일수있다. 가는축폭과어두운외곽이원본보다굵어지는지확인.
- 짧은형태의아래꺾임·원본빈틈이새연속그림에서채워지는부분이있을수있다. 동작중단절/잘못된새연결로보이는지확인.
- 긴형태의양끝이무기다른파츠/움직임선과이어질때어긋나지않는지. 새막대가무기전체또는빔이라고과도하게보이지않는지.
- OAM반전/중복사용을원래대로적용해야한다. 두개설치가다른무기91896의정상접합을보장하지않는다.

Fixture: `test_current/combat/getter_cutin.state`. Claude용프레임56/57/59와90/110/126,추가로207/234의완성무기연결문맥.

검증명령예시:
`python -X utf8 scripts/verify/verify_runtime_path.py --state test_current/combat/getter_cutin.state --frames 300 --pure-native --save-frames 56 57 59 90 110 126 207 234 --track-atlas <새설치atlas명> --name getter_pole_claude_review`
