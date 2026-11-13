# 마징카이저 +179 후보: Claude 검증 인계

## 현재 상태

**미검증 그림 후보 / 연결 준비됨. 라이브 미설치.** 최종 그림을 수정한 뒤 공식 audit와 실제 재생 검사를 추가하지 않았다. 검증은 Claude 담당이다. 아래의 이전 검사 파일을 최종 후보 통과 근거로 사용하면 안 된다.

작업 폴더: `test_current/parts/borrowed_shape_rework/mazinkaiser_running179_pose/`

## 실제 프레임과 원인 분류

unit297 / weapon1213 / frame300.state를180프레임 실행한 offset+179의 실제 Core OAM·VRAM·팔레트를 캡처했다. 마징카이저는 palette1, OAM33~54의22개다. 그레이트0~17과 겟타18~32는 제외했다.

22개 모두 기존 binding은 있다. 그중5개는 실제RGB exact 연결이며,17 OAM(15고유RGB)은 다른 팔레트의 indexed proxy를 선택했다. 따라서 해당 프레임의 문제를 단순한22개 전체 연결 누락이라고 부르면 틀린다. 실제 색 구성에 맞춘 exact 그림이 부족하고, 기존 그림을 다른 팔레트로 재색칠하는 경로와 기존 그림의 형태/영역 오류가 섞여 있다.

`classification.json`에 실제hash·선택proxyhash·현재atlas·사용색slot별 source/actual 색 차이를 기록했다. 일부proxy는 사용색 최대차222/255 또는247/255다. 이것만으로 모든실제 깨짐의 원인을 재색칠로 확정한 것은 아니다.

## 계약과 중복

- `contract.json`: 실제22 OAM, 행·속성·좌표·변환·priority·실제RGB/index hash·indexpixels·actual BGR555/RGB palette·native atlas_box.
- `contract_unique20.json`: 동일actualRGB 중복을 제거한20개.
-22 OAM /20고유RGB. 기존exact5, 신규actualRGB15개 필요.
- 셀7은 슬롯40/43, 셀8은 슬롯41/44에서 재사용한다. `duplicate_check.json`으로 인덱스bytes·actual팔레트·같은그림좌표가 모두 같은 것을 확인했다. 반전은 원래OAM 변환에 맡겼다.
- 원본 native atlas320×288, 최종 후보1280×1152(4배). 각 사각형 크기와 원래OAM 배치를 유지한다.
- `installation_map.json`:20개 exactRGB 항목의 연결 준비자료. 적용하지 않았으며 root만 직렬 설치한다. 오래된 proxy spec의 hash/팔레트를 새그림에 복사하지 않는다. index fallback의 다른팔레트 지원은 유지한다.

## 최종 그림 제작

20개 모두 같은 실제palette1의 보라/라벤더 몸체, 빨강·분홍 트림, 황토갈색 날개, 작은 청록센서와 노랑 포인트를 원본대로 그리는 것을 목표로 새로 만들었다. 다른기체 그림을 재색칠해 채우지 않았다. 출처는 `provenance.json`.

최초생성에서 셀3/11을 얼굴 또는 허리라고 성급히 명명했다. 좌표만으로 역할을 단정하는 것도 오류였다. 이후 `jaw_or_waist_location_context.png`처럼 실제 전체OAM 원본에 bbox를 표시해 문맥을 확인했다. 이후 프롬프트는 그 실제위치·nativecrop·원본의 불규칙 색면을 사용했다. `waist_generated.png`라는 파일명은 초기작업명이며 역할의 정확성을 증명하지 않는다.

### 머리 아래 수평 접합과 뿔 중복 수정

`head3_4_5_native.png`와 `head3_4_5_location.png`를 참조해3/4/5를 한 연속 그림으로 다시 만들었다(`head3_4_5_generated.png`). 실제3사각형은 서로 인접하며 내부불투명 영역을 겹쳐 숨겨놓은 구조가 아니다. 하나의 그림을 원래OAM 사각형으로 나눠, 별개 그림의 흰뿔이 두 번 생기거나 하단 경계가 수평선이 되는 문제를 그림 제작단에서 다뤘다.

