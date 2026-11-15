# 재제작 후에도 소실로 남은 무장 2개 재검토

상태: 같은 ID 교체용 미검증 그림 후보 2개. 라이브/코어/DB 쓰기·공식 QA·실제 HD 재생 없음. 신규 연결 증가 0.

## 원인

- docs/PRODUCTION_ART_BATCH_CURRENT.json의 원래 두 제작 패킷을 따라 실제 cached 계약을 찾았습니다. 원본 index bytes, 실제 전체16팔레트와 live binding hash를 다시 계산해 일치시켰습니다.
- 현재 live atlas의 내용으로 texture_key를 계산하고 graphics/parts_baked.sqlite를 **mode=ro**로 열어 SELECT만 했습니다. 두 현재 key 모두 실제 구운 WebP가 있었습니다. current_baked_source_report.json.
- raw 그림부터 실제 원본의 폭/위치가 달랐고 구운 RGBA에서도 같았습니다. 캐시 미갱신·굽기 중 알파 소실로 확인된 문제가 아닙니다.
- #93902: native82texel 중23(28%)가 alpha128 기반 미칠. 검은 연결끝2와 회색재질21이 포함됩니다. 원래 검은 직사각 끝이 작은 점으로 축소되고 회색 직선 하단 면이 사라졌습니다.
- #94611: native120 중29(24.2%) 미칠. 위쪽~가운데 오른쪽의 검정/녹색 실제 재질이 연속으로 빠졌습니다. 기존 그림이 원래보다 왼쪽으로 휘며 중앙 경로·굵기가 달랐습니다.
- 따라서 소수 AA 차이로 보존하지 않고 2개를 새로 생성했습니다.

## 새 그림

- generated_two_raw.png는 내장 imagegen 출력 exec-b2f2029e-0da3-462f-b6bb-20049ac66970.png 그대로 복사한 원본입니다. new_art_reference.png는 생성 참조이며 설치 픽셀로 쓰지 않았습니다.
- 포비든은 연속 회청색 직선과 검은 불투명 짧은 연결끝·작은 회색 삽입면을 요청했습니다. 사슬 마디·픽셀 도트 확대·끝을 바늘로 축소하는 표현을 피했습니다. 원래 화면에서 잘린 오른쪽 끝을 그대로 유지합니다.
- Guaites는 밝은 올리브색 고형 띠와 어두운 실제 외곽 재질, 완만한 S 경로를 요청했습니다. 중앙을 임의의 원형 고리로 만들지 않았습니다.
- 자체 생성 셀 전체 RGBA를 원본 사각 bbox에 기하 확대·정렬했습니다. 원본 RGB/알파 전사, native mask로 자르기, 알파 팽창/침식·문턱 삭제·재색칠은 없습니다. initial_alignment_provenance.json.
- 기하 수치 외에 replacement_comparison.png를 직접 확인했습니다. 새 직선은 직선으로 유지되고 검은 끝이 보입니다. 호는 기존보다 원본의 오른쪽 경로/넓은 상단에 가깝습니다. 원본과 후보 모두 alpha16/128에서 한 성분이며, 검은 연결끝이 떠 있는 별도 점이 아닙니다. 이 확인은 실제 게임 QA가 아닙니다.

## 설치와 검사

- installation_map.json: 기존 #93902/#94611만 교체. 원본 hash/index/fullpalette/lookupflags/resource/source 좌표는 old_spec 보존. 후보 좌표만 공용 atlas의 x0/x64로 변경했습니다.
- candidate_atlas.png SHA256 `38f55f86bd0b2bad517e5500a81405152b044285994b8ad70553f0926f7cefec`. native_atlas.png/contract.json을 함께 사용합니다.
- candidate 및 NullCache prepare 모두 동일 사전기하 flags 없음.
- #93902 IoU .750, 미칠 .098, 외부0 (기존 .505/.280/.005).
- #94611 IoU .828, 미칠 .067, 외부0 (기존 .515/.242/.136).
- prepared_final_atlas.png/prepare_input_check.json/candidate_geometry_preflight.json/prepared_geometry_preflight.json.
- 같은 기존 atlas의 다른 #94608/#94609는 그림/spec을 바꾸지 않았습니다. preserved_normal_specs.json.

## Claude 확인할 한계

- 미칠이 0은 아닙니다. #93902 8texel 안팎, #94611 8texel 안팎 차이가 남으며 기하 기준 통과를 실제 완성이라고 부르지 않습니다.
- 새 회청색 직선의 밝은 금속 하이라이트가 원본의 회색보다 밝게 보일 수 있습니다. 검은 끝의 사각 비율·회색 삽입면·하단 접합, 올리브 띠의 밝은 면/어두운 외곽 분포는 실제 재생에서 확인해야 합니다.
- #93902 실제 fixture82/w351 +165 OAM20, 원래 test_current/parts/actual_mechanical_pose_82_165/whole_native_context.png.
- #94611 실제 source_mechanical_fixed_74_313_300/source_pose.state +0, screen146,65/flip_y True. 계약은 raw(비반전) 원본/새 그림이며 런타임의 원래 flip_y를 보존했습니다.
- 전체 state/epoch/attributes/팔레트는 contract.json source_contract와 source_original에 보존했습니다.
