# Getter 293_170 자기부품 alpha 재제작 v2

- root미설치보류한상위폴더의wholepose사각crop후보는폐기할설치입력임. 이isolated_v2폴더가대체후보. 기존상위그림은출처/실패분석용보존.
- 최종candidate_atlas/native_atlas/install_contract 5개. 원본actualhash/indices/palette/렌더OAM/좌표/fixture/frame계약불변. source_owner/source_image/resource=None/cached_obj도동일.
- 이번방법: 원본각파츠의자체모양을잘보이게확대한14셀/5셀참조→imagegen으로각각해당부품만독립새생성→imagegen으로이웃paint와불필요배경제거→생성된자체alpha의bbox만원본부품위치사각형으로기하환원. 전체기체그림을사각형으로잘라쓴후보아님. 원본alpha실루엣마스크/원본RGB복사없음.
- generator/원본셀geometry/각원위치사각형및source_oam은provenance.json에기록. source_and_generated_component_reference.png는원본부품과생성자체alpha의나란한제작참조.
- clipping: 원본부분조각을완전한머리/팔로자동완성하지않고부분모양유지를생성도구에지시. G3왼쪽큰plate직선단면에인위적검은테두리를그리지않도록별도수정지시. 미세검은선/형태·색정확성은Claude확인대기.
- 메모리NullCache를쓴실제PartsRenderer.prepare_texture 결과 5/5 alpha.max≥16,현재activeRGB/indexed0,오류0. production_input_check.json. filter약화/Core/라이브/DB쓰기없음.
- 이검사는준비결과가빈그림인지확인하는생산입력검사뿐. 공식audit/독립HD재생/품질완료판정아님. Claude가접합·색배치·부품의자체형태·다른자세재사용을확인.
- 292는main4/shadow10,같은shadow4분신반복을서로다른새그림으로세지않음. 293은body17원본중신규5,기존12보존. 다른색·자세·기술은미완료.
