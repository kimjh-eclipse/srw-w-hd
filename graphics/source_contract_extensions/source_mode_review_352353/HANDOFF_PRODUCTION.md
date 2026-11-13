# 352·353 원본 분류 정정: BG 누락이 아닌 기존 OBJ 연결

이전에 순수 원본 화면에서 기체가 도트로 보이고 unknown 목록이 비어 있다는 이유로 BG 미연결이라고 설명한 판단을 철회합니다. 순수 원본 캡처는 HD를 끈 그림이므로 도트가 보이는 것이 당연하며, unknown 목록은 기존 바인딩을 제외합니다. 따라서 그 두 사실로 HD 누락을 판정할 수 없습니다.

직접 retro_srw_copy_cached_obj와 core.parts·rendered OAM을 대조한 결과는 SOURCE_CLASSIFICATION_CORRECTION.json 및 각352_200/353_200/cached_rows_direct.json입니다.

- 352/w1407 +200: OAM0의 바인딩91512, 캐시64×64, 실제 해시2780743135. part 해시와 캐시 해시, 렌더 OAM 속성이 모두 일치합니다.
- 353/w1409 +200: OAM0/1/2의 바인딩87156/87155/87154, 실제 해시631479458/1280437678/2015994909. 각각 part 해시와 캐시 해시, 렌더 OAM 속성이 일치합니다.

HD를 켠 source 채집에서는 이미 연결된 OBJ의 원본이 숨겨지므로 그 위치의 native owners가 비어 있습니다. 이를 원본 데이터가 없거나 지원되지 않는 경로라고 해석한 것도 잘못입니다. 실제 기체가 BG라는 근거가 없고, bitmap·8bpp·3D 미지원이나 신규 BG 캐시 API 필요의 근거도 이 자료에서는 없습니다. 이 두 기체에 새 BG signature를 등록하거나 API를 추가하라고 요청하지 않습니다.

현재 연결된 그림이 올바른지·HD가 실제로 잘 보이는지의 판정은 별개이며 Claude의 실제 재생 검토가 필요합니다. 이 작업은 QA를 실행하지 않았고 연결 존재·제작 source 분류만 바로잡았습니다. 기존 그림의 정확성이나 완전 적용을 주장하지 않습니다.

보존 자료는 순수 원본 whole_native.png, rendered_native_planes.npz, rendered_oam_planes.npz, 실제 OAM 및 직접 캐시 행, 프레임 끝 MMU 양 엔진 BG의 map/tile/palette/register/스크롤/우선순위와 image/map signature입니다. 이 MMU BG 자료에 기체가 없는 것은 해당 기체가 실제 연결된 OBJ인 점과 일치하며, 그것만으로 draw-time 데이터 누락이나 MMU 프레임 불일치를 증명하지 않습니다. 원본 capture script는 기존 API 읽기만 사용했고 공유 코어·렌더·메타·DB를 변경하지 않았습니다.

실제 draw-time 캐시 경로 참고: scripts/assets/capture_rendered_obj_contract.py의 capture_rendered_obj_contracts, emulator/desmume/desmume/src/srww_texture_cache.h의 SRWWCopyCachedOBJ, srww_parts_impl.h의 SRWWHD_ShouldSkipRobot, libretro.cpp의 retro_srw_copy_cached_obj/retro_srw_copy_rendered_obj입니다. 이 경로로 두 fixture의 원본 입력은 이미 읽을 수 있습니다.
