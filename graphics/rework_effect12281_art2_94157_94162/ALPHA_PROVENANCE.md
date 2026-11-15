# 자체생성알파근거

builtin image_gen transparent_background=true로94157대각띠와94162쐐기를각각새로생성했습니다. API/CLI fallback없음. generation_sources.json과sha256.json에원천을고정했습니다. 원본은참조/좌표/fullpalette계약으로만사용했습니다.

alpha>=128은생성자체bbox측정에만사용하며출력alpha를삭제/이진화하지않았습니다. 생성RGBA crop/resize만으로원래native bbox에등록하고alpha연속값을보존했습니다. 원본mask/RGB/alpha전사,팔레트그림차용/자동재색칠,morphology없음. 첫94162계단형생성은폐기근거로보존하고새연속쐐기로재생성했습니다.

두source는한색민트실루엣이므로새질감HD이득으로계수하지않습니다. 정상44RGBA/metadata보존. 이번역할은그림/계약이며prepare·설치·굽기·공식검사·재생은실행하지않았습니다.
