# 22111 효과 문제7 후보 인계

상태: **같은 기존 ID7개 교체용 미검증 그림 후보**. 정상17 보존. root와 같은 사전 기하 도구에서 경고0이다. 실제 재생/공식 전체 품질 판정은 Claude 대기다. 기하 수치만으로 HD 그림 품질·색·연출이 완료됐다고 주장하지 않는다.

## 설치 입력

- installation_map.json / candidate_atlas.png / native_atlas.png / contract.json.
- 기존 ID92528/92529/92530/92531/92539/92540/92542.
- 후보 SHA256: f778a155e18d6d0c1c945d78ccb20cd900763801241069778720405dfcdc9c25
- normal17 전체 spec SHA는 preserved_normal17.json/latest.json에서 불변이다. 같은ID lookup/dynamic/effect/actual_observed flags는 그대로 유지한다.

## 실제 원본6 / 미관측 ROM 보충1

원본 install_contract는 true_missing_22111/install_contract.json이며 각 행의 source_packet_original로 통째로 보존한다. 실제 cached6개는 unit254/mechanical_cutin_168.state +59(암적색92542)/+61(92529)/+64(92530)/+66(92531,92539)/+69(92528)이다. 실제 OAM/attrs/flip/video_epoch/색16개/원index bytes가 source_contract에 남아 있다.

**92540은 actual_observed=False**이며 frame=None, slot=None인 원래 ROM 보충이다. 관측했다고 바꾸지 않았다. IMG22111 해당16×16 raw index exact와 실제 IMG22110 bank0 full16_exact 팔레트 근거(source_palette_confirmation)가 원래 계약에 있었다. 이 미관측 분리 붉은 조각의 실제 화면 확인은 아직 남아 있다. source_type=ROM_expansion_unobserved를 계약에 명시했고 실제관측6개와 구분한다.

모든7의 actual BGR555 CRC/wh/indexbytes/full16팔레트는 mechanical_input_identity.json에서 기존 바인딩과 일치한다. source_owner=None 보존, 후보 리소스 식별과 실제 업로드 소유 확정을 혼동하지 않는다. 정상/문제 사이 source사각·동일팔레트 교차는 source_intersections.json에서 없었다. hash별 다른 ID는 actual_hash_alias_lookup.json 참조.

## 실제 구조를 지키는 새 그림

밝은6개와 암적색1개는 실제 팔레트가 달라 독립 생성했다. 처음 전체 시트는 도트블록 경계를 그대로 키워 거절 보존했다. 다음 일반 불꽃 해석도92528 12→15성분/92529 1→2/92531 21→27성분이 되어 쓸 수 없었다. 임의로 불씨를 추가/삭제하거나 원본 마스크를 덮어 맞추지 않았다.

원본92528의 중앙22texel과92531의 중앙35texel은 굵은 일반 불꽃 덩어리가 아니라 가는 가지/틈이 있는 연결 네트워크였다. 보류4개(이3개+92540)의 실제36성분을 작은 원본 성분13종으로 분리하고 각자 자체 새 그림 재료를 생성했다(components_unique_contract.json). 같은 component indexbytes/크기/전체 실제팔레트가 모두 같을 때만 같은 자체 생성 RGBA를 여러 위치에 공유한다. 다른색/다른기체를 재색칠해서 빌리지 않았다.

중앙 두 네트워크는 generated_network_two_raw.png로 한 번 더 새로 그려 사각 타일 경계/내부 outline을 없애고 원래 가지·틈·끝 위치를 유지했다. 이 두 영역만 바뀌었고 다른5개 후보 RGBA가 완전히 동일한 근거는 network_edit_preserved_other_five.json이다. 실제 단순한1texel/2texel 불씨 재료는 장식을 발명하지 않고 원래 단색/두색 면을 유지했다.

출력은 생성 RGBA의 기하 정렬/원래 성분 좌표 조립이다. 원본 index/alpha는 참조 그림과 좌표/성분 조사에만 쓰고 출력에 찍지 않았다. 알파 임계삭제, 키색 덧칠, morphology, 강제 연결, source RGB 복사, 후보 재색칠은 하지 않았다. 생성alpha160은 앵커 측정에만 쓰였다.

## 생산 진단 / 남은 판정

- NullCache prepare_texture 뒤 원본 **39개 성분 각각의 bbox**에 유효paint가 모두 남는다. reference_fill_pixels/filled_edge_pixels/unattached removed/artificial cut ink는0. DB/라이브를 바꾸지 않았다.
- 사용자/root 요청에 따라 공통 preflight_candidate_geometry.py를 최종4배 후보에 그대로 사용했다. 원본 occupied index영역과 alpha128의4×4집계로 비교한다. 기준은 기존그대로 IoU<.60 / 미칠>.20 / 원거리밖>.15 경고이며 바꾸지 않았다.
- root_geometry_preflight.json:92528=1.000,92529=1.000,92530=.811,92531=1.000,92539=.750,92540=1.000,92542=.600. 모두 경고0지만92542는 경계값/미칠17.6%여서 실제 암적색 형상 판정이 특히 필요하다. 합격 판정이 아니다.

Claude는 실제 밝은 불꽃/암적색 소멸색, 네트워크의 가는 연결/틈/각, 독립 불씨의 위치와 끝 표시, UI/기체 위 가림/로딩 소실을 확인한다. 단순 불씨가 너무 사각이거나 중앙 네트워크가 여전히 도트 확대로 보이는지도 수치와 별개로 판단해야 한다.92540은 미관측 ROM 보충이므로 실제 나오는 프레임부터 찾아야 한다. 하나라도 부정확하면 해당 후보는 미완료 유지한다.

## 실행 변경 범위

후보/원본/계약/생성출처/기하 준비 자료만 작성했다. 공식 전체 audit·독립 HD 재생·라이브·DB·공유코어/스크립트·EXE·설정·물리입력·화면끄기 변경 없음.
