# 고라이온 입·베헤모스 속도띠 같은 ID 후보

미검증 후보2. 신규 완료 수 없음. 실제 재생·공식 QA는 Claude 담당이다.

- 설치: installation_map.json / candidate_atlas.png / native_atlas.png. 후보 SHA256 798ed5b7ee6c2322d2ad2fad0912bc21a0fa35709721e662709cc843ca9f0875.
- #94547 metadata94546 RGB2275216898 32×32. unit404 weapon1589 source fixture +395 OAM5 (131,66). 실제 source_owner=None 유지. 원본 입 안의 검정은 불투명 재료인데 이전 HD는 투명 구멍이었다. 새 생성은 검정 입 내부가 불투명하다(생성본 표본13,12,13,254). 원본 RGB나 알파를 덮어찍지 않았다.
- #93188 metadata93187 RGB3037743501 16×32. actual source contract 보존. 원래 기계 분류였지만 실제 그림은 올리브 수직 속도 띠 FX이다. 처음 보고한 '6개 독립선'은 부정확하다. 실제 opaque는 열0..2/4..7/9..12/14 네 묶음에 여러 길이의 세로 면이 연결돼 있다. 새 생성은 기존 노란 가는 막대 대신 이 어두운 굵은 면과 투명 채널을 유지한다. 실제 사용 색 번호는2/3/4/5뿐이며 unused 자홍13~15를 그림색으로 사용하지 않았다.

원본 계약과 기존 metadata의 실제 RGB hash/wh/index bytes/전체16색은 mechanical_input_identity.json에서 일치했다. 94547 dynamic_palette=True,93188=False 기존 역할 유지. render effect_part 등 기존 플래그를 임의 변경하지 않았고, 역할 재분류는 설치 맵의 별도 설명으로만 남겼다. 분류/manifest/runtime 연결 결정은 root/Claude가 한다.

## Claude 위험

94547의 네 이빨과 상하 입술 비율/색면은 새 생성에서 약간 매끈하고 밝다. 검정 재료 복원은 명확하지만 실제 미사일 연출 가림 순서는 이번 제작에서 검사하지 않았다. 93188은 원본의 여러 긴 띠의 끝점·연결부를 smooth하게 만들면서 위치/폭 차이가 남을 수 있어 실제 원본과 판정이 필요하다. 제작용 replacement_preview.png는 공식 검사 결과가 아니다.

## 제작 근거

generated_source_0/1.png와 generation_provenance.json에 내장 imagegen 원본/출처 보존. generated_sheet는 자체 생성 두 이미지만 합쳐 4배 OAM 영역에 정렬했다. 생성 알파를 문턱/침식/팽창으로 지우지 않았다. 원본 bbox는 위치/크기에만 사용했다. 실제 source owner 모르는 부분을 다른 IMG로 추정하지 않았다. actual_hash_alias_lookup.json에서 두 대상과 같은 RGBhash의 다른 연결은 없었다. 공유 라이브/DB/코어/공식 QA/물리 입력 변경 없음.
