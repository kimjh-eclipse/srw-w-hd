# 오공비 눈 6종 제작 보류

- 실제 unit4 weapon18 source state +210/+225/+240의 각 눈2종, 모두 exact0/indexed0이다. 기계 파츠가 아니다.
- 활성 컷인은 ID17 / pilot_bg_22825 / graphics/pilot_cutins/cutin_22825_hd.png이며 이미 전신 그림이 있다. 새 전신을 중복 제작하지 않고 원래 OBJ 사각형 눈6만 생성했다.
- 원본 실제 사각형은120,16의16×16과136,24의16×16으로 서로8px 아래로 어긋나 붙는다. raw bytes SHA 및 원본 팔레트/크기는 mechanical_contract_checks.json에 있다. ROM 소유 IMG는 미확정이다.
- candidate_atlas.png는4배, native_atlas.png는96×72. 생성 출처 parts_generated.png, 내장 imagegen. 후보 SHA2569793c117bf8a2f74ee27723c1ea913a430d66bcd7e9171ee448ff54b467f3465.
- 설치 보류: candidate_face_sequence_production.png에 기존 HD fullcutin 위에 실제 원좌표로 올린 제작용 조립을 저장했다. 왼쪽의 기존 닫힌눈은 OBJ 사각형보다 왼쪽에 있어 바깥에 별도 눈으로 남고 피부 경계도 크게 보인다. 따라서 이6을 그냥 설치하면 문제를 만든다.
- 이 조립은 정적 제작 미리보기이며 게임 재생/공식 QA가 아니다. Claude 실재생 판정은 수행하지 않았다. 라이브/DB/코어/공유 runtime 수정 없음.
- 필요한 선행 그림 작업은 기존 fullcutin17 얼굴의 눈 위치를 원본 전체컷인과 OBJ 사각형에 맞추는 것이다. 원본 지지 밖을 추가 페인트로 무작정 덮거나 전체그림을 두 번 그리는 방식은 사용하지 않았다.

## 얼굴 교정 추가 시도 및 최종 보류

full_cutin_generated_correction.png 및 full_cutin_generated_skin_edit.png는 imagegen으로 기존 눈자리/피부를 편집한 후보다. 전체 결과는 좌석/팔 등까지 일부 바꾸어 그대로 대체하지 않았다. face_only_correction_candidate.png에는 생성 얼굴 영역 HD좌표440,32..684,228만 넣고 그 밖의 기존 HD 픽셀은 완전히 보존했다. face_only_preservation.json에 영역 밖 RGBA SHA와 불변 확인을 기록했다. 원본 도트 RGB/alpha를 찍지 않았다.

그러나 face_only_sequence_production.png에서 왼쪽 눈 정합과 피부 사각형 경계가 여전히 해결되지 않는다. 따라서 전체6과 얼굴 교정은 모두 **설치 보류**다. 이 상태를 성공 또는 전체컷인 완료라고 보고하지 않는다. 다음 시도는 잘린 눈 두 조각 각각을 독립 얼굴로 완성하지 말고, 원래 컷인 전체 얼굴의 실제 좌표와 닫힌 눈부터 한 번에 재등록해 원본 OBJ 지지 안에 들어가도록 설계해야 한다. 후보를 무한 재시도하지 않고 다음 확정 원본 묶음 작업으로 넘어갈 수 있도록 실패 원인과 모든 시도 파일을 보존했다.
