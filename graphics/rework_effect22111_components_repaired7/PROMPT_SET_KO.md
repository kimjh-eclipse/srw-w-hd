# 생성 지시/출처

imagegen 스킬 기본 내장 도구 사용. 모든 원출력은 이 폴더에 보존했다.

1. 실제 밝은 불꽃6/암적색1을 원본 위치·성분·폭·팔레트로 그리도록 요청. 처음 도트블록 해석은 rejected_block_bright_raw.png(exec-58140291-c5a2-4e4f-b659-9ab9078aac7a)/dark(exec-c694fbec-2178-4a65-b662-e340f1bebf59)로 거절했다.
2. 기존 타일 경계를 없애고 smooth cel화하되 같은 성분/지지면/구멍/실제색을 유지. generated_bright_raw.png(exec-c9ffbeef-960e-4268-8e5c-a96cf70ba020), generated_dark_raw.png(exec-4718505f-df6c-453e-9882-ff208e15307b). 밝은별92530/열린불꽃92539/암적색92542만 이 후보를 사용한다. 나머지 원호/파편은 아래 성분별 생성으로 대체.
3. 원본36성분을 같은bytes/전체palette로13종 분리. 4×4 시트13개를 실제 단순 재료/가지 네트워크로 새로 그림. generated_components_raw.png(exec-4fcf0ca2-c4bd-49ee-8dc2-544b02368679). 셀1/5는 얇은가지 네트워크이며 큰 별폭발이나원형구름으로 채우지 않도록 요청. 다른 단색 작은 셀은 원래 material색 유지, 추가 장식/윤곽선 금지.
4. 중앙 두 네트워크만 수정: 전체 가지 위상/끝/폭/빈틈/색 보존, 사각타일 seam·검은 outline 없애고 smooth한 좁은 ribbon에 가깝게 새로 그림. generated_network_two_raw.png(exec-f96a8202-6760-420a-96c5-c51db337b609). 이 두 셀 외5개 후보 RGBA 불변 증거 보존.

모델 출력 외곽의 실제 generatedalpha는 지우지 않았다. 원본 nativealpha/RGB 출력전사·키색 후칠·강제구멍닫기 없음. 정렬/공유 위치·사용 source/관측 구분은 계약과 generation_alignment_provenance.json.
