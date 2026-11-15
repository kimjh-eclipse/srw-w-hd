# 전함 연출 회색 파편 같은 ID 후보1

미검증 후보. 신규 완료 수 없음. 공식 검사·실제 재생은Claude담당이다.

설치installation_map.json/candidate_atlas.png/native_atlas.png. 후보SHA256 1af416475133f5f9e951e519dfabb2e491a8fbad530cf7c96bca39234c5eb0e5.

#93247 metadata93246의actualcached계약이다. source_mechanical_267_1103/source_pose.state +0 OAM9 (167,76),32×8. 실제full16색과hash/index/wh를보존했고resource=None이다. ROM확장추정이아니다. 그림은기계가아니라전함연출의회색파편FX다. 원본은7/5/8texel덩어리3개와1texel조각7개,총10분리성분27texel이다(native_component_layout.json). 실제사용회색은41/57/90/106이며다른색변형을빌리지않았다.

내장imagegen exec-975fd559-fde6-4f6f-a1c3-c2e9b52c9fcd.png로원래10성분배치/작은면을지킨새그림을제작했다. parts_generated_raw.png보존. 원본RGBA/alpha전사없고alpha문턱/침식/팽창없음. nativebbox는위치/크기정렬에만사용했다. 기존render/lookup/dynamicflags는보존.

root요청으로최종계약좌표의NullCache prepare뒤성분별존재를생산진단했다(per_component_prepare_presence.json). 모든10개원본성분bbox에alpha16이상paint가남았다. 큰3개ge16면적112/69/109,작은7개14/14/15/14/14/11/13픽셀,각maxalpha249~255. unattached paint 제거0/경계선수정0. DB쓰기없음. 이결과는각bbox에그림이남는다는생산근거뿐이며형상·색·정체가맞다는공식QA아니다.

위험: 작은한texel을둥글게그린면적·농도,세덩어리의명암/윤곽/정확한성분간거리차이는Claude판정대기. 기존3D바위같은표현을줄였지만native계단을부드럽게하면서일부형태가달라질수있다. 실제가림/시점/alpha해석은재생확인필요. 라이브/코어/DB/공식QA/물리입력변경없음.
