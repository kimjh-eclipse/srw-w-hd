# Android HD 합성 이식 명세 (C + OpenGL ES 2)

작성 2026-11-21. 대상: `android/jni/host.c`가 이미 로드하는 같은 `libretro.so`(이 저장소 소스로 빌드한 arm64 코어). 코드 변경 없음. 모든 주장은 `파일:줄` 근거를 단다. 근거 경로 약어:

- `core.py` = `emulator/hd_core.py`
- `renderer.py` = `emulator/hd_renderer.py`
- `parts.py` = `emulator/hd_parts.py`
- `vis.py` = `emulator/native_composition.py`, `vis.c` = `emulator/native_composition.c`
- `fg.py` = `emulator/foreground_blend.py`
- `gpu.py` = `emulator/gpu_surface.py`
- `GPU.cpp` = `emulator/desmume/desmume/src/GPU.cpp`
- `impl.h` = `emulator/desmume/desmume/src/srww_parts_impl.h`
- `hd.h` = `emulator/desmume/desmume/src/srww_hd.h`
- `lr.cpp` = `emulator/desmume/desmume/src/frontend/libretro/libretro.cpp`

PC 플레이어의 실제 경로는 `player_worker.py` → `frame_compositor.py` → `frame_process.py:84`의 `HDRenderer.render_top/render_bottom`이며, `async_parts=True`(코어에 `retro_srw_native_hd_fallback`이 있으면, `player_worker.py:47`)와 GPU 합성(`frame_process.py:43`, `gpu_surface.Surface`)을 쓴다. 이 문서는 그 경로(GPU 분기)를 기준으로 기술한다.

---

## 0. 상수와 좌표계

| 이름 | 값 | 근거 |
|---|---|---|
| 네이티브 화면 | 256×192 화면 2개, 프레임은 위 화면(행 0–191) 위에 아래 화면(행 192–383) | `renderer.py:155`, `renderer.py:300` |
| 렌더 폭 `W` | 768–960, 32 단위, 기본 960. 높이 `H = W*3/4` | `emulator/render_resolution.py:2-9`, `renderer.py:69-71` |
| `SCALE` | `W/256` (기본 3.75). 모듈 기본값 `1440/256`은 `set_resolution`이 덮어씀 | `parts.py:21`, `renderer.py:73-75` |
| `STORE_SCALE` | 4. 굽힌 파츠 텍스처는 네이티브 크기의 4배로 저장 | `parts.py:22-24`, `parts.py:346` |
| 화면 좌표 변환 | HD 픽셀 `(X,Y)` ↔ 네이티브 `(X/SCALE, Y/SCALE)` | `parts.py:816-818,882` |
| 컷인 배율 | x는 `W/256`, y는 `H/192` (둘 다 `SCALE`과 같음) | `renderer.py:217` |

"nearest 확대"는 Pillow `NEAREST` 규칙이다. GPU 경로는 이 규칙을 좌표 테이블로 그대로 재현한다(`gpu.py:60-72`). 출력 픽셀 `i`(길이 `M`)는 원본 길이 `N`의 `floor((i+0.5)*N/M)`번째 텍셀을 고른다(Pillow 동작 기준; `gpu.py:67-68`이 Pillow 결과를 그대로 테이블로 만든다). GLES2에서는 같은 테이블을 텍스처로 올리거나 셰이더에서 같은 식으로 계산한다.

---

## 1. 시작 시 등록

`Core.__init__`(`core.py:23-163`)이 `retro_load_game` 뒤에 아래 순서로 호출한다. 순서가 중요하다. `retro_srw_register_parts`는 effect/dynamic 표를 지우고(`impl.h:51-58`), `retro_srw_register_cutins`는 cut-in map/window 표를 지운다(`GPU.cpp:96-97`).

### 1.1 `retro_srw_register_parts(const unsigned *hashes, unsigned count)`

- 인자: 길이 `N = len(library['bindings'])`(현재 113,783) 배열. `hashes[i]`는 바인딩 `i+1`의 `hash`, 단 `rgb_enabled`(기본 True)가 거짓이거나 `disabled`이거나 `robot_binding_ids`에 있으면 0 (`core.py:77-78`).
- `robot_binding_ids`는 기본(`SRWW_ROBOT_SPRITE_HD`≠`0`)에서 빈 집합 (`core.py:74-76`, `emulator/robot_sprite_switch.py:24-25`).
- 코어 동작: `SRWWPartBindings[hash]=i+1`(0 제외), `SRWWAsyncParts=false`, 텍스처 캐시·effect·dynamic 표 초기화 (`impl.h:51-58`). `count<200000` 검사 (`lr.cpp:123`).
- 입력 파일: `graphics/kazuma_parts_library.json`(196 MB, `bindings`, `atlas`, `atlases`, `source_palette_rgb`, `indexed_collision_keys`). PC는 `parts_catalog.load_parts_library`로 읽는다(`emulator/parts_catalog.py:47-88`). 이 스냅샷에서 등록되는(해시≠0) 바인딩은 95,079개(측정값).
- 이 해시 하나가 OBJ 스프라이트(`impl.h:96-97`)와 BG 타일(`impl.h:173-175`) 양쪽 매칭에 쓰인다. 별도의 BG 파츠 등록 함수는 없다.

### 1.2 `retro_srw_register_effect_parts(const unsigned *ids, unsigned count)`

- 인자: 바인딩 ID 목록. 각 바인딩에서 `source_binding` 체인을 따라가며 처음 나오는 명시적 `effect_part` 값이 `True`인 것, `disabled`면 제외, 순환 차단 (`core.py:83-95`).
- 코어 동작: `SRWWEffectParts[id]=1` (`impl.h:34-38`). 용도는 아래 "유닛 폴백"(`impl.h:130-143`)에서 독립 VFX를 팔레트 그룹 계산에서 빼는 분류뿐이며 텍스처 준비 여부와 무관 (`impl.h:31-33` 주석).
- 반드시 1.1 **뒤에** 호출 (1.1이 표를 지움, `impl.h:53`).

### 1.3 `retro_srw_register_indexed_parts(const unsigned *hashes, const unsigned *bindings, unsigned count)`

- 인자: `(index_hash, binding)` 쌍의 두 배열. 대상은 `dynamic_palette` 참, `indexed_safe`(기본 True) 참, `disabled` 아님, `index_hash`가 `indexed_collision_keys`에 없음 (`core.py:97-98`).
- 기본 `SRWW_NO_RECOLOUR`≠`0`이면 로봇 바인딩(`robot_ids`, `emulator/robot_sprite_switch.py:45-76`의 분류)을 뺀다 (`core.py:104-107`). 즉 인덱스 매칭은 효과·HUD 숫자 등 비로봇 파츠에만 쓰인다(`core.py:99-103` 주석).
- 코어 동작: 같은 `index_hash`는 첫 항목 우선 (`impl.h:46-49`). 매칭 순서는 RGB 해시 → index 해시(4bpp만) → dynamic (`impl.h:96-105`).
- 의미: 인덱스 매칭된 스프라이트는 **다른 팔레트로** 그려지고 있을 수 있다. 호스트가 `part_palettes`로 재색칠해야 원래 색이 나온다(4.3.4).

### 1.4 `retro_srw_register_cutins(const unsigned *rows, unsigned count)`

- 행 = 5 uint: `[signature, id, layer|mode, native_w, native_h]`, `count`=행 수 (`core.py:136-140`).
  - `mode`: `signature_mode`가 `image_origin`→256, `origin_8192`→512, `row_padded`→768, 없으면 0 (`core.py:137`).
  - `cutin['layers']`(없으면 `[cutin['layer']]`)의 각 레이어와 각 `signatures` 원소마다 1행 (`core.py:136-138`).
  - `graphics/<cutin.image>`가 없으면 그 컷인 전체를 건너뜀 (`core.py:134`). `map_window_entries`가 있는데 코어에 `retro_srw_register_cutin_map_windows`가 없으면 건너뜀 (`core.py:135`).
