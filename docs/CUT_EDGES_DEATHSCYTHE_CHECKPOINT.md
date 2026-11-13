# 공통 절단 경계·데스사이즈 확대 자세 체크포인트

2026-11-12. 전체 기체·전 무장 완료 보고서가 아니다.

## 적용

- `part_cut_edges.py`: 원본 아틀라스의 양쪽에서 불투명한 유사 색 면이 이어지고 원본에는 어두운 선이 없을 때만, 절단 가장자리의 얇은 검은 잉크를 HD 안쪽 색으로 보정한다. 알파는 바꾸지 않는다. 실제 외곽/장갑선은 보존한다. 의미를 판단할 수 없는 경계까지 자동으로 해결했다는 뜻은 아니다.
- 이 보정은 특정 기체가 아니라 모든 `PartsRenderer.prepare_texture` 소스에 적용된다. 캐시 키에 정책 세대를 넣었다. 기존 정렬된 4배 텍스처를 재사용해 보정하고, 변경된 데스사이즈 소스는 새로 정렬·굽는다.
- 재굽기 총 소스 89,199개, 오류 0. 중단 전에 구운 3,000개를 제외한 마지막 실행은 86,199개를 처리했다. 이전 캐시 행은 삭제하지 않아 저장소가 약 2.57GB다.
- 데스사이즈 IMG7108의 110개 연결 항목을 새 전용 그림으로 연결했다. 확대 자세의 세 OBJ는 같은 완성 그림을 실제 OAM 변형의 역변환으로 구웠다. 팔/몸통에 임의로 다른 그림을 재사용하지 않았다. 원본 금색 뿔, 초록 눈, 회색/백색 장갑, 빨간 턱·통풍구 배색을 기준으로 그렸다.
- 새 그림의 턱 아래 불필요한 가로 막대를 제거하고, 두 손이 같은 높이의 자루를 잡도록 다시 제작했다. 중앙 파츠의 실제 출력 창 위쪽으로 머리가 잘리지 않도록 배치했다.
- 명시적으로 분류한 캐릭터 컷인은 기체/무기 뒤가 아니라 앞에 표시하고 대사 UI 아래에 둔다. 기체 확대 컷인·구름 BG는 이 규칙에 포함하지 않는다. 아직 분류되지 않은 모든 BG까지 검증했다는 뜻은 아니다.

## 검사

- 공통 경계 보정: 네 방향, 원본 장갑선 보존, 실제 외곽 보존, 알파 불변 합성 사례 검사 통과.
- `verify_repository_layout.py`: 보호 ROM/기존 얼굴 변경 없음, 소스 묶음 private 파일 없음, 런타임 가져오기/구조 검사 통과.
- 데스사이즈의 해당 확대 자세 20프레임: 아래 실제 기록. REVIEW는 자동 검사에서 측정한 결함이 없다는 뜻이며 전체 공격 완료 판정이 아니다.

```json
{
  "verdict": "REVIEW",
  "frames": 20,
  "vanished_frames": 0,
  "loading_frames": 0,
  "held_frames": 0,
  "mixed_frames": 0,
  "hd_area_share_settled": 1.0
}
```

- 실제 출력은 `test_current/combat/runtime_path/deathscythe_pose/`에 있다. 0프레임은 ready 전달 전 원본이 남을 수 있으므로 8프레임 이후도 함께 본다. 컷인이 기체보다 앞, 대사창이 컷인보다 앞인 것을 확인했다.
- 기체 연결 상태를 가리는 컷인과 별도로, 실제 프레임의 세 OBJ 변형으로 조립한 그림은 `test_current/parts/deathscythe/assembled_pose.png`다. 이는 고정된 미술 검사이며 실시간 재생 성능 검사는 아니다.
- 6개 추가 상태 180프레임 회귀: 소실 0. REVIEW 1, INCOMPLETE 5. 기존 미연결 파츠/효과는 남아 있으며 이 숫자를 정상 완료로 보고하지 않는다.

## 재현

```powershell
python scripts/assets/install_deathscythe_attack.py --apply
python scripts/assets/bake_parts.py --workers 4
python scripts/verify/verify_runtime_path.py --state test_current/parts/deathscythe/pose_7108.state --frames 20 --save-frames 0 4 8 12 16 --name deathscythe_pose
python scripts/verify/verify_deathscythe_art.py
```

설치 도구는 전용 연속 그림이 있으면 역변환까지 수행한다. 그림을 다시 저장하면 반드시 다시 굽는다. 테스트 EXE는 현재 작업 폴더의 에셋과 구운 저장소를 읽게 했고, 일반 배포 실행과 구분한다. ROM/상태/캐시는 공개 소스에 추가하지 않는다.

## 남은 것

전 기체의 그림을 사람이 검사한 것은 아니다. 명백한 절단 잉크만 공통 보정했으므로 잘못 그린 장갑선·해부학적 구조·색·알파는 추가 원본 대조와 재작화가 필요하다. 데스사이즈의 다른 자세, 빔 날/효과와 기존 INCOMPLETE 장면도 남는다. CPU/GPU 읽기 통합·60fps 달성은 이 작업의 검증 범위가 아니다.

## 최종 재검사
마지막 머리 가드와 재굽기 이후 20프레임 검사를 다시 실행했다. REVIEW 1, 소실/로딩/원본 유지/혼용 0, 안정 구간 HD 면적 비율 1.0이다. 8프레임 그림과 기체 단독 조립 그림을 직접 확인했다.
최신 SRW_W_Test.exe는 기체별 전투 테스트 창으로 실행됐다. 다만 Windows 캡처가 두 번 모두 'window crop is outside captured monitor'로 실패해 EXE 화면의 시각 검증은 미완료다. 실행 성공을 시각 검증 성공으로 간주하지 않는다.
