# 생성 알파 보존

각 팔레트 자신의 generated_*.png RGB와 alpha를 사용. preserve_generated. alpha threshold/이진화/모폴로지 없음. 원본 RGB/alpha stamp나 타 팔레트 재색칠 없음. 원 생성 파일과 후보 모두 보존.

기존 prepare 내부 분리성분 제거가 발생한 crop은 production_report.json에 명시. 이는 자체 생성 그림 후처리와 별도이며, 가는 선/약한 glow 손실은 Claude 실제 재생 판단 대기.

## 基본형태 / 실제 색변형 구분 (최종)
- 16계약은 각각 고유 raw 도형의 현재 관측 중 가장 밝은 실제 palette를 골랐다. 원본에 관측되지 않은 기본색이나 PLT색을 추정하지 않았다. 다른 11개 actual 색변형은 held_fade_source_base_pairs.json에 base hash/원본actual/state/frame/기본후보 그림을 연결했다. 이 11개는 신규그림 및 완료수 제외.
- 실제 palette별로 각자 새 그림을 생성했다. 21748은 3팔레트(분홍/청백/어두운청색),22409는 2팔레트(분홍/청백)이며 다른 palette의 RGB/alpha를 빌리거나 재색칠하지 않았다. 같은 source IMG 영역의 교집합은 palette마다 한 sheet를 나눠 같은 픽셀을 공유한다.
- 미해결: 원본의 거의 일정한 pale 면이 생성본에서는 테두리 gradient가 강해지고, 실제 alpha가 아주 작은 외부 흰색/자홍/청색 haze가 남는다. 자동 알파threshold로 일괄삭제하지 않았음. 내부 직선 절단면의 명암 연결/흰 중심 불투명 유지/가는 파편 및 빔효과 전면순서는 Claude 실제조립 검증 대기. 약한 haze를 새 유효효과라고 확정하지 않음.
- source_overlap.json/production_report.json은 제작 입력/준비 존재 확인이며, 실제 시각정상 QA가 아니다. 라이브/DB/runtime 변경 없음.
