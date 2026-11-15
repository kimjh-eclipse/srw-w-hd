# 생성 알파 근거

builtin image_gen transparent_background=true로 각 target에 별도 새 PNG를 생성했습니다. API/CLI를 사용하지 않았습니다. generation_sources.json에 내장생성 원천 파일명, sha256.json에 파일SHA를 고정했습니다. 원본은 참조/좌표/측정 입력으로만 사용했습니다.

94300,94313은 생성 RGBA 전체를 target4배 크기에 resize했습니다. 94304,94317은 생성 자체성분 bbox crop/resize로 원래 채워진 폭/높이를 등록했습니다. 94305는 원본6성분의 bbox 위치와 각각 대응하는 생성6성분 자체RGBA crop/resize입니다. alpha>=128은 생성 성분 bbox 측정만 하며 픽셀 alpha를 0으로 삭제하거나 이진화해 출력하지 않습니다. 알파 채널은 생성된 연속값을 보존하며 crop/resize 외 조작하지 않았습니다. 원본 mask/RGB/alpha 전사, morphology 또는 색상 치환 없음. 정상21개 RGBA와 binding metadata는 byte 비교를 통과했습니다.

manual_native_candidate_prepare.png는 회색 배경 합성이므로 PNG alpha0 RGB ghosts를 실색 또는 테두리로 판정하지 않습니다. 생산 preflight는 공식 시각QA 또는 재생검증이 아닙니다.
