import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from datetime import datetime


url = "https://comp.wisereport.co.kr/company/c1010001.aspx?cmp_cd="

# 종목코드 
# codes = ['000660', '005930', '053280']
codes = []
# 유저가 입력한 값을 codes에 추가 
# 최대codes의 개수는 10개 
# 유저가 입력한 값이 존재하지 않으면 추가작업도 종료
for i in range(10):
    # 유저가 값을 입력한다. 
    input_code = input("검색하려는 종목의 코드를 입력하시오 : ")
    # input_code가 존재하지 않는다면 반복문을 종료
    if input_code:
        codes.append(input_code)
    else:
        break

# while True:
#     input_code = input("검색하려는 종목의 코드를 입력하시오 : ")
#     if input_code:
#         codes.append(input_code)
#         if len(codes) == 10:
#             break
#     else:
#         break


# 빈 데이터프레임을 생성 
df = pd.DataFrame()

# codes 만큼 반복 실행 -> 결과는 데이터프레임 ->
# 하나의 데이터프레임으로 결합(추가) -> csv 파일로 저장 
for code in codes:
    # url 과 code를 이용해서 요청 
    res = requests.get(url+code)
    # 응답 데이터를 BeautifulSoup을 이용하여 파싱 
    soup = bs(res.text, 'html.parser')
    # 종목의 코드가 잘못된 경우
    try:
        cmp_info = list(
            map(
                lambda x : x.get_text(),
                soup.find('div', attrs={'class' : 'cmp_comment'}).find_all('li')
            )
        )
        cmp_etc = list(
            map(
                lambda x : x.get_text(), 
                soup.find('div', attrs={'class' : 'cmp_comment_etc'}).find_all('li')
            )
        )
    except Exception as e:
        print(e)
        # 종목 코드가 잘못되었을때 다음 종목코드로 이동
        continue
    
    code_df = pd.DataFrame(
        {
            'cmp_info' : cmp_info, 
            'cmp_etc' : cmp_etc
        }
    )
    # code_df에 code컬럼을 추가하여 code값을 대입
    code_df['code'] = code
    # df에 code_df를 추가 -> 단순한 행의 결합 -> concat()함수를 이용
    df = pd.concat([df, code_df], axis=0)
    time.sleep(1)
    # 반복 실행될때마다 로그를 추가 진행 상황 확인 
    print(f"{code} 데이터 수집 완료")

# 현재시간을 불러온다. 
now_time = datetime.now() # 현재의 시간을 로드 -> 나노초 표시
now_str = now_time.strftime('%Y%m%d_%H%M%S')   # ->현재 시간의 포멧을 년월일_시분초
# df를 csv 파일로 저장 
df.to_csv(f'wise_data{now_str}.csv', index=False)
