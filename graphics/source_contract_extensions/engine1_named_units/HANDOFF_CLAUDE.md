# engine1 기체 원본 입력 연결 조사

샌드록/데스사이즈 forecast·weapons 네 source의 동일epoch subOAM/subparts+cachedOBJ1 indexbytes/actualpalette로RGB·indexCRC를재계산한생산입력근거입니다. HD실재생/형태/색/레이어판정이아닙니다.

- 샌드록forecast 기체2는secondary_unit_6089/6253에연결. weapons기체17는sandrock_cached_pose exact.
- 데스사이즈forecast 기체3는secondary_unit_6089/6429/6253에연결. weapons기체17는deathscythe_forecast_closed_pose exact.
- 이source에새그림누락이없어중복그림제작/완료수를늘리지않았습니다. 기존그림의품질/오연결/실제sub렌더경로미적용은별도Claude확인필요. 모든서브장면이정상이라는뜻은아닙니다.
- Core.binding_id는1-based이며실제hash+크기로metadata연결을분류. 공통producer가단일engine만읽는한계를별도privatehelper로극복했을뿐공유runtime/DLL/추출helper변경없음.
- 원자료는test_current/parts/borrowed_shape_rework의각동명폴더,재현fixture/saves는공개Git에포함하지않음.
