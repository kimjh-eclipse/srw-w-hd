# 20050 보류 2개 자체 생성 재시도

94721/94722의 원본은 실제frame350 master에서 작은6조각+연속선1+끝1=8성분입니다. generated_components_v1은 자체생성된7작은직사각형에만 사용하며 이 출력의 계단형선은 폐기했습니다. generated_line_v2는 부드러운새선이고 자체중앙부분crop+전역affine 중심선2계수/폭scalar등록만 했습니다. 원본mask/RGB를그림에전사하지않고알파문턱삭제·형태학처리도하지않았습니다. registration_provenance.json/main_v3_geometry.json에기하계수를보존했습니다.

메모리준비는둘다maxA255이고fill/cleanup제거0이지만94721의native미칠비율은첫후보30%,v3후보25%라생산기준20%를넘습니다.94722는5.1%로줄었지만같은master의연결일관성을위해2개모두설치하지않습니다. candidate_geometry_comparison.json과master350_v3_gray.png를보세요. 격리/원본표시유지,완료/누락감소에가산하지않습니다.

생성은기본image_gen도구를썼습니다. 생성참조reference_eight_components.png는원본NN확대관찰용이며paint에복사하지않습니다. 생성1프롬프트: 같은순서8개독립파란성분을투명4x2시트로만들고성분7을연속가는내려가는선으로. 생성2프롬프트: 파랑(0,115,255)/청록(0,180,255)/아쿠아(0,230,255)만의한연속가는20도내려가는선,흰중심/광택후광/추가성분/픽셀계단없음. 모든출력은이폴더로복사했습니다.
