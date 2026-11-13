# EI-15 관측 기계 조각 20개 인계

최종 입력: packed/install_contract.json, packed/native_atlas.png, packed/candidate_atlas.png. fixture342/w1385 실제 원본 +185/+215/+230/+295/+370/+470/+475에서 선정했습니다. 실제 원본 상태 native_weapon_source_342_1385/unit342_weapon1385_source.state를 사용하며 whole 원본은 actual_mechanical_pose_342_FRAME/whole_native_context.png입니다.

20계약을 18개 생성 영역으로 제작했습니다. 실제 같은 열린 손을 구성하는 두 쌍은 같은 팔레트·우선순위·무반전·비아핀·화면 인접 위치가 확인되어 한 손 마스터에서 원래 사각형으로 분할했습니다(additional_component_groups.json). 이 두 쌍은 인덱스 겹침 증명이 아니라 실제 문맥에 근거한 인접 연결이며 raw_flat_overlap.json은 0건입니다. 원본 포함 관계도 0건입니다.

왼손 마스터 첫 출력은 원래 지원 사각 밖에 A16 이상 픽셀 2개가 남아 보류했고, 생성 도구로 해당 손만 재제작했습니다(generated_left_hand_v2.png). 최종 지원 밖 최대 알파4·A16 이상0이며 원본 알파 전사나 잘라 지우기 없이 해결했습니다. 나머지18개는 원래 후보 픽셀을 보존했습니다(other18_unchanged_proof.json). 최종 분할 증명은 generated_continuous_split_proof_final.json입니다. 기본 정규화 스크립트를 재실행하면 첫 손 출력으로 돌아가므로 v2 교정 절차도 함께 보존해야 합니다.

20개 모두 메모리 prepare 비어 있지 않음, 제작 시점 활성 exact RGB·안전 indexed 연결0입니다. 공식 QA와 HD 실제 재생은 Claude 대기입니다. +470 OAM11은 최대 가시면적1픽셀, 그 외 작은 경계 조각도 포함하되 정상 전체 기체 가시성으로 주장하지 않습니다. 기존 OAM·검은 단면·분홍 손가락/남색 장갑 접합, 노란 커프의 두께, 실제 소량 녹색 표시 위치를 확인해 주세요. 원본 소스 인덱스29의 주황 작은 조각은 역할 미확정이라 미완료로 남겼고, 그 외 FX/가림 조각을 전체 완료로 세지 않았습니다. 라이브/DB/코어 변경 없음.
