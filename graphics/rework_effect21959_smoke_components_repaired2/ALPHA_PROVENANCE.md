# 생성 알파 근거

builtin image_gen transparent_background=true로주요6개성분과작은성분시트1개를새로그렸습니다. API/CLI fallback없음. generated_component_0/2/3/6/8/9/small.png가생성원천이며generation_sources.json/sha256.json에고정했습니다.

source index0투명과index1검정불투명을구분했습니다. 회색배경RGBA합성으로생성black재질이실제불투명임을확인했습니다. 원본은참조이미지및성분bbox/팔레트/검사입력으로만사용했습니다. 원본RGB/alpha/mask를출력으로복사하지않았습니다.

alpha>=128은생성자체bbox측정에만사용합니다. 출력픽셀을삭제/이진화하거나morph처리하지않았습니다. 생성자체RGBA bbox crop/resize후원래성분좌표에alpha_composite했습니다. 작은1px검정재질만새생성시트첫셀의완전불투명내부crop을공유합니다. 원본shape mask로해당조각을그리지않았습니다.

17개원래성분은각각bbox등록을유지하며최종native-grid6/2/9성분을확인했습니다. 정상3개metadata/key/RGBA보존. 사전검사통과는공식QA/재생검증이아닙니다.
