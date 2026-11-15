# 19954 문제 10개 교정 후보 — Claude 검토 대기

## 현재 상태
초기 분류10/16을 제작했습니다. 최신 atlas에는 92512가 추가되어 현재17개입니다. 정상 초기6개와92512까지7개 영역/바인딩은 보존했습니다. 원본 component33개를 분리하고 같은 RGBA motif/단색 material 중복을 묶어23개 생성 motif를 만들었습니다. 2개 자체생성 atlas panel의 각 성분을 원본 bbox 위치로만 등록했습니다. 원본 mask/RGB 복사 없음, alpha문턱 삭제 없음입니다.

## 입력/좌표/준비
`source_candidate_palette_integrity10.json`: 모든10개 actual cached source의 rawbytes/w/h/indexhash/fullpalette15bit/RGBhash가 일치합니다. 후보의 atlas_box는 source별칭이 아니라 기존 live x/y입니다. `normalized_installer_prepare10.json`: normalized installer의 실제 좌표/spec로 NullCache prepare한10개 RGBA가 직접 기존좌표 prepare와 모두 같습니다. 최대alpha255이고 빈그림 없습니다.
단색 material 5종은 해당 생성 셀의 내부 opaque RGBA crop을 사용했습니다. 생성값 자체alpha는253~254여서255로 덮지 않았습니다. 원본1texel 단색점과 같은 칸에 들어갑니다.

## 알려진 위험
- 원본격자 alpha128 IoU .834~1.0, 면적비 .842~1.0. 큰 섬광의 일부 끝 가시 AA가 원본보다 조금 가늘 수 있으며 공식 검사/재생으로 판단해야 합니다.
- 매우 작은 파편은 source의 계단 배치 유지 때문에 HD 화면에서도 모양이 단순합니다. 생성 panel은 다소 광택 음영이 있는데 원본색 역할이 맞는지는 Claude 확인 필요합니다.
- 기하학적 component 추적은 도트 기준 연결을 사용했으며 실제 동시에 한 화면에 조립됐다는 증거로 쓰지 않습니다. 각 source fixture/frame은 normalized 계약에 있습니다.
- 현재 새 공식audit/HD실재생 안 했습니다. 생산 입력과 메모리 준비 확인이지 최종 QA가 아닙니다.

## 인계
`ready_replacement10.json`, `normalized_installer_contract10.json`, `candidate_atlas.png`, `native_atlas.png`.
새 atlas effect19954_components_repaired10으로 같은10 ID만 교체하고 기존 정상7과 기존atlas/key를 변경하지 마십시오. `native_prepared_pairs10.png`는 원본/실제 준비후 후보 쌍입니다.
