# 22163 중앙 fill까지 포함한 24개 한벌 / 읽기 API 인수

## 최종 후보

- `candidate_complete24.png`:768×512 RGBA,두실제팔레트의full192×64원본영역을4배로각각한번에새로그렸다.
- `complete24_contract.json`:24개(exactRGB/static/effect_part=True/resource=None).앞16개는기존91861~91876과동일hash이므로메인에서갱신,뒤8개는새fill등록.
- full_candidate_cyan.png / full_candidate_white.png:각768×256.
- `complete24_assembled_55.png`, `complete24_assembled_56.png`:실제OAM좌표/반전/우선순위로조립한후보.
- `complete24_native_pair_55/56.png`:왼쪽렌더시점캐시원본/오른쪽후보.

**이24개는아직live설치/굽기/게임재생하지않았다.메인인수필요.기존16그림도교체되므로기존16+새8전부다시구워야한다.**

## 근본 누락 확인

이전내가그린x64..192만으로는완결되지않았다. IMG22163의왼쪽x0..64,y0..64가중앙원형fill이다. 4모양64×64/32×64/64×32/32×32가모두그(0,0)에서잘린부분이다.실제두팔레트라서8개이며16edge+8fill=24개다.

+55의fill OAM26~29는단색cyan(index0/4),+56의whitefill은OAM30~33으로옮겨간다.이전같은OAM번호를따라가색을읽으면+56의다른edge를fill로오인한다. `cached_fill_unique_contract.json`은정확8개hash/index/palette/OAM/priority/좌표/fixture를포함한다. raw index8개가모두ROM22163(0,0)crop과완전일치.두팔레트의같은4크기index배열동일assert는paired_index_validation.json.

fixture: test_current/combat/named_attacks/unit_299/mechanical_cutin_141.state

## 읽기 API 구현/빌드

부모공유수정예약후정확3파일만변경:
- emulator/desmume/desmume/src/srww_texture_cache.h:SRWWCopyCachedOBJ 읽기helper
- emulator/desmume/desmume/src/srww_hd.h:선언
- emulator/desmume/desmume/src/frontend/libretro/libretro.cpp:retro_srw_copy_cached_obj export

기존GPU.cpp는-W로재컴파일만했고코드수정없음. knownlookup/unknownfilter/HDdraw/가림/async/ready규칙미변경.

API unsigned retro_srw_copy_cached_obj(engine,oam,row,rowCount,indices,indexCount,palette,paletteCount)
- row는unsigned8개: w,h,RGBhash,indexhash,material,usedMask,opaque,eight
- indices는최대4096 uint8,indexCount는요소개수
- palette는4bit16 /8bit256개의uint16,paletteCount는요소개수
- engine<2,oam<128,valid,w/h1..64및각출력버퍼capacity검사
- null출력은생략가능.짧은버퍼/범위초과시0반환,출력불변
- 캐시를다시만들지않고기존렌더시점snapshot만복사
- 비활성OAM의이전캐시가남을수있으므로호출자는rendered OAM활성/크기/좌표확인필수

별도진단DLL:desmume_cached_obj_debug.dll,5975552bytes,SHA256=982947d3ff182115550773e8b1fab0795556c987bcad404b5b7425a6b5149a6f
build.log:make-j2 platform=win DESMUME_JIT=1 DEBUG=0,target별도DLL,-WGPU.cpp/-Wlibretro.cpp,exit0.기본DLL교체없음.

정확성검증 api_validation.json:
- known8snapshot에서cacheRGBhash==core.parts[4],indexhash==library,index_pixels==library,palette==core.part_palettes전부True
- invalidengine/OAM/rowshort/indexshort/paletteshort5case전부0반환+출력sentinel불변
- normal_regression_comparison.json:기본DLL과진단DLL에서unit299141/unit333168각120frame, native+parts+owners+unknown전체SHA비교:240frame모두차이0.진단쪽은매frame읽기API호출함.

## 그림 제작과 투명채널 복원

기존16edge와새fill을따로끼우면미세색차이가남아두팔레트각full192×64전체아틀라스를독립imagegen으로다시제작했다.이펙트를통째로그린뒤원본계약crop으로분할하며cut외곽선을넣지않았다. 다른기체/색변형재사용없음.

full_generated_cyan.png / full_generated_white.png가원출력이다. imagegen투명처리가큰순백fill을배경으로오인해회색반투명/alpha0구멍을만들었다.그대로쓰기엔부적합했다.

동일효과의두팔레트index일치를assert한뒤생성cyanfill자체alpha를whitefill지원영역으로사용하고,white생성물에살아있는동일흰핵RGB(각채널>=254)를인접확장하여구멍을복원했다.다른색영역으로확장하지않고첫64×64fill영역에만적용했다. 원본nativealpha/RGB복사나원본색으로codepaint하지않았다. alpha_recovery.json/prepare_complete24.py에재현가능.원출력/복원결과둘다보존.

최종크기에서생성alpha의얇은고립찌꺼기만Min3/Max3으로정리했다.원본mask찍기없음.

## 최종 검사와 시각 판단

공식QA모듈후보메모리검사(audit_complete24.py):
- 20개flags0,whitefill4개는flatflag.원래정확한단색fill이므로의도된단색이며잡음을추가해flag를속이지않았다.
- shape/colour/key/outside/unpaintedflags24개모두0.
- edge16IoU최소0.836,fill8최소0.985.
- palette_alignment24개misplaced0/wrong_colour_share0/slots_never_native없음.

실제OAM오프라인조립2팔레트를직접봤다.큰원본사각patch와검은내부선/투명구멍은없다.하지만cyan중앙에생성그림의미세gradient가반복되며아주옅은직사각색영역이남는다. white중앙에도미세한255/254차이가있다.후보가조립검사를통과했다고'모든이음새완전제거'라고주장하지않는다.메인이그림보고인수여부결정해야한다.원본순수단색에비해새edge의스파이크가날카롭고내부불꽃형태가달라진부분도있다.

## 미인수/폐기 후보

- capture_flat.py/directVRAM계약은렌더이후MMU갱신때문에불일치하여UNVERIFIED_DIRECT_READ.md로사용금지.
- generated_full_cyan/white.png 및candidate_fill8.png는기존16edge와별도그림을합치면patch가남아최종아님.
- quarter_generated.png는whitealpha구멍이있어그대로사용금지.
- 최종은candidate_complete24.png/complete24_contract.json만.

라이브그림/library/DB/defaultDLL/EXE/사용자창변경없음.
