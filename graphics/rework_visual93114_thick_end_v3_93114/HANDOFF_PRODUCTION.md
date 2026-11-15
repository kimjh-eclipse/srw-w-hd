# 93114 오른쪽 아래 굵기 교정 새 후보

## 최신 실제 지적 반영
지침4에서93114의 오른쪽 아래가 원본처럼 두꺼워져야 한다고 판정했습니다. 실제 오른쪽 끝은 위쪽1텍셀·아래쪽2텍셀입니다. 이번 새 그림은 아래 띠가 오른쪽으로 갈수록 두꺼워지는 채워진 면으로 제작했고, 오른쪽 양끝 X좌표도 원본처럼 맞췄습니다.

상단은 실제 연노랑FFFFCD,하단은FFFF94입니다. 이전 패킷은 변경하지 않았습니다. 통과한93115는 수정 대상에서 제외했고 당시 메타데이터·그림 지문은 preserved_93115.json에 보존했습니다.

## 새 패킷
- candidate_packet.json에 최종 계약·4배RGBA 그림·1배 원본·생성 원천 네 파일 SHA와 작업 시작 당시93114 spec SHA를 넣었습니다.
- 시작 상태는 prior_binding_spec.json / prior_binding_spec_sha256.json입니다. 현재 spec이 이 지문과 다르면 덮어쓰지 말아 주세요.
- install_contract.json / candidate_atlas.png / native_atlas.png / generated_selected.png는 이 폴더의 새 파일입니다.
- 원천은 test_current/parts/effect_20966_base_four/source_contract.json의 unit190/mechanical_cutin_136.state 상대30프레임 OAM11입니다. 실제 raw/index 해시·인덱스·palette_15bit 전체16색을 계약에 보존했고 원본 좌표와 새 atlas_box를 구분했습니다.
- 원본 RGB나 알파를 그림에 전사하거나 생성 알파를 문턱으로 지우지 않았습니다. 같은 자체 생성 그림에서 위쪽 끝이 짧게 나온 첫 출력은 도구로 다시 그려 양끝 X좌표를 맞췄습니다.

## 확인 대기
연결·굽기·검사·캐시·중앙 목록 갱신은 Claude 담당이며 이번 후보에서 실행하지 않았습니다. source_candidate_pair.png와 실제 원천에서 오른쪽 하단 선폭·왼쪽 굽음·상단 위치·실제 연노랑 비율을 확인해 주세요. 새 후보를 만든 사실은 합격이나 실제 재생 완료 판정이 아닙니다.
