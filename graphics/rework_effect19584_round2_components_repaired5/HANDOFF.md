# observed_effect_round2_19584 문제5/26 후보 인계

- 이전 observed_effect_19584_gray32 및 새12개와 다른 묶음입니다. 대상은 94300,94304,94305,94313,94317입니다. 정상21개는 RGBA/바인딩 메타데이터를 모두 그대로 보존했습니다(preserved_normal21.json). 정상과 문제의 직접 영역 겹침 없음. 정상부모와 같은 child의 임의 교체 없음.
- 설치용 최종 flat 계약은 final_flat_contract.json, 원본은 native_atlas.png(176×128), 정확4배 후보는 candidate_atlas.png(704×512)입니다. 별도 생성 원천은 generated_ID.png, 등록 후 자체 그림은 own_rgba_ID.png입니다.
- 실제 관측 원자료 actual_observed_contract.json을 원본 그대로 복사했습니다. 최종 계약에는 index raw, 전체16색 BGR555와 RGB, state/frame, 원래 source_box와 별도의 candidate atlas_box가 있습니다. 전부 group1 실제 황금/노랑 팔레트이며 타팔레트 재색칠/알파 차용 없음. 미관측 추가 추정 없음.
- 관측 state는 native_weapon_source_57_259/unit57_weapon259_source.state이며 94300 +440,94304 +450,94305 +455,94313 +480,94317 +585입니다. 모든 source 좌표는 IMG19584 실제 raw와 연결된 기존 관측 계약을 유지했습니다.
- 94300/94313은 넓고 채워진 황금 쐐기를 새로 그렸습니다. 픽셀 계단을 그대로 확대한 경계 대신 고해상도 연속 경계/그라데이션을 사용했습니다. 94304는 짧은 우측 절단 끝을 가진 굵은 가로빔,94317은 양 끝이 잘린 굵은 직선 가로빔입니다. 같은 생성을 억지 공유하지 않고 독립으로 그렸습니다.
- 94305 입자는 원래6성분입니다. 새로 생성한6성분 자체 RGBA를 각각 crop/resize하여 원래 위치/폭/개수로 등록했습니다. geometry_registration.json에서 원천bbox/원래bbox를 확인할 수 있습니다. 원본 RGB/alpha 전사, alpha문턱 삭제, morphology 없음.
- 후보 및 NullCache prepare를 모두 같은 preflight 기준으로 검사하여 geometry_flags=[]입니다(candidate_geometry.json,prepare_geometry.json). IoU는 .844/.965/1/.906/1, 미칠 최대.078/밖최대.006입니다. 원본의 미세 계단과 새 연속 경계 차이가 남아 있습니다.
- PartsRenderer.prepare_texture 최종좌표 26개 모두 nonempty 및 실제 index/alpha/RGB 입력 일치입니다(production_report.json). 원본 채우기/성분삭제 등 prepare stats0입니다.
- 수동 비교는 manual_native_candidate_prepare.png의 왼쪽 원본/가운데후보/오른쪽prepare입니다. 회색 RGBA 합성으로 확인했습니다. 빔이 가는 선으로 줄지 않고, 노랑/황금 계열과6입자 위치가 유지됩니다. 예전 그림의 떠 있던 별도 가는 줄은 새 후보에서 없어졌습니다.
- 후보 SHA256=e15138081cbf43977983ab1559d8b4230c679100aebe9308e5b0455f76a4ed7d. 전체 SHA는 sha256.json입니다.
- 라이브러리/sqlite/공유코드/EXE/배포/푸시/모니터/게임창 미수정. 중앙설치·굽기·동일도구검사 및 Claude 독립시각/실제게임검증이 남았습니다. 사전검사 통과를 공식QA 완료로 표시하지 않습니다.
