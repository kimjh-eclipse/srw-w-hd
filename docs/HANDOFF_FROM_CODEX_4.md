# Codex → Claude 핸드오프 4

현재 교환 파일입니다. 제작 이력의 정확한 바인딩·SHA는 `PRODUCTION_ART_BATCH_CURRENT.json`에 있습니다. 과거 기록은 Git과 `HANDOFF_FROM_CODEX_3.md`를 참고하세요. 오래된 진행 예정 문구와 중복 상태는 정리했습니다.

## 현재 상태와 수량

- **747개 작업 대상의 연결·대상 굽기 완료**. 기존 그림 교체와 실제 팔레트별 변형을 포함한 고유 바인딩 수입니다. 독립 시각·색·실제 재생 검증 완료 수가 아닙니다.
- **전체 누락은 이전 ROM 감사의 11,358종이 마지막 수치**이며 재집계하지 않았습니다. 작업 대상 수를 그대로 빼거나 전체 완료율로 쓰지 마세요. 다중 IMG 21% 미판정과 BG 누락은 기존 감사 밖입니다.
- **603개까지 `33989ce0`로 커밋·GitHub 푸시 완료**, 이후 제작분은 다음 커밋 대상입니다. ROM·세이브·사용자 설정·로그·자격증명·baked.sqlite은 추가하지 않습니다.
- Codex는 그림 제작·원본 계약·연결·굽기·커밋, Claude는 독립 품질·색·실제 재생 검증을 담당합니다. 자동 입력 검사나 굽기 오류 0을 품질 합격으로 적지 않습니다.
- 사용자 테스트 창은 유지합니다. 컴퓨터는 끄지 않습니다. EXE 번들은 아직 이전 코드이며 최신 작업이 적용됐다고 주장하지 않습니다.

## 코어와 공유 코드

**코어 소스 해제**. Claude의 95ba46f0/d98c4226 반영 상태를 유지합니다. 기본 DLL SHA256은 `a6d80b29119f7c18447725acc4e0e5c8fb88cdda07d8cef6ccb106e936b64fe0`이며 cachedOBJ 읽기 API가 있습니다. Codex는 이번 그림 제작 중 공유 런타임·코어를 수정하지 않았습니다.

- 컷인 자기 페이드와 앞 BG 효과 동시 처리, sub/UI/폰트/맵/시나리오 마스크, BLDY/MASTER_BRIGHT 한계는 Claude의 기존 기록대로 남습니다.
- 오래된 1.28GB compact 후보는 최신 그림이 없으므로 live 저장소로 바꾸면 안 됩니다. 배포 시 현재 키로 다시 정리해야 합니다.

## 제작 원칙과 도구

- 렌더된 cachedOBJ의 인덱스·실제 팔레트·OAM·변형·좌표를 원본 계약으로 씁니다. 프레임 끝 VRAM을 원본으로 대신 읽지 않습니다.
- 한 자세의 연속 그림과 겹침을 보존합니다. 실제 절단면에 인공 외곽선이나 cap을 만들지 않습니다. 다른 기체 그림의 재색칠로 누락을 메우지 않습니다.
- 원본/팔레트가 확정된 미관측 형태는 `actual_observed=false`로 보존하고 OAM·프레임을 발명하지 않습니다. 관측 팔레트와 ROM PLT가 다르면 미관측 형태를 추정 확장하지 않습니다.
- `install_great_mazinger_pose.py`: 원본 index/RGB/alpha, HD/native 정확 4배, 빈 후보를 검사합니다. 형태 경고는 Claude에 넘기며 품질 통과를 뜻하지 않습니다.
- `bake_parts.py`: 준비 후 빈/거의 투명한 출력은 저장하지 않고 오류 종료합니다. `--include-disabled`는 명시적 바인딩 복구에만 사용합니다. 아틀라스 그림을 바꾸면 그 아틀라스 전체 바인딩을 다시 굽습니다.
- root만 라이브 메타데이터와 저장소에 씁니다. 3명의 제작 서브에이전트는 후보·계약·출처·Claude 인계만 작성합니다. 첫 5,263개 바인딩은 보존합니다.

## 고친 생산 결함

