# PUSH START 문자 HD 후보

새 그림은 PUSH START 한 단어 master 1장/실제 원본 조회키 4개입니다. 철자와 한 칸 공백을 유지했습니다. 원본은 start_menu_source/start180.state +0/15/30/60/90의 실제 cached engine0 하단 OBJ0~3입니다. IMG23의 원본사각·인덱스 전체와 actual 전체16색 PLT22 bank1을 대조해 일치 확인했습니다.

선과 프레임 4고유키는 시작 메뉴 후보와 raw/full16이 완전히 같아 재제작·중복연결하지 않습니다. existing_menu_frame_dependencies.json에 같은 메뉴 candidate master의 의존 좌표와 실제 계약이 있습니다. 이 4개는 메뉴24에 이미 포함됩니다.

source 시트 마지막 글자 조각만 다음행에 있지만 실제 화면 x64/96/128/160,y88에 수평연속입니다. 새128×16 master를 그 좌표로 나눠 글자 사이 절단선이 생기지 않게 했습니다. 원본 글자색 위치는 위치·배율 측정에만 썼고 원본 RGB/알파 전사·마스크찍기·색변환은 하지 않았습니다.

producer_push_start_menu_frame은 실제 원래 OAM에 후보만 조립한 제작 참고이며 게임 재생이 아닙니다. 지구/타이틀로고·하드웨어15/15 혼합은 포함하지 않았습니다. 메뉴 인계에 기록한 engine0/sub_parts 표시 및 blend 계수 위험을 그대로 검토해야 합니다. 중앙 연결·굽기·공식 QA는 Claude 담당입니다.
