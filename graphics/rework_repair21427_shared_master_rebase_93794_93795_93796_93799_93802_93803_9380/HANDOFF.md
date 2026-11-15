# 21427 현재live 대조 후 별도 rebase 패킷

이전repaint패킷은13:47원래후보설치전 spec이라거부되었습니다. 이전게시파일은수정하지않고별도고정폴더에서현재live를다시읽어대조했습니다. 현재atlas repair21427_shared_master_93794_93795_93796_93799_93802_93803_9380의이미지/원본/native/specSHA를작업시점에동결했습니다.

rebase_source_outside_proof.json:현재liveRGBA는원래설치된격자후보와전체같습니다. 원본nativeRGBA와9개대상의hash/indexhash/rawindex/full16/atlas좌표는기존실제원천과모두같았습니다. 현재그림위에기존연속면repaint의4개교정사각형만다시적용했습니다. 그밖모든RGBA변경픽셀은0이며,이전repaint와현재그림의범위밖차이도0입니다. 새spec지문만임의로바꾼것이아닙니다.

변경9개:93794/93795/93796/93799/93802/93803/93804/93806/93809. 원래master source[0,0,32,64]와atlas[0,240,32,64], full16/raw/state/공유ownRGBA는그대로입니다. native256×400/candidate1024×1600정확4배입니다. 새ready_candidate.json은현재live의9개specSHA와네파일SHA를포함합니다. 그림SHA c516...은앞서거부된연속면repaint와같은그림인것이정상입니다.

manual_current_repaint_gray.png:현재설치/새연속면후보. 미세성분1~3px라HD세부이득제한/미세회색농도차위험은그대로입니다. alpha0RGB와실제표시를회색합성으로구분했습니다. 중앙쓰기/연결/굽기/공식QA는수행하지않았습니다.
