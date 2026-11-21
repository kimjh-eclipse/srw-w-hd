# 로봇 새작화 화풍 기준 — 사용자 지시 (2026-11-15)

사용자: 톨기스와 블루프레임 **전 자세를 다시, 데스사이즈처럼 쨍하고 매끈하게**. 한 장 최대9자세, 각 장 첫 칸 공통 기본 자세 유지.

## 반드시 직접 넣을 화풍 실물

`C:/Emul/Workshop/SRW_W_HD/test_current/parts/pose_packets/unit_1/robot_set/pose_00/generated.png`

이 그림을 view_image로 보고 **매 호출의 style-only 이미지 참조**로 사용합니다. 사용자가 언급한 데스사이즈 실물입니다. 이 파일을 이번 새그림의 사용자 최종 승인으로 해석하지 않습니다.

## 그리는 방식

- 원본 SHEETS/native_sheet_4x.png는 기체 설계·실제색·포즈·위치·크기·가려짐·실루엣의 기준입니다. layout.json은 변경하지 않습니다.
- 데스사이즈처럼 안정된 매끈한 잉크 곡선, 넓고 깨끗하게 이어지는 장갑면, 간결하고 강한 빛/그림자, 쨍한 적색·황금색·청색·녹색 악센트로 새로 그립니다. 작은 금속 조각마다 번쩍이는 크롬, 과잉 패널·베벨·기계장식·모자이크·까슬한 질감을 추가하지 않습니다.
- 실제 부품의 색 구역과 색조를 보존하면서 명암을 또렷하게 합니다. 톨기스의 회녹색 은색을 흰색으로 바꾸지 않고, 블루프레임의 청색·은백색과 황적색 무장 포인트를 선명하게 합니다. 다른 기체의 팔레트 그림을 재색칠하지 않습니다.
- 얼굴은 작은 기계식 눈/바이저와 마스크·턱의 경계가 명확해야 합니다. 회녹색 덩어리로 뭉개거나 인간 코/눈/입을 그리지 않습니다. 팔·손·다리는 원본 수와 접합 그대로, 가슴 장갑을 추가 주먹으로 만들지 않습니다.
- 후속 판에는 자기 기체의 **이번 새 첫판**도 설계 참고로 함께 넣습니다. 데스사이즈 화풍 참조는 계속 유지합니다. 사용자 반려본을 스타일 기준으로 사용하지 않습니다.
- 효과·궤적은 원본 개수/길이/틈을 보존해 매끈하게 그립니다. 검정 실루엣은 빈칸으로 오해하지 않습니다.
- 실루엣 밖·부품 사이·빈칸은 알파0. 코드로 원본 알파마스크를 씌우거나 색·배경을 삭제하지 않습니다. 프레임별 정합·분할·설치는 Claude 담당입니다.

## 공통 프롬프트 핵심

Image1 is ORIGINAL GEOMETRY/COLOUR/LAYOUT authority. Image2 is the mandatory DEATHSCYTHE RENDERING STYLE reference: same illustrator, smooth confident ink curves, broad clean unbroken painted armour planes, bold clear contours, luminous saturated accents, strong simple light/shadow separation, a few confident highlight shapes. NO tiny chrome blobs, scratches, extra bevels/vents/panels/greebles, diamond facets, mosaic or rough stipple. Fresh clean2D painted-cel redraw, not pixel enlargement, blur or recolour. Preserve original source placement, compact proportions, actual colour blocks and every pose. Mechanical faces crisp and legible. True alpha0 background and gaps. At most9 poses including the common base_pose.

## 전달·검증 구분

각 sheet 폴더에 generated_sheet.png/candidate_sheet.png, 실제 사용 prompt 및 HANDOFF를 즉시 저장합니다. 이전 반려 그림은 *_style_rejected_v1.png로 보존합니다. 새 후보도 사용자 승인·Claude 검수·게임 설치 완료를 뜻하지 않습니다. 얼굴·손발·부품 접합·원본색·효과·배치/실루엣·알파 경계를 Claude가 확인할 항목으로 기록합니다.


## 11/16 최신입력방식 — 이전프롬프트참조순서대체
사용자지시로 실제4xBRZ판을주참조로사용합니다. Image1 reference_4xbrz.png(윤곽참조/reference-only), Image2 native_sheet_4x.png(형태·원본색·작은경계최종기준), Image3 위데스사이즈실물(style-only), 후속판Image4자기새첫판(design-only). 필터출력을그림후보로설치하지말고새작화합니다. 필터의작은뭉침은비필터원본으로판정합니다. 역할·자료형식·실행방법은 HANDOFF_FROM_CODEX_32.md를따릅니다. 원본팔·다리와사자발처럼실제동물형부품은그정체성을유지하며일반부츠/가짜얼굴로바꾸지않습니다.
