# 윙제로 수평 속도선 같은 ID 후보2

미검증 후보. 신규 완료 수 없음. 공식 검사·실제 재생은 Claude 담당이다.

- 설치 installation_map.json / candidate_atlas.png / native_atlas.png. 후보 SHA256 c76c660d36c7232da1f827b6ea68bd1b698ebc375e38f9d4691e57a905e53db9.
- #93574 metadata93573 RGB2664882122 32×8. #93575 metadata93574 RGB2647704864 32×16.
- 실제 source test_current/parts/native_weapon_source_0_2/unit0_weapon2_source.state +160. cached OBJ/core.obj 계약 source_contract 필드에 보존. 각 OAM의 실제 좌표는 다르며, 화면상 같은 위치라고 주장하지 않는다.
- 두 원본의 전체16색은 같고 작은32×8의 index bytes 전체가 큰32×16의 상단8행과 정확히 같다(shared_raw_upper_half_proof.json). 그러므로 그림도 동일 master 상단8행/전체16행을 공유한다. 각각 별도 정렬하거나 다른 그림으로 만들지 않았다.

## 제작 내용과 역할

원본은 기계 부품이 아니라 회색·회청색 수평 속도선 FX다. 기존 후보는 원본의 두꺼운 면/어두운 밑줄이 가는 밝은 선으로 줄었다. 원본의 어두운 회색 밑면까지 포함해 더 두꺼운 새 속도선 master를 생성했다. 실제색은 gray74/medium106·123·131/bluegray148·172·189/pale180·197·205/213·222·222다. 포화 청색/흰색을 별도로 넣지 않도록 요청했다. 역할 설명만 문서에 추가하고 기존 lookup/render flags를 보존했다.

내장 imagegen exec-1861fb4a-b471-4236-8cb7-66227eb22cd4.png를 parts_generated_raw.png에 보존. 생성 RGB에 청록 잡음이 보이지만 해당 픽셀의 alpha 최대는2다. generated_on_opaque.png에서 실제 불투명 배경 합성으로 확인할 수 있다. 이 픽셀을 문턱으로 지우지 않고 생성 알파 그대로 보존했다. 저알파 주변 잡음이 실제 실행에서 영향을 주는지는 Claude 검토 위험으로 남긴다.

## 위험

새 생성의 양끝 taper/밑줄의 흐릿함/줄 사이 공간이 원본과 다를 수 있다. 부드럽게 만든 회청색 면을 기계 금속으로 해석하면 안 된다. 전체 master를 한 번만 정렬한 뒤 작은 텍스처가 상단 절반을 그대로 공유하므로 두 그림 사이 생성 픽셀 일치가 유지된다. 그러나 이것이 원본 형태 품질을 보장하지는 않는다. replacement_preview.png는 제작용 비교이며 공식 QA가 아니다.

원본 RGBA/알파 stamp 없음. 알파 문턱/침식/팽창 없음. alpha160은 정렬 anchor 측정만. hash/indices/full palette 일치는 mechanical_input_identity.json. 라이브/코어/DB/공식 QA/물리 입력 변경 없음.
