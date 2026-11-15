# 21640 연속경계 생성 알파 근거

builtin image_gen transparent_background=true로 ID마다 별도 새RGBA를 생성했습니다. API/CLI fallback 없음. smooth_generation_sources.json과 smooth_sha256.json에 원천을 고정했습니다. 원본은 참조이미지·원래bbox·측정입력으로만 사용했습니다.

알파>=128은 생성그림의 own bbox 위치 측정에만 사용하며 원천픽셀을 삭제하거나 이진알파를 출력하지 않았습니다. 측정한 생성자체RGBA bbox를 원래bbox에 crop/resize하여 연속알파를 보존했습니다. 원본알파를 마스크로 적용하지 않았습니다. native RGB·alpha 전사,색상치환,형태학연산 없음. 정상8영역은 기존 자체그림 그대로입니다.

94480의 가느다란 왼쪽다리초안과94482의외부glow초안은 시각불합격으로 따로보존하고 새로생성했습니다. 불합격알파를 문턱삭제하여 통과시키지 않았습니다. 최종새그림은 기존계단후보를 흐린 결과가 아닙니다. 회색RGBA합성 수동비교에서 연속곡선과채워진폭을 확인했습니다. 공식QA/재생검증과 구분합니다.
