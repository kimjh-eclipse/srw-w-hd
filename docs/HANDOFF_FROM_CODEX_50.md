# Codex → Claude 인계 50 — 한도 해제 전 생성 준비

입력 HANDOFF_TO_CODEX_9.md의 2026-11-18 19:45 추가 요청까지 확인했습니다. 이번 연속 작업은 원본·참조·프롬프트 준비와 중복/변경 자료 확인입니다. **새 imagegen 호출0회, 새 RAW0개, 새 candidate0개**입니다. 원본/기존후보/라이브러리/큐/시험롬/설치 변경 없음.
이전 실제 한도 응답 해제 예정은 **오늘 21:05:57 KST**입니다. 아직 그 시각 전이라 호출하지 않았고, 새429를 받았다고 주장하지 않습니다. 시간 도래가 자동 재개 실행 증거는 아닙니다.

## 새 컷인 3건·5레이어 준비

통합 인덱스: test_current/parts/CUTIN_CODEX_PREPARED_INDEX_20261118.json.
각 레이어 contract/원본 NN4의 크기·RGBA/참조SHA를 확인하고 실제 xbrz_compare.dll로 4xBRZ를 만들었습니다. NN4 원본이 절대권위,BRZ는 윤곽 보조입니다. 생성 전에 참조 이미지를 직접 열고 SHA/candidate 존재 여부를 다시 확인해야 합니다.

| 레이어 | 요청 크기 | 요청 파일 위치 |
|---|---|---|
| 마징카이저 상반신23021 |1024×576,A0외곽|cutin_requests/mazinkaiser_fire_blaster/codex_prepared_20261118/request_23021.json|
| 녹황색 배경24557 |1024×512,전체불투명·가로반복|같은폴더/request_24557.json|
| 크루제22864 |960×576,A0외곽|cutin_requests/creuset_helmet/codex_prepared_20261118/generation_request_22864.json|
| 파란배경26391 |1024×1024,전체불투명·세로반복|같은폴더/generation_request_26391.json|
| 녹색기둥무대23591 |1024×1024,전체불투명|cutin_requests/taiga_goldion_stage/codex_prepared_20261118/generation_request_23591.json|

- 최신19:45 요청대로 IMG별로 따로 그립니다. 오래된 HD_TODO_NON_ROBOT.md의 한 장 합성 안내는 이번 요청에 적용하지 않습니다.
- 마징카이저는 RED V 가슴판+둥근 RED 보석/검은 장갑/은색 얼굴·뿔/두 주먹. 게임의 청록 V 발광은 별도 OBJ이므로 그리지 않습니다.
- 크루제는 원본의 눈을 덮은 WHITE mask가 권위입니다. 기존 HD의 드러난 노란 눈과 잘못된 square 구도를 복사하지 않습니다.
- 두 인물/기체 레이어 바깥에서 viewer에 보이는 녹색은 원본 RGB[0,255,0]/A0입니다. 녹색 배경으로 칠하면 오류입니다. 무대는 인물 BG2를 그리지 않고 256×256 전체 카메라 pan 범위를 그립니다.
- 요청 크기/위치·투명외곽·내부불투명·매끈한 윤곽을 지킵니다. 잘못된 크기의 RAW를 코드 리사이즈/alpha삭제로 숨기지 않습니다. RAW 먼저 보존하고 차이를 기록합니다. 배경 반복 경계와 실제 화면 연결은 Claude 검증.
- 각 폴더 HANDOFF_PREPARED.md와 xbrz_provenance/XBRZ_SOURCE_PROVENANCE.json 참조. 원본 NN4/xBRZ는 새 HD 후보가 아닙니다.

## Affine: 현재 전체 최종 수량이 아닌 안전 snapshot

문서/인덱스:
- test_current/parts/AFFINE_CODEX_PREPARATION_20261118.md/.json
- AFFINE_CODEX_PREPARED_REQUESTS_20261118.json
- AFFINE_CODEX_SOURCE_IDENTITY_20261118.json
- AFFINE_CODEX_PREPARATION_FINAL_AUDIT_20261118.json

중앙 경로: test_current/parts/affine_codex_prepared_20261118/unit_N/sheet_aNN/.
빌더가 live SHEETS를 다시 쓰면서 그 아래 준비 폴더도 사라졌으므로 새 준비는 중앙에 source/layout/contract를 복사해 보존했습니다. live 원본을 이동/삭제하지 않았습니다.

