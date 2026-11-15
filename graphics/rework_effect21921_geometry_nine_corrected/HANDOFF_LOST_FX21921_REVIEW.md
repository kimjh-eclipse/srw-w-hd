# 최신 정정 — 원후보6 / 별도 기하교정3

root의 공통 geometry preflight에서 #94776/#94779/#94786은 실제 지지면/폭/위치가 미달하여 설치하지 않았다. 원본 성분 bbox에 paint가 남는다는 것만으로 실제 면을 보존한 것은 아니었다. installation_map.json은 이3개를 제외한6개만 유지한다. 이전9맵은 before_root_geometry_rejection 파일에 이력 보존한다.

이3개는 candidate_atlas_geometry_v2.png / installation_map_geometry3.json으로 별도 미검증 교정했다. 원본의 제한된 중심/폭 기하 앵커와 자체 생성 고해상도 RGBA만 사용했다. 두 원호는7개 실제 중심 앵커의 monotone PCHIP와1.25native 법선폭, 십자는10개 폭/중심 앵커를 사용한다. 원본 RGB/alpha 전사, 알파 증폭/문턱 조정, 원본 픽셀 마스크 출력은 하지 않았다. 나머지6 RGBA 불변 SHA는 geometry_v2_provenance.json. root의 같은 preflight 재검토 대기이며 완성/합격 주장이 아니다.

# 21921 가는 광선·분리 원호 문제9 후보 인계

상태: **기존 ID9개 같은 ID 교체용 미검증 후보**. 정상6개 보존. 신규 누락/완료 수 증가는 없다. 공식 QA/실제 HD 재생은 Claude 담당이며 이 작업에서 수행하지 않았다.

## 파일과 계약

- installation_map.json / candidate_atlas.png / native_atlas.png / contract.json.
- 기존 ID:94776,94779,94781,94783,94785,94786,94787,94788,94790.
- 후보 SHA256: ff571498d577f1e1fc29cbd47c31b81df9b5165860e265af44fac8e3cd76b266
- source_box와 후보 atlas_box를 분리했다. 각 cached raw indexbytes/full actual BGR555/RGB/wh/CRC는 mechanical_input_identity.json에서 기존 ID와 일치한다.
- 정상6의 전체 spec SHA는 preserved_normal6.json/latest.json에서 불변이다. lookup/dynamic/effect 플래그는 기존 spec 그대로 둔다.

## 실제 원본과 팔레트

청색4개는 native_weapon_source_43_183/unit43_weapon183_source.state +330/335/345, 흰회색5개는 native_weapon_source_98_410/unit98_weapon410_source.state +455/460/465 실제 cached OBJ다. frame/video_epoch/engine/OAM/attrs/flip/원본 index/full16색은 contract.json에 보존한다. 원래 retained source의 IMG21921 raw 대조근거도 original_cached_to_ROM_source_proof.json에 복사했다. 후보 리소스를 실제 업로드 소유로 단정하지 않고 owner=None을 유지한다.

같은 raw형상의 두 색 단계도 실제 전체 팔레트가 달라 독립 생성했다. 다른 기체/다른 색 그림을 빌려 재색칠하거나 alpha를 공유하지 않았다. source_intersections.json에서 정상/문제 source 사각 사이에 같은 전체팔레트의 겹침은 없었다. 실제 hash의 다른 ID 여부는 actual_hash_alias_lookup.json.

## 성분 제작과 실패 기록

처음 생성은 가는 광선을 금속 타일/사각 윤곽으로 해석하여 rejected_block_cyan_raw.png / gray_raw.png로 보존하고 사용하지 않았다. 다음 교정에서 전체 연결 원호/십자광/끊어진 세로선은 유지됐으나 분리 원호3은 원본10/9/10성분과 생성9/10/12성분이 달라 보류했다(rejected_whole_arc_component_counts.json). 임의 점 추가/삭제로 개수만 맞추지 않았다.

이3개는 실제 원본의 모든 독립 성분을 components_cyan_contract.json(10개) / components_gray_contract.json(19개)로 분리했다. 각 성분별 새 생성 RGBA 재료를 원래 bbox 위치/크기로 기하 정렬하여 원래 빈틈과 위치에 다시 조립했다. 원본RGB/alpha를 출력에 전사하지 않았다. 대각선에서 두 생성 블록으로 갈라진4성분은 새로 생성한 하나의 대각 광선 재료로 바꿨다(generated_diagonal_four_raw.png). 새로운 외곽선으로 원래 파츠를 닫거나 다른 파츠의 접합을 발명하지 않았다.

#94783 세로선은 첫 그림이 실제 청색보다 과하게 흰색이었다. 최종 generated_components_cyan_vertical_raw.png의 실제 #5aace6/#62c5de/#94deee 자체 생성 재료로 세 성분을 다시 만들었다. 이것은 픽셀 재색칠이 아니라 새 그림이다. source24:4:2 길이/1행 간격/실제 x7 지지 좌표를 보존했다. 세로2성분94785와3성분94790도 원래 개수/빈틈을 유지한다.

생성 alpha160은 위치/성분 앵커를 측정하는 데만 사용했다. 출력 alpha 임계처리/키색 삭제/원본 마스크 찍기/강제 연결은 하지 않았다. 각 생성 원출력은 모두 보존한다. 최종 사용한 방법은 generation_alignment_provenance.json의 selected_for_final_candidate=True 행이다.

## 생산 진단과 Claude 위험

NullCache prepare_texture 뒤 원본 **40개 성분 각각의 bbox**에 alpha16 이상 paint가 모두 남는다(per_component_prepare_presence.json). DB 읽기/쓰기 없이 메모리에서만 준비했다. 전체 maxA만 보는 방식이 아니며, 공식 검사 통과를 뜻하지 않는다.

- 작은1texel 물질 조각은 매우 단순하다. 생성의 미세 명암선/테두리와 둥근 AA가 작은 크기에서 어둡거나 밝게 보일 위험이 있다.
- 대각선4개는 원본2~3texel 연결을 매끄러운 한 줄로 새로 만들었다. 위치는 정확한 bbox에 맞췄으나 source pixels의 모서리 접촉을 smoothing한 점은 실제 장면에서 판정해야 한다. 주변 반투명 광후광도 강제로 삭제하지 않았다.
- 연결 원호94779/94786의 원본 중심 경로와 새 곡선의 미세 차이, 십자광94776의 중심 크기를 확인한다.
- prepared_colour_presence_statistics.json은 source RGB와 최종 고알파 RGB 평균을 기록한 생산 자료일 뿐 팔레트 일치 검사나 품질 합격이 아니다. 통과시키려고 색을 수정하지 않았다.
- 실제 재생은 위 fixture +330/+335/+345 및 +455/+460/+465에서 작은 원호/점선/세로선, UI/기체 위 가림, 준비 뒤 소실을 Claude가 확인한다.

라이브/DB/공유코어/EXE/화면끄기/물리입력 변경 없음.
