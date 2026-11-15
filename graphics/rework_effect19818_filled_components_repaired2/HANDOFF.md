# observed_effect_19818_new51 검토4개: 교체2/기술보존2

- 92855/92861/92872/92881의 fixed current classified와 현재live atlas가 동일함을 확인했습니다.
- **교체는92872와92881 두개만**입니다. 최종입력 final_flat_contract.json,native_atlas.png(256×160),candidate_atlas.png(1024×640)입니다. SHA256=4b4c8fbb0d6806b4e035a8a5bd0b37c22aa494ea06e70f07b6fbe328ad474a5f. sha256.json에계약/원본/생성파일SHA를고정했습니다.
- **92855와92861은기술보존**입니다. 정상부모92856과source crop/index raw/full16 BGR555/RGB/아틀라스자체RGBA가같습니다. held_shared_parent_proof.json에근거가있습니다. 별도새그림으로공유를깨지않았습니다. 해당2개는교체완료/시각QA통과로세지않습니다.
- 주의: held2개의prepare결과는정상부모prepare crop과완전byte일치하지않습니다. raw아틀라스그림/원본은같고prepare차이는별도기술검토대상입니다. 이생산작업은공유코드를고치거나이를가리기위해그림을바꾸지않았습니다. 정상부모와자식메타/key를보존했습니다.
- 전체51중정상47+held2=49개의기존자체RGBA/메타를byte비교로보존했습니다(preserved49_including_held2.json). 새그림2개와정상영역직접겹침은없습니다.
- actual_observed_contracts.json/source_original_install_contract.json에true_missing_19818의실제관측원자료를복사했습니다. 92872/92881은 unit130_weapon543_source.state +490 실제관측입니다. 원본raw와전체16색을그대로유지했으며미관측추정추가없음. 최종flat에source_box/atlas_box를구분했습니다.
- 92872 원본은x3~15,y7의13×1 완전채움입니다. 기존분홍대칭lens와달리왼쪽은분홍에서시작해오른쪽대부분은near-white로유지하는새자체생성재질을13×1의정확4배로등록했습니다. 원본RGB전사나자동색칠없음. 사실상색교정이며작은직선한행이라HD형태이득은작습니다.
- 92881은긴흰세로기둥과아래수평흰strip,그둘을이어주는곡선flared base를새로그렸습니다. 세로기둥폭을hairline으로줄이지않고,원본의수평흰base를가로대칭분홍lens로바꾸지않았습니다. 원본미세계단은새연속곡선으로해석했습니다.
- generated_92872.png는전체불투명자체생성재질이며13×1 target bbox에resize했습니다. generated_92881.png는transparent_background=true의별도자체생성PNG입니다. own_rgba_ID.png가등록후그림입니다. 원본mask/RGB/alpha전사/문턱삭제/morphology/팔레트차용없음.
- 후보및prepare preflight2개모두flags=[]입니다(candidate_geometry.json,prepare_geometry.json). IoU 92872=1,92881=.841,미칠최대.068,밖0. 사전검사통과는정식QA가아닙니다.
- 최종target NullCache PartsRenderer.prepare_texture2개모두nonempty/sourceindexalphaRGB일치입니다(production_report.json). 전체51개생산입력검사도기록했습니다.
- manual_native_before_candidate_prepare.png는원본/기존/새후보/prepare를회색RGBA합성으로비교한파일입니다. 원본의흰면적과가로/세로폭이돌아온것을수동확인했습니다. alpha0RGBghosts를실색으로오인하지않았습니다.
- 라이브러리/sqlite/공유코드/코어/EXE/배포/푸시/모니터/게임창미수정. 중앙설치·굽기·동일도구검사및Claude독립시각/실제게임검증이남았습니다.