- 입력 파일: `graphics/cutins_library.json`(현재 206개, id 2–207). 필드: `id,name,layer,layers,native_size,image,paint_image,signatures,signature_mode,map_signature,map_window_signature,map_window_entries,presentation_role,restore_rect,repeat_native_plane` 등(측정).
- 코어 동작: `id>1`이고 `(layer|mode)&~768 < 4`인 행만 `SRWWCutins[(layer|mode)<<32 | signature] = {id,w,h}` (`GPU.cpp:96-102`). `count<4096` (`lr.cpp:126`).

### 1.5 `retro_srw_register_cutin_maps(rows, count)` / `retro_srw_register_cutin_map_windows(rows, count)`

- maps: 2 uint 행 `[id, map_signature]`, `map_signature`가 있는 컷인만 (`core.py:141-146`, `GPU.cpp:68-71`).
- map windows: 3 uint 행 `[id, map_window_signature, map_window_entries]`, `map_window_entries`가 있는 컷인만 (`core.py:147-152`). 코어는 `16 < entries ≤ 512`만 받음 (`GPU.cpp:72-78`).
- 둘 다 1.4 **뒤에** 호출 (1.4가 지움, `GPU.cpp:97`).

### 1.6 `retro_srw_set_hd_enabled(unsigned)`

- `SRWWHD_Enabled` 설정 (`lr.cpp:104`, `core.py:154`). 0이면 코어는 아무것도 숨기지 않고(`impl.h:68`, `GPU.cpp:105`, `impl.h:161`) foreground/window 기록도 하지 않는다(`GPU.cpp:4317`, `GPU.cpp:6521`).

### 1.7 `retro_srw_set_ready_parts(const unsigned *ids, unsigned count)` (시작 후, 수시로)

- 호출 시 `SRWWAsyncParts=true`가 되고 준비 표가 통째로 교체된다 (`impl.h:39-42`). 이후 준비 표에 없는 바인딩은 매 프레임 `control` bit31이 켜져 **네이티브로 남는다**(`impl.h:123`, `impl.h:180-182`).
- PC는 시작 직후(`player_worker.py:60`)와 준비 세대가 바뀔 때(`core.py:206-216`) 호출한다. 목록은 "굽힌(sqlite에 있는) 소스 바인딩 + 메모리에 준비된 것"을 `source_binding` 별칭까지 펼친 것 (`parts.py:113-115`, `parts.py:211-218`, `parts.py:318-333`).
- **한 번도 호출하지 않으면** `SRWWAsyncParts=false`이므로 등록된 모든 파츠가 즉시 숨겨진다. 이때 호스트가 텍스처를 못 그리면 그 픽셀은 사라진다(3장).

### 1.8 `retro_srw_add_dynamic_part(hash, material, binding)` (선택)

- 미등록 OBJ를 호스트가 런타임 조립(`parts.py:146-189`, `tile_compositor`)한 뒤 코어에 알리는 경로. 등록하면 그 OBJ도 숨겨진다 (`impl.h:43-45`, `impl.h:102-105`). `SRWW_ROBOT_SPRITE_HD`가 켜졌을 때만 보냄(`core.py:207-212`). MVP에서는 호출하지 않는다.

### 1.9 코어 등록이 없는 것

- 배경 라이브러리 `graphics/backgrounds/library.json`(16개): 코어 등록 없음. 호스트가 매 프레임 VRAM을 읽어 CRC로 식별(`core.py:120-127`, `core.py:259-276`). 코어는 이 배경을 숨기지 않는다.
- 전투 배경 `graphics/battle_backgrounds/catalog.json`(344개, 이미지 존재 336개 측정) + `runtime_index/{index.json,references.npy,possible_colors.npz}`: 코어 등록 없음. 호스트가 네이티브 픽셀로 식별(`emulator/hd_battle_backgrounds.py:121-173`).
- 글꼴·대사·초상화·UI 라벨·현지화 화면·HUD 바·맵 타일/아이콘·시나리오 배경·메뉴 장면: 모두 호스트가 네이티브 픽셀을 인식해 위에 덧그리는 오버레이(`renderer.py:142`, `renderer.py:283-289`, `renderer.py:315-326`). 코어 등록 없음.

### 1.10 용도별 필요 등록

| 용도 | 필요한 호출 | 비고 |
|---|---|---|
| (a) 로봇/OBJ 파츠 | 1.1 (필수), 1.2 (유닛 폴백 분류 정확도), 1.6, 1.7(권장) | 1.3은 비로봇 재색칠용 |
| (b) 컷인 | 1.4, 1.5, 1.6 | id 1(기본 내장 카즈마 컷인)은 등록 없이도 1.6만으로 매칭됨(`GPU.cpp:180-186`) |
| (c) 배경 | 없음(BG 타일이 파츠 라이브러리에 있으면 1.1이 BG 타일을 숨김) | 라이브러리·전투 배경은 호스트 식별 |
| (d) 글꼴/HUD | 글꼴은 없음. HUD 숫자 등 OBJ는 1.1/1.3 | 1.3 대상이 재색칠 필요 |

---

## 2. 프레임별 데이터

`Core.run`(`core.py:232-278`)이 `retro_run` 직후, 비디오 콜백이 왔을 때만(`core.py:233-234`) 읽는다. 코어는 `retro_run` 시작 시 `SRWWHD_Frame++`, `SRWWHD_Info[0]=0`, `SRWWHD_Layers` 0, `SRWWRobot_Info[0]=0`, `SRWWBeginPartsFrame()`(foreground·window·parts·bgparts·BG 마스크 초기화)을 한다 (`lr.cpp:2187`, `impl.h:151-158`). 따라서 아래 데이터는 방금 비디오로 나온 그 프레임의 것이다.

"위 화면 엔진"은 `SRWWTargetEngine()` = 메인 엔진이 위 디스플레이면 0, 아니면 1 (`impl.h:50`). 위 화면 데이터는 그 엔진, `sub_*`는 다른 엔진이다.

### 2.1 `retro_srw_get_hd_state(unsigned out[12])` → `core.hd`

`SRWWHD_Info` 복사 (`lr.cpp:118`). 가장 앞(우선순위 높은) 컷인 평면 1개.

| 인덱스 | 의미 | 근거 |
|---|---|---|
| 0 | 컷인 id (0=없음, 1=내장 카즈마) | `GPU.cpp:200` |
| 1,2 | BG 스크롤 xOffset, yOffset (9비트; ≥256이면 −512로 해석) | `GPU.cpp:200`, `renderer.py:215` |
| 3,4 | native_w, native_h | `GPU.cpp:201` |
| 5 | BG 레이어 0–3 | `GPU.cpp:201` |
| 6 | BG 우선순위 0–3 | `GPU.cpp:202` |
| 7 | MASTER_BRIGHT 레지스터 값 | `GPU.cpp:202`, `GPU.cpp:6599` |
| 8 | SCR[0]의 타일 번호(base) | `GPU.cpp:107,202` |
| 10 | **호스트가 덮어씀**: HD 사용 여부 | `core.py:237`, `core.py:290` |
| 9, 11 | 사용 안 함 | — |

### 2.2 `retro_srw_get_hd_layers(unsigned out[4][12])` → `core.cutin_layers` (4×12 uint32)

`SRWWHD_Layers` 복사 (`lr.cpp:119`). 행 = BG 레이어 0–3. 각 행 열 0–8은 2.1과 같은 의미, 그 레이어의 **첫 래스터 창**의 값 (`GPU.cpp:189-197`). `row[0]==0`이면 그 레이어에 컷인 없음.

### 2.3 `retro_srw_copy_layer_ids(u8 out[192][256])` → `core.ids`

위 엔진의 `_renderLineLayerIDNative` (`lr.cpp:170`, `GPU.h:1645`). 최종 픽셀을 소유한 레이어: 0–3=BG0–3, 4=OBJ, 5=backdrop (`GPU.h:1065-1070`; 프레임 시작 시 5로 초기화 `GPU.cpp:2747`). **코어가 숨긴 스프라이트/BG 타일은 이 값에 나타나지 않는다**(그 뒤에 있던 레이어 번호가 남음).

### 2.4 `retro_srw_copy_parts(u32 parts[128][8], u8 owners[192][256])`

