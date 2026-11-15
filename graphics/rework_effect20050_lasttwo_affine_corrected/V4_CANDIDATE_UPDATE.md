# 20050 후속 v4 기하 등록

앞선 보류 상태를 바로 완료로 바꾼 것이 아닙니다. 자체 생성된 선 RGBA에 build 시점 전역 affine 정렬을 적용했습니다(수평scale0.9/shear0.125/shift5). 원본은 기하 점수에만 사용했고 RGB/alpha 픽셀을 출력에 복사하지 않았습니다. 원본 마스크를 alpha로 쓰거나 문턱/형태학 삭제를 하지 않았습니다. offline_registration_v4.json에459개 전역 정렬 후보와 선택 계수·기준을 기록했습니다. 실제 코드 offline_align_main_v4.py도 보존했습니다.

v4 사전 기하 검사에서2개 모두 경고가 없습니다. 새 원천8성분은 같은 화면master를 원래OAM2/3 사각형에 나눴고 작고 떨어진7조각과선1개를 모두 보존했습니다. candidate_atlas_v4.png/ generated_master350_v4.png/ master350_v4_gray.png를 확인하세요. 설치·굽기·동일 도구 재검사 뒤에도 독립 검증은 Claude 대기입니다. 이전 실패후보/지표를 지우지 않습니다.
