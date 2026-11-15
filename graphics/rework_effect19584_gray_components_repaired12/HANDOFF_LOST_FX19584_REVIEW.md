# IMG19584 밝은 회색 효과 문제13 인계

상태: **미검증 교체 후보12 / 기존 그림 보존·기술 문제 미해결1**. 새 그림은9개이고 공유 child3개가 추가된다. 신규 누락/완료 수 증가 없음. 공식 검사와 실제 HD 재생은 Claude 담당이다.

## 설치 파일

- installation_map.json은 기존 ID 92223~92234 총12개만 포함한다. candidate_atlas.png / native_atlas.png / contract.json과 함께 사용한다.
- 후보 SHA256: 0b5c800b1ef8930ad342c884ec20d9cdef458a19d0358e13499eb3ee1c289714
- #92220은 설치 제외, 원래 spec/그림을 보존한다. 새 그림 공유만으로 해결하지 못한 기술 문제이며 완료로 세지 않는다.
- 정상19의 전체 spec SHA는 preserved_normal19.json/latest.json에서 전부 불변이다.

## 원본·실제 팔레트

실제 원본은 effect_21819_19584/candidate_19584_contract.json에 보존된 unit261/mechanical_cutin_168.state +111/114/119/124/127/131의 cached OBJ다. native VRAM 추정이나 ROM 패턴 미관측 확장이 아니다. 모든 state/frame/video_epoch/OAM/flip/attributes/실제 전체 BGR555/원본 indexbytes를 각 contract.json에 보존했다. source resource는 None이며 후보 IMG19584 좌표 대조 근거를 확정 소유와 혼동하지 않았다.

원본은 모두 같은 실제 밝은 팔레트(white255/gray230/205/180/148/123)이다. 암회색 다른 변형32개로 재색칠하지 않았다. 13개 원본 실제 CRC/bytes/fullpalette/wh는 mechanical_input_identity.json에서 기존 바인딩과 일치한다. 정상 dark 변형과 보유#91679는 손대지 않았다.

## 공유 의존과 미해결1

source_intersections.json에서 원래 source 좌표 교차와 실제 indexbytes/전체 팔레트를 검사했다.

- #92231은 #92229 source의 오른쪽16열이다. #92229를 하나의 자체 생성 HD master로 정렬한 뒤 #92231을 같은 RGBA에서 나눈다.
- #92232는 #92233 source의 x8~23열, #92234는 x24~31열이다. #92233의 6개 독립 성분을 한 벌로 그린 뒤 두 child를 같은 master에서 나눈다. child를 따로 그리지 않아 겹침 RGBA가 같고 실제 작은 성분을 유지한다.
- #92220은 정상 #92211의 오른쪽16열에 포함된다. 조사 결과 **기존 #92220 rawpaint 자체가 정상 부모 crop과 이미 완전 동일**했다(normal_child_raw_unchanged_proof.json). 같은 그림을 다시 연결하는 것은 수정이 아니므로 설치 맵에서 제외했다. 정상 부모를 건드리지 않고 이 child의 실제 소실을 해소했다고 주장하지 않는다.

shared_normal_parent_child_proof.json은 정상 부모와 새 문제 master의 의존을 함께 보존한다. 기존 생성 HD 공유이며 원본 RGB/alpha 전사가 아니다.

## 제작과 작은 성분

imagegen 스킬 기본 내장 도구로 generated_nine_raw.png를 새로 만들었다. reference_nine.png는 원본 위치/형태/실제 색 참조다. 원본 native의 RGBA/alpha 스탬프, 임계값 알파 삭제, 구멍 메우기, 형태 늘리기는 하지 않았다. 생성 전체 RGBA를 원본 bbox 위치/크기로 기하 정렬했고, 생성 alpha160은 위치 측정 앵커로만 썼다.

원본6개 작은 파편 #92233은 생성 주요 성분도6개, #92226은 원본/생성 각각2개다. 세부 생산 기록은 generation_alignment_provenance.json이다. source 반올림이나 raw master 이웃파츠를 잘못 포함하지 않았다.

NullCache prepare 뒤 원본 총22성분(교체12에 해당21성분)의 각 bbox 안에 paint가 모두 남는다(per_component_prepare_presence.json). 모든 개별 원본 성분 위치를 검사했고 전체 maxA만 본 것이 아니다. 이 진단은 공식 품질 판정이 아니다.

## Claude 확인 위험 / 장면

- 새 속도선은 가는 바늘로 줄었던 지지면을 넓혔다. 원본의 실제 gray band 순서/폭, squared crop 끝, 밝은 하단/중앙의 차이를 확인한다. 특히 #92225는 흰 하단, #92230은 밝은 중앙과 어두운 위아래로 다르다.
- model이 원본의 계단형 경계를 너무 그대로 HD로 따라갔거나 컷 끝에 얇은 명암선을 추가했을 위험이 있다. 원본 구성 보존과 그림 미관의 최종 판정은 Claude 담당이다.
- #92220은 원래 큰 정상 부모와 함께 기술 검토가 필요하다. 이번 후보에서 개선됐다고 보지 않는다.
- +111/+114 원호 조각, +119 긴 띠, +124/+127 작은 파편과 긴 speed strip, +131 작은 마지막 조각을 확인한다. 각 실제 OAM/반전은 source contract 참조.

라이브/DB/공유 코드/코어/모니터 제어 변경 없음. 부모와 이웃 파츠를 새로 해석하지 않았다. lookup/effect/dynamic flags는 기존 spec에서 유지한다.
