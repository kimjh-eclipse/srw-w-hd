# Codex → Claude 인계 51 — 실제 한도 재확인·원본 검토 준비 완료

최신 인계입니다. 50의 준비 단계 뒤 실제 신규 작업1개를 요청해 도구 상태를 확인했습니다.
마징카이저23021 요청은 **HTTP429 usage_limit_reached**로 실패했습니다. 이번 연속 작업 실제호출1/실패1/새RAW0/새candidate0. 이후 추가 생성 호출은 하지 않았습니다.
응답 epoch1795003558,당시 resets_in_seconds3604,해제예정 **2026-11-18 21:05:58 KST**.
실제 응답 원문은 cutin_requests/mazinkaiser_fire_blaster/codex_prepared_20261118/request_23021.json의 failure와 quota_response에 보존했습니다.
종합 상태: test_current/parts/CODEX_PREPARATION_STATUS_20261118.json. 시간 도래가 재개 실행 증거는 아닙니다.

## Affine 원본 사전 검토 완료분

**AFFINE_CODEX_VISUALLY_PREPARED_INDEX_20261118.json**의 preferred request를 사용하세요.
43generic+142specific 총44판을 각 담당자가 실제 native/actual4xBRZ/style 이미지로 확인했습니다. source/참조SHA132개를 마지막에 재검증했습니다.
- 안전 snapshot43기체44판114 unit-pose target. 실제 그림 내용이 있는 대상113개.
- unit131 pose_a02는 원본128×96 전체A0. source_empty_needs_claude_validation/skip_generation이며 의도된 빈 프레임인지 builder 누락인지는 미확정. 새 로봇을 발명하거나 HD완료로 세지 않습니다.
- 각 폴더의 generation_request_visual.json이 구체 시각 주의사항을 담습니다. 기존 generation_request.json은 보존했으며 generic 요청을 그대로 실행하지 않습니다.142는 기존 구체 요청이 우선입니다.
- cutin_agent14판43target / remaining_agent14판26target / affine_agent15판42target +142의3target=114입니다. 총량 중 빈1개는 위와 같이 분리했습니다.
- 분리 파츠판(unit0),불투명 사각 구역(3/46),세로field형태(7),아주 작은 쐐기조각(19/77),잘린 조각·사선효과묶음(49),가로기계assembly(52),긴대각shaft(81),후면파이프/부분기체(98) 등은 기본로봇 몸통을 복사하거나 숨은부품을 채우면 오류입니다.
- source opaque nearBLACK과 A0를 구분했고,패딩 안의 내부 hardcut을 전체 슬롯 가장자리 접촉과 혼동하지 않도록 기록했습니다.
- 원본 중복을 합친 target원본93개/고유source판38개는 기존 snapshot통계이며 실제그림/승인수가 아닙니다. exact source+layout 일치군만 같은 RAW 재사용 가능,색이 다르면 재색칠 공유 금지.

각 집계와 HANDOFF:
AFFINE_VISUAL_REVIEW_CUTIN_AGENT_20261118.json / _HANDOFF.md
AFFINE_VISUAL_REVIEW_REMAINING_AGENT_20261118.json / .md
AFFINE_VISUAL_REVIEW_AFFINE_AGENT_20261118.json / AFFINE_VISUAL_REVIEW_AFFINE_AGENT_HANDOFF_20261118.md

## Live builder 변경 주의

live SHEETS를 빌더가 다시 쓰며 그 안의 준비 폴더도 삭제됐습니다. 중앙 snapshot 경로 affine_codex_prepared_20261118/에 원본/계약/레이아웃을 복사해 보존했고, live원본을 이동/삭제하지 않았습니다.
초기8판38target은 변경6판·삭제2판의 오래된 snapshot으로 격리했습니다. 현재 미생성에 단순 합산하지 마세요.
19:56:41 live snapshot은60기체61판178target였고 중앙밖17판은 미감사입니다. 진행중인 빌더라 현재 전체/최종잔여수량은 아닙니다.

생성 직전 **현재 unit/pose_aNN↔weapon/object/source/layout/contract SHA**가 snapshot과 일치하는지 다시 확인합니다. READY manifest가 있으면 이용하되, 별도 작업 허가/승인 절차를 만들라는 뜻은 아닙니다. 핵심은 실제 원본·계약의 일치입니다. 바뀌거나 사라진 자료는 오래된 요청으로 생성/설치하지 말고 다시 준비합니다.
그림은 정방향·원래 크기 그대로,회전/확대는 게임이 적용합니다. 첫 칸 기본 자세는 비교용,가려진 조각 설치정책은 Claude 담당이며 보이는 원본 조각 삭제/숨은부위 완성 금지입니다.

## 컷인5·기존미생성 준비

**CUTIN_CODEX_PREPARED_INDEX_20261118.json**에5레이어의 최신 preferred request/참조SHA/실제호출상태를 갱신했습니다.
23021만 실제1회429,나머지4개는 준비만/호출0입니다. 모두 새RAW/candidate없음.
-23021 1024×576 투명기체:RED V/RED보석·검은장갑·은색얼굴·뿔·두주먹. 청록OBJ V와배경/HUD그리지않음.
-24557 1024×512 불투명녹황색배경:가로반복좌우연결.
-22864 960×576 투명크루제:화이트 eye-mask가 원본권위. preferred는 **generation_request_22864_source_only.json**입니다. 잘못된 맨눈 기존HD를 참고에서 빼고 원본 회색합성 보조를 추가했습니다. 기존5참조 요청은 비교보존,새요청의5번째는 잘못된HD가 아니라 동일원본 alpha0확인용GRAY입니다.
-26391 1024² 불투명파란scan배경:세로반복.
-23591 1024² 불투명녹색기둥무대전체:인물BG2제외,전체카메라pan범위. 강제타일요청아님.
최신19:45요청대로 IMG별분리,오래된한장합성안내를적용하지않습니다. 바깥 viewer녹색은 RGB[0,255,0]/A0인원본숨은색입니다. 원본상반신에녹색배경을그리지않습니다.

기존30자세6판(21414/24711/124B5) 준비/참조SHA/RAW없음은 CODEX_REMAINING_PREPARATION_20261118.json/.md에 재확인했습니다.
172전체2자세는 unit172/robot_set/codex_prepared_redraw_20261118/generation_request.json에 직접원본검토·실제BRZ/낮은갈고리윤곽복원프롬프트 준비. 아직새그림없음.
130돌진요청은 PREPARED_NONSTANDARD_SOURCE/weapon541_obj072_20261118/에비표준원본준비.18OAM재합성RGBA0차이지만 원본에왼쪽긴총이있어 요청한왼팔주먹돌진장면과동일한지확인필요합니다. 붉은장갑결합두번째정확obj/패킷은아직없습니다. INDEX/기존큐변경없음.
12401/09·26512·36402 보류검토4건,23/386 도구거부2건은49참조. 앞서최소40은이전범위이지새affine·컷인을포함한전체총량아닙니다.

## 재개

한도해제후 기존미생성6판과새컷인5를우선실제작업으로재개하고,원본/계약이안정된affine visual요청을이어갑니다. 같은기체다른팔레트는자기원본으로새작화하며RAW를바로저장·인계합니다.
생성 전에 준비이미지를 직접 열고참조SHA/기존candidate를 재확인합니다. RAW는바이트그대로보존,코드재색칠/강제warp/alpha threshold삭제없음. 요청크기와다르면차이를숨기지않고보고합니다. Claude가정합/분할/설치/실게임검증합니다.
모든상태는준비또는미완이며,이번에새HD그림이완료됐다고표시하지마세요.

