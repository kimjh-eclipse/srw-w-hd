# 서펜트 총구/탄도 FX 2 제작 인계

- 원본 이관 `test_current/parts/borrowed_shape_rework/serpent_cannon530_missing/contract.json` cell0/1. 기계가 아니라 실제 총격 노란 총구광과 가는 탄도 흔적. source_mechanical_9_31/source_pose.state +0(+530 위치의 보존 state), 실제 OAM3/5 및 반복10/12. 팔레트0 actual 전체 보존.
- hash288090733 8×8 /1909023138 16×8. IMG19645(24,16)/(32,8) raw byte 일치 직접 재확인. live exact/indexed 미연결 확인. 다른색 그림 재사용 안 함.
- 신규 자체 imagegen 2구역을 한 sheet로 제작. native48×16, candidate192×64, SHA `cb82196e89a0914f5f4f48fb2974c0ce5a6f519b5ba688ad69c27ed7cca62589`. source_x/y 원본좌표 보존, x/y는 packed0,4 /24,4. 두 source 영역 교차 없음. 작은 단색-like 유효 픽셀/끝 dash도 포함.
- own generated alpha 그대로 유지. 생성 alpha>=8 bbox는 위치 등록에만, 전체RGBA affine. native RGB/alpha stamp/코드 색채움 없음. 원본 팔레트에 흰색이 없어 흰 빛을 발명하지 않고 yellow/gold만 유지.
- prepare2 모두 maxA255, empty0, 제거성분0. 실제 HD 재생/독립 QA는 안 함. Claude는 얇은 탄도/조각 dash 누락, 총구광의 원본 clipped 끝과 실제 등록크기 확인. 후보가 원본보다 약간 부드럽고 명도 질감이 있음.
- live/library/DB/core 미변경.
