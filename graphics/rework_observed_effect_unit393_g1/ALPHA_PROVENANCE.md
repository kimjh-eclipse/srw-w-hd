# Unit393/w1559 FX 후보 group1: 노랑원형/반원광선7

- 실제 원본은 `test_current/parts/native_weapon_source_393_1559/unbound_now.json`의 rendered_obj_cache. actual raw index bytes, 전체 실제palette16색, RGBhash,indexhash,크기, OAM속성/좌표/변환, state/frame을 각 계약에 보존. 대표 `test_current\parts\native_weapon_source_393_1559\unit393_weapon1559_source.state` +545. MMU source/PLT기본색 추정 사용 없음.
- 7신규기본 raw도형 계약, 실제palette1. 원본40 FX실계약 중 고유raw37을4그룹으로 제작, 같은raw 다른3색변형은 `unit393_1559_input/fade3_source_base_pairs.json`에 source/base그림과 state/frame페어로분리. 그3은 새그림/완료수제외. 기계/보라역할불명 source_contact index41/42 등은제외.
- resource=None/owner_confirmed=false. 원본IMG 소유미확정이며 x/y 및 source_x/y는 가상40셀생산좌표, 실제IMG좌표가아님. red 일부는22419/22420 rawalias가확인되지만소유단정없음. raw/실제색이동일한사각은 중복제외하며 다른기체그림/다른색재색칠 안함.
- candidate.png [800, 320], native [200, 80], SHA `e8e66429e99ee039cb98b4bb5f7864e45ea188bb51bd07e248bb1bb336b4d8da`. 최신 live exact/indexed 중복0, 실제 인수 때 root재대조. actual RGBhash 원본재계산전부일치. native/cache별Source계약과그림 생성provenance 보존.
- 실제pal별자체새생성1장,자체RGBA/alpha만 사용. 생성cell alpha>=32 bbox는 affine 위치/크기등록에만사용하고 전체cell RGBA를 변환해 OAM사각에그림. alpha를32로threshold/이진화하지않음. 원본alpha/RGB stamp,타생성alpha공유,코드색채움 없음.
- prepare7 모두 maxA>=16/support>=.1, nearblank0. 이생산검사는 누락그림/해시/빈출력방지만이며 실제HD정상 QA아님. 원본/후보gray합성쌍 native_candidate_comparison.png와 candidate_on_gray.png를 우선볼것. 투명PNG raw RGB의밝은흔적만으로 실제fringe존재라판단하지말것.
- 알려진한계/Claude: 첫 금속고리/빈중앙을 채운 출력은 rejected_*로 보존하고 미사용. 최종은 자체 새 navy 평면곡선 생성→navy배경제거. 최종 gray 합성에서 내부 빈중심과 선사이 틈 보존. 곡선수/두께/간격이 원본과 완전히 같지 않고 일부 brown색 비율이 달라 실제 효과 강도/색영역 Claude 확인 필요. prepare분리성분제거는production_report에보존. 실제가림/UI순서/회전/부분연결/동적pal색은Claude실재생대기.
- 라이브/library/DB/core/EXE수정과 독립audit/실제HD재생을 하지않음. builtin imagegen사용, 입력ref/native/원생성/실패출력 보존.
