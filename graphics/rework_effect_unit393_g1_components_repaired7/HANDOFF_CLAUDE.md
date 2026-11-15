# unit393_g1 노란고리 7개 교정 후보 — Claude 검토대기

## 현재 상태
observed_effect_unit393_g1의분류7개(94953~94959)모두자체새RGBA로제작했습니다. 원본25개연결성분을14개 motif/2개생성panel로분리해원본bbox자리에등록했습니다. g0푸른전격과는그림을공유하지않았습니다. g0_raw_palette_sharing_check.json에raw/fullpal중복대조결과를보존했습니다.
고리의여러띠·끊긴부분·안쪽나선·어두운자주색끝부분·따로떨어진작은노란점도유지했습니다. 고리중심의원본투명공간을흰원반으로메우지않았습니다. 이source시트25성분이동시에실제로조립됐다는주장은아닙니다.

## 입력과좌표
실제cached원본7개모두rawbytes/크기/indexhash/전체16색BGR555/RGBhash일치확인했습니다. 정확state/frame/OAM/변환은normalized_installer_contract7.json에있습니다. sourcebox는actualsource,candidatebox/spec는기존live좌표입니다. source별칭으로candidate좌표를바꾸지않았습니다.
normalized installer자체좌표로NullCache prepare7을돌려direct기존좌표준비RGBA와모두동일/maxA255/referencefill0을확인했습니다. target밖기존그림은byte동일입니다. 다른정상바인딩/atlas/키수정없음.

## 알파출처
imagegen자체RGBA만사용,원본mask/RGBstamp·다른팔레트alpha공유·threshold/morph삭제없습니다. A>=16은생성bbox위치측정용,출력alpha문턱아닙니다. 단색3material은같은생성셀의내부RGBAcrop(생성alpha253~254그대로)을1texel성분으로배치했습니다.

## 남은위험
원본격자alpha128IoU .861~1.0/면적.935~1.0. 일부고리내부얇은띠끝/부드러운AA는원본계단과차이가있고색상연속음영도원본과완전동일하지않습니다. 공식audit/HD실재생정상판정은하지않았습니다. native_prepared_pairs7.png로원본/준비후후보를확인하고Claude가판정해야합니다.

## 인계
ready_replacement7.json/normalized_installer_contract7.json/candidate_atlas.png/native_atlas.png. 새atlas effect_unit393_g1_components_repaired7로같은7ID만교체하는제안입니다. root설치·굽기/Claude공식QA대기. shared/runtime/live/DB/EXE/Git변경없음입니다.