`SRWWParts`, `SRWWNativeOwner` 복사 (`lr.cpp:148-151`). OAM 인덱스 `i`의 행. `row[0]==0`이면 HD 파츠 아님 (`impl.h:65`에서 프레임마다 0으로 지움).

| 열 | 의미 | 근거 |
|---|---|---|
| 0 | binding id (1-based) | `impl.h:119` |
| 1 | OAM attr0 (`a`) | `impl.h:119` |
| 2 | OAM attr1 (`b`) | `impl.h:119` |
| 3 | OAM attr2 (`c`) | `impl.h:119` |
| 4 | 그 프레임 실제 RGB 내용 해시(재색칠 판단용) | `impl.h:119`, `parts.py:638` |
| 5 | MASTER_BRIGHT (reg 0x6C) | `impl.h:121` |
| 6 | BLDALPHA (reg 0x52) | `impl.h:122` |
| 7 | BLDCNT (reg 0x50) \| bit31 = "이번 프레임 네이티브 유지" | `impl.h:123`, `impl.h:141` |

`owners[y][x]` = 그 픽셀을 그린 OAM 스프라이트 번호(`_sprNum` 줄 복사, `GPU.cpp:5825`). **`ids==4`인 픽셀에서만 의미가 있다.** `_sprNum`의 초기화는 리셋(`GPU.cpp:1673`)에서만 찾았으므로 다른 픽셀 값은 신뢰하지 말 것.

### 2.5 `retro_srw_copy_part_palettes(u16 out[128][16])`

OAM `i`가 HD 파츠일 때 그 스프라이트의 현재 16색 팔레트(BGR555) (`impl.h:120`, `lr.cpp:147`). 재색칠 입력.

### 2.6 `retro_srw_copy_rendered_obj(u8 out[1024])` → `core.obj`

위 엔진 OAM 1 KB 스냅샷(그 프레임 첫 스프라이트 렌더 시점) (`impl.h:67`, `lr.cpp:122`). 용도: 네이티브 OBJ 우선순위 `(attr2>>10)&3`(`parts.py:774-775`), affine 행렬(`parts.py:600-601`).

### 2.7 `retro_srw_get_robot_state(int out[8])`

`out[0]` = 이번 프레임 위 화면 HD 파츠 수 (`impl.h:124`). 렌더에 쓰이지 않음.

### 2.8 `retro_srw_copy_bg_parts(u32 out[3200][8])`

`SRWWBGParts[4*800*8]` (`hd.h:24`, `lr.cpp:152`). 레이어 `L`의 항목은 `L*800 .. L*800+799` 행, `row[0]==0`에서 끝. 8×8 타일 1개 = 1행.

| 열 | 의미 | 근거 |
|---|---|---|
| 0 | binding id | `impl.h:178` |
| 1 | 맵 항목 `entry & 0xC00` (bit10 H-flip, bit11 V-flip) | `impl.h:178` |
| 2,3 | 화면 x, y (int32, −7..255 / −7..191) | `impl.h:165,178` |
| 4 | BG 레이어 | `impl.h:178` |
| 5 | BG 우선순위 | `impl.h:178` |
| 6 | MASTER_BRIGHT | `impl.h:180` |
| 7 | BLDCNT \| bit31(준비 안 됨 → 네이티브 유지) | `impl.h:180` |

### 2.9 `retro_srw_get_bg_info(layer, unsigned out[9])` (layer 0–3)

`[BGnCNT, tileMapAddress, tileEntryAddress, xOffset, yOffset, width, height, isVisible, priority]` (`lr.cpp:86-95`). PC는 `bgpriors[layer]=out[8]`, `bgpriors[4]=bgpriors[5]=4`(OBJ·backdrop은 가장 뒤로 취급; `core.py:68`, `core.py:261`), 전체를 `bg_layout`으로 보관(`core.py:262,274`).

### 2.10 `retro_srw_copy_foreground(u64 out[192][256])` → `effect_foreground` (반환 1=유효)

`retro_srw_foreground_format()==3`일 때만 사용 (`core.py:53`, `lr.cpp:154`). BG 픽셀이 1차 대상으로 알파 블렌딩될 때 그 BG가 기록 (`GPU.cpp:4317-4325`):

| 비트 | 의미 |
|---|---|
| 0–14 | 그 BG의 원색 BGR555 |
| 15–17 | BG 레이어+1 (0=기록 없음) |
| 18–22 | EVA (≤16) |
| 23–27 | EVB (≤16) |
| 32–36 | BLDCNT 2차 대상 BG0–3,OBJ 비트 |
| 37–39 | 그 BG가 쓰기 직전 그 픽셀의 레이어 ID(0–5) |

### 2.11 `retro_srw_copy_window(u8 out[192*256])` → `window` (반환 1=유효)

픽셀마다 bit0–4 = BG0–3/OBJ가 윈도우 테스트를 통과(또는 레이어 꺼짐) (`GPU.cpp:6521-6528`, `lr.cpp:155-156`). 기본 0x1F (`impl.h:153`). PC는 전부 0x1F면 None 취급 (`core.py:240`).

### 2.12 `retro_srw_copy_sub_parts(parts, owners, oam, palettes, layers, priorities)` (아래 화면)

다른 엔진에 대해 2.4/2.3/2.6/2.5와 같은 형식: `parts u32[128][8]`, `owners u8[192][256]`, `oam u8[1024]`, `palettes u16[128][16]`, `layers u8[192][256]`(레이어 ID), `priorities u8[4]`(BG 우선순위) (`lr.cpp:160-169`, `core.py:157-161`, `core.py:258`). PC는 `priorities`를 길이 6, 기본 4 배열에 받는다(`core.py:159`). 아래 화면에는 BG 파츠·컷인·foreground·window가 없다(코어가 위 엔진에만 기록: `impl.h:161`, `GPU.cpp:105`, `GPU.cpp:4317`, `GPU.cpp:6521`).

### 2.13 기타 (선택)

- `retro_srw_copy_bg_banks(layer, u8 out[4096], 4096, NULL)` + `retro_srw_copy_effect_debug(NULL,NULL,u16 bgpal[256],NULL)`: 회색 컷인을 팔레트로 물들이는 기능용. 컷인 레이어 타일들이 전부 같은 뱅크일 때만 `(bank, bgpal[bank*16..+16])` (`core.py:241-252`, `GPU.cpp:207-217`).
- `retro_srw_copy_vram(addr, buf, n)`: 배경 라이브러리 식별용 (`core.py:265-268`, `lr.cpp:97-102`).
- `retro_srw_copy_unknown_parts(rows u32[128][8], pixels u8[128][4096], palettes u16[128][16])` / `retro_srw_copy_sub_unknown_parts`: 런타임 조립용 미등록 OBJ (`impl.h:106-114`, `core.py:221-230`). MVP 불필요.

---

## 3. HD 등록 후 코어가 네이티브에서 빼는 픽셀

`SRWWHD_Enabled=1`이면 코어는 다음을 **그리지 않는다**. 호스트가 그리지 않으면 그 자리에 뒤 레이어(또는 backdrop)가 보인다.

### 3.1 OBJ 스프라이트 (위·아래 화면 모두)

- `_SpriteRenderPerform`이 스프라이트마다 `SRWWHD_ShouldSkipRobot`이 참이면 `continue` (`GPU.cpp:5408`). 아래 엔진도 같은 함수를 지나며 `SRWWSubParts`에 기록한다 (`impl.h:60-61`).
- 숨김 조건: 그 OAM의 `parts[i][0]≠0` **그리고** `parts[i][7]` bit31이 꺼짐 (`impl.h:148`).
- 파츠 행이 만들어지지 않는(=항상 네이티브) 스프라이트: affine 아님+double-size 비트(=숨김 OBJ), shape 3, OBJ 모드 ≥2(윈도우/비트맵), 화면 밖, 8bpp 확장 OBJ 팔레트 사용, 바인딩 없음 (`impl.h:80-88`, `impl.h:106-115`).
- bit31이 켜지는 경우: (1) `set_ready_parts`를 한 번이라도 불렀고 준비 표에 없는 바인딩 (`impl.h:123`), (2) 전투 레이아웃(BG3 tile base 0x06018000, BG2 0x06010000)에서 같은 팔레트 그룹의 네이티브 비율이 `SRWW_UNIT_FALLBACK_PERCENT`(기본 10%) 이상인 그룹 전체(effect 파츠 제외) (`impl.h:126-143`). 이 경우 코어가 네이티브로 그리므로 호스트는 그리지 않는다(`parts.py:813-815`).

