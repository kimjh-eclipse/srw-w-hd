# 확대·회전(affine) 스프라이트 HD 누락 (Claude 작성, 11/18 04:10)

## 사용자 지적
필드 전개 장면(히카루·이즈미·아카츠키, unit 142·143·144, 147~149)에서 기체가 원본 도트로 나온다.

## 원인 (조사 확정)
- `scripts/assets/build_pose_packets.py` 69~70행 `rows=[r for r in rows if not r['affine']]` 가 확대·회전 OBJ(affine)를 자세 패킷에서 통째로 뺀다. 개수만 `affine_skipped` 로 센다.
- 그래서 이런 장면은 자세 폴더·native·코덱스 그림 요청·설치가 모두 없다. "모든 자세 accepted/INSTALLED" 는 affine 을 뺀 나머지 자세에 대한 표시였다.
- 팔레트·재색칠 문제가 아니다(142/143/148 필드 형태는 각자 다른 텍스처 해시).
- 예: 142 weapon_592 frame 344~360, affine 64x64 OBJ 두 장(hash 3824650151, 4252818401), binding 0.
- 그리는 쪽(코어 ShouldSkipRobot 의 affine 해시 조회, emulator/hd_parts.py 579/702행 affine 행렬·double-size)은 이미 있어 바인딩만 생기면 그려질 것으로 보인다(실제 표시는 미검증).

## 영향 범위
- affine_skipped>0 캡처: 304개 유닛·550개 무기, 그중 INSTALLED 138개 유닛. 누적 116,697건(회전 빔 같은 이펙트 포함, 기체 본체 고유 텍스처 수는 재생 없이 확정 불가).

## 할 일
1. build_pose_packets.py 에서 affine 행을 버리지 말고 변환 전 정방향 텍스처 기준 `affine_NNN/` 패킷(native.png/native_4x.png/contract.json, 참고용 화면 합성도)을 만든다.
2. 여러 장이 겹쳐 한 형태를 이루면(142: 64x64 두 장, y 10px 차) 한 그림으로 요청하고 나눠서 이음새를 막는다.
3. 이펙트(회전 빔 등)와 기체 본체를 가른 뒤 본체부터 코덱스 그림 요청 → 기존 split/package/install 흐름으로 일반 해시 바인딩 설치 → 실제 렌더로 확인.

증거: scratchpad field_crops.png, 조사 스크립트 probe_affine.py (세션 임시 폴더).
