# 격룡신374 무장1488 실제 주황 상태 374_90

현재: 소스 확정·그림 후보 준비. 실제 HD QA는 Claude 담당.

- candidate_atlas.png / native_atlas.png / install_contract.json 2개 / provenance.json. 실제 source색 주황/금색 그대로. ordinary 녹청 기체색 완료로 세지 않음.
- fixture `test_current\parts\native_weapon_source_374_1488\unit374_weapon1488_source.state` +90, OAM [0, 1]. 실제전체원본문맥 test_current/parts/actual_mechanical_pose_374_90/whole_native_context.png.
- +90에서는기체/초상화가따뜻한주황이지만BG는우주색. 일반기본색/조명원인은판정하지않고실제팔레트상태로만제작. phase_only 후보임.
- +145 OAM13은16x8(84 native가시픽셀)로기존 min256 source scan5에서빠진 실제작은기계부품. tiny라는이유로제외하지않고추가하여6계약. +150 OAM1/8은+145두원본과동일하므로추가생성하지않음.
- 각부품 자체 생성alpha. 첫생성배경의반투명헤이즈는imagegen배경제거edit로교정(프로그램색삭제/원본alpha스탬프아님). 기하정렬은native bbox만사용. 전체6 prepare메모리nonempty, 독립QA/HD replay없음.
- 알려진위험: 원래성분과생성장갑면/절단면·좁은구멍·강조색차이가능. 따뜻한조명phase를일반RGB기본색/전체무장완료로해석금지.
