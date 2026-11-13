# 민트 효과 38개 색영역 재제작 결과

현재 인수 후보: `candidate_observed_colour_support_preserved.png` (1024×256, RGBA).
라이브 아틀라스·라이브러리·구운 DB는 변경하지 않았다. 실제 재생은 메인 담당.

## 문제와 수정

11개 경고 모두 원본 x160..256,y0..32의 파편·수평 광선·우상단 코너 영역이다. 이전 후보는 파편을 종횡비만으로 선택하여 큰 흰 영역에 jade 조각을 배치했다. 새 imagegen으로 흰/민트 파편, 긴 흰 핵, 흰 코너, 얇은 민트 띠와 작은 흰 핵 파편을 별도로 그렸다. 새 생성 RGB만 사용하며 원본 native RGB/alpha 복사, 원본 마스크 찍기, 색 슬롯 강제 메우기는 없다.

최종 후보는 이전 **생성 그림 자체의 alpha**를 보존했다. 신규 그림의 투명 경계에 필요한 RGB는 신규 그림의 인접 색을 연장했다(1555 픽셀, 최대 14회 인접 확장). 원본 native alpha를 쓰지 않았다. 문제 없던 224,16,32,8 조각은 이전 생성 후보를 유지했다.

## 검사

- `audit_colour_support.py` (공식 audit_all_parts / audit_palette_alignment, candidate를 메모리에서 대입): 38개, quality flags 0, palette failures 0.
- 공식 IoU 최소 0.643. **이전 설치 후보도 같은 공식 검사에서는 0.643**이다. 신규 저하가 아니다.
- `audit_colour_support_shape.py` (기존 BOX 축소·alpha>64 동일 기준): 최소 0.7714286, 0.7 미만 0, key flags 0, material misplaced 0.
- 두 IoU 검사는 축소/alpha 기준이 달라 숫자를 직접 비교하면 안 된다.
- 임계값을 낮추거나 공식 검사 모듈을 바꾸지 않았다.

## 눈으로 본 결과와 한계

`colour_final_flagged_comparison.png`: 왼쪽 native / 가운데 이전 / 오른쪽 새 후보. 91824의 초록 사각 내부에 흰 코어가 생겼고, 91804 긴 흰 핵이 실제 길이로 복원됐다. 91815/91826/91830의 큰 파편도 흰 핵 위치를 맞췄다.

생성 파편은 원본보다 둥글고 정사각형처럼 보이는 일부 조각이 남는다. 이 후보는 잘못된 흰/초록 영역을 고치는 것이며, 원본과 모든 파편 외형이 완전히 동일하다고 주장하지 않는다. 다른 팔레트 변형/게임 재생은 이 검사에서 확인하지 않았다.

## 재현 파일

- `prepare_colour_corrected.py`: 파편 색영역별 새 생성 조각 등록, 긴 핵/코너 교체
- `prepare_colour_final.py`: 얇은 띠와 흰 핵 파편 신규 생성 조각 교체 (주의: 문제 없던 224,16,32,8 복원은 아래 support 스크립트 선행 입력에 이미 반영됨)
- `prepare_colour_support.py`: 이전 생성 alpha 보존; 입력 final 후보에는 224,16,32,8 복원이 반영되어 있음
- `colour_support_review.json`: 공식 38개 세부 결과
- `colour_support_shape_review.json`: 이전과 같은 별도 기준 shape/key 검증
- 원출력 4개: colour_particles_generated.png / colour_strip_corner_generated.png / colour_small_repairs_generated.png (이전 generated_grid_observed는 jade 조각 일부 유지)

이번 결과는 후보 전달이며 설치·재굽기·실재생 완료 보고가 아니다.
