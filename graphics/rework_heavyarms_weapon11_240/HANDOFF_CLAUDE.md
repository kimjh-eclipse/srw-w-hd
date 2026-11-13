# 헤비암즈 unit2 / weapon11 +240 제작 후보

현재: 그림 제작·설치 입력 준비. Claude 독립 품질/HD 재생검사 대기.

- 정상 native 메뉴에서 weapon11을 선택하여 별도 source state 생성. 실제 원본 byte/palette/attrs는 `install_contract.json` 안 rendered_source_contract.
- 대상: 주먹/어깨 장갑, OAM [7, 8], 총 2개.
- 최종 `candidate_atlas.png` / `native_atlas.png` / `install_contract.json` / `provenance.json`. native 정확4배.
- 전체 원본 문맥 `test_current/parts/actual_mechanical_pose_2_240/whole_native_context.png`, 전체 원본 OAM 계약도 같은 폴더.
- 다른 연결 부품은 `preserved_existing_pose.json`대로 보존. 자체 생성 알파이며 wholepose 사각crop 이웃 부품 없음, 원본RGB/alpha stamp 없음.
- 현재meta raw index bytes+w/h+사용색 일치 0, active RGB/indexed도0. source_owner IMG는 미확정 None.
- actual prepare_texture 메모리(NullCache)로 maxA>=16만 확인. 공식 감사/독립 HD 재생검증 없음. 라이브/DB/코어 수정 없음.
- Claude 확인 fixture: `test_current/parts/native_weapon_source_2_11/unit2_weapon11_source.state` +240.
- 알려진 위험: 개별 생성이므로 인접 부품과 절단면 연결·작은 부분 상세 발명·금색 센서 및 장갑 음영 정확성 확인 필요. 준비된 부품 숫자를 해당 기술 전체 HD 완료로 해석하지 않음.
