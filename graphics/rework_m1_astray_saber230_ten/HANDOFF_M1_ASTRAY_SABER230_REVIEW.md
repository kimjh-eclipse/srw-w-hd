# M1 아스트레이 +230 한 자세10종 미검증 제작후보

- 실제 native 메뉴 unit38/w160 +230, source_mechanical_38_160/source_pose.state +0의 cachedOBJ와 렌더된 OAM 계약입니다. palette0 기계13 OAM 중 existing3개를 보존하고 actual exact0인10종을 제작했습니다. actual indexed도없는9종 + 기존머리indexed 실제색재제작1종이며 신규누락10으로세지마십시오.
- 모든원본 index bytes가 IMG7893의사각형과동일합니다. actual15bit팔레트/사용색/attrs/wh/CRC와source자료보존,첫ROM일치가유일소유증명은아닙니다. 원본사각형교차0쌍이므로임의그림재사용/다른기체재색칠없습니다.
- 실제머리녹색눈·카메라와빨강V장갑을보존했습니다. 캐릭터일반인상으로노랑눈/금색뿔을넣지않았습니다. 작은빨강끝/sliver는전체머리로확대해석하지않도록했고 큰cell7은whole-native에서몸통·골반장갑문맥으로제작했으며 눈을새로넣지않았습니다.
- imagegen 내장도구3열4행새그림, 생성알파bbox정렬및자체alpha<64 RGBA0만적용했습니다. >=64 RGBA불변SHA/제거수는generated_alpha_cleanup_proof에보존. 원본RGB/alpha스탬프나색마스크사용없음.
- 위험: 머리V장갑각도·눈/카메라위치와cell7몸통면/접합, 셀5빨강분리삼각패널, 작은cell6암부sliver형태, 기존3장갑과의명암·선연속성은Claude가실제재생으로판정해야합니다. 생성자가일부장갑면을구체화했으며AA경계손실가능성도있습니다.
- 모든10후보가비어있지않고alpha최대160이상이며raw/palette/크기/사각형교차기계적확인만했습니다. 공식형태·색audit/실제HD재생검증은하지않았습니다. native/candidate_pose_production은OAM우선순위·역순·반전대로한제작조립자료일뿐전체HD완료주장이아닙니다.
- FX나타기체팔레트는범위제외,라이브/DB/코어/공유runtime변경없음. root직렬연결및Claude검증대기입니다.
