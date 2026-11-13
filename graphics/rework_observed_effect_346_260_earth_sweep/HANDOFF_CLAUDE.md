# Unit346/w1395 실제 타격 궤적 FX: 346_260

- 5신규 계약 / 실제 source `test_current\parts\native_weapon_source_346_1395\unit346_weapon1395_source.state` +260. root/기계담당이 분리한 타격/먼지 궤적이며 기체/무장 자체그림이 아니다. 원본 install_contract.json의 category='unit'/role='기계조각'은 이관 전 상속명칭이므로 사용하지 말 것. 최종 new_candidate_contract.json은 category='effect', effect_part=True, static.
- 346_260의5+346_270의6은 실제 전체16팔레트가 동일해 한 새 generated_isolated_grid.png(11개 4x3배치)에서 각각같은그림영역을읽는다. 다른색기체/다른팔레트 재색칠/알파공유아님.
- 실제색은 적갈[131,49,41]~tan[213,172,139]. 파랑 index0은투명,초록index6+는 원본에사용되지않음. 이를 밝은주황불꽃으로발명하지않음. rawbytes/실제palette/RGBhash/크기/OAM/좌표/변환은원래 rendered_source_contract와new_candidate_contract에보존, RGBhash모두재계산일치.
- resource=None/owner_confirmed=false, x/y는 가상native_atlas 생산좌표이지 ROM IMG좌표가아니다. sourceIMG 소유추정 없음. 같은 source raw 포함관계는 raw_containment.json에0,교집합재사용을꾸며내지않음.
- candidate_atlas.png [1440, 288] /native [360, 72], SHA `e133c9444747eb0afafb292ad6d0b6cc8ced540dc3da73c9b755a604774cf22e`. 최신exact/indexed중복0. root라이브인수시재대조.
- source bbox는위치/확대율에만사용. 자체생성cell의alpha>=16 bbox로 affine등록하고 전체own RGBA를그렸으며 alpha16threshold로삭제/이진화하거나 nativealpha/RGB를붙이지않음. 자체 생성alpha만보존. 모든5 prepare maxA>=16/support>=.1, nearblank0. runtime/core/DB/라이브 쓰기 없음.
- producer시각확인: gray합성에서 muted 갈색 뾰족 궤적으로보임. 원본보다fan끝이 더뾰족/면분할이강하고 가는파편갯수/두께가달라질수있음. 색위치,절단면끝,실제OAM 회전/flip/효과전면순서와 약한선prepare손실은 Claude실재생대기. 독립audit/실제HD 검증 안함.
- 입력/원생성/최종후보/provenance 보존. 생성은built-in imagegen, CLI/API 미사용. 모니터/플레이어 창 조작 없음.
