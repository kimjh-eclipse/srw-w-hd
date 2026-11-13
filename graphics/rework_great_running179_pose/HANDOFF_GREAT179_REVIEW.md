# 그레이트 마징가 +179 자세: 설치 검토용 최종 후보

## 현재 판정

**18개 한 벌 최종 후보: 슬롯15도 새 그림으로 교정, 18개 전부 IoU0.70 이상. 메인 설치·18개굽기오류0 이후 실제300프레임검사완료. FINAL_REPLAY_REVIEW.md 참조.** 이 에이전트는 라이브나 DB를 수정하지 않았다. 검사상 경고가 0이라는 사실을 실제 게임 적용 완료로 바꾸어 보고하면 안 된다.

- 실제 상태: unit297 / weapon1213 / frame300.state에서 180프레임 실행한 offset+179. 캡처 `scene.state`.
- OAM0~17 모두 포함, 실제 RGB 해시18종, 중복0. existing exact RGB5 / 새 actual RGB13종.
- `contract.json`: 실제 VRAM의 index_pixels, actual_palette_bgr555/RGB, 실제 RGB/index 해시, 원래 OAM 행·좌표·변환·priority, native atlas_box. spec의 오래된 팔레트/해시를 복사하지 않는다.
- native atlas200×160, 후보4배800×640. 18개의 원래 사각형 크기·OAM 좌표 보존.

## 최종 검사

production `audit_all_parts.analyse`를 DB 없이 실제 캡처 팔레트/인덱스와 후보로 실행한 `native_colour_audit.json`: **18개 모두 flags=[]**. shape/outside/unpainted/colour/flat/key/empty 경고 없음. 설치용0.70 IoU 기준도18개 모두 통과.

| 교정 대상 | 최종 colour_bad | 최종 alpha IoU | 처리 |
|---|---:|---:|---|
|손2|0.193|0.921|새 손 그림을 +0.5,+0.5 native픽셀 정렬|
|뺨 뿔11|0.140|0.758|새 뿔 그림을 y -0.5 native픽셀 정렬|
|얼굴13|0.246|0.830|원본 두 파츠 문맥에서 새로 그린 머리의 얼굴13 영역만 사용|
|상부 헬멧14|0.179|0.868|원래 좋은 후보를 그대로 보존|

다른 파츠도 flags가 없으며 전체 alpha IoU0.758~0.924. 슬롯15는 새로운 그림으로0.905이며 colour_bad0.105다. 수치 기준을 변경하지 않았다.

`check_candidate.py`의 production material_map 검사도18개 모두 주변 native에 없는 색 번호 비율0, 큰 색 차이 비율0, native 미사용 slot 없음, 설명되지 않는 초록/자홍 키색0. 이 번호 검사만으로 그림의 정확성을 판단하지 않았다.

`preserved_good15.json`: 얼굴 재작업에서 바뀐 것은2/11/13이었다. 이후 슬롯15만 별도로 새로 그렸다. 최종 변경범위2/11/13/15,14포함 나머지14개 보존. 슬롯15 마지막 교정시 나머지17개 픽셀 배열 동일은 preserved_other17.json 참조.

## 얼굴 중복 문제와 채택 방법

얼굴13은 screen(176,79),32×16이고 헬멧14는(182,58),32×32다. 눈 부근이 실제로 겹친다. 두 원본이 함께 불투명한21texel 중 RGB동일3/다름18이었다(`head_shared_native_check.json`). 따라서 서로의 원본이나 기존HD 눈 영역을 무작정 공유하면 안 된다.

얼굴만 따로 생성하면 전체 눈을 자동 완성해14의 눈과 겹쳐 두 줄 눈이 됐다. 실제 두 파츠를 올바른 OAM순서로 조립한 `head_pair_native.png`를 문맥으로 연속한 머리를 새로 그렸다. 그 연속 그림은 `head_pair_generated.png`(생성출처 exec-ad3d2bda-35e9-4321-b32c-3089bf3efdc2.png)다.

처음 두 사각형으로 모두 역투영한 후보는 헬멧14의 원래 숨은 내용까지 얼굴색으로 채워 다른 자세에 위험하므로 **기각**했다. `rejected_joint_atlas.png`를 설치하면 안 된다.

최종 후보는 원래 좋은14를 복구하고 **새 연속 그림의 얼굴13 사각형만** 사용한다. 실제 특징 위치를 맞추기 위해 머리 그림에 +1,+0.5 native픽셀의 작은 평행이동만 적용했다. 잘라낸13의 alpha는 기존에 생성한13 HD 자체의 alpha 지원영역 안에서 제한했다. **native RGB·native alpha를 복사하거나 재색칠하지 않았다.** 숨은14 내용은 전혀 바꾸지 않았다. 수치 때문에 색맵을 덧씌운 것도 아니다.

## 직접 본 조립 결과와 남은 검증

