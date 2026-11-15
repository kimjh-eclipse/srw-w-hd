# 시작 메뉴 제보: 그림 수정과 로고 연결 판정

## 실제 그림 결함과 수정

- 제보 screenshot c4be520b-ce9c-4136-b656-3498b648fb80의 선택 LOAD판은 기존 HD후보와 같은 형태입니다. 원본selected_1 화면/OAM원본과 비교하니 선택 패널의 옆면이 지나치게 서 있었고 윗변이 넓었습니다.
- IMG23 원본 선택패널64×32의 맨윗줄 지원범위는[14,50](폭36)인데 기존후보는[8,56](폭48):윗변33%과대입니다. 새vector후보는[13,51](폭38,안티앨리어싱경계1픽셀포함)이며 원래 약45도 옆면을 복원했습니다. alphaIoU0.8964→0.9667입니다.
- 비선택회색판의 윗변/각도도 원래 설계 꼭짓점으로 복원했습니다. alphaIoU0.9466→0.9623입니다. 단순 polygon/gradient UI라 코드-native vector로 제작했고 panel_geometry.svg에 설계꼭짓점을 보존했습니다. imagegen 그림에 원본알파를 덮어 합격시킨 것이 아닙니다.
- LOAD글자가 크게 느껴지는 원인이 글자 지원크기 오류라는 근거는 없습니다. 선택 LOAD의 흰색본문bbox는 원본과 기존HD 모두[8,2,57,14], NEW GAME은[4,2,93,14], CONTINUE는[5,2,92,14]로 정확히 같습니다. label_size_proof.json 참조. 이미 좋은 기존 단어그림과 반복선을 그대로 유지했습니다.
- 원래 OAM좌표/선택상태/전체판크기는 보존했습니다. producer_selected0..2는 같은 원래 OAM으로 조립한 제작미리보기이며 실제 재생이 아닙니다. BLDCNT/하단OBJ혼합·폰트·HP·런타임 코드는 변경하지 않았습니다.

## 제출 후보

- candidate_packet.json: 교체6바인딩[95316,95317,95318,95323,95325,95326]. contract/drawing/native/generated 4역할SHA와 live prior_binding_spec_sha256 맵을 기록했습니다.
- candidate_atlas.png: 기존 생성메뉴에서 두 패널 부모영역만 새vector로 교체했습니다. 18개 나머지조회키의 그림은 bitwise변화없음. 공유/포함되는6조각은 모두 같은 새wholeatlas 좌표를 읽습니다.
- generated_master.png는 기존좋은자체생성그림+새vector패널의 최종완성wholemaster이며 candidate와 픽셀이 같습니다. drawing_provenance.json에 기존생성원천SHA·수정native부모영역·vector설계점을 기록했습니다. 새패널2 / 새문자0 / 새로고0.
- source_contract_proof.json: IMG23 정확 인덱스·full16 CRC hash/index_hash 일치, 6개 live사전SHA재확인, 겹치는 부모영역의 새RGBA동일성 검증. 원본RGBA/alpha스탬프·임계값cleanup없음.
- menu_native_existing_repaired.png는 원본/기존후보/수정후보3단 비교입니다. native/source·reported 화면축소본과 vector_geometry_check.json도 동봉했습니다.

## 로고: 새로 그리지 않음

- 기존 test_current/parts/title_logo_hd/candidate_logo.png가 이미 있으며4역할SHA가 여전히 유효합니다. SHA a5cebbc3cea56d5529402b6656a3c88c935181c2aad58a5a199994c8b4c8a81e.
- 원본 IMG38 / PLT36 / PAT39 pose0(248×104), 기존후보992×416. 금색 일본어 두줄 제목, 검정/은색두께, 남색→파랑큰W, 파랑외곽림을 유지합니다. 시각적으로 스ーパーロボット大戦W 제목에 명백한 단어 누락/대체는 보이지 않았습니다. 다만 획단위정밀일치/게임합성합격을 보증하지 않습니다.
- 제보 화면 로고는 도트원본으로 보입니다. 제한된 화면맞춤 비교도 원본이 기존HD후보보다 훨씬 가깝습니다(최대채널오차평균22.42 vs64.28). 스크린샷크기/위치오차가 있으므로 바이트일치 증명으로 보지 않습니다.
- 현재검사한 renderer/cutin/background등록에서 candidate_logo/title_logo 경로 참조를 찾지 못했습니다. 기존packet도 title_logo_whole_master/automatic_parts_install_supported=false로 별도연결대기입니다. 정상기존그림을 중복생성하기보다 Claude가 원래 layer/팔레트/스크롤과 해당master를 연결해 실제검사할 단계입니다.
- title_logo_inspection.json / title_logo_screen_comparison.json에 이 판정과 한계를 기록했습니다. 기존로고패킷·그림·공유문서·중앙파일·설치목록은 변경하지 않았습니다.

중앙 실행/라이브러리/DB/큐/manifest/공유 인계는 무수정입니다. 실제연결·굽기·아래화면블렌드·제목일본어획·재생QA는 Claude 담당입니다.
