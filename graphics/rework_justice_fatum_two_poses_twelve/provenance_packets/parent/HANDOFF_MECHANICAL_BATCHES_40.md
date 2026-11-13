# 후속 기계 그림 후보 인계 색인

상태: 9묶음 40종 제작·기계적 연결 계약 준비. 라이브 설치·굽기·Git은 root, 공식 시각 QA·실제 HD 재생은 Claude 담당. 검증 완료 또는 전체 누락 해소 주장 없음.

| 폴더 | 고유 그림 | 인계 문서 |
|---|---:|---|
| aestivalis_custom_hand_missing | 2 | HANDOFF_AESTIVALIS_CUSTOM_HAND_REVIEW.md |
| aestivalis_custom_gai_cannon_missing | 2 | HANDOFF_AESTIVALIS_CUSTOM_GAI_REVIEW.md |
| aestivalis_custom_gai_legs_missing | 2 | HANDOFF_AESTIVALIS_CUSTOM_GAI_LEGS_REVIEW.md |
| fmp_enemy_weapons_missing | 8 | HANDOFF_FMP_ENEMY_WEAPONS_REVIEW.md |
| fmp_followup_source_missing | 6 | HANDOFF_FMP_FOLLOWUP_REVIEW.md |
| fmp_enemy_second_source_missing | 4 | HANDOFF_FMP_ENEMY_SECOND_REVIEW.md |
| fmp_behemoth_mistral_followup_missing | 9 | HANDOFF_CANDIDATE_REVIEW.md |
| fmp_codarl_body_missing | 5 | HANDOFF_CANDIDATE_REVIEW.md |
| fmp_m9_basic_feet_missing | 2 | HANDOFF_CANDIDATE_REVIEW.md |

모든 묶음에 native_atlas.png, candidate_atlas.png, parts_generated.png, contract.json, whole_pose_dependencies.json, installation_map.json, 원본 ROM bytes 첫 일치 근거, 실제 palette/당시 exact·indexed 연결 조회, native indexSHA·크기·원본색/alpha 정합과 후보 빈 그림 여부 기록이 있다. 후보는 원본의 실제 cached OBJ + rendered OAM만 사용한다. 코어/DLL/라이브/DB/공유 런타임 수정 없음.

베헤모스9는 처음 후보 slot0의 큰 투명 홈/slot6 레일 틈 문제가 있어 root가 설치 보류했다. 두 슬롯을 생성도구로 새로 만들고 최종 candidate 갱신, 원본 alpha 찍기 없음. 다른7은 RGBA 완전 동일(support_fix_preservation.json). 이전 candidate_atlas_pre_support_fix.png는 참고 보존본이며 설치 입력 아님. 교정본의 색·외곽 스필·정확한 레일 지원 영역은 여전히 Claude 판정 대상.

보류/기계 오분류 제외:

- 163/705는 앞선 heavy_lunar 11종과 actualRGB 차집합0.
- 157/682는 기준을 만족하는 실제 새 기계 자세 관측 안 됨.
- 190/789는 190/788 두 그림 외 차집합0;790은 네이티브 메뉴에서 사용 불가(788/789만 목록).
- 196/814 두 파츠는 전체 문맥의 흰 방사선과 겹쳐 기계/효과 역할 불명확.
- 194/808 작은 노랑 단1792706204/3201486845는 원본 그룹을 root에게 제안했고 직접 제작 안 함.
- 273/1120은 이전 코다르 팔3파트와 raw index가 같고 사용 palette 대부분이 채널+3 밝기 변형. fmp_codarl_followup_missing에 원본 보존, 이를 새 자세 누락으로 집계하거나 재색칠로 추가하지 않음.
- 274/1121·278/1133 새 기계 차집합0.
- 검정 극소슬리버3734296757/2089952647 역할 불명확으로 보류.
- 해군267/1103·268/1106의 18종은 연기/물보라 효과. fmp_ship_m9_source_missing cell0~17에 실제 계약/팔레트/whole 문맥이 있으며 기계로 그리지 않음.
- 양산본타286/1149·287/1152·288/1155의2종은 동일 폭발 파편. fmp_mass_bonta_source_missing에 원본 보존, 기계로 그리지 않음.

새로운 source 탐색을 계속할 경우 같은 사용색 팔레트의 다른 자세·새 무장 단계가 우선이며, 밝기/페이드로만 바뀐 RGB를 끝없이 별도 그림으로 늘리지 않도록 raw index와 사용 palette 차이를 함께 확인해야 한다.