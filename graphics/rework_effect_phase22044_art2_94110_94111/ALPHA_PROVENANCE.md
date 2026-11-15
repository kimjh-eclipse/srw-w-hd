# 자체생성RGBA근거

builtin image_gen transparent_background=true로94110두덩어리와94111먼지/분리조각을새로그렸습니다. API/CLI fallback없음. generation_sources.json/sha256.json에원천을고정했습니다. 원본은참조/fullpal/좌표측정에만사용했습니다.

모든출력은생성자체RGBA crop/resize와alpha_composite입니다. 94111안쪽작은곡선은같은main원천에서crop한자체생성조각을source feature3×3좌표범위에제한등록했습니다. 원본마스크/색/알파전사,다른팔레트차용/자동재색칠/문턱삭제/morphology없음. alpha>=128은생성성분bbox측정과저작배치확인만하며실제출력알파를삭제하지않았습니다.

원래성분수2/3과정상5개를보존했습니다. 그림저작과공식검증역할을분리하여prepare/공식검사/설치/굽기는실행하지않았습니다. Claude독립검증대기입니다.
