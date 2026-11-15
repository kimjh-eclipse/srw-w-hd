# 93510 격리: 93493 부모32×8 한벌 새그림

- 최종 candidate_packet.json / final_packet_index.json을 제출합니다. 교체대상93493·93510, 새wholemaster1장(생성2회 중flat최종1), 일반조각별새그림0입니다. source_only상태가 아니라 생성그림 후보가 있으며 설치/공식QA/재생완료는0입니다.
- 후보 candidate.png128×32 RGBA, 원본 native.png32×8, 실제생성원천 generated.png2048×768(32×12 padded canvas). 4역할SHA와 두 live prior_binding_spec_sha256을 기록했습니다.
- 최종그림은 generated_flat.png와동일한생성원천입니다. generated_draft.png는 형태는맞았지만 내부칸의광택/셀경계가 있어제외했습니다. sourcefolder밖 root의 parent_whole_draft /parent_cells_draft는 사용하지 않았습니다.

## 출처와 부모 공유

- 실제IMG19678 source부모[160,56,32,8], child[160,56,16,8]. source_proof_three의 actual_cached 계약과 최신live를 대조했고 ROM인덱스·full16·RGB/indexCRC가 모두정확합니다.
- 93493은새atlas[0,0,32,8],93510은같은atlas[0,0,16,8]을읽습니다. 원래atlas좌표/source좌표를구분했고, 자식만따로그려끝을막지않았습니다.
- 같은source영역과full16을동시에공유하는live바인딩은93493/93510뿐입니다. 93523은같은인덱스여도full16이다르므로병합하지않았습니다. live_shared_region_palette_proof.json 참조.
- 기존dynamic_palette모드와lookup/effect플래그를보존하는계약입니다. palette변형93523의그림/정책을이후보로바꾸지않습니다.

## 형태·끝점·스타일 확인

- 부모 native47 /candidate47, child native14 /candidate14. 읽기전용alpha64통계이며alpha파일을문턱으로자른것이아닙니다.
- 8연결성분7개가원본과같은면적/경계상자를유지합니다:5,8,5,23,3,2,1텍셀. 원본낮은해상도로줄여지원비교IoU1.0입니다. 원본alpha를스탬프해서만든수치가아니며generator결과의단순resize/unpad만사용했습니다.
- 핵심경계 x15,y5에서큰부모cluster로이어지는새alpha는246,오른쪽x16,y4=244/x16,y5=250입니다. 원래원소의좌우경계연결을유지했고자식에별도끝마개/외곽선을그리지않았습니다.
- 내부각pixel을따로솟게만드는pillows/bevel을첫결과에서줄였고, 최종은연결그룹별평평한밝은노랑/연노랑/금색면과매끄러운약한외곽으로정리했습니다. native_candidate_gray_pair.png에서부모/자식각각회색합성비교를확인했습니다. 실제게임에서과한광택/blur가없는지는Claude최종눈검사대기입니다.
- 먼빈공간alpha8초과0%,최대alpha3. alpha1~3인미세픽셀155개는생성값그대로남았습니다. 회색불투명안개나넓은배경매트를깨끗한alpha라고위장하지않았고, 임계값삭제도하지않았습니다.

## 실제생성·정규화증거

- 4:1소스가도구에서변형되지않게32×12패딩canvas위8행에정확한native32×8을넣었습니다. 아래4행은빈기술패딩입니다. 생성전체를128×48로균일resize한후고정위128×32만내보냅니다. 성분별bbox추출/원본마스크/색채움/alphacleanup없습니다.
- generated.png원천경로와첫생성/최종flat생성계보는 generation_origins.json /producer_whole_master_proof.json에있습니다. candidate픽셀은자체생성wholemaster resize/unpad와완전히같고child는그부모crop과완전히같습니다.
- source_contract_proof.json은실제ROM/full16/hash/indexhash·부모포함공유RGBA검사를보존합니다. producer_geometry_check.json은성분7·면적·경계alpha·배경검사를보존합니다. 자동수치통과를독립게임시각합격이라고기록하지않았습니다.

중앙라이브러리/DB/런타임/큐/격리목록/공유인계문서는무수정입니다. Claude가두바인딩을한벌로연결/굽고실제unit8/weapon29의작은황색연출에서경계/폭/과한광택을확인해주세요.
