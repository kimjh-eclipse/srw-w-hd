# 사용자 추가 화면 제보 — 현재 처리 중

그림은 Codex, 연결·굽기·런타임·폰트·최종 재생 검증은 Claude 담당입니다. 완료된 것은 여기서 지우고 판정 근거를 현재 핸드오프에 남깁니다.

현재 총괄 핸드오프: `HANDOFF_FROM_CODEX_17.md`. 최근13건 상태는 `USER_ART_REPAIR_WORKLIST.json` 참조.

## 후보 제작 완료·연결 검증 대기

1. **타이틀 로고·지구 배경**
   - 제보: `C:/Users/OXP2/AppData/Local/Temp/codex-clipboard-914469f9-a962-40e8-9e49-a0551045ccca.png`
   - 로고: next_key_art가 ROM IMG38/PLT36/PAT39로 원본 조립 확인. `test_current/parts/title_logo_hd/`. 실제 연결 층은 별도 확인 필요. ROM PAT가 곧 런타임 OBJ라는 뜻은 아님.
   - 지구: root가 IMG11/SCR20 별·IMG12/SCR21 지구를 실제추출해두레이어새후보인계완료.960×480crop/960×1920패딩.아직게임연결검증대기. `test_current/boot_art_source/capture.state`는 부팅1800프레임의 타이틀. `source_timeline.png` 및 BG/OBJ/VRAM 원천 포함. HD QA가 아님. 기존 추출기의 target engine 의존/팔레트 범위 주의.
2. **NEW GAME / LOAD / CONTINUE 시작 메뉴**
   - 제보: `C:/Users/OXP2/AppData/Local/Temp/codex-clipboard-2b93802a-1c51-483a-9a39-60afd341c06b.png`
   - 기존 메뉴/PUSH START 후보 외에 선택판 윗변33% 과대 결함을 수정한6교체 후보 `test_current/ui/start_menu_user_repair/candidate_packet.json`을 추가했습니다. 단어·반복선은 보존. 실제 연결·선택상태 재생 검증 대기.
3. **프롤로그 우주·행성 배경**
   - 제보: `C:/Users/OXP2/AppData/Local/Temp/codex-clipboard-deb752f9-415c-4a2b-a94a-515fdc7dd8c6.png`
   - effect_palette_continue 새배경2장후보인계완료,연결검증대기. `test_current/formation/current.state` 원본과 동일, `test_current/parts/prologue_space_hd/source_capture/`에 HD-off 추출. 물리상단 BG3 행성·은하, BG0 별도한국어 본문. 글자를 새 배경에 굽지 않음.

## 기체 그림·합성 판별 필요

### 추가 기체·무장 요청

- **미히로 full 컷인 HD 누락**: 기존24924 한 장으로 해결된다는 이전 판정을 철회합니다. 별도 캐주얼복 IMG25224~25237/PLT25210~25223/MAP25238~25254의17표정군을 찾았습니다. MAP가14개가 아니라17개여서 기존 inventory 후반이 잘못 조립됐습니다. 정확 원본17개 조립·지문 대조 후 그림 제작 중. 실제 호출 장면은 미관측이며 후보 설치 전입니다.
- **미사일·흰 궤적·연기 HD 누락**: 원본은 unit172/weapon737, IMG20224/20225로 확인했습니다. whole타일재료2개+격리95343교체1개 후보 `test_current/parts/missile_trails_user_report/final_packet_index.json` 제출. 기존DB에도 빠진66타일 위치를 채움. 타일재료 adapter/기존 좋은 타일 우선순위/실제 접합·반전·팔레트 재생 확인 대기.

4. **발호크 총 주변 외곽선, 발 형태**
   - 제보: `C:/Users/OXP2/AppData/Local/Temp/codex-clipboard-7f3c64f5-ffc2-436a-b351-53dde135366a.png`
   - 현재 총4481/4482·발901/2364 수정본 설치/굽기 기록과 실제 현재그림SHA 일치. `test_current/parts/reported_valhawk_taurus_current_audit/HANDOFF.md`. 중복 제작0, 실제 게임 활성그림/캐시·재생 검증 대기.
   - 새actual 무장조각 #95312(기존 new18624_art_source)는 별도각도여서 이 자세를 해결했다고 간주하지 않음.
