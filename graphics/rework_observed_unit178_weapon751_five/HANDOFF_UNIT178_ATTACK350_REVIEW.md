# 실제 unit178 / weapon751 메뉴350 기계5조각 후보

CACHED_OBJ_ARTWORK_CANDIDATE_UNVERIFIED. 실제HD 재생·공식시각검사는Claude담당. 라이브/코어/DB변경없음.

- 설치입력 installation_map.json/candidate_atlas.png/native_atlas.png/contract.json. 후보 SHA256 ab2099b6d11c01874937ee3d49fc15c471ec9dd3ed3f7456f103a57dbb769a6c.
- source_mechanical_fixed_178_751_350/source_pose.state +0. 실제RGB3972787109/3303797019/913933999/895175680/3336823298 다섯조각 actualexact0/indexed0. 원본IMG11106 각각(80,0)16×16,(64,0)16×16,(8,16)16×16,(0,0)32×16,(0,16)8×16 rawbytes일치. full16 PLT1953 bank0동일.
- actual14 OAM의나머지9개기존파츠의존보존. 붉은세로연결면2/회색소형판1/짙은넓은기계면1/남색삽입면1로만명명했다. 원본전체 bbox 강조위치를확인했지만 얼굴/손/특정해부학명으로완성하지않았다.
- raw시트에서맞닿은조각도 실제screen에서는원본좌표/가림이달라세로로묶지않았다. 특히cell2·3·4가화면겹치지만숨긴원본RGB내용을공통완성머리로그리지않고각자기계면으로남겼다. 원본source사각형교집합은없음.
- 첫exec-aed0a8b1-97ae-4d79-b437-9e105fb4ffe2.png는도트확대및후광으로거절(보존). 새exec-2487da53-d146-4a1c-8593-33eef856baf8.png는새로매끈하게그린기계면. 생성자체alpha<64만정리해저알파후광제거/고알파RGBA완전불변. 검정기계면을배경색으로지우거나nativeRGB/alpha/mask를찍지않았다. 강한추가임계값사용없음.
- 기계적원본계약raw/크기/actual팔레트/후보비어있지않음확인. candidate_pose_production은신규5+다른native 조립의제작참고이며실제HD게임검사가아니다.

Claude 위험: 작은기계면에서모델이붉은면을C형테두리로완성하거나밝은세로면/검정연결면두께·곡률을변경했을수있다. 닫힌형상의가짜원형구멍이나눈처럼보이는구조를만들지않았는지,내부절단면검은선/좁은면지원/기존몸체겹침·색을확인해야한다. 그림자영역도원본solid검정이라투명삭제하지않음. 전체기체/무장완료주장없음.
