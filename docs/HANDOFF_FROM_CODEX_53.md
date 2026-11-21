# Codex → Claude: 11/19 새 그림 수령 및 검수

## 현재 범위와 숫자

- 11/18 23:28에 고정한 일반 자세 필수 반려 180자세 중 **179자세에 새 RAW가 있음**. unit22 pose02는 고유 runtime_original_preserved_no_hd_recolour 원본 증거를 재검증해 신규 생성 없이 정책제외. 이 목록에서 미수령 신규 그림은 0자세.
- 위 숫자는 **그림 수령**이며 구조 합격·원본 픽셀 위치 일치·분할·설치·게임 확인 완료 수가 아님. 추가 교정 실패도 아래에 별도 기록.
- affine 현재 254판/894타깃 중252판에RAW 있음. unit386 sheet_a01/a02 두 판은 기존 도구 콘텐츠 제한 중단 항목. 재시도/우회 안 함.
- built-in imagegen만 사용. 원본 자체 색으로 새그림, actual4xBRZ는 윤곽 보조. 생성 RAW는 반환 즉시 프로젝트에 바이트 그대로 저장. 생성 픽셀 재색칠·마스킹·크기변경·합성 없이 인계. ROM·라이브러리·큐·기존 후보는 이번 재개 작업에서 수정하지 않음.

## 수령 목록 / 프롬프트 / 좌표

- 전체 일반 자세 신규RAW 가용성: [NATIVE_REDRAW_CAMPAIGN_PROGRESS_20261118.json](C:/Emul/Workshop/SRW_W_HD/test_current/parts/NATIVE_REDRAW_CAMPAIGN_PROGRESS_20261118.json)
- 일반 자세 각 RAW/SHA/요청 프롬프트/알파/크기/새 layout: [NATIVE_ROOT_REDRAW_DELIVERY_INDEX_20261118.json](C:/Emul/Workshop/SRW_W_HD/test_current/parts/NATIVE_ROOT_REDRAW_DELIVERY_INDEX_20261118.json)
- 추가 중간군 preferred RAW→layout: [NATIVE_MIDDLE_PREFERRED_RAW_LAYOUT_20261118.json](C:/Emul/Workshop/SRW_W_HD/test_current/parts/NATIVE_MIDDLE_PREFERRED_RAW_LAYOUT_20261118.json)
- 추가 저번군: [NATIVE_REJECT_LOW_FINISH_DELIVERY_20261119.json](C:/Emul/Workshop/SRW_W_HD/test_current/parts/NATIVE_REJECT_LOW_FINISH_DELIVERY_20261119.json)
- 추가 고번군: [NATIVE_REJECT_HIGH_FINISH_DELIVERY_INDEX_20261118.json](C:/Emul/Workshop/SRW_W_HD/test_current/parts/NATIVE_REJECT_HIGH_FINISH_DELIVERY_INDEX_20261118.json)
- 앞선 담당별 납품과 affine/cutin 전량의 상세는 [HANDOFF_FROM_CODEX_52.md](C:/Emul/Workshop/SRW_W_HD/docs/HANDOFF_FROM_CODEX_52.md), 각 local HANDOFF/DELIVERY/PREFERRED 파일을 함께 볼 것.

원본만 재배열한 보조판은 옛 SHEETS 좌표를 바로 적용하면 안 됨. 각 RAW에 짝지은 새 layout으로 추출한 뒤 원본 contract 위치에 연결. RAW 실제 캔버스는 요청과 다를 수 있으므로 비율·개별 자세 크기·여백을 독립 검수. 해상도/aspect gate 통과는 구조 승인 아님.

## 최근 우선 수령 그림

