# 생성 알파 근거

builtin image_gen transparent_background=true로새원천3개를생성했습니다. API/CLI fallback없음. generation_sources.json/sha256.json에원천을고정했습니다. 각파편을filled opaque core로새로그렸으며배경/주변halo는투명하게요청했습니다.

alpha>=128은생성성분의bbox측정과개수검사에만사용했습니다. 출력알파를문턱삭제/이진화하거나morph처리하지않았습니다. 생성자체RGBA를crop/resize해원래각성분bbox에놓았습니다. 원본mask/RGB/알파전사/픽셀별색주입/타팔레트alpha차용없음.

93451첫생성은연결조각이갈라져재생성했습니다. 출력알파조작으로검사를맞추지않았습니다. 최종source6/8/7성분과native-grid footprint를유지하고원본의약한알파가아닌새불투명재질의폭을확보했습니다. 원본소유자는미확정그대로이며생산검사를공식QA로표시하지않습니다.