5. **어두운 기체 머리·어깨 수평 절단선**
   - 제보: `C:/Users/OXP2/AppData/Local/Temp/codex-clipboard-69c03bb0-9bfc-435c-aa74-66721e18b681.png`
   - 검정·회색 기체의 뾰족한 머리/어깨 중간에 일직선 절단/이음매. 원천으로unit8 토라스/IMG1219/PLT1220확정.부품4985/4988/4996/4997의 수정본이 이미 설치/굽기 기록 및 현재그림SHA와 일치합니다. 실제 재생 검증 대기, 중복 제작하지 않음.
   - atlas절단면에 새 외곽선이 들어갔는지, 파츠끼리 source/atlas좌표가 어긋났는지 Claude 실제 재생/원본대조 요청. Codex는 원천이 식별되면 같은자세 master 그림을 교정.

## Claude 폰트·런타임 담당 요청

6. **전투 전 상단 `攻·防·反` 한자 상태 표시만 도트 글자**
   - 제보: `C:/Users/OXP2/AppData/Local/Temp/codex-clipboard-9f470763-ba97-4ff5-a55e-6d4fcd22006d.png`
   - HP·EN 사이 중앙 패널. 현재 한국어/숫자는 HD인데 공격·방어·반격 한자 표시가 native로 남음. 기존 같은 UI폰트/두께/외곽선을 쓰고 상태전환 전부 포함해 주세요.
   - Codex가 폰트 코드를 수정하지 않습니다. 런타임/폰트 연결은 Claude 담당이며 그림 작업과 병행할 수 있습니다.

7. **전투 결과창 초록색 이름·경험치·레벨의 HD 글자/숫자 누락**
   - 제보: `C:/Users/OXP2/AppData/Local/Temp/codex-clipboard-84a07717-63be-46ca-8e2e-f4fc131f69eb.png`
   - 카즈마/미히로, +217, 5→6 등이 밝은초록색native로 남음. 위쪽 흰색제목·숫자는HD이므로 색상변형의인식/스타일연결누락 가능성. 글자·숫자·기호·변환화살표를 구분해 확인하고 원래초록색을유지해같은UI폰트로처리해 주세요.
   - 한자누락과같이공통폰트입력/팔레트조건을확인할 항목. Codex는공유폰트코드를수정하지않습니다.

8. **정신 커맨드 청록색 `신뢰` 글자 HD 누락**
   - 제보: `C:/Users/OXP2/AppData/Local/Temp/codex-clipboard-a8f8f1cf-9b38-4eba-a039-808d89c53cba.png`
   - 미히로 정신메뉴, 오른쪽지원열의청록색신뢰만도트로남음. 다른흰색/회색/물음표는HD.7번초록과같이유색폰트공통경로확인요청. 원래색을보존하고선택/비선택둘다처리해 주세요.

9. **전투 보조 화면 HP 라벨·게이지의 HD 누락**
   - 제보: `C:/Users/OXP2/AppData/Local/Temp/codex-clipboard-620696ae-cdd2-4d3e-bc2b-a6b7dce9528e.png`
   - 오른쪽 보조 화면의 노란HP라벨, 초록/빨강채움, 테두리가 도트. 현재 체력숫자는HD로보임. 숫자폰트와분리해HUD라벨/게이지트랙·채움경계·동적감소를공통으로처리해 주세요. HP값이나비율을새정적그림에굽지않음.
   - Codex가필요한게이지원천/후보그림을준비하되 runtime 연결/동적비율유지/최종재생은Claude담당.


### HP 라벨·게이지 소스 확인 업데이트
IMG4651/PLT4650, 아래 화면 engine1 BG0로 확인했습니다. 원본 라벨14×6, 게이지70×5이며 수치·잔량은 동적입니다. HD 적용은 아직 미해결입니다. 자세한 수정 후보와 검증 항목은 HANDOFF_FROM_CODEX_15.md 최우선 항목을 확인해 주세요.


### 타이틀 로고·오른쪽 메뉴 재제보
첨부 codex-clipboard-c4be520b-ce9c-4136-b656-3498b648fb80.png. 로고 원본 잔존과 오른쪽 메뉴 이상. 실제 화면 검증 대기. 메뉴6패널 그림수정은17번에 기록했고 로고는 기존후보 연결을 요청했습니다.


### 샌드록 전면/공격/후면 손상
사용자3사진776318dc/2bdd4997/51c152aa. 얼굴·양쇼텔·가슴·다리·후면 색/파츠 경계 이상. 실제게임검증 대기. 머리1+연결편6+실드2+공격/후면54종, 총63종 그림 후보 제출. `sandrock_user_report/agent_repair/delivery_index.json` 및 핸드오프17 참조.
