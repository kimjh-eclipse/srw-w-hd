# 빅 볼포그 연속 그림 여섯 조각 제작 인계

현재 단계: 후보 그림과 생산 입력 준비 완료. 연결·굽기는 루트 담당, 실제 HD 재생·형태/색/레이어 판정은 Claude 대기입니다.

- 설치 입력: `install_contract.json`, `candidate_atlas.png`, `native_atlas.png`
- 새 그림: `generated_master.png`, `candidate_continuous_master.png`
- 원본 전체 문맥: `actual_mechanical_pose_378_215/whole_native_context.png`, `actual_mechanical_pose_378_235/whole_native_context.png` (같은 parts 폴더 아래)
- 실제 상태: `native_weapon_source_378_1506/unit378_weapon1506_source.state`, +215 / +235.
- 여섯 고유 계약: 신규 미연결 네 종 + 기존 54395 / 54399 두 종 교체. 반드시 여섯 조각을 한 master로 함께 연결해야 합니다.
- 원본 같은 그림 겹침 13곳은 인덱스/실제 16색 동일. 새 그림 겹침 13곳의 RGBA SHA 동일, 여섯 crop SHA 동일을 기록했습니다. 원본 alpha나 RGB를 새 그림에 찍지 않았습니다.
- 메모리 전용 준비 결과 여섯 모두 alpha 최대 255입니다. 신규 네 종은 현 활성 RGB/안전 indexed 연결이 없고, 기존 두 종은 명시적 교체 대상입니다. 이 확인은 입력 누락 검사이며 공식 QA가 아닙니다.
- +245 네 조각은 동일 원본 형상의 노란 조명 단계로 `palette_phase_aliases_pending.json`에 실제 색/해시/기본 계약 포인터를 기록했습니다. 미완료이며 새 붉은 그림이 그 단계에도 보인다고 주장하지 않습니다.

Claude 확인점: 원래 비대칭 얼굴/날/오른 주먹/오른 발의 위치와 폭, 가는 날의 연결, 생성된 장갑 면과 원본 실루엣 차이, 조각 경계의 단절, 확대·축소 단계에서의 한 픽셀 겹침입니다. 실제 화면 affine와 좌표는 변경하지 않았습니다. 이 그림은 관측된 붉은 조명 전용이며 일반 색상 완료가 아닙니다.
