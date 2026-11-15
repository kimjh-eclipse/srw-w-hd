# 미사일·궤적 사용자 제보: wholeIMG 소스2 +95343교체1

## 원본과 현재 누락 확인

- 제보: codex-clipboard-891e7216-b0fa-403f-b3c7-308d24c1b34a.png. 기존 실제원본 채집 unit172/weapon737(카탈로그 델파니움/미사일)의 native_unmodified210 등과 같은 회색4포드·녹색창 장면입니다. 기체 외형으로 이름을 추측하지 않았습니다.
- 흰 궤적·연기는 IMG20224(192×96), 미사일/분사체는 IMG20225(64×96). 기존실제 renderedcached OBJ의 full16 기본팔레트와 ROM인덱스 사각형 비교가 이미 있고, 이번에도 최신lib·ROM·DB를 읽어 대조했습니다. 두bank의 실제기본팔레트는 같습니다.
- 기존58개 direct binding(20224=47,20225=11)이 존재합니다. IMG20224의 기본팔레트34개 직접사각형은 원본7181비영텍셀 중4976을 덮고2205는 바깥에 있습니다. 전체누락을 단순바인딩개수로 닫지 않았습니다.
- 더 강한 확인: 최신 parts_tile_library.sqlite를 mode=ro로 읽어 모든8×8원본raw와 완전히 같은 타일이 있는지 검사했습니다. IMG20224:243비영tile위치/242고유raw 중 어느팔레트에도 없는53위치, 실제기본팔레트에는 없는61위치. IMG20225:89위치/87고유raw 중13위치가 어느팔레트와기본팔레트 모두에 없습니다.
- 합계66위치(어느팔레트에도없음),74위치(실제기본팔레트없음)는 tile위치수이지 새그림66장/새OBJ66개가 아닙니다. current_tile_database_coverage*.json에 rawCRC와 출처당 조회결과를 보존했습니다.
- 현재 DB에는 IMG20224출처47행,20225출처11행이 있어 예전처럼 bank전체가 라이브러리에 없는 상황은 아닙니다. 캐시/실행중 DLL갱신 문제와 새그림 누락을 분리해야 합니다.

## root 제출3패킷

1. candidate_packet_whole_img20224.json
   - 새wholeIMG sourcekey3522638746. candidate_img20224.png(768×384), native192×96.
   - drawing SHA f09679eac93d41d63673d822984d2e2837940ef854248baa0d7df823bbc11e16.
2. candidate_packet_whole_img20225.json
   - 새wholeIMG sourcekey2659413298. candidate_img20225_assembled.png(256×384), native64×96.
   - drawing SHA 487c2a7eb2a733009e6849eab0bd9df2fcb4b48c0721dc2086dc251a7d46e6dd.
3. candidate_packet_replace95343.json
   - 일반binding95343 교체. 정확한 IMG20225 source[24,0,8,8], 원본45텍셀/새후보45, IoU0.7647.
   - 별도작은그림을 그리지 않고 위whole20225의 동일좌표RGBA를 그대로 읽습니다. full16·hash/index_hash·실제관측계약·live priorSHA를 유지했습니다.

모든packet은 contract/drawing/native/generated 4역할SHA를 갖고 마지막에 재검증했습니다. 최종목록 final_packet_index.json SHA b34f52095e6d3a783e80f557fee587ab8e78de3d8590cb9f4ef3d2899c4ee973.

## wholeIMG 계약의 정확한 의미

- whole2계약은 tile_source_only=true / actual_observed=false입니다. 전체192×96 또는64×96이 직접NDS OBJ로 관측됐다고 기록하지 않았습니다. 실제로 관측된 것은 그bank의 일부OBJ와full16팔레트이며, 대표원천프레임/좌표를 계약에 함께 넣었습니다.
- 전체ROM IMG바이트SHA·header·인덱스SHA·폭높이·full index_pixels·기본팔레트RGB/BGR555·fullCRC hash/index_hash·8×8 coverage proof를 제공합니다.
- 일반파츠 자동설치완료로 표시하지 않았습니다. packet의 adapter_required=true / automatic_parts_install_supported=false. Claude가 wholeIMG를 타일재료로 연결하고 기존accepted 직접그림·타일우선순위를 유지해야 합니다. wholebank를 화면에 하나의OBJ로 그리지 마세요.
- sourcebank fullCRC는 새자료의 정체를 위한sourcekey입니다. 실제게임OBJ바인딩ID인 것처럼 만들지 않았습니다. 일반95343교체는 별도로 인계합니다.

