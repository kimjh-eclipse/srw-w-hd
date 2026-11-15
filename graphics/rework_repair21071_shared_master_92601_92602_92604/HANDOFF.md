# 21071 부모 상부8성분 곡선 띠 교정

92302와별개인21071 묶음입니다. 목표92601/92604와부모92602 총3개를 같은 own_master.png로 교정했습니다. source/atlas master[80,32,32,64]의상부32×32만새로그렸고, 하부기존그림과다른21개live바인딩은그대로입니다.

실제성분8개의 자리/폭/서로분리된간격을유지했습니다. 왼쪽작은3성분(2×3/1×2/1×1)도빠뜨리지않았습니다. 큰띠5개는새연속곡선과흰중심·청록면의연속색면으로그렸습니다. 팔레트 full16/BGR555/index raw/관측frame·state/source_box/atlas_box는flat계약에보존했습니다. native256×192/candidate1024×768정확4배입니다.

생성원천RGBA crop/resize와제한된자체geometry registration을사용했습니다. 가늘게생성된곡선은자체RGBA의행/열별alpha중심을따라두께1.1~1.5배만조정하여source bbox안에등록했습니다. 원본mask/alpha/RGB전사없이자체RGBA만재표본화했습니다. output alpha문턱삭제/형태학삭제는없습니다. author_config.json의own_geometry와authoring_area_notes.json에그림제작근거가있으며공식QA결과가아닙니다.

manual_comparison_gray.png는원본/이전/새그림입니다. 시작specSHA/네파일SHA는ready_candidate.json에있습니다. 위험: 작은점의HD세부이득이제한적이고, 곡선끝/청록과흰내부면의배치·두께는연속면으로근사하여차이가남습니다. 면적메모는상단개별성분의제작기록일뿐공식검사가아닙니다. 중앙쓰기/연결/굽기/공식QA미수행입니다.