`pose_comparison.png`: 같은 캡처 프레임의 native왼쪽/후보오른쪽. priority와 OAM 번호 내림차순으로 뒤부터 그려 낮은 OAM 번호가 앞에 온다. `candidate_detail.png` 확대도 직접 확인했다. 눈은 한 줄이고, 오른쪽 노랑/옅은 노랑 눈·파랑 중앙 얼굴·보라 그릴·빨강 crest가 연속된다. 두 줄 눈이나 얼굴/어깨를 가로지르는 큰 수평 사각형 절단선은 보이지 않는다. 원래 upper helmet14의 눈과 새13이 같은 장소에 놓이도록 맞췄다.

이것은 offline 실제OAM 조립 확인이다. 설치 뒤 defaultcore의 ready/vanish/대사창 가림과 다른 자세에서 얼굴13이 단독으로 나오거나14와 상대좌표가 달라질 때는 메인의 실제 재생 검사가 필요하다. 아직 이 후보를 라이브로 설치하지 않았으므로 그 검증을 완료했다고 쓰지 않는다.

## 설치 계약

1. `candidate_atlas.png`와 `native_atlas.png`를 새 atlas_id(예: great_mazinger_running179_pose)로 등록한다. atlas_box의x/y/w/h는native단위다.
2. 각 contract의 **actual hash / index_hash / index_pixels / actual_palette_rgb**로 등록한다. 이전proxy spec 팔레트·해시는 사용하지 않는다.
3. 같은 actual RGB5종은 정확한 항목을 갱신하고 없는13종은actual RGB전용 항목을 추가한다. 기존 indexed-safe fallback의 다른 팔레트 지원은 유지한다.
4. 새source 재굽기와ready확인 뒤 +179/+190/+220 및 이전+3 장면을 검사한다. 얼굴13의 다른 배치도 확인한다.
5. 기체18개 실제등장/HD/vanish와UI가림을 메인이 확인한다. 마징카이저는 이 후보 범위가 아니다.

## 재현과 출처

- `prepare_candidate.py`: 선택한 생성물 추출·세부 정렬·18개 역순OAM 조립. 슬롯15도 이제새생성그림을 쓰므로 라이브그림을 가져오지 않는다.
- `check_native_colour.py`: production개별shape/색/키검사, 메모리adapter만사용.
- `check_candidate.py`: production palette material_map 검사, 메모리객체만사용.
- `provenance.json`: 최종생성물·기각후보·미세정렬·색검사·15개보존·atlasSHA256.

공유코드·라이브 라이브러리·DB·메인핸드오프 변경없음.


## 설치 dry-run 이후 슬롯15 교정 완료

이전 rawpaint는 `graphics/rework_great_mazinger/pose_hd.png`(800×640)의 native좌표(160,80,32,8)를4배로 자른 원래 그림이 맞았다. baked/renderer.part() 결과나 재정렬된그림이 아니었다. rawcrop IoU가0.681818이어서 설치기의0.70기준에 걸렸다. 이 결과는 slot15_raw_crop_check.json에 보존했다.

기준을 낮추지 않고 **같은 actual원본과 기존좋은rawpaint를 참조해 두 연결편을 새로 생성**했다. 생성출처 exec-13a0407f-ea08-4f41-9e5a-2e6635d04f58.png, 로컬slot15_generated.png. near-black 바탕, 아주작은 빨강끝, 좁은황토띠 구성을 유지했다. 큰 빨강삼각형으로 만들지 않았다. 각 생성조각을 native component의 bounding box (0,0,3,4)/(17,0,5,4)에 맞췄고 **생성그림 자체alpha만 사용**했다. native RGB·alpha를 복사하거나 색맵으로 다시칠하지 않았다.

최종 슬롯15 IoU0.904762, colour_bad0.105/flags0. 전체18 native audit flags0, palette번호/키색검사 전부0. slot15_final_comparison.png는 원본왼쪽/새후보오른쪽이며 slot15_final_crop.png가 실제4배새파츠다. `preserved_other17.json`: 이번 마지막교정에서15외17개 전부픽셀동일.

슬롯15의 actual RGB2925529104는 기존7340과 동일하므로 새RGB를 중복추가하지 않고 해당exact항목에 연결해야 한다. 원래+3첫자세에서도7340을 사용하므로 +179뿐아니라 +3도 다시재생해야 한다. 이 에이전트는 라이브를 수정하지 않았다.

최종 candidate_atlas SHA256: `3f4cd2c52d4a224adbfa57334238e9e3b1e59f5bc526c44a97fb17fe197258e2`.


## 설치 후 실제 재생 결과

메인이새18개를설치했고굽기18/errors0확인후great179_final로300프레임재생했다. 추적18종모두등장/HD>0, vanish0/loading0/rescued0/held2. 실제179/190/220에서그레이트눈한줄·목·손·뿔정상과대사창가림을확인했다. +3의7340은컷인에가려시각확인할수없으며코어준비/HD추적만확인했다. 자세한18개계수와한계는 FINAL_REPLAY_REVIEW.md. 마징카이저는별도미완료다.
