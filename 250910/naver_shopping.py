import pandas as pd 
import time 
import re
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from sqlalchemy import create_engine

search_item = input("검색어를 입력하시오 :")
save_type = input("저장 방식을 지정하시오 (csv / db) :")

while True:
    if len(search_item) == 0:
        search_item = input("검색어를 입력하시오 :")
    else:
        break

while True:
    if save_type in ['csv', 'db']:
        break
    else:
        save_type = input("저장 방식을 지정하시오 (csv / db) :")

driver = webdriver.Chrome()
# 딜레이 
time.sleep(1)
# driver 네이버 요청을 보낸다
driver.get('http://www.naver.com')
time.sleep(1)
# id 가 query인 태그를 선택 
search_element = driver.find_element(By.ID, 'query')

# 검색어를 입력한다. 
search_element.send_keys(search_item)
# 검색어 창에 ENTER 이벤트 발생 
search_element.send_keys(Keys.ENTER)
time.sleep(1)

# 쇼핑 문구가 있는 하이퍼링크를 선택하여 클릭한다.
driver.find_element(By.LINK_TEXT, '쇼핑').click()
time.sleep(1)

# driver에서 탭을 이동
driver.switch_to.window(driver.window_handles[1])

while True:
    # 현재 driver의 스크롤의 현재의 높이 
    last_height = driver.execute_script("return window.pageYOffset")

    # driver에서 스크롤을 일정 간격으로 내린다. 
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(3)

    # 스크롤 이동 후 스크롤의 현재의 높이 
    new_height = driver.execute_script("return window.pageYOffset")

    if new_height == last_height:
        break
# driver에 있는 html문서를 변수에 저장 
html_data = driver.page_source
# selenium의 역할 끝 -> driver를 종료
driver.quit()

