# 22410 문제 15개 교체 후보 — Claude 검토 대기

## 현재 상태
- 원본 atlas `observed_effect_22410_new19` 19개 중 분류된 문제 15개를 새 자체 RGBA로 제작했습니다. 정상 4개(92480/92483/92484/92495)는 기존 픽셀 및 바인딩/키 보존 대상입니다.
- parent 11개를 실제 두 팔레트별로 생성했고, 하위 사각 alias 4개(92488/92490/92491/92494)는 같은 parent RGBA의 해당 crop을 공유합니다.
- `ready_replacement15.json`의 새 atlas `effect22410_components_repaired15`로 같은 ID 15개만 교체하는 전략입니다. 기존 atlas 파일 자체는 덮지 않습니다.
- 원본 15개 모두 실제 rendered OBJ cached 계약입니다. indices/크기/indexhash/전체16색/BGR555에서 다시 계산한 RGBhash를 대조했습니다. `source_candidate_palette_integrity15.json` 참조.
- candidate native 192×64, HD 768×256. 위 32줄은 밝은 녹색/흰색 실제 palette bank10, 아래 32줄은 짙은 녹색 bank11. 두 팔레트 그림·alpha를 빌려 쓰지 않았습니다.

## 좌표와 생산 준비
- installer `atlas_box`와 spec x/y는 `source_live_bindings19.json`의 원래 candidate 좌표입니다. source_box는 실제 ROM/cached 원본 좌표이며 별도입니다. 아래 팔레트 y32를 원본 y0과 혼동하지 않습니다.
- normalized installer 자체를 읽어 `prepare_texture(NullCache)` 15개를 실행했고, 원래 candidate 좌표로 준비한 RGBA와 전부 동일합니다. 전부 max alpha255입니다.
- 생성 alpha를 문턱/형태학으로 삭제하지 않았습니다. A>=16 bbox는 자체 그림 위치 등록에만 사용했고 원본 alpha/RGB를 전사하지 않았습니다.
- 정상 4개 및 target밖 기존 픽셀은 byte 동일입니다. 92482 내부와 정상92483은 실제 사각형이 겹치므로 그 정상 하위 영역을 기존 그림 그대로 보존했습니다. 이 경계의 스타일 차이는 검토 필요합니다.

## 남은 검토 위험 (완료 판정 아님)
- 원본 격자로 줄인 alpha128 면적/IoU는 0.846~1.026입니다. 일부 작은 빔/빛점의 둥근 AA 경계와 원본 도트 경계가 다릅니다. 성분 전체가 빈 것은 없지만 이 정도 차이를 허용할지는 Claude 판정입니다.
- 92482는 정상92483 영역을 보존하여 큰 빔 내부에 기존 하위 그림 접합이 남습니다. 실제 frame에서 이음새를 확인해야 합니다.
- 짙은 녹색92493은 새 색영역 교정 후에도 원본 디더링과 연속 그라데이션 차이가 있습니다. 이 후보는 잘못된 흰 코어를 넣지 않았습니다.
- 작은92489는 원본 계단 성분 자체를 조금 매끈하게 만든 것으로, 큰 실제 크기에서는 계단 흔적이 남을 수 있습니다.
- 새 공식 audit/HD 실재생/사용자창 조작은 하지 않았습니다. 이 문서는 제작 입력·prepare 확인이지 최종 QA가 아닙니다.

## 실제 원본 재현 포인터
각 normalized installer의 `rendered_source_contract`에 state/frame/engine/OAM/attrs 전체가 있습니다. 다수는 `unit_413/native_reference/diagnostic_preview/weapon_1613_capture/frame_1320.state` +24, 일부 palette bank11은 같은 actual 수집의 별도 frame입니다. 계약마다 정확한 값을 사용하십시오.

## 다른 atlas와의 실제 중복 대조
pink6는 일부 raw 모양이 같지만 전체 팔레트와 RGB해시가 다릅니다. `pink6_raw_palette_overlap.json`에 기록했고 그림/alpha 공유하지 않습니다.

## 파일
- `candidate_atlas.png`, `native_atlas.png`, `normalized_installer_contract15.json`, `ready_replacement15.json`
- `normalized_installer_prepare15.json`, `production_report.json`, `native_prepared_pairs15.png`
- `generation_sources*.json`, `own_registration11.json`, `parent*_generated.png`는 생성 출처입니다.
