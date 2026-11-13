# 아스테바리스 flight 미연결 원본 계약

상태: 원본 계약 확보. 후보 미제작, 검증은 Claude 담당.

contract.json: 실제 cached OBJ + rendered OAM 계약, 고유 해시와 사용 팔레트·원본 bytes 기준 중복 제거. whole_pose_dependencies.json: 기존 연결 포함 모든 기체 OAM 의존. 각 contexts의 state를 로드하고 offset 90(래퍼는 91회 run)에서 확보. core path/SHA 계약에 보존.

원본 참조 native_atlas.png / native_atlas_reference_gray.png / whole_native_bbox_context.png. 기체 palette bank 0만 포함, 에이드 및 효과 제외. 일부 유닛에는 타이밍 차로 추가 에너지 효과가 있지만 기체는 팔레트 0으로 분리. native_cells_context.png는 셀 번호 참조.

선정 시 binding_id=0인 것만 포함. RGB 해시가 같고 원본 index bytes 및 실제 사용 palette entries가 같으면 중복 공유. 사용하지 않는 palette entry 차이는 구분하지 않음. 원본 그림에 덧칠하거나 alpha를 찍는 작업 없음.
