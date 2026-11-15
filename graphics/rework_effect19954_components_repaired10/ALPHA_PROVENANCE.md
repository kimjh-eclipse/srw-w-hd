# 알파 출처

2개 imagegen 자체생성 RGBA의 각 셀을 사용했습니다. 원본색/alpha전사·다른팔레트alpha차용·threshold·morphology 없음. A>=16은 생성 성분 위치 bbox측정용으로만사용합니다. flat material은 자체생성내부 RGBA를crop해사용하며 alpha253~254그대로보존,255강제채우기없음.
