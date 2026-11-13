# 배 주변 검정연기13 · 흰물보라5 신규 한벌

제작 완료, live/DB/공유코드 변경 및 독립QA/HD재생 미수행.

- candidate_eighteen.png 1024×1440/native256×360(상위 원본atlas좌표유지), SHA d23b834508b27742f84c363e85fc9ef4174e08c8b22148be18336daae1f4ba86. new_candidate_contract.json18. cell18/19 M9발은 제외.
- source 실제 unit267/1103 menu610 source_pose+1run(frame0), unit268/1106 menu310 source_pose+1run(frame0). actualcached source계약/contexts 보존. 현재 library exact중복0 확인. 원본IMG소유 단정하지않아 resourceNone/ownerfalse.
- 실제OAM 위치로 검정연기13을128×64 한벌, 흰물보라5를130×16 한벌로 조립해 각각 전체 새그림 생성. 생성그림의 자체alpha만 정리하여 bbox위치·크기맞춤. 실제OAM좌표로 분할하고 물보라cell15의flipX 역변환. 조각마다 외곽선을 새로 그리지 않음.
- 실제단색/소량픽셀도 모두18계약에 포함, 누락안함. 준비검사18/18 maxA255,지원면적비.798~1.150. 셀0/3/6/12에서분리성분1/1/1/3 제거. actualRGBhash재계산18/18일치(nativeRGBAstamp0/cachewrite0).
- Claude 확인대상: 연기의 작은원본입자 위치/형태, native보다 둥근연기, 사각crop경계와전체연속성, 작은분리성분제거, 흰물보라의 회색명암비율. 제작presence는품질판정아님. generated_smoke/splash.png 원출력 및 whole_generated_*_registered.png 전체등록그림 보존.
