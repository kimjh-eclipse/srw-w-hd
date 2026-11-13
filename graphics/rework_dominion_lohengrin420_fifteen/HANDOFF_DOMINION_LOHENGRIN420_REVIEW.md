# 도미니온 로엔그린 전개 하부함체 15종 — 미검증 후보

- 실제 unit83/weapon356 메뉴420. `source_mechanical_83_356/source_pose.state` +0. palette0 OAM19 중 실제 미연결15(exact0/indexed0), 기존 exact4 상부함교 의존 보존. 새RGB를기존full-pose교체로오인하지않음.
- cached raw/actual 팔레트·hash·크기 확정, IMG8272/8269/1560 바이트 일치. actual PLT1559 bank0 사용색 일치. 작은 원본 first match를 고유소유자 추정으로 쓰지 않음.
- 연속4쌍: cell1/0(screen108→140,y86),2/3(49→81,y87),5/4(66→82,y76),13/14(156→164,y74). palette16/화면연속·flip/affine없음 검산. 같은 IMG인5/4와13/14는 source좌표도연속. 다른IMG의1/0·2/3은 actual 화면연속을 근거로 합쳤으며 서로다른그림의원본RGBA/alpha찍기가아니라새생성연속그림의분할이다.
- 총11생성그룹→15OAM. 같은그룹분할재조립RGBA완전일치/지원사각형밖생성내용0. 원래 가려진 조각의 내용을 하나의전체화면으로덮지않고각그룹원본내용별로제작하여뒤쪽원본지원보존.
- 생성raw보존,자체alpha<64만RGBA0/고알파불변. native RGB/alpha스탬프없음. native CRC·palette·4배크기·후보존재 기계적확인.
- SHA256 c13baeb4eeeec14c4347506fe05d9f05e99131b6ead2a08c14552f65d4fcfed1
- 설치 입력 installation_map.json/candidate_atlas.png/native_atlas.png. continuous_screen_source_proof/continuous_generated_split_proof 및 원본/제작조립 포함. 공식 QA/HD실재생아님.
- Claude 위험: 전개함체cell10과후부13/14가 기존상부4그림과이어지는절단면/레이어, 짙은하부포드1/2의볼륨, 가는ㄱ자프레임7의끝/두께, 주황기둥8·10·13과실제황록후부띠14의색영역, 잘린암부11/12의지원형태. 생성의낮은알파색노이즈는정리했으나높은알파에남은불필요색/외곽도Claude별도확인필요. 시각/실재생미검증.
- 라이브/DB/코어 수정없음,headless/모니터off유지.
