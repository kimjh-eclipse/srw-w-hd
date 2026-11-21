# Codex 인계31 — 실제 4xBRZ 원본 비교

# 원본 자세 4xBRZ 비교

- 사용자 요청으로 실제 DeSmuME xBRZ 코드를 적용했습니다. 이미지젠으로 흉내 낸 비교가 아닙니다.
- 대상 unit404 전체5판, unit403/405/215/380 첫판씩: 중복을 뺀 원본72자세, 조립판9개. 원본 native.png에서 정확히4배로 처리했습니다.
- 모든 native_4x.png가 원본 native.png의 nearest4x와 바이트상 동일함을 먼저 확인했습니다. 이미4배인 이미지를 다시4배 처리하지 않았습니다.
- comparison_00.png: unit404 기본/녹색팔올림/공중자세.
- comparison_01.png: unit403 주황변형/통상색, unit405 기본.
- comparison_02.png: unit405 다른자세, unit215, unit380.
- 각 비교의 왼쪽은 nearest4x, 오른쪽은 DeSmuME의 Render4xBRZ RGB 함수를 실제 호출한 결과입니다. 둘 다 같은 짙은 회색 바탕을 원본1배 단계에 먼저 합성했습니다. 게임 캡처는 아닙니다.
- unit_N/poses/*_4xbrz_rgba.png와 unit_N/sheet_NN_4xbrz_rgba.png는 투명 원본에서 xBRZ ARGB로 처리한 참조용입니다. 비교 화면 RGB 모드와 투명 경계 계산이 다릅니다.
- 원본/기존 HD/candidate/바인딩/에뮬레이터 설정/ROM은 변경하지 않았습니다. 이 파일들을 새로 그린 HD 그림으로 등록하면 안 됩니다.
- 실제 원본 경로·SHA·필터 소스/브리지/DLL SHA·생성판·원본 무변경 확인은 provenance.json에 기록했습니다.

## 생산자 육안 비교
9자세를 실제로 나란히 봤습니다. 외곽 계단이 감소하고 원래의 팔·다리·사자발/분리 구조를 유지한 채 곡선이 이어집니다. 작은 얼굴/복잡한 장갑 문양은 둥글게 뭉치는 부분이 남습니다. 원본에 없는 세부 구조를 복원하지는 않습니다.

## 다음 그림 입력
조립된 투명4xBRZ 판을 매끈한 윤곽의 주참조로, unfiltered native_sheet_4x.png를 원본 형태/색/부품 경계의 보조 참조로 함께 넣습니다. 데스사이즈 화풍 참조는 유지합니다. 원본과 필터가 다른 작은 부품은 원본으로 판정합니다. 최대9자세/기본자세 첫칸/원본색·자세·누락상태 보존 규칙은 유지합니다.

## Claude 검증
- 필터 전후의 작은 손·발·눈/센서·뿔·선형 무장/효과 경계가 합쳐지거나 얇아지지 않았는지.
- 이미지젠 새 그림에서 필터의 둥근 얼룩을 새 장갑·얼굴로 오해하지 않았는지.
- RGB 배경 합성 비교는 참고자료이며 설치용 알파로 쓰지 않는지.
- 필터 참조와 후보의 구분, 실제 새 그림의 원본 좌표/색/접합/배율 검수 후 기존 분할/설치 절차 유지.


[비교1](../test_current/parts/xbrz_reference_compare/comparison_00.png) · [비교2](../test_current/parts/xbrz_reference_compare/comparison_01.png) · [비교3](../test_current/parts/xbrz_reference_compare/comparison_02.png)

[출처/해시/대상 목록](../test_current/parts/xbrz_reference_compare/provenance.json) · [이전 그림수정 인계30](HANDOFF_FROM_CODEX_30.md)
