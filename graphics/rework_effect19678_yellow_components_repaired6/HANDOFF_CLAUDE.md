# 19678yellow58 문제7 중 후보6 / 기술보존1 — Claude 검토대기

## 범위와수량
문제7개중93510은정상부모93493의동일raw/full16palette 하위영역입니다. 구운child와부모crop는AA끝18픽셀차이뿐이고source격자면적.357/미칠.643지표가둘다같았습니다. 실제입자소실인지타원HD의엄격면적문제인지미확정이므로새그림/완료수제외하고기술보존했습니다. normal_parent_child_readonly_comparison.json/그림참조.
후보는문제6개:독립부모4(93486/93489/93496/93498)와동일새parentRGBA crop을공유하는문제child2(93490/93502). 미관측후보0,actual관측6입니다.

## 정상51보존/93503접합
정상51의메타/기존atlas/key는변경하지않았습니다. 문제부모93496의오른쪽16x8은정상93503과동일raw/fullpal입니다. 처음정상의존재연결을검토했으나root지시에따라미실행하고기존4배자체HDRGBA를candidate에서byte그대로보존했습니다. normal93503_preservation.json의기존/후보RGBA SHA가같습니다. 원본성분중x208경계를가로지르는것은0개라끊긴입자접합은없습니다. parent93496_normal93503_seam.png에서왼쪽새성분/오른쪽기존성분과원본을대조하십시오.
정상52(원래51+보류93510)와대상밖영역픽셀은기존과같습니다. 부모93496의오른쪽정상보존때문에그부모전체source면적비는.757/IoU.757로남습니다. 왼쪽새child93502는면적1/IoU1입니다. 이잔여지표를해결완료로보지않으며최종판정은Claude대기입니다.

## 그림과alpha출처
원본4parent에는17성분이있고2panel17개자체motif를제작했지만정상93503안의3성분은신규출력미사용,기존그림을보존했습니다. 실제새후보에사용한새원본성분은14개입니다. 작은사각입자와filledbeam strip이빈그림으로바뀌지않도록자기생성RGBA의폭과채워진영역을유지했습니다.
원본alpha/RGBstamp·다른팔레트alpha차용·threshold/morph삭제없음입니다. A>=16은자체생성bbox측정용. flat2material은자체생성내부RGBA crop(253~254alpha그대로)이고255강제칠하기없습니다.

## 입력/좌표/메모리준비
actualcached6개의raw/w/h/indexhash/전체16색BGR555/RGBhash일치확인. source_candidate_palette_integrity6.json/normalized installer안에정확state/frame/OAM보존했습니다. sourcebox와candidatebox를분리했고candidatebox/spec는기존live좌표그대로입니다.
normalized installer좌표로NullCache prepare6를실행,기존좌표직접준비와RGBA모두일치/maxA255/fill0입니다. 부모93496이외5개는source격자IoU/면적비1입니다. 색음영차이는colour_production_comparison6.json에보존했습니다. 공식audit/HD실재생판정없음입니다.

## 인계
ready_replacement6.json / normalized_installer_contract6.json / candidate_atlas.png / native_atlas.png / native_prepared_pairs6.png.
새atlas effect19678_yellow_components_repaired6으로same6ID만교체하고정상93503포함51및보류93510은기존ID/oldatlas/key그대로두십시오. root설치·굽기/Claude QA대기,공유코드/live/DB/EXE/Git변경없습니다.
