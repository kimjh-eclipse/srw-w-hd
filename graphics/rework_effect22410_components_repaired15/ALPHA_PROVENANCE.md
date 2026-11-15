# 알파 출처

모든 새 영역은 imagegen 자체 RGBA입니다. 원본 mask/RGB 전사, morphology, alpha threshold 삭제 없음. 밝은 중심을 지워버린 배경 추출은 쓰지 않았습니다. 92487 마지막 출력은 자체 생성본에서 잘못 추가된 외부 흰안개만 imagegen으로 다시 추출한 판본이며 원본/다른팔레트 alpha 공유가 아닙니다. bbox A>=16은 위치 측정용일 뿐 출력 alpha는 그대로 변환했습니다. 정상4 및 target밖은 기존 그림을 보존했습니다.
