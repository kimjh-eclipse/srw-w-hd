# 흰 회청색 빔 같은 ID 후보6

상태: 미검증 후보. 신규 완료 수 없음. 공식 검사·실제 재생 판정은 Claude 담당이다. 모든 입력은 실제 cached OBJ 관측이고 ROM 패턴에서 추측 확장한 그림이 아니다.

설치 installation_map.json / candidate_atlas.png / native_atlas.png. 후보 SHA256 12dd51e3db8ff129ddc0b4b26046626e3da1de88d7380662897b00da4985a003.

| 기존 ID | actual RGB | 크기 | 실제 source state | 시점 |
|---|---|---|---|---|
| 94834 | 1197390202 | 32×8 | test_current\parts\native_weapon_source_231_952\unit231_weapon952_source.state | +655 / OAM9 |
| 94837 | 3395044551 | 32×32 | test_current\parts\native_weapon_source_237_965\unit237_weapon965_source.state | +540 / OAM2 |
| 94840 | 477780745 | 32×32 | test_current\parts\native_weapon_source_237_965\unit237_weapon965_source.state | +535 / OAM4 |
| 94841 | 1324927907 | 32×32 | test_current\parts\native_weapon_source_237_965\unit237_weapon965_source.state | +535 / OAM5 |
| 94842 | 1220154195 | 16×16 | test_current\parts\native_weapon_source_237_965\unit237_weapon965_source.state | +595 / OAM2 |
| 94846 | 4245804887 | 32×8 | test_current\parts\native_weapon_source_231_952\unit231_weapon952_source.state | +660 / OAM6 |

## 실제 역할·팔레트

원래 machine-lost로 분류됐지만 실제 그림은 흰색·회청색 빔/속도 FX다. 이름 pink_base와 다르게 이 실제 사용색은 흰255, 옅은 회보라238·238·246/213·222·238, 회청189·205·222/164·189·213/139·172·197이다. 실제16색BGR555 전체는 계약의 palette_15bit를 보존했다. 다른 분홍 팔레트를 재색칠해 가져온 것이 아니다.

resource는 원래 metadata의 source lookup 값으로 보존했고 실제 owner=None이다. 일부 raw가IMG22410·21748·22409에 중복된 후보를 source_candidate_matches/source_alias_observations.json에 보존했다. source 이미지 소유를 단일 확정하지 않았다. 94834의 동일 raw/fullpalette가 두 retained source 묶음에서 발견된 것은 별칭 관측으로 병합했다.

## 생성 공유

94840/94841은 raw시트의 단순 가로접함을 따라 그리지 않았다. 실제 화면 위치(77,90)/(53,114), 둘 flipXY,56×56공간의(24,0)/(0,24)배치를 사용했다. 겹친8×8 원본RGBA64개가 모두 같았다(screen_overlap_proof.json). 단일 실제 배치 master를 생성·한번정렬한뒤각사각형을잘라역flip하여원래OAM으로돌렸다. 최종 candidate에서다시읽은겹침32×32 HD RGBA전부동일(shared_generated_overlap_proof.json)이다. 다른4개는실제각조각모양을새시트에서제작했다. 94846의두분리수평면과간격도유지했다.

22410담당과대조: cell1↔92487/92493,cell2↔92484,cell3↔92485는raw/indexhash/wh는같아도실제RGB와전체팔레트가다르다. 같은RGBA·alpha를자동재사용하지않고각실제색으로별도제작했다. 근거effect22410_repair15/pink6_raw_palette_overlap.json. 같은resource/fullpalette의다른source사각교차는source_overlap_lookup.json에서없다.

## 제작 및 위험

generated_master535_raw.png / generated_four_raw.png는내장imagegen원본보존. generation_provenance.json에출처SHA/정렬/분할기록. 생성alpha문턱·침식·팽창없음. nativeRGB/alpha를후보에덮어찍지않았다. 실제입력hash/indexbytes/fullpalette/wh일치는mechanical_input_identity.json. 기존lookup/dynamic/renderflags는보존하고역할설명만덧붙였다.

새그림에서빔폭·tip taper·희미한테두리·짧은수평둘간격은원본과차이가남을수있다. 535master겹침픽셀이같다는것이원본형태나시점의공식정답을의미하지않는다. 생성RGBA의저알파RGB잡음은성급하게키색잔여라고지우지않았다. Claude는실제flip/가림/채움폭/색비율을판정해야한다. 라이브/코어/DB/공식QA/물리입력변경없음.
