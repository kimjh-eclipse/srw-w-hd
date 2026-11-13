# IMG12077 별빛·파편 효과 제작 인계

- 기체아님: source 전체는 빨강/분홍/흰색 별빛 및 작은파편 효과. 실제unit214/mechanical_cutin_144.state+10 등 source캐시에서19고유관측. 동일한그림의두source좌표가있어계약20으로표시됨.
- install_contract.json107계약=관측20(19고유)+PLT full16확정 미관측87. 전체고유hash는root설치시중복제외할것. 관측/미관측fixture 필드분리.
- candidate_atlas1024×320/native_atlas256×80,연속전체source시트 독립새생성. native_reference/sourceindices/hash/palette/sourcebox/proof 모두계약포함.
- 전체그림에서생성누락된작은edgefragment8개를새imagegen그림으로보완. 각소스8×8범위만변경,나머지atlas픽셀동일assert. 원본RGB/alpha스탬프없음. generated_missing_eight.png/provenance.json참조.
- all107 cropmaxA≥16 기계확인. 공식audit/HD재생/독립QA없음. Claude가선폭/조밀한별빛위치/단색tinyfragment/실제알파검증.
- whole native문맥 ../mechanical_missing_source_lookup/whole_native_12077.png.
- 라이브/DB/코어쓰기없음,root설치굽기.
