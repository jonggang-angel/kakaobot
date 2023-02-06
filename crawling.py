import time, win32con, win32api, win32gui
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time 
from selenium.common.exceptions import NoSuchElementException
import re,sys,os

def weather():
    ##크롤링
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("window-size=1920x1080")
    options.add_argument("--headless")

    s = Service("c:/py_temp/chromedriver.exe")
    driver = webdriver.Chrome(service=s,options=options)
    url = 'https://www.naver.com/'
    driver.get(url)
    driver.maximize_window()

    #네이버에서 날씨 가져오기
    element = driver.find_element(By.ID,'query')
    driver.find_element(By.ID,'query').click( )
    element.send_keys('오늘의 날씨')
    element.send_keys("\n")

    time.sleep(0.5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #날씨비교
    weather=soup.find('div','temperature_info').find('span','weather before_slash').get_text()
    info=soup.find('div','temperature_info').find('p','summary').get_text()
    info=info[0:-3]

    #온도
    temperature = soup.find('div','temperature_text').find('strong').get_text()
    temperature_low = soup.find('div','cell_temperature').find('span','lowest').get_text()
    temperature_high = soup.find('div','cell_temperature').find('span','highest').get_text()

    #강수확률
    rain_am= soup.find('span','weather_left').find('span','rainfall').get_text()
    rain_pm= soup.find_all('span',{'weather_left'})[1].find('span','rainfall').get_text()

    #미세먼지
    driver.find_element(By.LINK_TEXT, '미세먼지').click()

    driver.switch_to.window(driver.window_handles[-1])

    html1 = driver.page_source
    soup1 = BeautifulSoup(html1, 'html.parser')
    dust= soup1.find('div','top_area').find('span','value _cnPm10Value').get_text()
    dust_info=soup1.find('div','top_area').find('span','grade _cnPm10Grade').get_text()
    
    sdust= soup1.find('div','top_area').find('span','value _cnPm25Value').get_text()
    sdust_info=soup1.find('div','top_area').find('span','grade _cnPm25Grade').get_text()

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return ("[Today's weather]",'\n',weather,',',info,'\n','현재',temperature[5:],
    '(최저',temperature_low[4:],'/최고',temperature_high[4:],')','\n','오전 강수확률',rain_am,',오후 강수확률',rain_pm,
    '\n','미세먼지 ',dust,'μg/㎥',dust_info,'\n','초미세먼지 ',sdust,'μg/㎥',sdust_info)

def news():
    #뉴스 가져오기
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("window-size=1920x1080")
    options.add_argument("--headless")

    s = Service("c:/py_temp/chromedriver.exe")
    driver = webdriver.Chrome(service=s,options=options)
    url = 'https://zdnet.co.kr/news/?lstcode=0050'
    driver.get(url)

    html1 = driver.page_source
    soup1 = BeautifulSoup(html1, 'html.parser')

    iframes = driver.find_elements(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(iframes[2])

    html1 = driver.page_source
    soup1 = BeautifulSoup(html1, 'html.parser')
    news=soup1.find('div','right_hit_news_box').find_all('a')
    news_10=[]
    for b in news:
        news_10.append(b.get_text())
        news_10.append(b['href'])

    return news_10

def eng():
    #영어 지문
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("window-size=1920x1080")
    options.add_argument("--headless")

    s = Service("c:/py_temp/chromedriver.exe")
    driver = webdriver.Chrome(service=s,options=options)
    url = 'https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english'
    driver.get(url)
    html1 = driver.page_source
    soup1 = BeautifulSoup(html1, 'html.parser')

    eng= soup1.find_all('div','conv_txt')
    return '영어회화 지문',eng[1].get_text(),'한글회화 지문',eng[0].get_text()
 