파트 지원영역은 이전에 생성한 해당HD alpha 안으로 제한했다. native alpha나 RGB를 찍거나 부족한 부분에 원본픽셀을 넣지 않았다. 숨은 다른파츠 그림을 통째로 덮어쓴 방식이 아니다. 새그림 적용 뒤의 실제색·다른자세 연결은 아직 검증하지 않았다.

### 오른쪽 날개 접합 수정

16/17/18/19의 실제native 사각형·좌표를 합쳐 `right_wing_joint_native.png`와 bbox문맥 `right_wing_location.png`를 만들었다.6쌍 모두 양쪽불투명 native 겹침이0이었다(`right_wing_overlap_contract.json`). 따라서 다른색의 숨은 내부가 겹치는 문제와 구분된다.

같은 날개를 한 연속 그림으로 다시 그려 `right_wing_joint_generated.png`에서 원래4사각형을 나눴다. 원래 떨어져 있는 아래 얕은조각도 이어 붙이지 않았다. 이때도 이전 생성HD 지원alpha 안에서만 색을 가져왔다. 반투명 경계나 다른자세에서의 연속성은 Claude가 봐야 한다.

## 산출물과 기계적 확인

- `candidate_atlas.png`: root가 설치 검토할 최종1280×1152 그림.
- `native_atlas.png`: 실제native320×288 원본 참조.
- `parts_generated.png`: 최초 생성물 출처. 최종그림은 여러후속생성물로 수정했으므로 최초물로 되돌려 설치하지 않는다.
- `candidate_pose.png`, `pose_comparison.png`: 원래OAM priority와 slot 내림차순으로 조립한 제작용 그림. 실제게임 재생검증이 아니다.
- `prepare_candidate.py`: 전용폴더에서만 조립한다. shared runtime 코드 수정 없음.
- `candidate_report.json`: 최종캔버스 크기만 기록. 검증담당 변경 뒤 새공식audit는 하지 않는다.
- `native_colour_audit_pre_final.json`, `colour_key_check_pre_final.json`: 최종머리/날개 교정 **이전** 검사. 최신후보의 통과 근거가 아니다.

## Claude가 확인할 알려진 위험

1. 새3/4/5의 하단·옆면 접합, 노랑눈/청록센서/보라면의 위치가 원본과 맞는지.
2. 셀11은 초기 역할오해를 고치며 새로 그렸으나 실제위치에서 원본형태를 유지했는지 독립적으로 판단해야 한다.
3. 오른쪽날개16~19의 지원alpha 경계에 가는 틈이나 원본노출이 남는지, 다른OAM 위치에서도 맞는지.
4. 빨강 연결편2의 가장자리를 원본형태에 맞추다 계단 모양이 남을 수 있다. 실제크기에서 확인할 것.
5. 신규15 actualRGB 연결, 기존exact5 교체가 다른공격에 미치는 영향.20개는22OAM에 공유되므로 중복계수하지 않는다.
6. 다른 기체·배경·이펙트는 이 그림범위가 아니다. 이 후보로 전체합체장면 완료를 주장하지 않는다.

## 검증용 실제 상태와 명령

상태: `test_current/combat/named_attacks/unit_297/diagnostic_preview/weapon_1213_capture/frame_300.state`

확인할 offset:179/190(한벌 정면),220(이동·팔자세 변경),3(초기 다른자세는 컷인이 가릴 수 있음).

root 설치·새source굽기가 끝난 뒤 Claude가 실행할 예시:

```powershell
& 'C:\Program Files\Python311\python.exe' -X utf8 scripts/verify/verify_runtime_path.py --state test_current/combat/named_attacks/unit_297/diagnostic_preview/weapon_1213_capture/frame_300.state --frames 300 --pure-native --save-frames 3 179 190 220 --track-atlas mazinkaiser_running179_pose --name mazinkaiser179_claude
```

실제로 설치할 atlas_id가 바뀌면 track-atlas도 함께 바꾼다. ready/vanish/loading뿐 아니라 저장된 원본/HD그림을 비교해야 한다. 검사는 이 에이전트가 실행하지 않았다.

라이브 라이브러리·DB·공유소스·메인 HANDOFF_FROM_CODEX는 변경하지 않았다.
