# Codex → Claude 핸드오프 7

현재 교환 파일입니다. 정확한 바인딩·그림 SHA·관측 대상은 PRODUCTION_ART_BATCH_CURRENT.json, 이전 검증 항목은 CLAUDE_VERIFICATION_QUEUE.md 및 CLAUDE_VERIFICATION_QUEUE_1.md, 각 그림 폴더의 계약과 HANDOFF를 읽으세요. 20KB 또는 300행에 도달하면 8번 파일로 옮기고 안내합니다. 오래된 현재 상태·대기 목록은 이 문서에서 제거했습니다.

## 현재 상태 — 2026-11-14

- **2,943개 고유 작업 대상 연결·대상 굽기 완료**. 기존 그림 교체와 실제 팔레트 변형 포함. 기체 수·ROM 누락 감소량·독립 QA 완료 수가 아닙니다.
- 마지막 공개 푸시는 main **d46d1a2e**, 당시 2,870개까지였습니다. 이후 작업은 커밋 준비 중이며 캐시를 다시 만들고 SHA를 확인한 뒤 푸시합니다.
- 전체 ROM 누락은 독립 감사 11,358종 이후 재집계하지 않았습니다. 다중 IMG 21% 미판정·BG는 그 감사 밖입니다. 작업 수를 빼서 잔여를 계산하지 마세요.
- Codex 담당: 새 그림·원본 계약·연결·굽기·커밋. Claude 담당: 독립 색상·형상·접합·레이어·실제 HD 재생 검증. 오류 0과 CRC/nonempty 통과는 시각 품질 판정이 아닙니다.
- **코어 소스 해제**. 이번 작업에서 공유 런타임을 수정하지 않았습니다. 최신 EXE·배포 팩은 미갱신, 열린 사용자 게임 창은 유지했습니다.
- ROM·세이브·settings·log·credentials·sqlite는 공개 Git 제외. 원본 5,263개 바인딩 불변.
- 사용자 지시대로 모니터만 끄고 진행합니다. keep_system_awake.flag를 읽는 숨김 작업이 시스템 절전을 방지하며, keep_monitor_off.ps1 숨김 작업은 keep_monitor_off.flag가 존재하면 15초마다 화면 전원 끄기 메시지만 보냅니다(PID는 keep_monitor_off.pid). 물리 입력·게임 창 조작은 하지 않습니다. **컴퓨터는 종료하지 않습니다.** 사용자가 화면을 켜라고 하면 keep_monitor_off.flag를 제거하고, 모든 작업 종료 때 두 flag를 제거해 반복 끄기·절전 방지를 해제해야 합니다.

## 현재 병렬 제작

- next_key_art: EI-01 4개/EI-13 27개 인계 후 fixture342/346/357 실제 기계 원본 채집·새 그림 제작. fixture346의 카탈로그와 실제 포르네우스 MAP무기 화자가 불일치해 이름 소유를 단정하지 않습니다.
- next_shape_art: unit110 6개와 unit123 5개 인계 후 다음 실제 미연결·공유 경계 제작. unit123의 단색처럼 보이던 패치는 검산에서 3색으로 밝혀져 검정1/회보라3/짙은회색4 비율의 불투명 평면 재료를 코드로 별도 작성했습니다. 원본 pixels/alpha를 복사한 그림이 아니며 장식 없는 평면 재료임을 출처에 명시했습니다.
- effect_live_palette: 393/w1559 실제 관측 효과 raw37종(전격24/흰베기2/노랑원형7/붉은충격4)을 제작 중입니다. 금속처럼 나온 첫 전격/고리는 거절하고 재제작합니다. 3개 팔레트 변형은 별도 미완료 큐입니다.

## 최신 묶음의 검증 요청

- 각 새 graphics/rework_* 폴더에 installation_report.json, 실제 팔레트·cached raw 계약, 생성 출처 및 batch_bake_report.json을 보존했습니다. 신규 대상과 기존 바인딩 교체를 혼동하지 마세요.
- Big Volfogg 연속 6개는 **54395/54399도 같은 새 master로 교체**했습니다. 새 조각만 붙여 옛 조각과 혼합하지 않았습니다. 원본/생성 겹침 13건은 굽기 전 일치이며 실제 접합 판정은 아닙니다.
- 카라미티 Todes의 raw 인접 조각은 화면 y가 16px 어긋납니다. 실제 64×48 계단 문맥으로 다시 그려 분할했습니다. 후속 Schlag는 실제 수평 64×32 문맥입니다. 두 경우를 같은 접합으로 취급하지 마세요. tiny hash365017408은 보류했습니다.
- 프라누스 첫 후보의 원본 없는 초록 센서는 교정됐고, 피바타 첫 도트 확대 후보는 배제됐습니다. 작은 조각 가시 면적 한계와 팔·장갑 접합을 각 HANDOFF에서 확인해 주세요.
- 새 registered_attack_bank 그림은 register_part 탐색을 건너뛰지만 remove_unattached_paint·repair_crop_ink·8→4배 축소는 남습니다. 생성 master RGBA 일치는 **굽기 후 이음매 정상 증거가 아닙니다**. 얇은 선/입자/경계 소실을 조립된 실제 HD로 확인해 주세요.
- 작은 효과의 자체 생성 성분 배치와 단색면 alpha, 22472 고리의 원래 구멍, 기체 앞 빔/기체 뒤 컷인/대사창 앞뒤·플래시·페이드는 독립 확인 대기입니다.
- EI-01 4개·EI-13 27개(큰25+최대가시12px/1px의 작은 경계2), 미겔 진1, unit86/93/102/117/118/111 관측 기계24, unit110 6개, unit123 5개를 추가 연결·굽기했습니다. 보이는 큰 조각만으로 자세 전체/무장 전체 완료를 주장하지 않습니다. 각 접합/가림·실제 색/투시·가시범위는 Claude 판정 대기입니다.
- Codex 직접 제작: unit100/w420 IMG9505 내부 암부1(네 원본색의 단순 가림 구조, 완성 기체 그림 아님), unit94/w389 실제 palette4 캡슐/발사체1(IMG 소유 미확정). 후자는 블록 같은 첫 출력은 거절하고 매끈한 곡선 후보를 자체 RGBA 지원 사각으로 등록했습니다. 중앙 하이라이트·캡 곡률/두께·실제 이동 방향을 확인해 주세요. source mask/RGB 스탬프는 쓰지 않았습니다.

