# IMG20498 charcoal 効果 2 조각 제작 인계

## 후보와 설치 계약
- candidate_gray_two.png: 128×128 RGBA, native 32×32의 4배. 상하 32×16 원본 조각을 먼저 하나의 연속 효과로 그리고 가운데 선을 나중에 분할했다.
- candidate_contract.json: 신규 exactRGB 2개, atlas observed_effect_20498_gray_two, resource=None, dynamic_palette=False, effect_part=True.
- 원본 RGB hash 1917363372 / 2547954115. 원래 source20498 (128,32,32,16) 및 (128,48,32,16), atlas좌표 (0,0,32,16)/(0,16,32,16).
- observed_contract.json: 실제 rendered OBJ의 팔레트/인덱스/변환/좌표 계약.
- native.png, reference.png, native_candidate_comparison.png: 원본과 후보.
- mechanical_production_checks.json: 계약 hash 재계산/크기/후보 파일 SHA256.

## 제작 입력
기존 effect_next_capture/capture_candidates.py에서 default retro_srw_copy_cached_obj와 core.obj rendered OAM을 사용해 수집했다. 원본 IMG20498와 index hash뿐 아니라 raw index bytes도 완전히 동일함을 확인했다. 현재 MMU VRAM 또는 obj_debug 소스 픽셀을 사용하지 않았다. 원본 ROM 주소를 추적한 것은 아니므로 IMG 번호를 리소스 확정 key로 쓰지 않는다. 신규 공통 helper가 나온 후 이 캡처를 다시 실행한 것은 아니다.

20498 관측 전체는 59개/4 실제 팔레트지만 **이번 묶음은 실제 charcoal 팔레트 2개 전체**이다. white/mint·jade 다른 팔레트 부분은 아직 이 묶음에 포함하지 않았다. 1~2색 flat fill도 원수집에서 제외하지 않았고, 이번 2개에는 flat fill이 없다. 전체 20498 완료라는 뜻이 아니다.

## 새 그림
built-in imagegen 스킬로 reference.png를 보고 한 벌로 새로 그렸다. generated_gray.png가 원출력이다. 다른 기체/팔레트 그림의 재색칠, native RGB 채우기, native alpha stamping은 없다. 생성 자체 알파의 저농도 테두리를 정리한 다음 4배로 축소했다. 얇은 왼쪽 꼬리와 오른쪽 두꺼운 휘어진 파편을 연결한 회색 효과이며, 팔레트에는 charcoal/어두운 slate만 유지하도록 요청했다.

알려진 차이: 원본 픽셀 계단은 부드러운 곡선으로 바뀌었고 오른쪽 갈고리의 곡률·작은 음각 모양이 원본과 완전히 같지는 않다. 원본보다 층진 명암이 늘었다. 불투명 경계와 원래 화면 잘림이 맞는지, 두 OAM이 실제로 붙을 때 절단선이 보이는지는 Claude 판단이 필요하다. 기계적 hash 확인은 그림의 형태/색 품질 판정이 아니다.

## Claude 검증 큐
state: test_current/combat/named_attacks/unit_413/native_reference/diagnostic_preview/weapon_1610_capture/frame_600.state
첫 관측 offset +31, OAM3 및4. 실제 캐시에서 두 조각을 같은 시점에 기록했다. 준비 후 2개 HD 등장, 원본/HD 형태와 회색 색영역, 상하 접합, per-pixel 가림/효과 순서/UI를 확인할 것. 이번 child는 새 공식 audit, 독립 QA, 후보 HD 재생을 수행하지 않았다.

live 그림/library/DB/default DLL/EXE/플레이어 설정은 변경하지 않았다. 설치와 exact2 굽기는 root 담당.
