# 아스테바리스 공전형 미연결 11종 새 그림 인계

현재 상태: **미검증 후보·연결 준비 완료**. 실제 재생과 색·형태 판정은 Claude 담당. 라이브 메타·DB·코어 변경 없음.

## 범위

기체145~150의 mechanical_cutin_168.state +90에서 실제 cached OBJ와 rendered OAM으로 추출했다. 각 기체의 팔레트0 본체13OAM 중 미연결3OAM씩, 총18OAM이 11고유 RGB 그림을 사용한다. 기존 exact 및 indexed 연결은 11종 전부 없다(source_identity_and_connection.json). 남은 본체60OAM의 기존 연결은 whole_pose_dependencies.json으로 보존한다. 에이드 및 효과 OAM은 제외했다.

11종은 손·팔 연결편 두 형태의 색 배치별 그림10종과 아주 작은 어두운 연결편1종이다. 동일 해시라도 index bytes, 크기, 실제 사용 팔레트 번호가 일치한 경우에만 공유했다. 미사용 팔레트 색의 차이는 공유를 막지 않는다.

## 설치 파일

- installation_map.json: 루트 설치기 입력11개, actual RGB 전용·indexed_safe=false.
- candidate_atlas.png: 768×768, native_atlas.png:192×192, 정확4배.
- contract.json:11고유 실제 계약, 각 contexts에 unit/state/OAM/offset 기록.
- whole_pose_dependencies.json: 기존 파츠를 포함한78OAM 원본 계약.
- mechanical_contract_checks.json: 크기/index SHA/실제 원본 RGB와알파·ROM index bytes 동일성 확인. 형태나 색 영역 QA가 아니다.
- rom_indices_identity.json: 두 큰 연결편은 ROM image10768의(24,0,32,16)/(0,16,32,16)와 index bytes 완전 일치. 작은 연결편은 image10698 첫 일치 영역(128,0,8,32), 다른 이미지에도 같은 작은 bytes가 있을 수 있다.
- source_identity_and_connection.json: 실제 사용 팔레트와 ROM 팔레트 후보. 일부 색 변형은 animation_audit에 열거된 팔레트와 일치 후보가 없다. 원본색 기준은 렌더 당시 캐시값이며, ROM 팔레트 전부 일치라고 주장하지 않는다.

후보 SHA256: `589fa512349a3557abd56bce4d47ea36f4ce40a26cf5a40e3a3c4f0cafa2d0ca`

## 제작 출처

imagegen 스킬로 원본 셀과 원본 기체 문맥을 참조해 11종을 새로 그렸다. parts_generated.png 원본 생성파일 exec-cdf0c0e3-c1fd-45cb-9142-3a38d141dc02.png. 원본 RGB나 원본 alpha를 후보에 복사하지 않았다. 생성 alpha bbox만 원본 보이는 bbox 위치로 정렬하고 4배 셀에 저장했다. 원본은 참조/기계적 정합 확인용이다.

prepare_candidate.py가 셀 분리와 제작 조립을 재현한다. unit145~150_production_assembly.png는 새11종+기존파츠의 **원본**을 섞은 제작문맥일 뿐, 최종 HD 재생 증거나 품질 판정이 아니다. 연결된 기존 HD 의존관계는 루트와 Claude가 최신 결과에서 확인한다.

## Claude 인계

각 test_current/combat/named_attacks/unit_145..150/mechanical_cutin_168.state를 사용. 예시:

```powershell
python scripts/verify/verify_runtime_path.py --state test_current/combat/named_attacks/unit_145/mechanical_cutin_168.state --frames 180 --save-frames 60 90 120 --track-atlas aestivalis_flight_missing90 --name aestivalis_flight_145
```

90은 래퍼가 state로드 뒤91회 core.run하여 얻은 프레임이다. 다른 유닛에도 같은 규칙. 원본팔레트·노랑/주황 끝·파란 원형 장갑·검은 연결편의 실제 색 배치를 특히 확인한다. 셀2는 원본 불투명8픽셀의 매우 작은 조각이라 지원영역·생성형태가 어긋날 위험이 높다. 생성기 특유 추가 기계선/새 검은 외곽선이 접합면에 생겼는지도 판정 필요. 전체 기체가 완성됐다는 주장은 하지 않는다.
