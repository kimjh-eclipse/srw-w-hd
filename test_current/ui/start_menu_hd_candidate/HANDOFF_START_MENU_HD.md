# 시작 메뉴 HD 그림·원본 연결 인계

## 현재 상태
NEW GAME / LOAD / CONTINUE의 선택·비선택 UI 새 그림 후보입니다. 기본 imagegen으로 프레임 3소재와 문자 6상태를 새로 그렸습니다. 원본 IMG 23의 공유 좌표로 조립한 1024×256 RGBA(원본256×64의 4배)입니다. 실제 고유 원본 키는 24개이며 모두 실제 표시가 관측됐습니다. 연결·굽기·공식 QA·HD 실재생은 하지 않았습니다.

## 원본 확정
- 원본 시트 IMG23, 팔레트 PLT22 뱅크0/1. 24개 cached OBJ의 인덱스 전체와 ROM 사각형이 바이트 단위로 일치합니다. 실제 전체16색도 PLT22 해당뱅크와 전부 같습니다.
- 선택0/1/2 상태: ../start_menu_source/selected_0..2/native_source.state. 상태를 읽고 한 프레임 실행한 cached OBJ를 source_contract에 보존했습니다. 실제 화면은 같은 폴더 native_screen.png입니다.
- 이 타이틀 장면은 상하 표시가 바뀌어 core target engine=1입니다. 메뉴는 물리 engine0/하단 화면이며 core.sub_parts/sub_oam/sub_palettes 쪽입니다. 반대로 core.parts/obj는 상단 로고 조각입니다. 이 둘을 혼동하면 메뉴가 안 바뀝니다.
- 메뉴는 BG가 아니라 OBJ입니다. 배경의 지구는 별도 담당이며 새로 그리지 않았습니다.

## 그림과 공유
- 후보 candidate_atlas.png, 원천 generated_raw.png, 대조 native_atlas.png, 정확한 raw/full16/원래 OAM 좌표는 contract.json입니다.
- 동일 원본 프레임의 포함/부분교차는 모두 한 master의 같은 좌표를 읽습니다. 반복되는 선은 새 그림의 평평한 자체 단면을 가로로 공유해 반복 경계에 단차가 생기지 않게 했습니다. 원본 RGB/알파 전사나 원본 마스크로 자른 작업은 없습니다.
- 원래 세 단어를 그대로 유지했습니다. 새 문자도 같은 뜻/철자이며 선택은 밝은 흰색, 비선택은 청록 발광입니다.
- producer_menu_assembly_selected0..2는 원래 OAM 좌표로 후보만 조립한 제작 미리보기입니다. 실제 게임 재생 결과가 아닙니다. 지구 BG와 하드웨어 블렌드도 넣지 않았습니다.

## Claude 연결·검토 주의
- 기존 parts 라이브러리 신규키 연결로 들어갈 수 있지만 반드시 하단 sub_parts 경로에서 실제 표시되는지 봐 주세요. 기존 렌더러의 render_bottom은 parts_renderer.compose를 호출합니다.
- 원본 BLDCNT=0x3f50, BLDALPHA=0x0f0f입니다. OBJ가 1차 혼합 대상이고 두 계수는 15/15입니다. sprite obj_mode 자체는0/우선순위0입니다. 이 메뉴는 단순 alpha=0.5 방식과 다릅니다. hardware_menu_layout.json에 전체 원래 값을 기록했습니다.
- 현재 render_bottom의 compose 호출에는 effect_foreground 인수가 없어 원래 하드웨어 가산 혼합 표현이 자동 재현되는지는 미확인입니다. 후보를 불투명 프레임으로만 덧그리면 지구가 원래보다 어둡게 가려질 수 있습니다. 이 문제는 공유 코드 담당인 Claude가 판정해야 합니다.
- 글자의 원래 어두운 광택/밝은 가장자리 지지와 새 안티앨리어싱 지지는 다릅니다. 선택/비선택 밝기, 잘림, 반복 선 접합, 프레임 각도는 실제 화면에서 검토해야 합니다.
- 원본 시트에 PUSH START도 있으나 이번 메뉴 24개 actual 계약에는 포함되지 않습니다. 이를 이미 HD로 처리했다고 세면 안 됩니다.

## 인수 파일
queue_entry.json에 source/contract/drawing/native/generated, 24개의 new_source_keys, 네 파일 SHA256이 있습니다. 새 그림은 9소재이며 24원본 조회키를 지원합니다. 상태 파일과 배터리 세이브는 진단용이며 공개 저장소에 올리지 마세요.