## 그림·공유 부모·제작 증거

- IMG20224는 한 장 전체를 image_gen으로 새로 그린 master를 통째로4배캔버스로 정규화했습니다. 원래 궤적·틈·연기·작은앰버네모·칸끝을 유지하도록 요청했습니다. 전체alphaIoU0.8680.
- IMG20225는 새로 그린 smoothwholemaster의 위64행과, 기존설치95351의 정확한 wholeparent IMG20225[0,64,64,32]를 원래source좌표에 통째로 공유한 완성전체시트입니다. 기존정상 아래분사체를 중복교체하지 않았습니다. 전체IoU0.8746.
- 95351은 원본raw와full16이 완전히 같고 기존그림의 정확한atlas부모[128,40,64,32]에서 복사했습니다. 신규atlas좌표를 source좌표로 오인하지 않았습니다. accepted_parent95351_reuse_proof.json에 원천파일SHA·부모cropSHA·live specSHA·RGBA완전일치를 보존했습니다.
- 95351상태는 설치됨/비격리/제작install보고IoU0.9599·형태경고없음입니다. visual_accepts에는 별도95351기록이 없으므로 독립눈검사완료라고 부르지 않습니다. 부모이미지사본을 패킷안에 고정하고 additional_file_sha256도 제공합니다.
- 새wholebank2 / 일반교체1(같은body그림공유) / 별도새작은조각0. 이 작업의 built-in image_gen 호출4회 중 선택원천2개이며, 나머지2개는 pixel계단유지 또는 glow/matte퇴행으로 폐기후보로 보존만 했습니다. generated_img20225_draft.png / generated_img20225_final.png를 설치하지 마세요.
- producer_whole_master_proof.json과 generation_origins.json은 실제생성파일 경로/SHA·부모전체공유·변환계보를 보존합니다. 생성알파를 임계값으로 삭제하지 않았고 원본alpha/RGB 스탬프·색채움·코드재색칠도 없습니다. 같은IMG의 정확한 전체HD부모를 좌표대로 atlas에 조립한 것입니다.
- 최종두bank의243+89개 모든 비영source tile위치에 후보그림이 있습니다. producer_per_tile_shape_checks_final.json에 tile별면적/빈그림검사를 기록했습니다. 새로없던66위치도 전부 비어있지 않습니다.
- 회색합성 production_native_candidate_comparison.png로 원본/완성sheet/95343을 확인했습니다. 원본/생성RGBA의 투명밑RGB ghost를 효과로 세지 않았습니다. 최종먼빈공간alpha8초과 비율은20224약0.486%,20225약2.632%이며 불투명사각매트는 없습니다. 미세생성경계는 남을수있습니다.

## Claude 실제연결/QA

- 기존accepted 타일을 새bank로 일괄덮지 마세요. 기존부모와 새wholebank가 같은실행조합에 섞일 때 틈/경계/팔레트가 맞는지 실제unit172/weapon737 재생으로 확인해야 합니다. 전체IoU통과는 타일조합 완성 판정이 아닙니다.
- 권장순서:95343 교체후검사, whole2를 source-only재료로adapter연결, accepted우선순위유지, 재질/타일DB 재생성, 실제미사일단계/회전/반전/밝은연기접합QA.
- 이번whole2는 기본실제팔레트입니다. 기존어두운2단계개별그림은 보존했고 어두운bank전체까지 새로 그렸다고 주장하지 않습니다.
- 중앙실행코드·라이브러리·DB·큐·manifest·공유 인계문서·격리목록은 변경하지 않았고 사용자UI도 조작하지 않았습니다. 연결/설치/실제재생검사0입니다.
