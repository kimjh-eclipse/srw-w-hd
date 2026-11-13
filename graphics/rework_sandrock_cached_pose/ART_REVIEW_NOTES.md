# 샌드록 일반 전투 몸체 — cachedOBJ 한 벌 제작 인계

상태: **미검증 그림 후보 / 연결 준비 가능**. 이번 작업은 기존 부분 그림16종을 한 벌로 새로 그린 품질 교정이다. 새로 누락16종을 채웠다고 집계하지 않는다. root가 설치·굽기하고 Claude가 공식 검사·독립 시각 판정·실제 재생을 담당한다. 이 최종 후보의 공식 audit/HD 재생 검증은 하지 않았다.

## 실제 입력

- state: `test_current/combat/quatre_cutin_full.state`
- offset0. Core.run1회 직후 cachedOBJ+rendered OAM을 제작 원본으로 추출했다.
- helper: `scripts/assets/capture_rendered_obj_contract.py`
- core_path: `C:/Emul/Workshop/SRW_W_HD/emulator/desmume/desmume/src/frontend/libretro/desmume_libretro.dll`
- 실제 DLL SHA256: `a6d80b29119f7c18447725acc4e0e5c8fb88cdda07d8cef6ccb106e936b64fe0`
- d98c4226은 Git 커밋ID이며 DLL SHA가 아니다. 이를 초기에 혼동했으나 실제SHA와 core_path를 각 계약에 기록했다.

helper는 cached 원본 크기와 rendered OAM attrs/크기, bound actual hash가 맞는 행만 돌려준다. 프레임 말 MMU OAM/VRAM은 원본으로 읽지 않았다. 이 상태는 카토르 컷인이 위를 가리지만 일반 전투 기체의 캐시 OBJ가 남아 있는 상태다. 원본 계약 추출이 화면에서 몸체가 전부 보였다는 재생 확인은 아니다.

## 실제 한 벌과 이전 부분 그림의 차집합

- OAM0~16의17개, actual RGB16종.
- 기존 rawRGB와 차집합0, existing exact16개.
- 기존 `wing_primary`11종(12 OAM) + `full_attack_018`5종. 따라서 기존16개를 교체하는 제안이며, 모두 기존 연결이 있다.
- 셀13/OAM13·15는 실제 index bytes/팔레트/크기가 같아 한 그림을 공유한다. 각 OAM 좌표와 반전은 유지했다.
- 원본 팔레트의 눈/센서 green15, V-fin gold13/bright yellow14, 붉은 패널11/12, 보라색 음영8~10과 밝은 장갑5~7 및 베이지2~4를 참조했다. 단순히 원작의 일반 흰색 기체 색으로 다시 칠하지 않았다.

## 파일

- `rendered_contract_all.json`:공통 helper 원본17행, 각 행 core_path/SHA 포함.
- `contract.json`:제작 atlas 좌표 + 원본 helper 계약 + actual palette/indices17행.
- `contract_unique16.json`:고유16종.
- `capture_meta.json`, `rendered_arrays.npz`:원본 추출 시점·코어·렌더OAM자료.
- `duplicate_check.json`:셀13 공유 근거.
- `classification.json`:기존 exact16개와 atlas 분류. 현재 연결이 있다는 사실과 그림이 올바르다는 판단은 구분한다.
- `native_atlas.png`:320×288. `grid_reference.png`, `grid_context_gray.png`:원본 확대/셀 번호.
- `native_pose_detail.png`, `whole_oam_context.png`:전체 원본 조립 및 실제 bbox 표시. 제작 전 역할을 임의 추측하지 않도록 이 문맥을 참조했다.
- `candidate_atlas.png`:1280×1152(4배), 고유16종. 마지막4셀은 빈 셀.
- `candidate_pose.png`/`candidate_detail.png`/`pose_comparison.png`:같은 원본 좌표·반전·priority/OAM역순으로 조립한 제작 자료. Claude 시각 판정 완료 근거가 아니다.
- `parts_generated.png`:16종 최초 생성 원본.
- `scarf5_9_generated.png`:5/9를 실제 native 두 crop으로 다시 생성한 원본. 첫 생성의 불필요한 둥근 금속 장식과 경계 잔여를 피하고 원본 부분 형태를 지시했다. 실제 성공 여부는 Claude가 판정한다.

셀5/9의 OAM 사각형은 겹친다. 그때 가려지는 원본 내용이 다른 부분까지 하나의 완성 몸체 그림으로 채우지 않도록 두 파츠를 개별 원본으로 생성했다. 다른 기체/다른 팔레트 그림을 빌리거나 재색칠하지 않았다. native RGB/alpha를 생성 후보에 복사하지 않았다. 생성 alpha의 작은 연결 요소 정리와 bbox 정렬만 했다. 작은 셀7의 떨어진 점을 지우지 않도록 구성요소 기준을0.5%로 잡았고, 이것이 잘 지켜졌는지 Claude 검토가 필요하다.

## root 설치 입력

`installation_map.json`16 entries.

- atlas_id: `sandrock_cached_pose`
- image: `graphics/rework_sandrock_cached_pose/pose_hd.png`
- reference: `graphics/rework_sandrock_cached_pose/pose_native.png`
- native_size: `[320,288]`
- candidate SHA256: `37ef225edd152d38093806ed150da556e93c9a84c31b7ed297b5f477fd148af8`

actual RGB 전용, indexed_safe=false. 기존 fallback은 다른 팔레트용으로 보존한다. exact16개를 바꾸면 같은 hash를 쓰는 다른 자세에도 영향을 미칠 수 있으므로 이전 그림을 삭제하지 않고 교체 이력을 남긴다. 라이브/DB/공유 코드는 수정하지 않았다.

`mechanical_final.json`은17/16개수·크기·indices길이·사각형 범위·각 후보 alpha존재·SHA 및 **native crop이 cached indices+actual palette와 일치**하는지만 확인했다. 후보 그림 색이 원본과 맞는지 수치QA를 한 것이 아니다. native reference의 alpha0 뒤RGB만0으로 정리했고 보이는 원본 색/alpha는 그대로다.

## Claude가 확인할 것

root 연결·굽기 뒤 예시:

```powershell
& 'C:\Program Files\Python311\python.exe' -X utf8 scripts/verify/verify_runtime_path.py --state test_current/combat/quatre_cutin_full.state --frames 240 --pure-native --save-frames 0 30 60 100 160 220 --track-atlas sandrock_cached_pose --name sandrock_cached_claude
```

이후 원본 몸체를 컷인이 가리지 않는 프레임/다른 보유상태에서 볼 필요가 있다. 그 시점의 cached hash가 이16종인지 확인해 따로 판정한다.

현재 미확인 위험:

1. 사용자가 반복 지적한 V-fin 금색/노랑과 붉은 패널 구분, 초록 눈/센서 위치가 실제 색 영역과 맞는지.
2. 셀7의 작은 두 분리 영역과 셀1/3/4/6의 매우 얇은 절단 조각 지원.
3. 겹치는 천/장갑5/9/13에서 인접 파츠와 형태·재질·색이 연속되는지. 개별 생성이므로 어긋날 가능성은 남아 있다.
4. 절단면에 새 외곽선이나 그림의 잘못된 alpha가 남는지.
5. 기존16개 exact 교체가 다른 공격/자세에서도 맞는지.
6. 컷인·대사창·효과 순서는 이번 그림만으로 해결됐다고 주장하지 않는다.

마징카이저179 slot51 alpha 경고와 코다르 정정14는 별도 항목이며 이 작업으로 해결했다고 집계하지 않는다.
