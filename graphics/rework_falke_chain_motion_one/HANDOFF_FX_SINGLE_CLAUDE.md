# 팔케 체인건 발사흔적1 — 제작 인계

- `candidate_fx_single.png`,128×32/native32×8.
- SHA256 `fe519528f6174a4a49996ca032e05698a0bbacb9492f76d45e040724e49027ad`.
- `new_fx_single_contract.json`,hash1862538953/index2161431896,atlas`observed_falke_chain_motion_one`.
- 부모가제공한cell4/sourcecached계약보존. unit276무장1125 `source_mechanical_276_1125/source_pose.state` load+1run에서확보한frame0원본이다.
- rawindex를ROM IMG14225(200,48,32,8)과직접비교하여byte동일확인. 실제16색palette로RGBhash재계산일치. sourceowner는이근거로명시,resource=None/static actualpalette/effect_part=true.
- built-in imagegen으로회청색수평발사/속도흔적을새로그렸다. native의32×8을입력참조로하여원래띠의높이·좌우offset·투명gap·실제회청색유지,끝cap/총열/칼/3Dbevel/outline/추가glow금지를명시.
- 생성alpha자체threshold220/min3/max3후nativebbox(0,1,32,8)의위치·크기에맞춤. nativeRGB/alpha를복사하거나native색으로코드채우지않음.
- 공유prepare_texture를메모리atlas/NullCache로직접호출:준비후maxA255,유효2284px,지원면적비1.081,분리성분제거0,referencefill0,cutink0. `fx_single_production.json`/`prepared_fx_single.png`.
- 이결과는준비처리후그림존재에대한생산무결성뿐이며실제HD재생/독립QA가아니다.
- 실제전투에서연속한수평띠의폭·색밴드·생성의미세한끝선이눈에띄는지Claude확인필요. 단정적으로끝cap/레이어/화질이정상이라고판정하지않음.
- 나머지4기계조각은shape담당영역이며수정하지않았다. 기존contract/native_atlas/source파일과live/library/DB/코어/설정/사용자창수정없음.

생성원출력`generated_fx_single.png`,재현`prepare_fx_single.py`,최종프롬프트:동일32:8layout의darkcoolgrayblue수평motionband,실제색#394A5A/#525A7B/#A4B4CD/#C5D5E6,투명gap과offset보존,기계총열/칼/탄알재질이아닌긴발사흔적일부분,끝cap/실린더/bevel/윤곽선추가금지,절단끝열린수평연속면유지,smoothflatcelbands,계단도트/3Dshine/whiteglow/새spark금지,검정투명,캔버스이동금지. built-in image_gen transparent mode.
