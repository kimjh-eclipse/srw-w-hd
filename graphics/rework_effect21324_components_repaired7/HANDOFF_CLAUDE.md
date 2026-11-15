# 21324 문제 7개 교정 후보 — Claude 검토 대기

## 현재 상태
observed_effect_phase_21324 분류된7개 모두(94117~94123)를 자체새그림으로 교정했습니다. candidate native256×192/HD1024×768. target밖 기존 그림은 byte 동일입니다. 다른 정상 바인딩 변경 없음입니다. 같은7ID만 새 atlas effect21324_components_repaired7로 옮기는 제안입니다.

## 입력과 좌표
7개 모두 실제 rendered cached 원본의 indexbytes/w/h/indexhash/전체16색 BGR555/RGBhash를 확인했습니다. 각 fixture/frame/팔레트는 normalized_installer_contract7.json에 그대로 들어 있습니다. sourcebox와 candidatebox 분리했고 candidatebox/spec는 기존 live좌표를 유지했습니다. source_candidate_palette_integrity7.json을 참조하십시오.
normalized installer를 실제로 읽어 NullCache prepare7개를 실행했고, direct oldcoords prepare와 모두 RGBA가 일치/maxA255입니다. sourcefill0이고 빈그림 없습니다.

## 그림·정렬 원칙
원본은 직선6개와 비대칭X 섬광1개입니다. 처음 일부 직선이 가늘고 뾰족하게 생성되어 미사용 rejected_taper 후보로 보존/교정했습니다. 최종은 자체 생성 RGBA를 각 원본bbox에 등록했습니다.
직선6은 이미지 생성 후 원본 직선의 중심선1차식과 평균 폭에 맞추는 전역 affine(폭스케일·shear·이동) 등록을 적용했습니다. 원본alpha 픽셀을 출력에 찍은 것이 아닙니다. 원본 binary geometry에서 얻은 1차계수2개와 폭스칼라1개만 사용했고 자체 생성RGBA 전체를 BICUBIC 변환했습니다. own_registration11.json 각 line_affine_registration에 계수/폭을 저장했습니다. threshold는 bbox/측정용이며 출력 alpha삭제/형태학 없음입니다.

## 남은 위험
- 원본격자 alpha128 IoU .876~1.0,면적비 .94~1.074입니다. X 섬광 끝 AA와 원본 계단 차이, 직선 끝 clip AA가 남습니다.
- 원본과 새 그림이 palette구성은 같지만 연속음영 RGB는 완전히 같지 않습니다. color_production_comparison7.json에서차이를 볼 수 있습니다.
- 전체 native시트에 별모양들이 인접해 있다는 것이 실제 같은frame에서함께조립된 근거는 아닙니다. 각 actual source계약만재현근거입니다.
- phase라는 이름의 이전자료에 보류중인 palette fade변형이 있어도이번7교정완료수에는 포함하지 않았습니다.
- 새공식audit·HD실재생·기본코어/EXE교체없음입니다. root설치/굽기후Claude판정대기입니다.

## 인계
ready_replacement7.json / normalized_installer_contract7.json / candidate_atlas.png / native_atlas.png / native_prepared_pairs7.png / normalized_installer_prepare7.json.
