# 생성 알파 근거

내장 image_gen의 transparent_background=true만 사용했습니다. CLI/API는 사용하지 않았습니다. 최종 원천은 generated_94797.png, generated_94798.png, generated_94799.png, generated_94800.png 및 선행 자체 생성 panel0_generated.png(cell3 L)입니다. final_sha256.json으로 원천과 후보를 고정했습니다.

원본은 참조/좌표/사전검사에만 썼으며 출력의 RGB·알파를 원본에서 복사하지 않았습니다. 생성 RGBA 전체 resize 또는 각 생성 성분의 bbox crop/resize만 했습니다. alpha>=128은 자체 생성 성분의 crop bbox를 측정하기 위한 연결성 검사이며 생성 픽셀의 알파값을 0으로 바꾸는 삭제 문턱이 아닙니다. 실제 crop/resize 후 생성된 연속 알파를 유지합니다. morph 연산 없음. 등록 과정은 finalize.py와 final_geometry_registration.json으로 재현됩니다.

첫 94797 생성의 회색 성분은 회색 RGBA 합성에서 실제 성분임을 확인해 채택하지 않았습니다. 최종 94797은 다시 생성한 원천이며 gray_haze/holes 파일은 폐기 근거입니다. 작은 입자의 수·bbox는 실제 index를 바탕으로 위치만 고정했습니다. 94799/94800은 서로 독립적인 생성 원천과 실제 다른 팔레트를 유지합니다. 94796은 94797 자체 RGBA의 같은 영역에 의존합니다. 정상 94795 자체 RGBA 및 metadata/key는 변경하지 않았습니다.

사전검사 통과는 공식 시각 QA/게임 검증 완료를 뜻하지 않습니다.