### 3.2 BG 타일 (위 화면만)

- `SRWWPrepareBG`가 레이어당 프레임 1회, 화면에 걸친 8×8 타일마다 내용 해시를 `SRWWPartBindings`에서 찾아 `SRWWBGParts`에 기록 (`impl.h:160-183`). 준비된(또는 비동기 모드가 아닌) 바인딩이면 그 8×8 영역을 `SRWWBGMask[layer]`에 표시 (`impl.h:181-182`).
- 픽셀 합성 시 `SRWWBGMask[layer][y*256+x]`이면 그 BG 픽셀을 버림 (`GPU.cpp:4326`). foreground 기록은 그보다 먼저 남는다 (`GPU.cpp:4319-4325`).
- 적용 제외: 레이어 0의 `sy≥120` 타일(대사·글꼴·초상화 영역) (`impl.h:166`), 텍스트 BG가 아닌 레이어, 8bpp+확장 BG 팔레트 (`GPU.cpp:6600`), 그 레이어에 id>1 컷인이 잡힌 프레임 (`GPU.cpp:6600`), 레이어당 800개 초과분 (`impl.h:176`).
- 주의: 위치는 그 레이어 첫 래스터 시점의 스크롤로 한 번 계산된다(`impl.h:162-165`). 프레임 중 스크롤이 바뀌는 래스터 효과에서는 마스크 위치와 실제 위치가 어긋날 수 있다(코드상 추론, 실측 안 함).

### 3.3 BG 레이어 전체 (id 1 컷인만)

- `SRWWHD_ShouldSkip`이 참이면 그 BG 라인 전체를 그리지 않는다 (`GPU.cpp:6598-6599`). 참을 반환하는 것은 **id==1**(내장 카즈마 컷인, 위 엔진 BG1, `SRWWHD_SIGNATURES`)뿐이다 (`GPU.cpp:180-186`, `GPU.cpp:203`).
- id>1 컷인은 `false`를 반환하므로 **네이티브 컷인 픽셀이 그대로 남는다**(`GPU.cpp:203` 주석 "Observed cut-ins retain native UI and raster windows"). 호스트는 그 위에 HD를 덮는다. 대신 그 레이어의 BG 파츠 처리는 꺼진다(`GPU.cpp:6600`).

### 3.4 숨기지 않는 것

배경 라이브러리, 전투 배경, 글꼴, 초상화, 메뉴, 맵 타일, 미등록 OBJ(`add_dynamic_part` 전): 코어는 그대로 그린다. 호스트 오버레이를 생략해도 픽셀이 사라지지 않는다.

---

## 4. 합성 알고리즘

GPU 경로의 기본 그리기 연산은 `Surface.draw(image, rect, mask, mask_rect, alpha, foreground, foreground_mode, gradient)`이며 셰이더는 `gpu.py:29-46`이다. GLES2 이식 시 이 셰이더를 그대로 옮기면 된다.

### 4.0 기본 그리기 연산(셰이더) 정의

입력: `picture`(RGBA), `rect`(목적지 HD 사각형), 선택 `mask`(+`mask_rect`), `alpha`(그림 알파 사용 여부), 선택 `foreground`(+모드), 선택 `gradient`.

```
p = picture 샘플 (선형 필터; nearest=True면 Pillow nearest 테이블)        gpu.py:38-39
a = alpha ? p.a : 1                                                        gpu.py:39
if gradient: level = dot(p.rgb, (.299,.587,.114)); p.rgb = gradient[level] gpu.py:40
if mask: a *= mask[nearest(HD픽셀→mask_rect 안 좌표)].r (L 마스크) / .a (RGBA)  gpu.py:41
if foreground mode 1: e = fg[HD픽셀→256x192 nearest];
     p.rgb = clamp(p.rgb * (e.a*255/16) + e.rgb)                           gpu.py:42
     -> 결과 (src-alpha 블렌드)  out = p*a + dst*(1-a)                     gpu.py:46
if foreground mode 2: eva=e.r*255/16, evb=e.g*255/16;
     color = (p.rgb*eva*a, a*(1-evb)) ; 블렌드 ONE, ONE_MINUS_SRC_ALPHA
     -> out = p*eva*a + dst*(1 - a + a*evb)                                gpu.py:43, 203-205
```

GLES2 차이: `texelFetch`·`usampler2D`·`gl_VertexID`·`int` 정수 텍스처가 없다. 정점 속성으로 사각형을 그리고, nearest 좌표는 `floor((d+0.5)*N/M)`로 계산해 `(index+0.5)/N`을 `GL_NEAREST`로 샘플하거나 RGBA8에 인코딩한 좌표 테이블을 쓴다. 960폭에서 정수 좌표를 다루므로 프래그먼트 `highp` 지원이 필요하다(`GL_FRAGMENT_PRECISION_HIGH`). NPOT 텍스처는 `CLAMP_TO_EDGE`, 밉맵 없음.

### 4.1 위 화면 (`render_top`, `renderer.py:112-290`)

1. **foreground 준비**: 기록 픽셀(`(rec>>15)&7 ≠ 0`)이 없으면 None (`renderer.py:114-119`, `fg.py:91-94`).
2. **컷인 목록**: `cutins=[hd]`(hd[0]≠0일 때). HD가 켜져 있고 `cutin_layers`에 알려진 id(1 또는 라이브러리 id) 행이 있으면 그 행들로 대체, `(priority, layer)` 내림차순(뒤→앞) 정렬 (`renderer.py:120-125`, `emulator/cutin_assets.py:15`).
3. **전투 판정**: `is_battle = hd[0]≠0 or (bg_layout[3].tileEntry==0x06018000 and bg_layout[2].tileEntry==0x06010000)` (`renderer.py:136-140`). `cyan` = 네이티브 행 124–131에서 R<64,G>96,B>96 픽셀이 80개 이상 (`renderer.py:134-135`).
4. **바탕**: 네이티브 위 화면을 nearest로 W×H 확대 (`renderer.py:159`, `gpu.py:237-238`). 전투/컷인 중에는 글꼴 렌더러가 글자를 지운 `clean_native`를, `hud_mask` 영역은 `_heal_native`를 쓴다(`renderer.py:155-158`). 메뉴 장면이면 바탕 대신 메뉴 장면(`renderer.py:150-153`).
5. (HD일 때) **메뉴 장면** `menu_scene.compose` (`renderer.py:163`, `emulator/menu_scene.py:48-112`). 메뉴가 아니면:
   - **복원 마스크**: `hd[0]>1`이고 컷인보다 뒤(우선순위 값이 큰) BG가 있으면, 컷인 레이어 픽셀(`ids==row[5]`, `restore_rect`가 있으면 그 사각형으로 제한)을 모아 `restoration`으로 하고, 가장 뒤의 "알려진"(배경이 매칭된) 레이어를 `restore_layer`로 정한다. 파츠 가시성용 `parts_layer_ids`에서 그 픽셀을 `restore_layer`로 바꾼다 (`renderer.py:165-188`). 목적: 네이티브 컷인 픽셀(3.3)을 HD 배경으로 지움.
   - **전투 배경** `battle_backgrounds.compose` (4.4.2) → **배경 라이브러리** `backgrounds.compose`(전투 배경이 이미 대체한 레이어 제외) (4.4.1) (`renderer.py:189-191`).
   - 전투가 아니면 시나리오 배경, 맵 타일, 맵 아이콘 (`renderer.py:192-195`).
