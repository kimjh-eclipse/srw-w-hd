# 클로드 검증 대기열

## 담당과 갱신 규칙

사용자 최신 지시: **Codex는 그림 제작·연결·굽기·커밋을 진행하고, 독립 검증은 Claude가 담당합니다.**
Codex가 새로 공식 전수 검사나 실제 재생 검증을 반복하지 않습니다. 설치 입력의 크기·실제 해시·팔레트·바인딩 중복·굽기 오류 같은 작업상 기계적 오류는 확인합니다.
이 파일은 제작 중 변경과 반영 직후마다 갱신합니다. 검증 대상을 새 그림으로 바꾸면 이전 검증은 자동 승계하지 않습니다. 결과는 Claude가 별도로 판정합니다.

## 지금 우선 검증/수정할 공통 런타임

|대상|현재 상태|자료와 확인점|
|---|---|---|
|컷인 자기 페이드|미수정,Claude 담당|`docs/REVIEW_CUTIN_FADE_FLASH.md`. getter_cutin+30/32, golion_cutin+0~5. source의첫대상EVA/EVB·뒤대상·윈도우색효과허용을래스터시점으로적용. 앞BG효과용foreground와구분|
|윈도우 플래시|미수정,Claude 담당|unit333 mechanical_cutin_168+28/+32. 상단주황/하늘색단색과하단UI보존. MASTER/BLDY는이번측정0. frame끝레지스터만사용하거나ID5일괄차단금지|
|단색 효과 수집/접합|일부원인확보,그림제작중|22163색3개미만unknown수집누락. 같은frame의현재VRAM은이미다음상태이므로폐기. 아래cachedOBJ읽기API로실제rendered 계약확보. known등록은단색에도가능|

## 신규 제작/반영 대기 묶음

|ID|작업 상태|변경범위·파일|Claude가 볼 장면·알려진 문제|
|---|---|---|---|
|P-22163-24|미검증후보,추가그림수정중|`test_current/parts/effect_22163/fill_completion/complete24_contract.json`,candidate_complete24.png. 앞16기존RGB+중앙fill8새RGB,두실제팔레트. 원본indices두벌동일assert.아직라이브미설치|unit299 mechanical_cutin_141+54/55/56. cyan gradient반복으로아주옅은사각접합남아균일cyan그림출력재제작중. whitefill4개flatflag는원래단색이므로잡음추가해속이지않음.24개전부재굽기필요|
|P-MAZINKAISER-179|미검증후보,그림접합수정중|`test_current/parts/borrowed_shape_rework/mazinkaiser_running179_pose/`. 실제22OAM/20고유RGB. 최초정확RGB5/다른팔레트indexed proxy15고유. metadata만늘리지않고한벌새그림제작|unit297 weapon1213 frame300+179/190/220. 머리아래수평띠·날개중간색면접합. SD부분을얼굴/허리로성급히명명한오해수정중. 실제bbox문맥+nativecrop을기준으로작업|
|P-GETTER-AXE|미검증후보,계약인계중|`test_current/parts/getter_remaining_effects/` 하위도끼머리.64×64 실제indices가IMG14461/14485 x192,y64와같고actualpalette16이PLT14460/14484 bank2와일치|getter_cutin+207~299,실제관측93회. 양날도끼머리+짧은중심연결부. 기체/갑옷/빔으로오인하면안됨. effect_part태그대상아님|

## 반영 완료, Claude 확인 대상

- **그레이트후속18**: atlas great_mazinger_running179_pose. 신규91877–91881/91886–91893,기존82809/7352/7346/7351/7340. `graphics/rework_great_running179_pose`,전용contract/provenance. 작은7340도새그림이므로첫자세+3에도영향. +179/190/220노출·다른팔자세, +3은테츠야컷인에가려육안판정불가. 기존Codex300프레임추적18개HD/vanish0은참고자료이며Claude검증대체아님.
- **겟타별빛/세로섬광2**:91894/91895, observed_getter_glints_21869. `test_current/parts/getter_remaining_effects/effect21869/observed_pair/`,actualRGB/static/effect태그. 별빛+234/세로광선+258/259. 원래12개중관측2단계만이며나머지10개미완료. 굽기2/오류0. 역할변경전Codex재생10/10·4/4HD는참고.
- **22163기존16**:91861–91876, observed_effect_22163_sixteen.24완결후보반영전이므로여전히중앙nativefill8개와접합차이있음. 검증시16개연결성공과효과전체정상을구분.
- **민트38/19645관측7/진겟타머리3/그레이트첫17/코다르16/데스3/파워드레드9/22378효과16**:현재상세binding·자료는HANDOFF_FROM_CODEX_3.md표참고. 최근공식선택133개에명암검토3개64207/82798/91777남음. 이검사에서ROM전체누락완료를뜻하지않음.

### 권장 재생 명령 틀(Claude 실행용)

Python311, C:작업공간에서:
```
python -X utf8 scripts/verify/verify_runtime_path.py --state <실제state> --frames 300 --pure-native --save-frames <offset들> --track-atlas <새atlas> --name <고유검증명>
```
`--pure-native`는별도HD-disabled프로세스원본을같은offset으로재생합니다. 예전저장쌍의좌측은HD suppression후framebuffer일수있으므로순수원본으로쓰지마세요.
도구결과REVIEW/INCOMPLETE와그림의정확성은별개입니다. 얼굴/몸통오연결,색/절단면/눈중복,대사창가림/효과앞뒤,fade/flash를실제쌍으로보아야합니다.

## 코드/바이너리 검증 대상

1. 효과의기체폴백제외: hd_core.py/srww_parts_impl.h/srww_hd.h/libretro.cpp. 기본10%기체보호유지,명시effect_part만제외. 기존162상태×90raw판정A/B와unready1249자료는effect_guard_review/. 정상기체보호와미준비원본보존을Claude가확인.
2. cachedOBJ읽기API: srww_texture_cache.h/srww_hd.h/libretro.cpp. **기본DLL미반영**,별도fill_completion/desmume_cached_obj_debug.dll만. 읽기전용capacity/엔진/OAM검사,known8snapshot/invalid5/240frame일치자료는HANDOFF_COMPLETE24_AND_API.md. Codex는이3파일수정종료,Claude수정과충돌안하게공유코드추가수정중단.
3. build/frozen_update EXE는효과가드코어까지빌드됨. cachedOBJAPI는없음. dist팩미갱신,PNG→WebP내용해시·baked키호환과실제배포팩검증별도필요.
4. 구운DB정리후보: baked_store_compaction/candidate.sqlite 1.28GB. live2.58GB는그대로. 현재87348유효키만복사·재인코딩없음. 이후새그림추가되어후속키를포함해다시생성해야함. 후보를현재live로바로덮지말것.

## 배포/커밋 처리

전체완료율160/11358같은비율은사용하지않습니다. 바인딩·원본고유파츠·팔레트변형·OAM중복은서로다름.
전체기체목표를유지하되83개테스트기체/보유장면을우선배포검증목록으로구분. 검증완료범위와미포함범위를배포설명에명시.
Codex가검증된변경부터기능별선택커밋을진행합니다. ROM/세이브/사용자설정/오류로그/거대미추적DB를일괄추가하지않습니다. 푸시·EXE팩갱신은별도상태기록.