- 안전 snapshot:43기체·44판·114 unit-pose target. 이 중 서로 다른 target 원본 그림은93개,전체 판+layout이 같은 경우를 합친 고유 원본 판은38개입니다. 이는 HD 품질 승인이나 실제 생성량이 아닙니다.
- 132참조SHA/원본crop158개/targetcontract114개 확인. 실제생성/RAW/candidate 모두0.
- 142 sheet_a01만 직접 source/BRZ/style를 보고 구체 프롬프트 준비. 그 외43판은 generic prepared_pending_visual_review이며 실행 전에 각 원본을 직접 보아야 합니다.
- 최초 cutoff52판 중8판38target은 source/layout변경6판·삭제2판 때문에 quarantined_stale_snapshot입니다. 새 미생성 수량에 그대로 더하지 마세요.
- live19:56:41 snapshot은60기체61판178target였고 중앙 밖17판은 미감사입니다. 빌더가 계속 만들고 있어 현재 전체/최종 잔여 수량이라고 주장하지 않습니다.
- Claude는 빌더 완료 후 **READY manifest(unit/pose_aNN↔weapon/object,source/layout/contract SHA)**를 확정해 주세요. 생성 직전 SHA가 다르면 오래된 준비 요청을 실행하지 말고 재구성해야 합니다.
- 정방향·원래 크기로 그립니다. 확대·회전은 게임이 적용하므로 이미지에서 비틀거나 키우지 않습니다. ≤9칸/첫칸 기본자세 비교만/자기 원본 팔레트 fresh/외곽 A0. <절반가시 조각 설치 제외>는 Claude 설치 정책이며, 보이는 source 조각을 그림에서 임의 삭제하거나 숨은 부분을 지어내지 않습니다.

## 이전 잔여 재확인 및 새 준비

test_current/parts/CODEX_REMAINING_PREPARATION_20261118.json/.md:
- 기존30자세6판(21414/24711/124B5)의 source/layout/실제BRZ/request·참조SHA와 RAW없음을 확인했습니다. 기존 완료 그림과 중복 생성하지 않습니다.
- unit172/robot_set/codex_prepared_redraw_20261118/ : 원본 전체2자세를 새로 그릴 요청·actualBRZ·layout 준비. 공식source2crop RGBA완전일치. 위쪽 I형block/관 과대화 없이 아래 갈고리 윤곽을 원본 바닥까지. 원본00/01 lowest y315,x180~199/184~203도 기록했습니다. 아직 새그림없음.
- unit130/robot_set/PREPARED_NONSTANDARD_SOURCE/weapon541_obj072_20261118/: raw127×86 wholeobject의18OAM 재합성RGBA0차이,exact508×344/실제BRZ/프롬프트·3참조SHA 준비. source는 BLUEWHITE 본체+RED부착/왼쪽긴총이고 전투전체나 파란불꽃은 아닙니다. 요청의 돌진본체(왼팔주먹)와 같은 장면인지 Claude 확인 전 생성하지 않습니다. INDEX/pose/기존큐는 변경하지 않았습니다.
- 붉은 장갑 결합 두 번째 장면은 정확 obj/조합 packet 미지정입니다. Claude가 장면 일치 원본 패킷을 제공해 주세요.
-130/135 affine target은 해당 snapshot에0,130obj072와감사한affine114target의1xRGBA/alpha-crop exact match도 없었습니다. 의미상 중복까지 증명한 것은 아닙니다.
-12401/09·26512·36402는 RAW가 있는 보류/검토4건,23/386은 도구 거부2건. 완료232/234315/182192197 등은 이미 납품했으므로 중복 생성 금지.
- 앞서 말한 최소40은 이전 잔여 범위입니다. 이번에 추가된 affine·컷인5를 포함한 현재 전체 잔여 총량으로 사용하면 안 됩니다.

## 재개·검수

한도 해제 후에도 먼저 한 개의 실제 작업을 실행해 도구 응답을 확인하고, 성공 RAW는 바로 프로젝트에 복사해 전달합니다. 이후 독립 기체/레이어를 병렬 처리하되 소유권/팔레트/pose를 섞지 않습니다. 준비 요청을 실행 완료라고 세지 마세요.
후보는 builtin RAW 그대로 보존하고 코드 재색칠/강제warp/알파threshold수정 없이 넘깁니다. 크기·접합·원본가림·반복경계·레이어분할·설치·실게임 확인은 Claude에게 인계합니다.
이전 실제 납품/한도 실패·보류 자세는 HANDOFF_FROM_CODEX_49.md 이하를 참조하세요.

