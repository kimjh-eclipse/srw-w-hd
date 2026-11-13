# 생성 알파 보존

각 팔레트 자신의 generated_*.png RGB와 alpha를 사용. preserve_generated. alpha threshold/이진화/모폴로지 없음. 원본 RGB/alpha stamp나 타 팔레트 재색칠 없음. 원 생성 파일과 후보 모두 보존.

기존 prepare 내부 분리성분 제거가 발생한 crop은 production_report.json에 명시. 이는 자체 생성 그림 후처리와 별도이며, 가는 선/약한 glow 손실은 Claude 실제 재생 판단 대기.

## 극소 파편 보완과 미해결
- slot13 hash3174226672, native source(128,24,32,8)는 불투명 9px가 여섯 성분으로 떨어진 파편이다. 처음 3개로 잘못 해석한 후보는 prepare 뒤 사실상 비어서 미사용으로 보존했다.
- 최종 tiny13_six_generated.png는 이 효과 자신의 6개 파편을 새로 그린 생성본이다. 자신의 각 생성 성분 RGBA를 원본 성분 bbox 위치/크기에만 정렬했다(tiny13_registration.json). 원본 alpha 모양을 전사하지 않았고 색을 코드로 채우지 않았다. 성분 bbox가 1~2 원본픽셀 크기여서 고해상도 사각 조각 형태/명도 변화는 Claude 판정 대기다.
- 전체 원본 sheet 단일 그림 공유에 이6파편만 새 생성 패치를 같은 sheet 좌표에 붙였다. 부분 교집합은 모두 최종 한 sheet를 읽는다. 다른 15계약 crop이 패치와 교차하는 경우 같은 픽셀로 재준비했다.
- 최종 prepare16 모두 maxA>=16, support ratio<.1 없음. raw source16 계약/실제 palette 그대로, 최신 live 중복0. 이는 생산 존재/해시 정합 확인이고 실제 HD QA는 아니다.
- 20050 전체 생성본은 주변 저알파 cyan haze와 원본보다 두꺼운 작은 glint가 남는다. 알파 threshold/노이즈 제거 필터를 적용하지 않았으며 실제 선 손실·형태·레이어는 Claude에게 요청한다.
