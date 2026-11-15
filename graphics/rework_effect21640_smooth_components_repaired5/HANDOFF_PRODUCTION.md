# 21640 연속 HD 경계 재제작 후보 5개

- 고정 폴더 claude_effect21640_correction의 이전 계단형 후보를 새 그림으로 교체했습니다. 교체대상은 94480/94481/94482/94483/94486입니다. 정상8개는 live_before.png 자체RGBA와 메타데이터를 byte비교로 보존했습니다. 최종후보는 정상8영역도 기존그림을 그대로 포함합니다. 정상부모와 동일한 child의 임의변경은 없습니다.
- 최종설치 입력은 final_flat_contract.json(install_contract.json도 같은내용),native_atlas.png(184×32),candidate_atlas.png(736×128)입니다. 후보 SHA256=21b4b52e79ff6a541d57733d98501fc318c70a45910db59df59e14dea1722c99. smooth_sha256.json에서 최종 계약/원본/생성원천 SHA를 확인하세요.
- 실제 index raw와 전체16색 BGR555/RGB 및 source좌표는 기존 관측계약 그대로입니다. final flat에 source_box와 atlas_box를 별도로 기록했습니다. fixture state/frame은 claude_fixture_frames.json과 계약의 state/frame 필드를 유지했습니다. 별도 미관측 확장 없음.
- 원호2개(94480,94481),좁은notch를 가진 넓은 채움1개(94486),삼각채움2개(94482,94483)를 각각 내장image_gen으로 새로 그렸습니다. 원본 픽셀계단을 확대하거나 흐린 것이 아니라 고해상도 연속 외곽/내곽 경계를 새로 만들었습니다. smooth_generated_ID.png와 smooth_own_ID.png에 원천과 등록후 그림을 보존했습니다.
- 94480 첫 연속생성은 왼쪽다리가 가늘어 채택하지 않았습니다(rejected_94480_thin_leftleg.png). 다시 생성하여 왼쪽 붉은 다리의 채워진폭을 확보했습니다. 94482 첫 생성의 외부glow도 폐기했습니다(rejected_94482_exterior_glow.png). 최종은 배경/원호중앙 구멍이 실제 투명한 그림입니다.
- 새그림은 흰 중심,옅은분홍과산호빨강테두리의 실제팔레트계열을 유지합니다. 기존 노랑/주황 불꽃색을 쓰지 않았습니다. 계단에서 연속곡선으로 바뀌며 원본의 미세격자 경계/색면과 다르게 보이는 부분은 남아 있습니다.
- 원본RGB/alpha전사,생성알파문턱삭제,morphology,타팔레트/다른기체alpha차용 없음. 생성자체RGBA bbox crop/resize만으로 원래위치/채워진범위에 등록했습니다(smooth_geometry_registration.json).
- 후보 및 최종prepare 사전검사 모두 flags=[]입니다(smooth_candidate_geometry.json,smooth_prepare_geometry.json). IoU는 94483=.836,94481=.881,94480=.829,94486=.959,94482=.883, 미칠최대.055,밖0입니다. 자동검사 통과는 공식QA가 아닙니다.
- NullCache PartsRenderer.prepare_texture로 최종좌표13개 모두 nonempty 및 실제index/alpha/RGB원본입력 일치입니다(smooth_production_report.json). 정상8개메타는 preserved_normal8_live_metadata.json입니다.
- 수동 회색RGBA합성 비교 smooth_native_rejected_candidate_prepare.png는 왼쪽부터 원본/이전불합격계단후보/새후보/prepare입니다. 알파0RGB 잔여를 실색으로 오인하지 않았습니다. 연속경계,원호구멍,삼각채움 및 아랫면 절단을 확인했습니다.
- 이전불합격근거는 rejected_pixelstairs_*로 보존했습니다. 새후보생성 재현은 smooth_finalize.py 또는 finalize_candidate.py입니다. 예전 rejected_pixelstairs_finalize.py는 실행하지 마세요.
- 라이브러리/sqlite/공유코드/코어/EXE/배포/푸시/모니터/게임창을 수정하지 않았습니다. 설치/굽기/동일도구정식검사 및 Claude 독립시각/게임검증 대기입니다.
