# 그레이트 마징가 썬더 브레이크 관측 자세 — 새그림10종

상태: **미검증 후보 / 연결 준비 가능**. root 설치·굽기, Claude QA·독립시각·실제재생 담당. 공유코드/코어/라이브/DB 수정이나 후보 공식audit/HD재생 검증은 하지 않았다.

## 실제 자세와 집계

- state `test_current/combat/named_attacks/unit_299/mechanical_cutin_168.state`, offset0.
- 공통 helper `scripts/assets/capture_rendered_obj_contract.py`로 cachedOBJ+rendered OAM을 Core.run1회 뒤 추출. MMU 프레임 말 OAM/VRAM은 원본으로 사용하지 않았다.
- pal0/OAM8~27의 그레이트 몸체20 OAM/19종. pal4/OAM0~7의 효과8개는 이 제작범위에서 제외했다.
- 이전 재제작17/18과 실제RGB가 같은9종(10 OAM)은 **기존 그림 보존**. 새로 그린 것은 다른10종이다.
- 새그림10종의 기존연결 분류: 최신 exact1종 교체 + 다른색 indexed proxy8종을 실제팔레트 그림으로 교정 + 실제 unbound1종 신규(셀7/OAM25/hash3614722722).
- 실제RGB 새등록9종을 미연결9종이라고 세면 안 된다. 기존 binding이 있는 indexed8개와 진짜unbound1개를 구분한다.

## 보존 의존성

`reuse_dependencies.json`의10 OAM/9종은 실제RGB뿐 아니라 원본 index bytes와 사용된 비투명 색번호의 RGB가 기존 그림 계약과 모두 같다. 바꾸지 않는 binding은82798,82802,7349(2회),91776,91777,91778,91779,82817,7353이다. 각 atlas_id와 actualhash/slot도 파일에 기록했다. 새그림10종을 이9종에 덮어쓰지 않는다.

## 원본과 그림

- `whole_pose_contract.json`:공통helper 몸체20행.
- `rendered_contract_all.json`:효과 포함 원래 추출 전체.
- `contract.json`, `contract_unique10.json`:신규제작10종의 actualhash/index/palette/coords 및 공통helper 원본.
- 각 계약의 core_path와 `capture_meta.json`:기본DLL 위치와 실제SHA.
- DLL SHA256 `a6d80b29119f7c18447725acc4e0e5c8fb88cdda07d8cef6ccb106e936b64fe0`.
- `native_atlas.png`:256×216. `candidate_atlas.png`:1024×864(4배),4×3셀 중10개 사용.
- `whole_native_pose.png`/`whole_native_detail.png`:기존 보존9종까지 포함한 전체cached 원본 조립.
- `whole_oam_context.png`:신규10종의 실제bbox 문맥. 역할명 추측 대신 이를 참조했다.
- `candidate_pose.png`/`candidate_detail.png`:새10개만 조립, 기존9개가 빠져 있으므로 전체기체로 판정하지 않는다.
- `candidate_with_retained_native_detail.png`:새10개 + 보존할10 OAM은 native로 넣은 제작문맥. 보존9종의 라이브HD가 그려진 화면이 아니며 native픽셀은 이 문맥 자료에만 사용했다.
- `actual_frame_native.png`는 **HD enabled Core.native 프레임버퍼**다. 이미 코어가 숨긴 영역이 있을 수 있어 pure-native 화면 증거로 쓰지 않는다. 원본 조립 기준은 cached indices/palette와 rendered OAM이다.

`parts_generated.png`에10종을 새로 그렸다. 첫 생성은 도트 계단이 남아 최종 후보에 사용하지 않았고, 부드러운 선으로 다시 그린 출처를 provenance에 기록했다. 파란 손과 팔, 보라/밝은 장갑, 붉은 장식, 노란 눈·옆 장식, 황토색 막/붉은 날개 경계를 실제 팔레트로 지시했다. 지켜졌는지는 Claude판정이다.

머리4/5는 origin(108,55),48×32의 서로 겹치지 않는 실제사각형이다. `head4_5_native.png`의 원본 연속 머리로 새그림 `head_joint_generated.png`를 만들고 원래16×32/32×32로 나눴다. 잘린 옆조각에 또 다른 얼굴을 넣지 않도록 했다. 나머지8개는 개별 생성이다. 생성alpha 정리·bbox정렬만 했고 native RGB/alpha 스탬프나 다른 기체 재색칠을 하지 않았다.

## root 설치

`installation_map.json`10 entries, atlas_id `great_thunder168_cached_pose`, image `graphics/rework_great_thunder168_cached_pose/pose_hd.png`, reference `graphics/rework_great_thunder168_cached_pose/pose_native.png`, native_size `[256,216]`.

candidate SHA256 `eb9124eae2f6ece5d3c4b8cbacbeb6bca4a6eb24d636eeae82e8fc150237e8e3`.

actual RGB 전용으로 등록한다. indexed_safe=false이며 이전 indexed fallback은 다른 팔레트용으로 보존한다. 이미제작9종도 그대로 둔다. 라이브/DB/공유코드는 변경하지 않았다.

`mechanical_final.json`은20/19전체와 새10/유지9 개수·크기·각후보alpha존재·파일hash 및 nativecrop 색/alpha가 actualcached indices/palette와 일치하는지만 확인했다. 후보 색/형태를 QA 통과시킨 것이 아니다.

## Claude 큐

root 설치·굽기 뒤 예시:

```powershell
& 'C:\Program Files\Python311\python.exe' -X utf8 scripts/verify/verify_runtime_path.py --state test_current/combat/named_attacks/unit_299/mechanical_cutin_168.state --frames 180 --pure-native --save-frames 0 30 60 90 140 --track-atlas great_thunder168_cached_pose --name great_thunder168_cached_claude
```

검토할 위험은 머리4/5 눈·마스크/뿔색과 접합, 새그림과 기존9종의 이음매·재질 차이, 파란손0/6의 손가락과지원형태, 아주 작은7조각, 날개8/9의 실제색 영역, 유지binding의 다른사용처, 대사창·컷인·번개효과의가림이다. 후보 조립자료로 실제HD 정상 여부를 대신 판단하지 않는다.