6. (선택) xBRZ 네이티브 OBJ 필터 (`renderer.py:196-202`). 기본 꺼짐(`emulator/robot_sprite_switch.py:28-30`).
7. **컷인 반복 평면 전개**: `repeat_native_plane`이고 그 레이어 하드웨어 크기가 256×256이면 `(x%256, x%256−256) × (y%256, y%256−256)` 4장으로 복제 (`renderer.py:203-213`).
8. **파츠 + 비(非)파일럿 컷인 합성** `parts_renderer.compose(top, parts, obj, parts_layer_ids, owners, bgpriors, bgparts, part_palettes, effect_foreground, background_planes=비파일럿 컷인, window)` (`renderer.py:262-267`, 4.2). 파일럿 컷인 = id 1, `presentation_role=='pilot_foreground'`, 이름 `compact_pilot_bg_`, 이미지 `compact_pilot_cutins/` (`renderer.py:27-29`).
9. **파일럿 컷인**: 파츠 전부 뒤에, 2의 순서대로 (`renderer.py:270-272`).
10. **전투 대사 띠 복원**: HD·전투·`cyan`이면 `clean_native(native)[128:192]`를 nearest로 HD 행 `round(128*H/192)`부터 끝까지 **모든 HD 위에** 다시 그림 (`renderer.py:273-282`).
11. 글꼴(`hd[0]`이면 글자만), 초상화, 글꼴(컷인 없을 때), UI 라벨, 현지화 화면 (`renderer.py:283-289`).

### 4.2 파츠 합성 (`PartsRenderer.compose`, `parts.py:771-927`)

#### 4.2.1 작업 목록과 순서

```
tasks = []
for i in 0..127 with parts[i][0]≠0:   (priority=(parts[i][3]>>10)&3, kind=0, item=i, row)   parts.py:773-776
for each bgparts row r (r[0]≠0):       (priority=r[5],            kind=1, item=r[4], r)     parts.py:777-779
for each 비파일럿 컷인 c:               (priority=c[6],            kind=1, item=c[5], draw)  parts.py:780, renderer.py:263
sorted(tasks, key=(priority, kind, item), reverse=True)   # 뒤 → 앞                         parts.py:796
```

결과: 우선순위 값 큰 것 먼저; 같은 우선순위에서 BG(kind 1)가 OBJ보다 먼저(=OBJ가 위); BG끼리는 레이어 번호 큰 것 먼저; OBJ끼리는 OAM 번호 큰 것 먼저(작은 번호가 위). DS 하드웨어 규칙과 같다. 컷인 작업은 4.3의 `draw_cutin`을 그 자리에서 호출 (`parts.py:797-799`).

#### 4.2.2 행 해석

- OBJ: `a,b,c = row[1..3]`, `x=b&511`(≥256→−512), `y=a&255`(≥192→−256), `control=row[7]` (`parts.py:806-809`).
- BG 파츠: `bid,flip,x,y,layer,_,bright,control = row`, x/y는 int32 부호 복원, 내부 행을 `[bid, 0, (flip&0xC00)<<2, priority<<10, 0, bright, 0, control]`로 만들어 OBJ와 같은 경로로 보냄(즉 bit12=H-flip, bit13=V-flip) (`parts.py:800-805`).
- `bit31`이 켜졌으면(네이티브 유지) 그리지 않음. 단 일시정지 중(`allow_native_fallback`)에는 그림 (`parts.py:813-815`, `renderer.py:267`).

#### 4.2.3 스프라이트 그림 만들기 (`sprite`, `parts.py:597-738`)

1. `spec = bindings[binding-1]`, `source = spec.source_binding or binding`. 격리(`quarantined_parts.json`) 목록이면 None (`parts.py:598-604`, `parts.py:297-316`).
2. 텍스처 = 소스 바인딩의 4× 텍스처(5장)를 `round(w*SCALE)×round(h*SCALE)`로 LANCZOS 축소 (`parts.py:631-634`). GLES2에서는 4× 텍스처를 그대로 목적 사각형에 선형(또는 밉맵) 샘플해도 된다(작은 차이).
3. **재색칠**(4.3.4): `spec.palette_rgb`(별칭 바인딩 고정 팔레트) 또는 `dynamic_palette`이고 `row[4]≠spec.hash`일 때의 실시간 팔레트(`part_palettes[i]`, BGR555→8비트 `c*255//31`) (`parts.py:637-642`).
4. **affine**(`a&256`): 행렬 번호 `(b>>9)&31`, `pa,pb,pc,pd` = OAM 바이트 `(index*4+k)*8+6`의 int16 /256. `fw,fh = w,h`(double-size `a&512`이면 ×2). PIL 역사상: 출력 `(X,Y)`(HD 픽셀) → 입력 `(pa*X+pb*Y+(w/2−fw/2*pa−fh/2*pb)*SCALE, pc*X+pd*Y+(h/2−fw/2*pc−fh/2*pd)*SCALE)`, BICUBIC, 출력 크기 `round(fw*SCALE)×round(fh*SCALE)` (`parts.py:600-601`, `parts.py:723-726`). affine이면 flip 무시.
5. 아니면 `b&4096` 좌우 반전, `b&8192` 상하 반전 (`parts.py:727-729`).
6. **MASTER_BRIGHT**(`row[5]`): `mode=v>>14`, `amount=min(v&31,16)/16`; mode1: `rgb += (255−rgb)*amount`; mode2: `rgb *= (1−amount)` (`parts.py:730-735`). 네이티브 바탕은 코어가 이미 밝기를 적용했으므로 HD 파츠에도 적용해야 맞는다.

#### 4.2.4 위치와 영역

```
px, py = round(x*SCALE), round(y*SCALE)                                     parts.py:816
left  = max(0, floor(px/SCALE)),  upper = max(0, floor(py/SCALE))
right = min(256, ceil((px+art.w)/SCALE)+1), lower = min(192, ceil((py+art.h)/SCALE)+1)   parts.py:817-818
```

#### 4.2.5 가시성 마스크 `PartVisibility.mask` (`vis.py:17-54`, C 구현 `vis.c:8-19`)

생성 인자: `layers`=레이어 ID(복원 적용된 `parts_layer_ids`), `owners`, `bgpriorities`(길이 6), `objpriorities = (obj OAM attr2>>10)&3`(128개) (`parts.py:774-775,781`). `mask(left,top,right,bottom, priority, kind, item, control, blend)`:

네이티브 픽셀마다(`vis.c:11-17`):
```
L = layers[p]
visible = (L==5)                                        # backdrop 위에는 항상
if L<4:  visible |= bgprio[L] > priority
                 || (bgprio[L]==priority && (kind==0 /*OBJ*/ || L > item))
         if alpha_bg && ((control>>L)&1): visible = 1    # 반투명 1차 대상 BG 아래
elif L==4: o = owners[p]
         visible = objprio[o] > priority || (objprio[o]==priority && o >= item && kind==0)
alpha_bg = (control&0xC0)==0x40 && control bit (kind ? 8+item : 12)       # 알파 모드 + 이 파츠가 2차 대상
out = visible ? 255 : 0 ; state = 0(전부 가림) / 1(일부) / 2(전부 보임)
```

`blend_mask`(`vis.py:41-54`, C에는 없음): `blend`(OBJ면 `row[6]`=BLDALPHA, BG 파츠면 첫 활성 OBJ 파츠의 `row[6]`, 없으면 None — `parts.py:782,823`)가 있고 `alpha_bg`이고 `EVB<16`이면, 앞쪽 1차 대상 BG 픽셀(`bgprio<priority` 또는 같고 `L<item`&BG)에서 마스크를 `×EVB/16`으로 약화하고 state를 다시 계산.

#### 4.2.6 foreground(BG 알파 블렌딩 앞 레이어)

`effect_foreground`가 있고 영역에 기록이 있으면 (`parts.py:825-840`):

```
target = kind ? item : 4
eligible(p) = rec.layer ∈ 0..3
  && (ids==rec.layer || (energy && ids==4))
  && (rec.targets>>target)&1
  && front && adjacent                                               fg.py:65-81
front    = fprio < priority || (fprio==priority && rec.layer<target && target<4) || energy
energy   = target==4 && EVA>0 && EVB==16 && fprio==priority        # 가산 빔이 같은 우선순위 유닛을 덮음
behind   = dest<4 && (dprio>priority || (dprio==priority && (target==4 || dest>target)))
adjacent = dest==target || dest==5 || behind
(fprio = bgprio[rec.layer], dprio = bgprio[dest])
eligible &= (ids!=4) || (visible!=0)                                 parts.py:831
visible[eligible] = 255                                              parts.py:839
```

