# 생성 알파 근거

builtin image_gen transparent_background=true로주요6개성분과작은성분시트1개를새로그렸습니다. API/CLI fallback없음. generated_component_0/2/3/6/8/9/small.png가생성원천이며generation_sources.json/sha256.json에고정했습니다.

source index0투명과index1검정불투명을구분했습니다. 회색배경RGBA합성으로생성black재질이실제불투명임을확인했습니다. 원본은참조이미지및성분bbox/팔레트/검사입력으로만사용했습니다. 원본RGB/alpha/mask를출력으로복사하지않았습니다.

alpha>=128은생성자체bbox측정에만사용합니다. 출력픽셀을삭제/이진화하거나morph처리하지않았습니다. 생성자체RGBA bbox crop/resize후원래성분좌표에alpha_composite했습니다. 작은1px검정재질만새생성시트첫셀의완전불투명내부crop을공유합니다. 원본shape mask로해당조각을그리지않았습니다.

17개원래성분은각각bbox등록을유지하며최종native-grid6/2/9성분을확인했습니다. 정상3개metadata/key/RGBA보존. 사전검사통과는공식QA/재생검증이아닙니다.

94102 추가재제작: generated_component_8/9.png를새연기원천으로교체하고,작은4성분은신규 generated_component_94102small.png에서자체RGBA crop/resize했습니다. 이전불합격블록형원천은rejected파일에보존했습니다.1px자체검정재질은유지했습니다.앞선94099/94101candidate crop은byte동일입니다.알파처리규칙변경없음.
