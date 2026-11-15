# 민트 효과95468 /95470 새 전체그림 후보

- 최신 HANDOFF_TO_CODEX_6.md를 읽고 중앙 live바인딩을 스냅샷과 대조했습니다. 두 prior spec 모두 같았으며 마지막 파일 검증 직전 다시 live SHA를 확인했습니다.
- 정확한 출처: IMG21657.95468=[160,0,32,16],95470=[160,32,16,32]. 두 raw사각형은 겹치지 않습니다. 더 큰32×64부모에는 무관한 다른 연출 조각이 들어 있으므로 무관한 그림을 다시 칠하지 않고 두 sourcecell을 각각 일관된 전체master로 그렸습니다.
- Native index_pixels를 ROM IMG의 정확한 사각형과 직접 비교했고 둘 다 전부 같습니다. actual16색 팔레트의 BGR555 재구성으로 hash/index_hash CRC도 live와 일치했습니다. key색은 index0 투명 밑에만 있고 실제 칠한 cyan key픽셀은0개입니다.

## 최종 패킷

- candidate_packet_95468_corrected.json: 생성원본 generated_95468_corrected.png / candidate_95468_corrected.png / contract_95468_corrected.json / native_95468.png.
- candidate_packet_95470.json: 생성원본 generated_95470.png / candidate_95470.png / contract_95470.json / native_95470.png.
- final_packet_index.json의2개만 제출 대상입니다. generated_95468.png/candidate_95468.png는 왼쪽 끝이 너무 가늘었던 초안이며 보존만 했습니다.
- 각 패킷에 contract/drawing/native/generated 4역할SHA와 해당바인딩 prior_binding_spec_sha256 맵을 기록했습니다. 중앙 라이브러리/큐/DB/manifest/설치목록은 수정하지 않았습니다.

## 형태·제작 증거

- 95468: native103 / 새그림105텍셀(alpha64초과로 읽기만한 측정), native/후보 bbox 모두[0,0,29,16]. IoU0.8571. 원본72로 가늘어진 결함을 재제작했고 왼쪽·아래 끝이 다시 칸 가장자리까지 닿습니다. 반투명 경계까지 포함한 알파 질량은87.81 native텍셀입니다.
- 95470: native150 / 새그림150텍셀, native/후보 bbox 모두[0,2,14,31]. IoU1.0. 기존76으로 반감된 면적을 복구했고 분리된 위 점·긴 틈·아래쪽 본체끝·오른쪽 분리꼬리 위치를 유지했습니다. 알파 질량129.45 native텍셀, 절반알파 이상136텍셀입니다.
- sourcealpha 스탬프나 마스크로 위 수치를 만들지 않았습니다. producer_whole_master_proof.json은 원본리소스/인덱스SHA, 각 실제 생성파일SHA, 선택master 계보, 전체 생성PNG를 단순resize한 후보와 픽셀이 완전히 같다는 증거를 담습니다. 생성3회 중 최종wholemaster2개입니다.
- native_candidate_gray_final.png를 회색 합성으로 눈 확인했습니다. 처음 source도 회색합성으로 확인하여 투명밑 cyan RGB를 연출로 오인하지 않았습니다. 최종 생성 프롬프트는 prompt_95468_corrected.txt / prompt_95470.txt입니다. built-in image_gen을 사용했습니다.
- 알파 임계값 삭제·형태 마스크·코드 재색칠·클린업은 전혀 하지 않았습니다. 생성알파 보존, 후보 변환은 전체canvas4배 해상도resize뿐입니다. 측정의 알파64/127 기준은 파일을 변경하지 않는 통계입니다.
- 먼 빈공간 alpha8초과 비율:95468=0%,95470≈0.187%. 새 배경사각 매트는 없습니다. 생성기 미세 경계/먼지는 남아 있을 수 있습니다.
- 제작 그림2 / native만 준비0 / 실제 게임 연결·검증0. 자동 수치와 제작 눈검사를 실제 게임 합격으로 표시하지 않았습니다. Claude가 최종 폭·끝점·분리점·실제 연출 이음매를 확인해 주세요.
