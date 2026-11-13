# 기계 입방체 연속 그림 네 조각 인계

현재 단계: 그림 후보·생산 입력 준비 완료, 연결/굽기는 루트 담당, 독립 QA·실제 HD 재생은 Claude 대기입니다.

- 직접 설치 입력: `install_contract.json`, `candidate_atlas.png`, `native_atlas.png` (packed 하위가 아닙니다).
- 실제 상태: `test_current/parts/native_weapon_source_348_1400/unit348_weapon1400_source.state`, +175.
- 전체 원본 문맥: `test_current/parts/actual_mechanical_pose_348_175/whole_native_context.png`
- 원본은 같은 80×80 입방체 그림을 네 사각형으로 겹쳐 그립니다. OAM0 (0,48)64×32, OAM1 (48,48)32×32, OAM2 (48,0)32×64, OAM3 (0,0)64×64입니다. 원본 화면 위치는 (92,40) 기준이고 반전/affine이 없습니다.
- 원본 겹침 여섯 곳의 indices/실제16색이 완전히 같습니다. 하나의 새 그림에서 네 개로 잘랐고 새 RGBA 겹침 여섯 곳의 SHA 동일을 기록했습니다.
- 현재 활성 RGB/안전 indexed 연결 없음, NullCache 메모리 준비 네 개 모두 불투명 입력 존재. 원본 RGB/알파 스탬프는 쓰지 않았습니다.

Claude 확인점: 입방체 투시/모서리와 굵은 전면 가로 틈의 위치·두께, 회로 홈의 밀도, 새 밝기와 원래 자홍색, 실제 조립한 네 조각의 경계입니다. 이 후보는 관측된 +175의 네 조각이며 다른 기술/팔레트 단계 전체 완료를 뜻하지 않습니다. 소유 IMG는 None/source_owner_confirmed=false입니다.
