# IMG20348 실제 효과 39 신규 그림 인계 (flat4 교정 최종)

## 대상과 원본
- actual cached unit48/w214 source. state/frame/OAM/priority/원색palette/raw/indexhash는 new_candidate_contract.json 보존. IMG20348 raw crop byte일치 source_integrity.json.
- 39 계약 /24 raw /5 실제 fullpalette. group0 mint particles4, group1 lime particles2,group2 단색pale opaque plane4,group3 whitecyan/red energy15,group4 blue/darkred energy14. source별 actual usedRGB를 확인한 색이며 PLT추정/다른 색 재사용 아님.
- g2는 원본 index가 여러개여도 실제 RGBA가 모두[246,255,238]로 합쳐진 사각전체불투명 fill4. 반드시 포함.
- candidate.png SHA `98e90333f109ebb97fd216db93885b8686feda5b9c73cf37f002c44400bd8ee3`,1024×1280 /native256×320. 각 palette 자기 imagegen RGBA, 동일source 부분crop은같은생성pixel 공유(source_overlap.json).

## flat4 최신 교정
- 처음 투명 생성본의 pale plane 내부가 대부분 alpha254였고 외곽 빈AA줄이 있었음. 이를255로칠하지 않고 같은 효과/group2 자기그림을 navy 배경의 imagegen 불투명판으로 새로 제작(generated_2_opaque_material.png).
- 그 불투명 pale plane의 내부 자체RGBA 사각(40,400,500,600),460×200 crop(own_opaque_interior_crop.png)을 native atlas(0,160,64,32)전체로resize. **이미완전불투명인 자체생성pixel만** 사용했고alpha값을코드로255덮지않았음. 원본RGBA/원본mask stamp/다른palette재사용 없음.
- flat4 hashes800048186/2909947323/2774206460/4096401178. 후보와prepare 모두 사각전체 minA255,opaque255 비율100%,중앙100%(flat_opacity_production.json). 코드색채움없음.
- 이 평면4만 바뀌고 나머지35 crop RGBA byte동일 assert(production_report). geometry가있는 전격/광점/연기엔 이 처리를 적용하지 않음. rejected_flat_AA_candidate.png는 실패 보존.

## 생산 확인 및 실제QA 미완료
- prepare39 maxA255/empty0. latest_live_duplicates0(인수시재확인),actualRGBhash계약·원본byte일치. 생산 존재/opacity 확인은 정상HD재생 판정 아님.
- 나머지35는 자기생성alpha 보존,자체alpha>=8 bbox는 위치등록에만 사용하고전체RGBA affine. threshold220/MinFilter없음.
- 작은 광점이 원본보다 큰 glow가 되어서 prepare에서 최대12개의 떨어진 성분을 제거한 crop이 있음. 원래광점 손실인지 추가glow제거인지는 Claude실제확인 필요.
- group3/4 전격/빔의 곡선/끝위치/명도차, palette전환시별도생성형상차이, flat4색/상대위치/UV연결선 실제검증 Claude대기.

## 미완료 구별
- 같은palette unit48+660 whiteflat32 hash1064685919는 IMG20348 raw일치영역이없어이39에포함하지않음. flat_actual_source_candidates.json/matches.json. 별도 실제원본/역할 확정 필요.
- group1 미등록좌하단 teal plane에 자체생성alpha구멍 있음. 현재계약2개는우측광점만사용하여영향없음. 그 미등록영역은미완료이며미래파츠등록에임의재사용금지. 이fullsheet전체의모든source모양완성이라는뜻아님.
- live/library/DB/core/EXE/독립audit/실재생 변경/실행없음.
