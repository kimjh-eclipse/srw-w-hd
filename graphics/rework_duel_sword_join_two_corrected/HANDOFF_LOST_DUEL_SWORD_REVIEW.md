# 검정 면·주황 접합 같은 ID 교체 후보

상태: 미검증 후보. 공식 검사와 실제 재생 판정은 Claude 담당이며 이번 작업에서 실행하지 않았다. 신규 누락/완료 수 없음.

- 교체 ID: 94534, 94822. 원본 계약과 현재 메타의 RGB 해시·크기·index bytes·16색 전체 팔레트 일치. 두 대상 모두 기존 dynamic_palette=True를 보존했다.
- 입력: contract.json / replacement_targets.json / native_atlas.png. 출력: installation_map.json / candidate_atlas.png.
- candidate SHA256: f1b218269a0ed9a7e39d8f973d50d9483d770d435a7c62c64702ccafc2e33d57.

## 94534

원본은 왼쪽 19×8 texel 전체가 불투명한 검정 면이며 나머지 13열은 투명이다. 이전 그림은 검정 재료를 배경으로 지우고 ㄴ자 선만 남겼다. 새 불투명 생성 재료를 그 실제 사각 지원 크기로 배치했다. native RGB/alpha를 찍지 않았다. 검정 면이 전체 유지되며, 희미한 회청색 표시가 남는다. 작은 회청 표시의 원본 대비 굵기/농도 차이는 여전히 Claude 검토 대상이다.

원본: unit54의 source_mechanical_fixed_54_245_350/source_pose.state +0, OAM7 (112,57), IMG8467 (0,32,32,8). 다른 원본 셀0/6의 공유 영역은 본 대상 셀4와 무관하다.

## 94822

기존 그림이 단일 얇은 주황 삼각형이 되어 검정 오른쪽 지지대와 분리 공간을 잃었다. 첫 생성도 도트 블록을 답습해 거절하고 별도 보존했다. 새 생성은 부드러운 대각 주황 면과 오른쪽 검정 수직 지지대, 그 사이 실제 삼각 투명 틈을 표현한다. 표면 홈은 원본에 없는 세부이며 tiny 축소에서 과장될 위험이 있다. 검정/주황 비율, 실제 오른쪽 이음매는 Claude 판정 대기다.

원본: unit131의 source_mechanical_fixed_131_546_550/source_pose.state +0, OAM4 (163,37), IMG10555 (160,80,8,16). 인접 정상 셀3 RGB2231202757, OAM5 (171,29)는 수정하지 않았다. 두 raw 사각형은 겹치지 않는다.

## 생성 및 알파

내장 imagegen 사용. 입력 원본과 생성 출처는 generation_provenance.json, generated_source_0.png/1.png에 보존. generated_sheet.png는 생성 그림만 합쳤다. 알파 문턱·팽창·침식 없음. 원본 bbox는 크기/위치 정렬에만 사용했고 원본 RGB/alpha 마스크는 후보에 복사하지 않았다. alpha_and_alignment_provenance.json 참조.

replacement_preview.png는 제작 대조 그림이며 공식 QA가 아니다. 라이브·DB·코어·공유 코드 변경 없음.
