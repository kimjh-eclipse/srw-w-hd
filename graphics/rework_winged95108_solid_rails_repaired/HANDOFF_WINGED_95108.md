# 날개형 기계의 두 레일 #95108 고형면 교정 후보

같은 ID1개 교체 후보, 신규 미연결 증가0. 정상 다른5개는 유지했습니다. 공식 QA/실제HD 재생·라이브/DB/코어쓰기 없음.

## 원본과 현재 상태

- 최신 fixed current machine lost, live atlas observed_fixture345_winged_six가 같은 것을 확인했습니다. 원래 winged_mechanical_native1394/packed/install_contract.json의 actual cached source와 live index/actual full16/RGB CRC를 재검산했습니다.
- 실제 source state native_weapon_source_345_1394/unit345_weapon1394_source.state +180/OAM6/screen135,57/32×16/127texel, flip/affine 없음. 실제 전체 문맥은 actual_mechanical_pose_345_180/whole_native_context.png입니다.
- 캐릭터 이름은 화면의 펜치논이며 카탈로그 EI-27과 실제 기체 소유를 동일시하지 않았습니다. 원본 IMG/resource 미확정은 그대로 유지합니다.
- 현재 texture_key로 graphics/parts_baked.sqlite를 mode=ro SELECT해 실제 baked를 확보했습니다. source와 현재 baked 비교에서 두 고형 레일의 실제 어두운 측면·끝이 가늘어져 사라졌습니다.
- native127 중28texel 미칠: 검정(16,16,16)10/37, 짙은 회보라(98,82,98)7/22, 다른 보라계11. 단순한1픽셀 밝은 AA만의 차이가 아닙니다. current_baked_report.json.
- 현재 IoU .643/미칠 .220/외부0. 같은 actualfullpal 정상 큰 raw 완전포함0(same_source_parent_matches.json). 따라서 정상 부모 동일child 보존 대상이 아니라 실제 그림 교정 대상입니다.

## 새 그림

- generated_raw.png: imagegen 새 출력 exec-e4370c51-7f97-4f7c-bf27-9a33a284a90b.png 보존. 실제 원본을 참조했고, 위쪽 레일은 더 길고 급한 경사/아래 레일은 짧고 완만한 실제 배치를 유지하도록 요청했습니다.
- 원래 색의 연보라 앞면, 짙은 회보라 측면, 검정 불투명 끝과 작은 주황 기부를 새로 그렸습니다. 가는 빛줄기·흰핵만 남기는 그림으로 바꾸지 않았습니다.
- 두 레일을 한 생성 그림으로 유지해 사이 빈틈과 기부 연결을 보존했습니다. 실제 끝은 원래 검정 재질이며 임의 투명으로 지우지 않았습니다.
- 생성 전체 RGBA의 bbox 기하 정렬만 적용, 원본 RGB/alpha 전사·native mask/알파문턱 삭제·팽창/침식·재색칠 없음. alignment_provenance.json.

## 인수 파일

- installation_map.json: 같은 #95108만 교체, 원래 lookupflags/hash/index/fullpalette/source속성 유지. contract.json actual source+old spec 보존.
- candidate_atlas.png SHA256 `0b1224c3447ea90dbf77e1584b62e86cee304ce5fbd89e8484e1ddf1400d0a55`, native_atlas.png 함께 사용. native32×16/후보128×64.
- candidate 및 NullCache prepare 사전기하 flags0, IoU .880/미칠 .016/외부0. 숫자를 실제 장면 화질 합격으로 부르지 않습니다.
- replacement_comparison.png는 원본/current baked/new candidate. 직접 제작 대조에서 실제 두 레일의 고형 측면과 끝·기부가 유지됨을 확인했습니다.
- 같은 atlas 다른5개 spec 불변 비교는 preserved_normal5_latest.json.

## Claude 확인할 위험

- 새 평면 명암이 이전보다 단순하고 검정 끝이 딱딱한 캡처럼 보일 수 있습니다. 실제 원본의 검정 측면/끝과 인접 기계 연결부에서 자연스러운지 확인해야 합니다.
- 원본127texel 중약2texel 위치/AA 차이가 남습니다. 실제 작은 주황 기부의 색/면적 및 두 레일 경사·간격은 실제 조립에서 판정해야 합니다.
- +200 다른 조각/다른 팔레트/전체 기체 모든 자세까지 이번1개로 완료하지 않습니다.