그릴 때 foreground 평면(256×192 RGBA, `fg.py:97-125`): eligible 픽셀은 `rgb = ((c5*255+15)//31 * EVA)//16`, `a = EVB`; 그 외 `rgb=0, a=16`. 셰이더 모드 1로 `HD*EVB/16 + BG색*EVA/16`이 된다(4.0). 즉 DS가 했던 블렌딩을 HD 그림을 2차 대상으로 다시 계산한다.

#### 4.2.7 윈도우

`window`가 있으면 `((window>>(kind?item:4))&1)==0`인 픽셀을 0으로 (`parts.py:843-847`). state 재계산.

#### 4.2.8 그리기 결정 (위 화면, GPU)

```
if state==0: skip                                                     parts.py:848
semi = (a>>10)&3==1   (OBJ 반투명)
if state==2 && (BG || !semi):
    draw(art, rect=(px,py,+w,+h), alpha=True, mask=None)              parts.py:879-881   # 그림 알파 그대로
elif BG || !semi:
    draw(art, rect, alpha=True, mask=native_mask(256x192, 영역 밖 0), mask_rect=(0,0,W,H),
         foreground=foreground ? gpu_plane(priority, target) : None)   parts.py:883-895   # 그림 알파 × nearest 확대 네이티브 마스크
else (반투명 OBJ, CPU 경로):
    local = visible 마스크를 HD 그림 크기로 nearest 변환 (coeff=(1/SCALE,0,px/SCALE-left,0,1/SCALE,py/SCALE-upper))   parts.py:882,896
    if foreground: art = blend_part(art, ...)  # rgb = min(255,(HD*EVB + BG색*EVA)/16)   parts.py:897-899, fg.py:128-142
    mask = art.A * local / 255
    eligible2 = 픽셀 아래 레이어가 BLDCNT 2차 대상((control>>(8+ids))&1)
    mask *= eligible2 ? min(BLDALPHA&31,16)/16 : 1                   parts.py:910-915
    paste(art, (px,py), mask)
```

"그림 알파를 그대로 쓰는 경우"는 state==2이고 반투명 OBJ가 아닐 때뿐이다. 그 외에는 항상 `art.alpha × (nearest 확대된 네이티브 가시성 마스크)`다. 이 때문에 네이티브 계단 모양은 **가림이 있는 경계에서만** 나타나고, 가리는 것이 없는 곳에서는 HD 윤곽이 네이티브 실루엣 밖으로 나갈 수 있다(`emulator/painted_edges.py:50-51` 같은 취지의 주석).

`self_plane`(`fg.py:147-173`): BG 파츠 레이어 자신이 블렌딩 1차 대상이면(페이드 중인 BG) 모드 2로 `HD*EVA + 뒤*EVB` (`parts.py:857-864`, `parts.py:875-878`). 행마다 그 레이어 기록의 EVA/EVB를 쓰고 기록 없는 행은 가장 가까운 행 값.

#### 4.2.9 아래 화면 전용 OBJ 블렌딩 (`obj_blend=True`)

아래 화면만 `obj_blend=True`(`renderer.py:320`). OBJ가 BLDCNT 1차 대상(bit4)+알파 모드이거나 반투명이면 평면 `R = 2차대상 픽셀? EVA : 16`, `G = 2차대상? EVB : 0` (2차 대상 = `(BLDCNT>>(8+ids))&1`, ids 5=backdrop은 bit13) (`parts.py:758-769`). 이런 스프라이트는 바로 그리지 않고 모아 두었다가 앞→뒤 순으로, 앞 스프라이트 실루엣(알파를 네이티브 크기로 BOX 축소 후 ≥128)이 이미 덮은 픽셀을 빼고 모드 2로 그린다(DS는 OBJ 레이어에서 맨 앞 픽셀 하나만 블렌딩) (`parts.py:865-874`, `parts.py:917-924`).

### 4.3 컷인 (`draw_cutin`, `renderer.py:214-261`)

```
x,y = row[1],row[2]; x>=256 → x-512; y>=256 → y-512                     renderer.py:215
position = (round(-x*W/256), round(-y*H/192))                           renderer.py:217
pilot = character_cutin(spec, id)                                        renderer.py:218
visible = cutin_visibility(ids, layer=row[5], priority=row[6], bgprios,
                           owners/obj = pilot ? None : 실제값)          renderer.py:219
   blocked = (ids<4 && (bgprio[ids]<priority || (==priority && ids<layer)))
          || (owners 주어짐 && ids==4 && OAM prio[owner] <= priority)
   visible = !blocked                                                    painted_edges.py:42-52
foreground: eligible = eligibility(target=layer) → visible=255, 모드1 평면     renderer.py:221-226
window: (window>>layer)&1==0 → 0                                         renderer.py:227-230
글꼴이 인식한 대사 글자 사각형(ty>=120, ±2px) → 255                        renderer.py:234-237
region, box = 컷인 그림의 bbox 잘라낸 것과 그 위치                         renderer.py:239, emulator/cutin_assets.py:21-27
rect = (position+box.xy, +region.size)
gradient = cutin_runtime_palettes.json에 있는 id면 회색→색 표               renderer.py:246, 83-110
자기 레이어가 블렌딩 1차 대상이면 foreground=self_plane, 모드 2              renderer.py:247-253
draw(region, rect, mask=visible(256x192), mask_rect=(0,0,W,H), alpha=True, ...)   renderer.py:254
```

- 컷인 가시성은 BG/OBJ 우선순위만 본다. backdrop(5)과 OBJ(파일럿이면 항상)는 가리지 않는다.
- 컷인 그림: `paint_image`(없으면 `image`)를 `(W, round(W*native_h/native_w))`로 LANCZOS, `paint_image`면 알파에 3×3 min→max 필터(`clean_alpha`) (`emulator/cutin_assets.py:29-40`, `emulator/painted_edges.py:5-10`). id 1은 `graphics/kazuma_cutin_hd.png`를 W×(W*3/4)로 (`renderer.py:40`, `emulator/cutin_assets.py:32-33`).
- MASTER_BRIGHT(`row[7]`)는 컷인에 적용하지 않는다(`renderer.py`에 사용처 없음, grep 확인). 의도인지는 코드로 판단 불가 — 확인 필요.
- id 1은 코어가 BG 레이어 전체를 숨기므로(3.3) 반드시 그려야 한다. id>1은 네이티브가 남아 있어 생략해도 사라지지 않는다.

#### 4.3.4 파츠 재색칠 (참고, MVP 제외 권장)

`target_palette`가 있을 때(`parts.py:637-642`):
1. **affine 팔레트 규칙**: 사용 슬롯에서 채널별 `target = a*source + b` 최소제곱, 최대 오차 ≤ `SRWW_PALETTE_AFFINE_TOLERANCE`(34)이면 HD 전체 픽셀에 적용 (`parts.py:644-665`).
2. 아니면 재질 맵(슬롯 인덱스 + 잔차) 기반 재색칠 및 smooth 선택 (`parts.py:666-706`, `parts.py:527-576`). 입력: `native_materials.npz`, `material_slots.npy`, `palette_luts.npz`, 바인딩의 `index_pixels`.
3. 팔레트가 원본과 같아도 `dynamic_palette`이고 `source_binding>5263`이며 `wing_img_first`/`preserve_canonical_paint`/`wing_live_palette`가 아니면, 원본 팔레트와 동떨어진 유채색 프린지를 재질색으로 교체 (`parts.py:707-722`). **이것은 sqlite에 구워지지 않은 런타임 후처리**다(`prepare_texture`는 정렬된 텍스처만 저장, `parts.py:386-390`). Android가 생략하면 해당 파츠에 색 프린지가 남을 수 있다. 바인딩별로 결정적이므로 오프라인에서 미리 적용해 팩에 넣는 편이 낫다.