| 대상 | 우선 RAW / 매핑 | 육안 확인과 남은 검수 |
|---|---|---|
|362 반려15자세|C:/Emul/Workshop/SRW_W_HD/test_current/parts/native_redraw_20261118/unit_362/sheet_01~03/ 각 RAW_imagegen.png|연녹색 궤적/3선·봉·손·총구·발·등짐·칸끝. 02판은09만; 비교/기존accept 교체금지.|
|223 누락8,225 반려5|C:/Emul/Workshop/SRW_W_HD/test_current/parts/native_redraw_20261118/unit_223 및 unit_225/ 각 request/DELIVERY|22500흰속도선,06검은상태,09/11/15흰어깨·팔·등. 대상외accept 교체금지.|
|29104/15/17|C:/Emul/Workshop/SRW_W_HD/test_current/parts/native_redraw_20261118/unit_291/sheet_selected/RAW_imagegen.png|보라선 사이 알파 빈틈 있음. 원본 날개 해칭 범위/밀도/각도·사지 정렬 검수.|
|29508/11,29607/10|C:/Emul/Workshop/SRW_W_HD/test_current/parts/native_redraw_20261118/unit_296/sheet_selected/IDENTICAL_SOURCE_PROOF.json|연속주먹 잔상 새작화. 295/296은 전체 원본RGBA·크기·칸좌표 완전동일 증거로 RAW byte공유, 색변환0.|
|30505/09|C:/Emul/Workshop/SRW_W_HD/test_current/parts/native_redraw_20261118/unit_305/sheet_selected/PREFERRED_TARGETS_ROOT_20261119.json|첫 금속봉 같은 속도선 제외. source-only RAW_imagegen_234725.png의 가는 평면선 우선 검수.|
|30901/08|C:/Emul/Workshop/SRW_W_HD/test_current/parts/native_redraw_20261118/unit_309/sheet_selected/RAW_imagegen.png|각target 눈6개와 좌하붉은손 보임. 원본 위치/촉수 연결/가림은 별도 검수.|
|47106,47508|각 unit의 C:/Emul/Workshop/SRW_W_HD/test_current/parts/native_redraw_20261118/unit_N/sheet_selected/|새판 발끝·구름상단이 캔버스 안에 있음. 원본 여백·정렬/크기·발모양 검수.|
|47905|C:/Emul/Workshop/SRW_W_HD/test_current/parts/native_redraw_20261118/unit_479/sheet_selected/RAW_imagegen.png|실제alpha 회색에서 검정 불투명 발사블록 보임. 블록/빔 원본 범위·색·가림 검수.|
|48301,48901|C:/Emul/Workshop/SRW_W_HD/test_current/parts/native_redraw_20261118/unit_483/sheet_selected/PREFERRED_TARGETS_ROOT_20261119.json 및 unit_489/sheet_selected/IDENTICAL_SOURCE_PROOF.json|첫pixelstyle RAW 제외, RAW_imagegen_072723.png 우선. 실제alpha 회색에서 중앙몸통 구멍과 분리파편 확인. 489는 동일원본RGBA 입증해 같은RAW byte공유. 파편 정확수·범위/색·위치검수.|
|48404|C:/Emul/Workshop/SRW_W_HD/test_current/parts/native_redraw_20261118/unit_484/sheet_selected/PREFERRED_TARGETS_ROOT_20261119.json|최종 target04_only/RAW_imagegen.png SHA0628e4e03a157cc903cd484cbc11fcd5913c8cf3b39ce74817d1f7611d68662d. 단독832×452 요청→1702×924 RAW, aspect gate통과. 실제alpha 회색에서 원형halo 없이 작은 십자/사각점 보임. 입자 수·크기·색·미세음영 검수. **단독layout 사용**, whole판 좌표로 직접추출 금지. 첫판 원형halo/두번째 비율실패 제외.|

## 미해결 또는 승인하지 않은 부분

- affine324 a26 mint6색 영역과 affine359 소형4색 패널: 11/19 source-only 추가1회씩 했으나 색면 내부 gradient/명도변화 잔존. preferred=false. 해결로 세지 않음. local qa_flat_sourceonly_20261119 RAW/HANDOFF 참고. 강제팔레트치환/양자화 안 함.
- 336 추가 교정에서 눈에 보이는 아래 그림자는 사라졌으나 실제 source밖 alpha1 잔여 있음(원래0). 엄격한 외곽alpha0 미해결. 새 preferred는 중간군 map에 있음. 마스킹 안 함.
- 372 새본체판 외 효과 전용 평행선 보조RAW 추가. 본체 없는 효과 RAW를 본체와 혼동하지 말 것. 일부 칼날 같은 읽힘과 범위·밀도·가려짐·정합 아직 미검증.
- 46907 실루엣은 검정뷰에서 비어보이지만 실제alpha 회색에서는 하단 검정형태 있음. 상단 비교그림은 출력 안 됐으므로 사용금지. 내부alpha252~253과 원본255 차이, 비율/coverage 검수 필요. 원본에 없는 내부몸체/눈 추가금지.
- 모든 신규RAW의 얼굴/손·발/어깨·몸통 연결과 효과색·불투명영역 coverage는 Claude 확인 필요. 정합에서 대량의 원본 도트로 메워져야 보이는 상태를 HD완료로 승인하지 말고 filled_px/원본덧메움과 함께 보고할 것.
- READONLY_GRAY_*.jpg/png는 실제알파를 회색에 올린 **검수 사진**이며 설치용 그림 아님. 검정뷰의 RGB노이즈가 알파0에 숨어 있는 것과 실제 잘못 그린 halo/그림자를 구분할 것.

## 새 원본 / 기존 판정 확인이 필요한 요청

[CLAUDE_SOURCE_PACKET_REQUEST_AUDIT_20261119.md](C:/Emul/Workshop/SRW_W_HD/docs/CLAUDE_SOURCE_PACKET_REQUEST_AUDIT_20261119.md)에 원본 경로·SHA·장면 증거와 요청을 정리함. 바로 그릴 수 있는 새 유효패킷은 현재0건.

- 33902: 깨진 상체 원본 그대로임. weapon1377 obj057 / pose150 frame614·616 정상 상체 재캡처 필요. 깨진 그림에서 정상몸체 추정 금지.
- unit1 크리티컬 몸체,130/135 돌진·붉은결합,130 형제자세050/083/134,213/40 자기팔레트: 정확 장면·조립 계약/자기색 원본 부족. 130 obj072 기존 준비본은 긴왼쪽총으로 보이며 사용자가 말한 왼팔주먹 돌진인지 확인 전 생성하지 않음.
- 26512·36402는 오래된 HELD와 최신 EYE accept가 충돌. 새그림으로 자동 재반려하지 말고 적용 후보SHA/가림/A0창 판단부터 재확인. 26614는 원본 headfragment만 있으며 하반신 없는 것을 새다리로 지어내지 말 것.

새 원본이나 구체적인 반려 검수가 오면 그 근거와 원래 색으로 이어서 새로 그릴 것. 현재 RAW 수령을 전체 이미지 작업 최종완료로 표시하지 않음.
