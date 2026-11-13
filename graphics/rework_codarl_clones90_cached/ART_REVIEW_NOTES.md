# 코다르 c 분신 계약 시점 정정 — 현재 설치 입력

상태: **미검증 그림 후보 / cachedOBJ 기준 연결 준비 가능**. 이전 `codarl_clone90_pose`의17종 계약은 폐기한다. 그림 원본 출처 보존용으로만 남기고 라이브 설치하지 않는다. 이 파일과 같은 폴더의 `installation_map.json`이 현재 입력이다.

## 왜 정정했나

앞 추출은 `retro_srw_copy_obj_debug`가 반환한 MMU OAM과 프레임 말 VRAM을 읽었다. 게임이 다음 그림을 준비하면서 OAM 순서·크기·위치와 일부 타일을 바꾼 상태라 실제 렌더와 맞지 않았다. source spec을 hash로 다시 찾는 것만으로 해결되지 않는다.

이번 추출은 `retro_srw_copy_cached_obj(0,slot,...)`의 실제 렌더 캐시 index/palette/hash와 `core.obj`의 `retro_srw_copy_rendered_obj` OAM을 짝지었다. 동일 state/offset의 **제작용 원본 입력 정정**이며 Claude의 독립 시각/재생 검증이 아니다. 현재 캐시 크기와 rendered OAM 크기는 전부 일치했고, binding이 있는 행의 cached RGB hash는 core.parts의 actual hash와 전부 일치한다. unbound행의 core.parts hash는0이므로 그 행은 캐시를 사용했다.

## 정확한 범위

- state: `test_current/combat/named_attacks/unit_280/mechanical_cutin_168.state`
- offset +90, 원본 제작 추출을 위해 Core.run91회.
- 좌우 분신 OAM0~38에서 중앙14/전신91684·85의 actual RGB를 제외.
- **26 OAM /14 고유 RGB**. 기존 exact3 + 새 actual RGB11.
- 좌우 공유12종은 native index bytes·actual palette·크기가 같다. 서로 다른 작은 날2종은 별도 그림이다.
- 기존 유지13 OAM은 설치 대상에서 뺀 기존 그림이며 지우지 않는다.
- 옛17종 중 hash1319154558/3969497505/593422960은 MMU 프레임 말에만 있던3종으로 제거했다. 그3종의 공동 큰 날 그림도 이번 설치에 사용하지 않는다.

나머지14종은 새 캐시 원본과 이전 원본의 actual hash뿐 아니라 **압축 해제한 index bytes·actual palette·가로세로**가 모두 같았다. 따라서 같은 기체·같은 팔레트·같은 native 그림을 참조해 생성한 기존14종 그림을 재사용하고, actual hash로 새14셀에 재배치했다. 재색칠이나 원본 RGB/alpha 스탬프는 하지 않았다. `paint_reuse_contract.json`이 근거다.

## 현재 파일

- `contract.json`: rendered OAM26개, 좌표/반전/실제 캐시팔레트/bytes.
- `contract_unique14.json`: 고유14종.
- `all_oam.json`, `cached_snapshot.npz`: 제작 추출의 렌더 캐시 메타와 rendered OAM.
- `duplicate_check.json`: 공유12종의 index/palette 일치.
- `retained_native_context.json`: 유지13 OAM.
- `native_atlas.png`:320×288.
- `candidate_atlas.png`:1280×1152(4배), 고유14종.
- `whole_native_pose_detail.png`: 기존 그림까지 포함한 원본 분신 조립.
- `candidate_with_retained_native_context_detail.png`: 새26 OAM + 유지13 OAM을 native로 넣은 문맥 자료. 유지13 OAM의 실제 라이브HD가 들어간 그림이 아니며 이 native는 후보 atlas에 사용되지 않았다.
- `candidate_pose_detail.png`: 새26 OAM만 조립. 기존13개가 빠지므로 전체 기체 그림으로 판정하지 않는다.
- `paint_source_atlas.png`/`paint_source_contract.json`/`parts_generated_source17.png`: 재사용한 생성 그림의 출처. 제외3종도 원출처에 남아 있으나 설치17종으로 오해하지 않는다.
- `mechanical_final.json`: 개수/크기/bytes/alpha존재/hash 확인만. 공식QA가 아니다.

## root 설치

`installation_map.json`14 entries. atlas_id `codarl_clones90_cached_pose`, image `graphics/rework_codarl_clones90_cached_pose/pose_hd.png`, reference `graphics/rework_codarl_clones90_cached_pose/pose_native.png`, native_size `[320,288]`.

candidate SHA256: `4e402047ce60011ad2ff6eb444010ee6cc5a7683c46b0cfbc1e4ddf1191aa27e`.

actual RGB 전용이며 indexed_safe=false. 다른 팔레트의 기존 indexed fallback은 보존한다. 라이브/DB/공유 실행 코드는 수정하지 않았다.

## Claude 검증 큐

root 설치·굽기 뒤:

```powershell
& 'C:\Program Files\Python311\python.exe' -X utf8 scripts/verify/verify_runtime_path.py --state test_current/combat/named_attacks/unit_280/mechanical_cutin_168.state --frames 160 --pure-native --save-frames 60 90 110 140 --track-atlas codarl_clones90_cached_pose --name codarl_clones90_cached_claude
```

미확인 위험은14종의 색/형태/alpha·내부 절단면·기존 중앙 그림과의 연결, 작은 날 두 가지의 구분, 기존 exact3종 교체의 다른 자세 영향, 좌우 반전·레이어다. 이번에 source 계약의 시점을 기계적으로 바로잡았을 뿐 그림 품질 통과를 주장하지 않는다.