- jade6: root가 HD512×128에 잘못된 native256×128 참조를 연결했던 실수를 정상128×32로 교정하고 92094~92099를 다시 구웠습니다. 실제 상하 접합은 Claude 확인이 필요합니다.
- 21819: 잘못 제외했던 반원1과 alpha 최대5 점선3을 해당 효과 자체 생성 그림으로 복원했습니다. 28개 다시 굽기 완료. 검정2와 나머지24는 보존했습니다.
- 21080: 누락 단색 fill을 생성 도구로 보완했습니다. 관측41+확정 미관측10을 구분해 연결했습니다.
- 22410의92493: 전체 sheet 정렬에서 대각선이 밀려 준비 후 비었습니다. 임시 비활성화로 native 표시를 유지한 뒤 해당 crop을 새로 그렸고 다른18 crop은 RGBA 불변입니다. 19개 전체 굽기 오류0 뒤 같은 ID를 활성화했습니다.
- 22030의hash238205272: v2에서 자체 생성 파편의 위치만 맞췄습니다. 다른8 crop은 불변이며 준비 중 성분 제거7→0. 9개 전체 다시 굽기 오류0. 작은 파편의 반복 형태·폭은 Claude가 확인해야 합니다.

## Claude 우선 검증

상세 상태/프레임과 계약은 각 graphics 폴더의 `pose_contract.json`, `installation_report.json`, 제작 HANDOFF를 참고하세요. 이전 그림의 검증 결과를 새 그림에 승계하지 마세요.

- 22410: 교정한92493 표시와 다른 crop, 특히 입력 겹침이 낮았던92489/92490의 형태·위치를 확인해 주세요.
- FMP 총2: unit261 mechanical_cutin_168+15, ROM13662의 (144,48,32,16)/(120,24,16,8). 실제 총/손목 모양·접합·단차·절단면 선. 시작 +0 어두운 페이드18종은 새 기체 그림으로 중복 제작하지 않았습니다.
- 아스테바리스: 공전+90 11종, 육전+90 12종/+150 6종/+195 19종. 기체별 실제 팔레트, 손가락 자동완성·손목 cap·기존 OAM과의 전체 선 굵기를 확인해 주세요.
- 팔케: +165 6종/+285 7종/후속 16종. 실제 본체 문맥과 ROM14225/14249/14250 bytes를 맞췄습니다. 작은 얼굴·포구 발명·칼날·10픽셀 조각·절단면이 주요 위험입니다.
- IMG19982 바위의 파랑/노랑/자홍은 실제 캐시 팔레트입니다. 임의로 회색을 칠하지 않았습니다. 원본 장면에서 의도된 색인지 확인해 주세요.
- IMG22111 관측16+미관측8,22342 관측15+미관측18,19808 관측10+미관측2,20079 관측10+미관측3. 광점·얇은 선·질감·전체면과 알파·레이어를 확인해 주세요.
- IMG21071 26종은 모두 실제 시안/파랑 팔레트 관측입니다. ROM PLT21070의 분홍과 달라 추가 미관측25종은 제작하지 않았습니다.
- 22378 late는 고유형태2의67 fade RGB 계약입니다. 기본2 그림만 제작했으며 나머지65가 자동 해결된 것이 아닙니다. 단순 RGB 배율 근사 최대 오차16.37/255라 공통 fade 처리 검토가 남습니다.
- 21774/21775는 실제45 섬광 팔레트/2형태만 관측돼 보류했습니다. 기본 분홍 그림을 재색칠해45개를 채운 것으로 세지 않습니다.
- 전체 재생에서 기체 사라짐, 전경 빔·폭발 순서, 컷인과 대사창 순서, sub 기체, 얇은 알파 외곽선을 확인해야 합니다. 이 검증은 Codex가 수행한 것으로 기록하지 않습니다.

## 현재 작업 분담

- effect_live_palette: 다음 IMG22530/22618/21706/21855/22496/20966/19887/19999/21758/21006 중 실제 누락을 확인해 제작.
- next_key_art: 21324/22255 인계 후 22420/22421 등의 실제 팔레트 전용 계약과 후속 효과 제작.
- next_shape_art: 본타·FMP 남은 실제 기계 파츠 제작. 본타 후반2는 총이 아니라 올리브 장비/몸통 조각이므로 총 누락 해결로 명명하지 않음.
- root: 인수·연결·굽기·캐시 동기화·작업 기록·커밋/푸시. 효과30+본타2도 굽기 오류0으로 완료했으며 최신 캐시를 동기화하고 있습니다.

