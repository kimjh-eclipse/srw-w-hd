# 21284 원천5개·의존1개 교체 후보

## 범위와 보존

- 검토 시 경고7개는 `classified_target_snapshot.json`에 동결했습니다. 새 원천5개와 그 새 부모에 포함되는 의존1개를 합쳐 같은 ID6개 후보입니다: 93727/93732/93733/93742/93743/93744. 신규 연결은0개입니다.
- 93727은 새 부모93732의 아래 [0,16,16,16]와 실제 인덱스·16색이 동일하여 같은 아틀라스의 같은 생성 영역을 공유합니다. 독립 새 그림으로 세지 않습니다.
- 기존 정상19개는 유지합니다. 93733의 [64,16,16,16]은 정상93735의 기존 자체 HD, 93742의 [96,16,16,16]은 정상93734의 기존 자체 HD를 그대로 보존했습니다. RGBA 해시는 `shared_generation_proof.json`에 있습니다.
- 경고93748은 정상 부모93731 안의 완전 포함 영역이며 실제 원본·16색·현재 자체HD RGBA가 완전히 같습니다. 따라서 그림을 바꾸지 않았고 새 완료에 넣지 않습니다. `held_93748_parent_proof.json`에서 개별 준비 후33픽셀 차이(부모의 부유 성분 정리 차이 포함)를 기록해 기술 검토 대상으로 남깁니다.
- 정상19개와 보류1개의 현재 메타·자체 그림 해시는 `preserved_twenty.json`입니다.

## 원본과 제작

- 실제 원본 `test_current/parts/next_confirmed_fx_source/art_21284_base26/source_contract.json`의 해시·인덱스·전체16색·상태/프레임에 대응시켰습니다. 원본 `source_box/spec.source_x/source_y`와 최종 `atlas_box/spec.x/y`를 구분합니다.
- 기존 얇은 뾰족한 칼날처럼 바뀐 그림을 실제 흰/청회색의 채워진 선과 둔한 절단면, 원래 꺾임/폭으로 다시 생성했습니다. 생성 자체 알파를 사용했고 원본 RGB/알파 전사나 강한 알파 문턱 처리는 하지 않았습니다. 경계 상자 탐색에만8을 사용했습니다.
- 생성 원천 `generated_selected.png`, 성분 `source_components.json`, 배치 `provenance.json`, 비교 `source_candidate6_contact.png`입니다. 실제 겹치는 정상 자체 그림을 제외하고 원본 픽셀을 후보에 붙이지 않았습니다.
- 설치 입력 `install_contract.json` 6개, 원본 `native_atlas.png`(208×64), 후보 `candidate_atlas.png`(정확한4배832×256)입니다.

## 사전 생산 점검

- 루트 지정 명령 `python test_current/parts/preflight_candidate_geometry.py test_current/parts/claude_effect21284_correction install_contract.json`을 최종 계약에 실행했습니다. `root_geometry_preflight.json`에서6개 모두 `geometry_flags`가 비어 있습니다. 기준이나 공유 코드는 바꾸지 않았습니다.
- 같은 최종 설치 좌표의 NullCache 준비6개 모두 비지 않으며 기존 ID 실제 해시·인덱스와 같습니다. 원본 실제 인덱스·16색과 최종 참조 RGB/알파 일치는 `source_input_check.json`에 있습니다. 사용 파일 지문은 `production_input_chain.json`에 있습니다.
- 사전 기하 점검 통과는 클로드 독립 판정이나 실제 재생 확인을 대신하지 않습니다. 새 전체 검사/재생 검증은 수행하지 않았습니다.

## 남은 확인

- 실제 흰 선의 폭·원래 꺾임·청회색 명암과 정상 공유 영역에서 새 그림이 만나는 경계를 확인해 주세요. 일부 생성 윤곽에는 원본 계단형 형태가 남아 있어 최종 화질까지 정상이라고 보장하지 않습니다.
- 상태·프레임은 `claude_fixture_frames.json`입니다. 보류93748은 정상 부모를 재제작하지 말고 준비/검사 경로 차이를 먼저 확인해 주세요.
- 라이브 메타·DB·공유 코드·코어·EXE·배포·푸시는 수정하지 않았습니다.
