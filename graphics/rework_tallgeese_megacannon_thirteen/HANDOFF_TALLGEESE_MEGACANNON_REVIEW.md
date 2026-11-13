# 톨기스III 실제 팔레트 전신 13종 제작 인계

미검증 후보. 공식 품질/실제 HD 재생 판정은 Claude 담당이며 수행하지 않았다. 공유 runtime/라이브/DB/코어 수정 없음.

## 분류

unit5 weapon23 정상 네이티브 메뉴 공격 +150에서 전체14 OAM, 고유13종을 확보했다. 고유1종이 두 OAM에서 반전/위치를 달리해 쓰이므로 그림은 공유한다.13종 모두 현재 exact RGB 연결은 없고 full_attack_018/019의 다른색 indexed proxy만 있다. **미연결13이라고 세지 않고 기존 indexed 그림의 실제 색 기준 재제작13**이다.

모든 raw index bytes가 카탈로그와 독립적으로 ROM primary IMG1200과 일치하고 actual 사용 팔레트는 PLT1201 bank0과 유일하게 일치했다. 따라서 이름/색은 fixture 이름만으로 추정하지 않았다. source_mechanical_fixed_5_23_150/source_pose.state +0이 같은 원본상태 입력이고 source_menu_frame150이다.

## 설치 입력

candidate_atlas.png/native_atlas.png/installation_map.json.4배. SHA25604a116d87aba727f4ead905c5d93d09ef20082c0a1c5e0a6dc3dfbdefc774e7c. mechanical_contract_checks.json에 raw SHA/실제팔레트 RGB/크기/후보 존재 확인. entries의 legacy_indexed_bindings는0-based 메타 인덱스이고 source_contract.binding_id는1-based 코어 ID임에 유의한다. 신규 RGB를 추가해 기존 다른팔레트 proxy를 보존하는 연결 계약이다.

## 실제 원본 교차영역 공유

원본 사각형은 포함 관계뿐 아니라 부분 교차4쌍이 있다. raw bytes와 전체 실제 palette가 같은 교집합만 생성 HD를 공유했다. 개별 파츠를 native 캔버스로 정렬한 뒤 source_coordinate_generated_master.png에 **생성된 HD만** 실제 ROM 좌표대로 배치하고 각 실제 source rectangle을 다시 잘랐다. 원본RGB/alpha를 찍거나, 전체 기체 생성 그림에서 주변 기체를 포함한 사각 crop을 하지 않았다.

shared_source_intersection_proof.json에4쌍의 source 교집합/bytes/팔레트/최종 후보 교차 RGBA 동일을 기록했다. candidate_before_shared.png와 비교해 공유교집합 밖 모든 RGBA 픽셀 불변 SHA도 남겼다.

## 제작 문맥과 미판정 항목

parts_generated.png 내장 imagegen 출처. 회백색/회녹색/파랑 장갑, 빨강노랑 헤드 장식과 녹색 렌즈는 actual native 문맥에 맞춰 생성했다. 작은 조각을 온전한 얼굴/기체로 자동 완성하지 않도록 했다.

native_pose_production.png/candidate_pose_production.png 및 detail 이미지는 실제 좌표/우선순위·OAM 역순/반전을 적용한 제작용 조립이다. 공식 게임 재생 결과가 아니다. 실제 한벌14 OAM 모두 고유13 후보를 사용한다.

Claude 확인 요청: 머리5의 눈/뿔/마스크 실제색과 상단 파랑 연결편4와의 간격; 어깨/팔/주먹0/1/6/10/12의 열린 절단면과 장갑 겹침; 기존 다른 무장/팔레트에서 proxy와 exact 우선순위가 맞는지. 원본의 미묘한 형태/피부가 아닌 기계 그늘색이 정확하다는 공식 판단은 아직 없다. 제작용 조립에서는 큰 사각 절단선이나 다른 기체 침범을 의도적으로 만들지 않았다.
