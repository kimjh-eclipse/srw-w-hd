# 19678 remaining18 문제6개 교정 후보 — Claude검토대기

## 범위와그림
observed_effect_19678_remaining18의문제6개(93517/18/19/21/22/23)를자체새RGBA로교정했습니다. 정상12와target밖영역은기존RGBA/바인딩/oldatlas/key그대로입니다. 정상부모포함관계는없습니다. source31개성분을27개motif/3개새생성panel로원래자리와폭에등록했습니다.

## actual 팔레트 차이
yellow58과이름/원본IMG가같지만이번actualfull16palette는흰색이빠진어두운올리브yellow팔레트입니다. yellow58그림/alpha를차용하거나재색칠하지않았습니다. yellow58_raw_palette_compare.json에raw/fullpalette대조근거가있습니다. 원본의작은사각입자를흰원형/타원으로대체하지않고각진배치와실제명도를유지했습니다.

## 입력·좌표·준비
actualcached6개의raw/w/h/indexhash/전체16색BGR555/RGBhash모두확인했습니다. source별state/frame/OAM/변환은normalized_installer_contract6.json에보존했습니다. candidatebox/spec는기존live좌표이고sourcebox는별도입니다.
normalized installer자체를읽어NullCache prepare6을실행했고direct기존좌표준비RGBA와모두일치/maxA255/fill0입니다. 최종flat계약으로preflight_candidate_geometry.py를실행하여root_geometry_preflight.json경고0입니다. source격자alpha128IoU/면적비도6개전부1입니다.

## Alpha와생성오류기록
imagegen자체RGBA만사용,원본mask/RGBstamp·다른팔레트alpha차용·threshold/morph삭제없음입니다. A>=16은생성bbox기하측정용. 단색4material은자체생성셀의내부RGBAcrop(생성alpha253~254그대로)사용,255강제칠하기없습니다.
첫생성묶음에서panel0/1성공후panel2출력이safety시스템violence400으로거절됐습니다. 원본은추상색면/입자도형이므로비폭력도형의동일뜻으로1회재요청했고성공했습니다. 처음실패request와성공기록은GENERATION_FAILURE.md에있습니다. 별도API/CLIfallback을사용하지않았습니다.

## 남은한계
원본대비새그림은연속음영/AA차이가있으며RGB편차는colour_production_comparison6.json참조. 지표가같다고실제HD화질완료를증명하는것은아닙니다. 공식audit/HD실재생검증안했고Claude판정대기입니다.

## 인계
ready_replacement6.json/normalized_installer_contract6.json/candidate_atlas.png/native_atlas.png/native_prepared_pairs6.png/root_geometry_preflight.json.
새atlas effect19678_remaining_components_repaired6으로same6ID만교체제안입니다. 정상12는변경하지마십시오. root설치·굽기/Claude공식QA대기,shared/runtime/live/DB/EXE/Git변경없음입니다.
