# unit250/weapon1026 발사광 6 계약 제작 인계

- 입력은 동료가 보존한 `unit250_actual_unknown.json`의 rendered OBJ cache + 실제 OAM. source state는 `test_current/parts/native_weapon_source_250_1026/unit250_weapon1026_source.state`, +290/+295. engine0 OAM/우선순위/변환은 계약에 보존.
- IMG21758 raw crop과 6개 모두 byte 동일. 원본 실제 팔레트 1개, 고유 raw 6개. 원본 IMG/PLT 기본색으로 actual을 추정하지 않음.
- candidate.png 768×128/native_combined.png 192×32. 4배 신규 자체 생성 그림. `new_candidate_contract.json`은 static/effect_part=true, resource=None 보수 설정.
- 생산 prepare 6개 모두 maxA255, empty0; 원본 RGB hash 계약 일치. 원본 RGB/alpha stamp와 native fill0. 1개 crop의 기존 prepare 분리 성분 제거1은 별도 Claude 확인 필요.
- 생성 alpha는 전부 보존. 단 own alpha1의 아주 먼 미세 흔적 때문에 본체가 과도하게 작아지는 위치 문제를 피하려고 own alpha>=8 bbox를 **좌표 정렬에만** 사용. alpha 자체를 이진화/삭제하지 않고 전체 생성 이미지를 affine으로 이동·축소하여 대상 캔버스로 그림. source alpha는 bbox 위치/크기 참조만.
- 알려진 위험: 원본보다 긴 불꽃형 미세 선과 흐름 음영이 추가됨. 색 영역/회전/크기와 준비 후 1개 제거 성분, 얇은 광 손실 여부는 Claude 실제 재생 판정 대기. 생산 존재 확인은 실제 HD 정상 판정이 아님.
- 라이브 라이브러리/DB/코어/EXE/독립 audit/실재생은 수정·실행하지 않음.