### 4.4 배경

#### 4.4.1 배경 라이브러리 (`emulator/hd_backgrounds.py:93-139`)

- 식별(코어 데이터로 호스트가): 레이어마다 `bg_info`가 보이고 그 레이어의 서명이 있으면 맵 `width*height/32` 바이트를 `copy_vram(map)`으로 읽어 CRC32, 같은 `(layer, map_crc)` 후보마다 타일 데이터 `tile_bytes`를 `tile_size` 단위로 잘라 `tile_indices` 순으로 이어 CRC32, `(layer, tile_crc, map_crc)`가 맞으면 `(id, xOffset, yOffset, layer)` (`core.py:259-272`). 메뉴(구성 배경 id 7,8 또는 메뉴 바인딩 20개 이상)면 id 9,10을 레이어 2,3에 추가 (`core.py:275-276`).
- 그리기: `art = image`를 `native` 크기×SCALE로 LANCZOS, `periodic`(기본: 이름이 `tower`가 아니면) 경계 페더(`space`는 세로도) (`hd_backgrounds.py:29-39`). `x%=native_w`, `y%=native_h`. `visible = ids==layer`; 32픽셀 미만이면 생략; 네이티브와 기대 픽셀(`native` 이미지를 스크롤해 샘플) 중앙값 오차 > 5면 생략(페이드·다른 장면에서 자동으로 네이티브 유지) (`hd_backgrounds.py:100-106`). `visible |= restoration`(복원 레이어일 때), 레이어 3이면 `|= hud_mask`, `&= window 비트` (`hd_backgrounds.py:107-109`). `(−px, w−px) × (−py, h−py)` 4장으로 감싸 그림, 마스크 = visible 256×192 nearest, 그림 알파 미사용(RGB) (`hd_backgrounds.py:110-122`).

#### 4.4.2 전투 배경 (`emulator/hd_battle_backgrounds.py`)

- 대상 레이어: `bg_layout`의 레이어 3, 2 중 보이고 크기 256/512이며 charbase(`(BGnCNT>>2)&15`)가 레이어3=6, 레이어2=4인 것 (`hd_battle_backgrounds.py:110-119`).
- 식별: `ids==layer` 픽셀 중 최대 128개 표본(64개 미만이면 포기), 서로 다른 색 3개 미만이면 포기. `possible_colors`로 후보 축소(표본 75%의 90%가 팔레트에 있어야). 마지막 보정값 포함 9개 UV 오프셋(±1)에 대해 `references.npy[후보, (y+ys+dy)%h, (x+xs+dx)%w]`(bit15=유효, 하위 15비트 BGR555)와 비교, 유효≥75%, ±1단계 일치≥90%, 정확 일치≥60%인 최고 점수 (`hd_battle_backgrounds.py:121-173`). 실패하면 4프레임 동안 재시도 안 함(`hd_battle_backgrounds.py:133-142`).
- 텍스처: `image`를 `native_size × (W/256, H/192)`로 LANCZOS; `art_owner`가 다르고 팔레트가 다르면 owner/item `native` 차이를 bilinear로 키워 더함; 하드웨어 크기 `(w,h)×scale` 투명 캔버스 좌상단에 붙임 (`hd_battle_backgrounds.py:36-53`).
- 그리기: `px=round((x%w)*W/256)`, `py=round((y%h)*H/192)`, `(−px, art.w−px)×(−py, art.h−py)` 4장, 마스크 = `ids==layer`(+레이어3 `hud_mask`, +복원) `& window`, **그림 알파 × 마스크** (`hd_battle_backgrounds.py:198-220`).

배경 둘 다 MASTER_BRIGHT를 적용하지 않는다. 대신 네이티브 대조 실패 시 그리지 않으므로 페이드 중에는 대개 네이티브가 보인다(전투 배경은 팔레트 필터 기준, 실측 안 함).

### 4.5 아래 화면 (`render_bottom`, `renderer.py:299-328`)

1. 바탕 = 네이티브 행 192–383 nearest 확대 (`renderer.py:310-313`).
2. HD일 때: 시나리오 배경 → 맵 타일 → 맵 아이콘 (호스트 오버레이) (`renderer.py:315-317`).
3. **sub 파츠**: `compose(bottom, sub_parts, sub_oam, sub_layer_ids, sub_owners, sub_priorities, bgparts=None, sub_palettes, obj_blend=True)` — 4.2와 같고 foreground·window·컷인 없음, 4.2.9 적용 (`renderer.py:318-320`).
4. 초상화, 글꼴, UI 라벨, HUD 바, 현지화 화면 (`renderer.py:321-326`).
5. 입력이 같으면 이전 결과 재사용 (`renderer.py:307-309`).

---

## 5. 텍스처 소스

### 5.1 파츠: binding → 텍스처

- 소스 바인딩: `source = spec.get('source_binding', binding)`; 별칭은 소스의 텍스처를 쓰고 팔레트만 다를 수 있다(`palette_rgb`) (`parts.py:603`, `parts.py:637`).
- 저장소: `graphics/parts_baked.sqlite`(이 스냅샷 1.48 GB, `textures` 106,375행). 스키마 `CREATE TABLE textures (key TEXT PRIMARY KEY, w INTEGER, h INTEGER, pixels BLOB, stats TEXT)` (+ `assembly_misses`) (`emulator/parts_disk_cache.py:10-16`, 측정). `pixels` = **무손실 WebP RGBA, `exact=True`**(투명 픽셀 아래 색 보존), 크기 = 네이티브 w,h × 4 (`emulator/parts_disk_cache.py:17-21`, `parts.py:346`). `stats` = 정렬 통계 JSON(렌더에 불필요).
- 키 `texture_key(binding, w, h)` (`parts.py:255-295`):
  ```
  mode = 'painted-attack-bank-v3' if registered_attack_bank
       else 'painted-mini-canvas-v1' if secondary_unit
       else 'painted-wing-v2' if atlas_id=='wing_primary' else 'native-crop-v2'
  version = sha256(hd_parts_registration.py 바이트, CRLF→LF)          parts.py:105-108
  tail = ['continuous-crop-ink-v1', 'store-4x-webp', 'atlas-content-v1',
          image파일명, 크기, blake2b16(image), reference파일명, 크기, blake2b16(reference)]
          (atlas_specs[atlas_id], 없으면 kazuma_parts_atlas_facefix.png / kazuma_parts_atlas_reference.png)
  s = json.dumps([version, mode])[:-1] + ', ' + f'{x}, {y}, {w}, {h}' + ', ' + json.dumps(tail)[1:]
  key = sha256(s).hexdigest()
  ```
  `POLICY`는 `emulator/part_cut_edges.py:9`. 아틀라스 다이제스트는 `graphics/atlas_digests.json`에 캐시 (`parts.py:220-253`).
  **키는 파이썬 소스 파일 해시와 2,657개 아틀라스 파일의 해시에 묶여 있다.** Android에서 재계산하지 말고, PC에서 `binding → sqlite rowid(또는 별도 팩 내 오프셋)` 표를 내보내는 것을 권장한다.
- 폴백(PC 전용):
  - `kazuma_parts_registration.npz`의 `part_N` 배열(스탬프가 맞을 때) (`parts.py:89-94`, `parts.py:606-608`). 이 스냅샷에서 일치 0개(측정).
  - 없으면 `rescue`/`prepare_texture`로 아틀라스에서 즉석 정렬·생성 후 sqlite에 저장 (`parts.py:578-595`, `parts.py:335-390`, `parts.py:610-622`). 런타임 텍스처(조립)는 `prepare_composite_task`.
  - **측정: 등록된 95,079개 중 358개는 굽힌 텍스처가 없다**(대부분 `observed_000` 157개 등). PC는 이들을 즉석 생성하거나 준비 전까지 네이티브로 둔다. Android가 즉석 생성을 하지 않는다면 이 바인딩들은 `set_ready_parts`에서 빼야 사라지지 않는다.
- 크기 조정: 표시 크기 `round(w*SCALE)×round(h*SCALE)`, LANCZOS (`parts.py:633-634`).

### 5.2 컷인

