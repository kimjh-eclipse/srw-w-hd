# 21427 문제7 중 독립후보3 / 기술보존4

## 범위
observed_effect_21427_twentytwo의독립문제93789/93790/93791만자체새RGBA로교정했습니다. 정상15는기존메타/atlas/key와candidate영역픽셀그대로보존했습니다. 정상부모와동일그림인4개는아래기술보존으로분리하고새그림/완료수에포함하지않았습니다.

- 93795↔정상93794:raw/full16pal동일,구운crop대비14AA끝픽셀차이뿐,부모와source면적/미칠지표동일.
- 93803↔정상93802:raw/full16pal동일,구운cropRGBA완전동일.
- 93804/93809↔정상93806:raw/full16pal동일,구운cropRGBA완전동일.
작은회색입자들은보존돼있으며새부모와다른그림으로만들면불일치가생길수있습니다. 최종기술판정대기이며normal_parent_child_readonly_comparison.json/그림에근거있습니다. 추가부모93799도93795를포함하지만이미정상93794비교로같은원본영역을확인했습니다.

## 신규그림3
원본회색각진파편/두떨어진덩어리의위치·굵기·회색명도를유지했습니다. 원본도형을돌/연기구름/타원으로재해석하지않았습니다. 자기생성RGBA3개만bbox등록,원본alpha/RGB전사·threshold/morph삭제·다른팔레트alpha공유없습니다. A>=16은생성bbox위치측정용입니다.

## 입력·좌표·준비·preflight
실제cached3개rawbytes/w/h/indexhash/전체16색BGR555/RGBhash일치확인,정확sourcefixture/frame/OAM계약은normalized_installer_contract3.json에있습니다. sourcebox와candidatebox분리,후자는기존live좌표유지했습니다. normalized installer실제좌표로NullCache prepare3을실행해direct기존좌표준비와RGBA모두동일/maxA255/fill0확인했습니다.
최종flat계약으로test_current/parts/preflight_candidate_geometry.py를실행했습니다. root_geometry_preflight.json 경고0입니다. 원본격자alpha128IoU/면적비도3개모두1입니다. 이생산전확인은공식HD화질검증/실재생정상판정이아니며Claude판정대기입니다.

## 인계
ready_replacement3.json / normalized_installer_contract3.json / candidate_atlas.png / native_atlas.png / native_prepared_pairs3.png / root_geometry_preflight.json.
새atlas effect21427_components_repaired3으로same3ID만교체하고정상15·기술보존4의oldatlas/메타/key는변경하지마십시오. root설치·굽기/Claude공식QA대기,shared/runtime/live/DB/EXE/Git변경없음입니다.
