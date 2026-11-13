# IMG12077 준비 단계 빈17개 복구 v2

- 최종v2: candidate_atlas.png(1024×320), native_atlas.png(256×80), install_contract.json(107source계약,95고유hash+w+h).
- 관측20계약=19고유, 미관측87계약=76고유. 중복12개. source/팔레트/계약바이트는v1과동일.
- root의 production_bake_blockers17ID에대응하는생성crop만기하교정. 원본alpha를베껴칠하지않고,원본불투명범위의바깥사각형좌표만사용해생성된색/alpha그림을이동·축척. 생성된조각의실제형태/색/alpha가그대로남음. geometry_repairs.json.
- 원인: 전체별빛시트생성시작은edgefragment의위치가원본seed에서벗어나,원시crop에alpha는있어도기존remove_unattached_paint가떨어진조각으로제거했음. 원본seed위치에그림기하를맞춰해소. 공유필터/임계값은변경없음.
- actual PartsRenderer.prepare_texture 경로에candidate/원본만메모리override하고 PartsDiskCache를메모리NullCache로대체.95개모두 alpha.max≥16(95/95),오류0. production_prepare_result.json. 라이브DB읽기/쓰기·코어·라이브그림수정없음.
- 위 결과는생산입력의비어있지않음확인뿐. 선폭·형태·별빛위치·재생품질·고유alpha검증은Claude대기. 작은조각축척의자연스러움은특히확인필요.
- root가이v2atlas를전체95대상에교체·재굽기후성공17을다시활성화. 원본fallback해제는root판단.
