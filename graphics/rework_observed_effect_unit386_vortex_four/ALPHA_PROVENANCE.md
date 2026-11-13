# Unit386/w1530 大청백색소용돌이4

- 실제cached4종의raw64x64가IMG21222 x128/0/64/192 y0에바이트일치. actual16palette동일한4그림을원본시트256x64로복원해한장새그림으로제작. source frames550/555/585/595의state/OAM/좌표/변환은각new_candidate_contract.json보존.
- 주의: 원본시트인접은runtime동시조립증거아님. 이번계약4는서로다른시점이며동시에두반쪽이이어졌다고단정하지않음. SHEET_VS_RUNTIME_CONTINUITY.md참조. 원본참조시트는IMG21222의raw와일치하지만ROM전체의유일소유까지독립증명한것은아니므로resource=None/owner_confirmed=false. reference_sheet_image=21222/raw_match_confirmed로시트연속성만기록. 실제palette는관측actual값만근거.
- builtinimagegen전체256x64시트용자체RGBA. 생성이상하투명padding을추가해단순resize시canvas끝밝은핵이alpha0위치로밀렸다. 이는386에서는내부hole이아닌global배치오류. 새생성자체alpha32bbox(12,86,2163,636)를원본전체bbox(0,0,256,64)에affine위치/확대등록해fullRGBA보존. 원본mask/RGB전사/alpha공유/색코드채움없음. corrected center samplesalpha250–254/원본밝은23,712샘플중alpha<16 0%.
- candidate1024x256 SHAd952fd2b07648da246c186584d70843795804d12bb3bab28119ab1b32ca5e0fa. prepare4maxA>=16/support>.1/nearblank0,latestexact/indexed중복0. 이값은제작존재확인이지독립QA/실제HD합성검증아님.
- 알려진위험: 원본중심(205,238,255)보다더청록색/짙어졌고,부드러운반투명중심alpha250전후라원본255와다르다. 소용돌이밴드위치/선수/외곽투명coverage가달라질수있음. native_candidate_comparison.png에서전체생성형상보존을보되실제레이어와각OAM크롭/이음선은Claude실재생대기.
- 설치는root만. 라이브/DB/core/EXE/공유코드/플레이어창/물리입력변경없음.