- id 1: `graphics/kazuma_cutin_hd.png`. 기타: `cutins_library.json`의 `paint_image`(없으면 `image`), 경로는 `graphics/` 기준 (`emulator/cutin_assets.py:29-40`). 패키지 빌드에서는 `.png`가 없고 `.webp`가 있으면 그것을 씀 (`emulator/asset_paths.py:5-11`).
- 스크롤: 위치 = `−(x 또는 x−512)*W/256`, `−(y 또는 y−512)*H/192` (4.3). 감싸기는 `repeat_native_plane`이고 BG가 256×256일 때만 4장 복제(4.1-7). 그 외에는 감싸지 않는다.
- 회색 컷인 착색: `graphics/cutin_runtime_palettes.json`(현재 id 168 하나) `ramp`(15단계)와 실시간 뱅크 16색으로 256단계 표 (`renderer.py:83-110`).

### 5.3 배경

- 라이브러리: `graphics/backgrounds/library.json`의 `image`(HD), `native`(대조용), `tile_bytes`, `tile_size`, `tile_indices`, `signatures [[tile_crc, map_crc],...]`, `periodic`, `menu_configuration` (측정, `core.py:121-127`).
- 전투: `graphics/battle_backgrounds/catalog.json`의 `image`, `native`, `native_size`, `art_owner`, `palette`, `uses[{scene,layer}]`; 식별용 `runtime_index/references.npy`(344×256×256 uint16, 약 45 MB), `index.json`, `possible_colors.npz` (`hd_battle_backgrounds.py:25-34`, `hd_battle_backgrounds.py:71-97`).
- 감싸기: 둘 다 네이티브 크기(라이브러리) 또는 하드웨어 BG 크기(전투) 주기로 2×2 타일링 (4.4).

---

## 6. 최소 구현 범위(MVP)

목표: 로봇·컷인·전투 배경을 HD로, 순서 정확, 사라지는 픽셀 없음.

### 6.1 반드시 할 것

1. **등록**: 1.1 → 1.2 → 1.4 → 1.5 → 1.6(1). 1.3(indexed)은 **호출하지 않는다** → 인덱스 매칭 파츠(다른 팔레트로 나온 효과·HUD 숫자)는 네이티브로 남아 재색칠이 필요 없다.
2. 1.1에서 **`palette_rgb` 별칭 바인딩**(재색칠이 필요한 것, 현재 2,106개 보유)은 해시를 0으로 두거나 오프라인에서 재색칠 결과를 별도 텍스처로 구워 넣는다. 둘 중 하나를 하지 않으면 원래 색과 다른 그림이 나온다.
3. **`retro_srw_set_ready_parts`를 반드시 호출**: Android 팩에 텍스처가 실제로 있는 바인딩(별칭 포함)만. 그러면 텍스처 없는 바인딩은 코어가 네이티브로 그린다(3.1). 호출하지 않으면 358개+α가 사라진다.
4. **프레임 읽기**: 2.1, 2.2, 2.3, 2.4(+owners), 2.6, 2.8, 2.9, 2.12. 2.11(window)은 비용이 작으니 포함 권장.
5. **위 화면**: 4.1의 1–4, 5(전투 배경만; 복원은 선택), 7, 8(4.2 전부: 우선순위 정렬, 4.2.3의 flip·affine·MASTER_BRIGHT, 4.2.4–4.2.5 가시성, 4.2.7 윈도우, 4.2.8 그리기 분기와 반투명 OBJ), 9, 10(전투 대사 띠 복원).
6. **id 1 컷인**: 코어가 BG1 전체를 숨기므로 필수(3.3).
7. **아래 화면**: 4.5-1, 4.5-3. sub 엔진에서도 HD 바인딩 스프라이트가 숨겨지므로(3.1) 이것을 빼면 아래 화면 HD 스프라이트가 사라진다. 엔진별로 숨김을 끄는 API는 없다.
8. **BG 파츠**(`bgparts`): 위 화면에서 등록된 BG 타일이 숨겨지므로(3.2) 4.2에 포함해야 한다. `set_ready_parts`에 BG 타일 바인딩을 넣지 않으면 그 타일은 네이티브로 남는다(`impl.h:181`).

### 6.2 미뤄도 되는 것과 그 결과

| 미루는 것 | 픽셀이 사라지나 | 눈에 보이는 결과 |
|---|---|---|
| 글꼴·대사 텍스트, 초상화, UI 라벨, 현지화 화면, HUD 바, 맵 타일/아이콘, 시나리오 배경 | 아니오(호스트 오버레이, 3.4) | 해당 부분이 네이티브 nearest 확대로 보임. 컷인의 대사 글자 사각형 보호(`renderer.py:234-237`)도 빠짐 |
| 메뉴 장면(`menu_scene`) | 아니오 | 즐겨찾기/소개 화면이 일반 파츠 경로로 그려짐(메뉴 바인딩은 4.2가 그림). 격자 배경 HD 없음 |
| 배경 라이브러리(4.4.1) | 아니오 | 맵·기지 배경이 네이티브 |
| 복원 마스크(4.1-5) | 아니오 | 뒤에 배경이 있는 id>1 컷인 둘레에 네이티브 컷인 픽셀 계단이 남음 |
| foreground 블렌딩(4.2.6, 2.10) | 아니오, 그러나 | 반투명 BG 효과(빔·섬광·연기)가 HD 유닛 앞에 있을 때 가시성이 그 픽셀을 막아 **유닛 자리에 구멍**(뒤 배경+효과)이 보임. `blend_mask`(4.2.5, BLDALPHA만 사용)를 넣으면 EVB 비율로 부분 완화됨 |
| self_plane(페이드 중인 BG 파츠·컷인) | 아니오 | 페이드 중 HD가 불투명하게 보임 |
| 아래 화면 OBJ 블렌딩(4.2.9) | 아니오 | 아래 화면 반투명 스프라이트가 불투명 |
| 윈도우(4.2.7) | 아니오 | 전체 화면 섬광 등에서 게임이 끈 레이어 위로 HD 파츠/컷인/배경이 보임 |
| 재색칠(4.3.4), indexed 등록 | 아니오(등록 안 하면) | 피격 섬광·페이드 중 해당 파츠가 네이티브로 바뀜(PC도 로봇은 같은 정책, `core.py:99-107`) |
| 프린지 정리(4.3.4-3) | 아니오 | 일부 파츠 가장자리에 유채색 프린지 가능 — 오프라인 사전 적용 권장 |
| 컷인 착색(gradient) | 아니오 | id 168이 회색으로 보임 |
| 동적 조립(1.8) | 아니오 | 미등록 OBJ는 네이티브 |
| xBRZ | 아니오 | 없음(기본 꺼짐) |

### 6.3 이식 순서 제안

1) 등록+`set_ready_parts`+위/아래 파츠(4.2, 블렌딩 없이) → 2) id 1 및 라이브러리 컷인(4.3) → 3) 전투 배경(4.4.2) → 4) window·`blend_mask` → 5) foreground·self_plane → 6) 오버레이류.
가시성 계산은 `emulator/native_composition.c`가 이미 독립 C 코드이므로 그대로 재사용 가능하다(`vis.c:1` "no emulator core modifications").

---

## 7. 불명확하거나 확인이 필요한 점

1. 컷인·배경에 MASTER_BRIGHT 미적용(4.3, 4.4)이 의도인지 코드로 판단할 수 없다.
2. `owners`의 비-OBJ 픽셀 값 초기화 지점을 찾지 못했다(2.4). PC 코드는 `ids==4`에서만 쓰므로 영향 없음.
3. BG 파츠는 레이어 첫 래스터의 스크롤로 위치가 정해진다(3.2). 래스터 스크롤 장면에서 어긋남 여부는 실측하지 않았다.
4. GLES2에서 Pillow LANCZOS/BICUBIC과 GPU 샘플링 차이는 경계 1px 수준이라 추정하나 PC 결과와 화면 대조가 필요하다.
5. 358개 미구움 바인딩 수, 1.48 GB sqlite 크기는 2026-11-21 스냅샷 측정값이며 팩 갱신 때마다 바뀐다.