## 소유·이름 매핑 불확실성

- valarm_observed_mechanical_eleven은 fixture420/w1640 관측 파츠일 뿐 소유 기체를 확정하지 않았습니다(source_owner_confirmed=false).
- 카탈로그 요청은 F호크 스트라이크였으나 실제 +430 대사는 아플리칸트의 플라즈마 노바 드라이버 풀 차지입니다. 메뉴 선택1640과 내부 애니메이션 ID/기술 이름 대응은 독립 확인 전입니다. 해당 graphics/HANDOFF_PRODUCTION.md의 카탈로그와 실제 장면 불일치 근거를 읽고 테스트 하네스/이름 표를 확인해 주세요.
- 원본 raw·실제 팔레트 계약으로 붙였다는 사실과 요청한 기체/기술을 검사했다는 주장은 별개입니다. 다른 fixture 이름도 이것만으로 전수 완료 판정하지 마세요.

## 팔레트 단계 — 미완료로 유지

- 신규 indexed_safe=false 그림이므로 같은 index/raw인 어두움·섬광 변형에 자동 적용됐다고 보장하지 않습니다.
- 각 palette_phase_aliases_pending.json에 실제 hash/index hash/16색/상태·프레임/기본 계약을 남겼습니다. Golion 어두움2, Big Volfogg 노랑4, Gimlet 어두움77, Polton 어두움9 등이 있습니다. 기본 그림 제작과 단순 fade 런타임 재사용을 구분해 주세요.
- 21855 특수 초록 팔레트1은 실제 녹색이며 여러 번호가640으로 모이는 원본입니다. 키 색이라고 삭제하거나 기본색으로 바꾸지 않았습니다. HANDOFF_PALETTE_HOLD.md 검토 대기입니다.
- 22378 late65 및 20966/19887 변형50 등 기존 런타임 큐는 CLAUDE_VERIFICATION_QUEUE.md에 유지합니다.
- fixture400/w1577의 기본14개는 별도 새 그림입니다. 추가28개 fade 계약은 graphics/source_contract_extensions/unit400_1577/fade28_source_base_pairs.json과 HANDOFF_FADE_VARIANTS.md에 보존했습니다. IMG 소유는 미확정이며 source_x/y는 가상 셀 좌표입니다. mint/gray 단색면은 자체 새 생성 재료의 균일 내부를 썼고 준비 후 전면 alpha255입니다. 얇은 효과의 실루엣 변화·회색 rim은 Claude 독립 검증 대기입니다.

## 보류 그림 — 연결/완료 수 제외

- graphics/review_pending/wufei_eye_animation: 6개. 기존 fullcutin17 눈자리·피부 경계 정합 미해결.
- graphics/review_pending/sandrock_heated270: 6개. 좁은 연결편을 큰 장갑/손으로 부풀린 형상 미해결. root_retry v4의 넓은 회색 후광은 실제 alpha0의 숨은 RGB였으나 형상 문제 때문에 여전히 보류입니다.
- graphics/review_pending/effect21934_white_core: 7개. 자체 생성 불투명 RGB의 채운 흰 중심은 있으나 imagegen 투명화가 중심을 지웁니다. HANDOFF_TECHNICAL_MATTING.md 검토 요청. 원본 mask/RGB 스탬프나 다른 팔레트 alpha를 빌려 통과시키지 않았습니다.
- 옛 graphics/review_pending/ginn_bazooka_dark_four는 거절 초안 증거로만 보존합니다. 새 기본색 암부4개는 graphics/rework_ginn_bazooka_dark_four_corrected에 연결·굽기를 마쳐 제작 보류 목록에서 해제했습니다. PLT1414 bank0 전체16색 일치로 fade가 아닌 실제 그림자/뒷면입니다. 색·절단면/곡선·가림은 Claude 실제QA 대기입니다.
- 22472 고리3은 위 보류 목록에서 제외됐습니다. 같은 ID94352/94354/94356에 새 sparse ring을 붙이고 전체16개를 재굽기했습니다. 다른13개 RGBA 불변. 최종 SHA81acfb205d38110338b84e4d6ef72ee5c68bae2d571c81476765bd8cce548e59. 여전히 독립 시각 검증 대기입니다.

## 미해결 공통 사항

- 모든 기체·무장·컷인·효과 완료를 주장하지 않습니다. 관측 안 된 IWSP/라이트닝·역할 미확정 tiny·제작 보류·palette phase는 남아 있습니다.
- 전체 효과 순서, 컷인 페이드, 전체화면 플래시, 단색 연출 조각, sub 화면 기체, 메뉴 글자 배경·HP/EN/피해 숫자 등 이전 재현 문제는 Claude가 최신 런타임으로 별도 판정해야 합니다.
- parts_baked.sqlite의 옛 compact 후보는 최신 그림을 포함하지 않아 교체하지 않았습니다. 이번 굽기 저장소·캐시가 배포 EXE에 반영됐다고 주장하지 않습니다.
