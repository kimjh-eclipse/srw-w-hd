# 20183 문제 5개 후보 인계

- 대상: 94796~94800. 독립 부모 94797,94798,94799,94800 4개와 94797의 공유 자식 94796 1개입니다. 정상 94795의 기존 RGBA와 바인딩 메타데이터는 보존했습니다.
- 최종 설치 입력은 final_flat_contract.json, native_atlas.png(96×64), candidate_atlas.png(384×256)입니다. 이전 candidate.png 및 parents5.json은 이전 시도이며 설치에 쓰지 마세요.
- 94797의 own_rgba_94797.png 하나를 부모/자식에 사용합니다. 자식은 부모의 오른쪽 절반을 그대로 참조합니다. 94795와 target의 직접 겹침은 없습니다.
- 두 팔레트는 별도 생성했습니다. group0 청록/흰색(94795~94799), group1 옅은청록/흰색(94800)입니다. source 시트 y32는 팔레트 경계이며 물리 연결이 아닙니다. 재색칠/타팔레트 알파 차용 없음.
- actual_observed_source_contract.json에 실제 index raw, 16색 BGR555, 관측 OAM, state 및 frame 원자료를 복사했습니다. 최종 계약에도 index_pixels/전체16색을 유지합니다. 전체 대상은 native_weapon_source_119_498/unit119_weapon498_source.state의 실제 관측이며 프레임은 94796,94797=210, 94798=215, 94799,94800=220입니다. 정상94795=205입니다. 미관측 추가 추정 없음.
- 최종 source_box와 atlas_box를 분리했습니다. 94800의 source_box=[64,0,32,16], atlas_box=[64,32,32,16]입니다.
- generated_94797~94800.png는 builtin image_gen의 별도 생성 PNG입니다. 94797 회색 배경/구멍 초안은 rejected_*로 보존하며 채택하지 않았습니다. 94799의 중앙 2×2 L은 같은 group0 팔레트로 앞서 생성한 panel0_generated.png cell3의 자체 RGBA를 재사용했습니다. 구체 좌표는 final_geometry_registration.json입니다.
- 입자열 각각 5성분을 원래 bbox에 자체 생성 RGBA crop/resize로 등록했습니다. 94800 마지막 입자의 위치도 원래 x28,y15로 등록했습니다. 생성 알파 삭제/형태학 연산이나 원본 RGB/알파 전사는 없습니다.
- NullCache PartsRenderer.prepare_texture 6개 전부 nonempty, 실제 index alpha/RGB 입력 일치입니다(final_production_report.json). 등록 파츠의 runtime alpha repair 통계도 모두0입니다.
- preflight는 5개 모두 geometry_flags=[]입니다. IoU: 94796=.995,94797=.976,94798=.939,94799=.971,94800=.943. 최대 미칠=.029, 밖=.000. 이것은 제작 사전검사이며 공식 QA가 아닙니다.
- final_candidate_gray.png와 final_native_gray.png로 RGBA 합성 비교했습니다. 생성 alpha0 RGB 잔여를 실색으로 판정하지 않았습니다.
- 설치/라이브러리/sqlite/공유 코드/EXE/배포/푸시/모니터/게임 조작 없음. 중앙 설치·굽기·동일 도구 검사 및 Claude 독립 시각/게임 검증이 남았습니다. 실제 표시 순서·시간별 혼합은 미검증입니다.
- 최종 SHA는 final_sha256.json을 보세요. candidate SHA256: 72fe194fc2d9f530501731b17b02852f43a73e451e7a91b6fd7ce9db5bd227fe.
