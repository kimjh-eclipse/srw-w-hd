# #92815 어두운 연기 안의 밝은 초승달 제거

- 실제 원본 raw/index/full16 팔레트와 작업 시작 당시 사양 SHA를 보존했습니다.
- 원본 계약: `source_contract.json`. 원본 시각 참고: `parent_native.png`. 비교: `source_installed_pair.png`, `source_candidate_pair.png`.
- 인계 입력: `candidate_packet.json`. 계약·그림·원본·생성 원천의 4개 SHA와 작업 시작 사양 SHA를 넣었습니다.
- 미세한 분리 조각의 위치/크기와 모서리 굴곡이 원본과 맞는지 확인이 필요합니다. 첫 출력은 픽셀 계단을 그대로 재현해 제출에서 제외했습니다. 선택 출력은 자체 생성된 부드러운 윤곽이며 원본의 단색 어두운 면을 유지합니다.
- 생성 원천은 내장 imagegen으로 새로 그렸으며 `generated_selected.png`에 보존했습니다. 원본 RGBA/알파 전사, 알파 문턱 삭제, 중앙 파일 변경은 하지 않았습니다.
- 공식 검사·굽기·실재생은 실행하지 않았습니다. 연결·판정은 Claude 대기입니다.