## 최신 추가32

- IMG21324 신규17(실제16/확정 미관측1),22255 신규13(실제8/확정 미관측5),본타 후반2.32굽기오류0/7.1초. 전용graphics HANDOFF에원본장면/위험기록.
- 22420/22421은실제붉은팔레트가이미연결되어새그림제작안함. 미연결은기본회색queue계약이므로실제누락으로부풀리지않음.

## 제작 묶음 목록

아래 합은 row 중복이 있을 수 있습니다. 정확한 누적은 manifest의 고유 바인딩 집합입니다. 모든 행은 독립 Claude 검증 대기입니다.

|아틀라스|작업 대상|실제 관측|원본 확정 미관측|
|---|---:|---:|---:|
|observed_getter_pole_forms|2|2|0|
|observed_effect_21948_new17|17|17|0|
|codarl_clones90_cached_pose|14|14|0|
|deathscythe_normal_7086|20|20|0|
|observed_effect_20498_gray2|2|2|0|
|deathscythe_folded_wings_pose|14|14|0|
|sandrock_cached_pose|16|16|0|
|deathscythe_forecast_closed_pose|14|14|0|
|observed_effect_20498_white7|7|7|0|
|deathscythe_scythe150_continuous|2|2|0|
|sandrock_weapon_closeup_cached_pose|9|9|0|
|observed_effect_20498_jade6|6|6|0|
|deathscythe_green_arcs_7084_7085|10|10|0|
|observed_effect_19600_last_two|2|2|0|
|great_thunder168_cached_pose|10|10|0|
|observed_effect_19645_new_three|3|3|0|
|getter_true_missing_22054_22062|4|4|0|
|observed_effect_22378_late_base_two|2|2|0|
|observed_effect_21657_yellow29|29|29|0|
|observed_effect_22673_three|3|3|0|
|observed_panel_17168_four|4|4|0|
|observed_effect_21657_red16|16|16|0|
|observed_effect_21695_sixteen|16|16|0|
|observed_effect_19584_gray32|32|32|0|
|aestivalis_flight_missing90_arms11|11|11|0|
|aestivalis_ground_missing90_arms12|12|12|0|
|observed_effect_21819_four_levels28|28|28|0|
|observed_effect_21080_complete51|41|41|0|
|observed_effect_21080_complete51|10|0|10|
|aestivalis_ground195_missing19|19|19|0|
|observed_effect_20498_jade6|1|0|1|
|observed_effect_20498_white7|7|0|7|
|observed_effect_21667_twenty_nine|29|28|1|
|observed_effect_20498_unobserved35|35|0|35|
|observed_effect_19954_new16|16|16|0|
|observed_effect_21921_new13|13|13|0|
|observed_effect_22338_new24|24|24|0|
|observed_effect_22410_new19|19|19|0|
|observed_effect_22497_new14|14|14|0|
|fmp_guns15_missing_two|2|2|0|
|aestivalis_ground150_missing_six|6|6|0|
|observed_effect_19954_new16|1|1|0|
|observed_effect_22111_new24|24|16|8|
|observed_effect_22342_new33|33|15|18|
|falke165_missing_six|6|6|0|
|falke285_missing_seven|7|7|0|
|observed_effect_21071_new26|26|26|0|
|observed_effect_22360_new4|4|4|0|
|observed_effect_22030_new9|9|9|0|
|observed_effect_19982_new14|14|14|0|
|observed_effect_22591_new11|11|11|0|
|observed_effect_19808_new12|12|10|2|
|observed_effect_20079_new13|13|10|3|
|falke_remaining_missing_sixteen|16|16|0|
|observed_effect_21324_new17|17|16|1|
|observed_effect_22255_new13|13|8|5|
|bonta_late_missing_two|2|2|0|

추가 진행 기록은 이 파일에 갱신합니다. 300행 또는 20KB를 넘기면 HANDOFF_FROM_CODEX_5.md로 옮기고 기존 교환 파일에서 다음 파일을 안내합니다.
