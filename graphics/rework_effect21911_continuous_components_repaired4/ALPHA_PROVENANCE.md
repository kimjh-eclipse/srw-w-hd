# 생성 알파 근거

builtin image_gen transparent_background=true를 사용해4개원천PNG를생성했습니다. API/CLI fallback없음. generation_sources.json의내장원천과sha256.json의파일SHA로고정했습니다. 원본은reference/좌표/검사용으로만사용했습니다.

출력은생성자체RGBA전체가아니라각대응성분의own bbox를crop/resize하여원래bbox에등록한그림입니다. alpha>=128은성분bbox측정에만사용하며 생성픽셀을문턱삭제하거나이진화하지않습니다. 생성의연속알파를유지합니다. 원본mask/RGB/alpha전사,색변환,morphology없음. 실제작은분리성분의개수와위치를고정했습니다.

rawPNG alpha0RGB ghosts는회색배경RGBA합성에서실제로안보이는지확인했습니다. 특히분홍/빨강외곽잔여RGB를새그림의불투명외곽으로오인하지않았습니다. 그림사전검사와공식독립QA/게임검증은구분합니다.
