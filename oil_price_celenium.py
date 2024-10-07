import os.path
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from PIL import Image

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select

chrome_driver_path = "/usr/bin/chromedriver"
service = Service(chrome_driver_path)

def get_oil_price(sy, sm, sd):

    op = Options()
    op.add_argument('headless')
    op.add_argument('window-size=1920x1080')
    op.add_argument('--no-sandbox')
    op.add_argument('--disable-dev-shm-usage')

    op.add_argument("disable-gpu")
    op.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0")
    op.add_argument('lang=ko_KR')

    try:
        driver = webdriver.Chrome(service=service, options=op)
    except:
        driver = webdriver.Chrome(options=op)

    url = 'https://www.opinet.co.kr/user/dopospdrg/dopOsPdrgSelect.do'

    driver.get(url)
    driver.maximize_window()    # start_year

    select_sy = Select(driver.find_element(By.ID, 'STA_Y'))
    select_sy.select_by_value(str(sy))

    select_sm = Select(driver.find_element(By.ID, 'STA_M'))
    select_sm.select_by_value(f'{sm:02d}')

    select_sd = Select(driver.find_element(By.ID, 'STA_D'))
    select_sd.select_by_value(f'{sd:02d}')

    select_ey = Select(driver.find_element(By.ID, 'END_Y'))
    select_ey.select_by_value(str(sy))

    select_em = Select(driver.find_element(By.ID, 'END_M'))
    select_em.select_by_value(f'{sm:02d}')

    select_ed = Select(driver.find_element(By.ID, 'END_D'))
    select_ed.select_by_value(f'{sd:02d}')

    time.sleep(1)

    btn_search = driver.find_element(By.ID, 'btn_search')
    btn_search.click()

    time.sleep(1)

    if not os.path.exists("./output"):
        os.makedirs("./output")

    driver.save_screenshot("./output/oil_price.png")

    cut_header = driver.find_element(By.ID, 'header')
    header_location = cut_header.location
    header_size = cut_header.size
    header_left = header_location['x']
    header_top = header_location['y']
    header_right = header_left + header_size['width']
    header_bottom = header_top + header_size['height']

    cut_headerpath = driver.find_element(By.CLASS_NAME, 'header_path')
    headerpath_location = cut_headerpath.location
    headerpath_size = cut_headerpath.size
    headerpath_left = headerpath_location['x']
    headerpath_top = headerpath_location['y']
    headerpath_right = headerpath_left + headerpath_size['width']
    headerpath_bottom = headerpath_top + headerpath_size['height']


    cut_content = driver.find_element(By.CLASS_NAME, 'content')
    content_location = cut_content.location
    content_size = cut_content.size
    content_left = content_location['x']
    content_top = content_location['y']
    content_right = content_left + content_size['width']
    content_bottom = content_top + content_size['height']

    image = Image.open('output/oil_price.png')

    element_screenshot = image.crop((content_left, header_top, content_right, content_bottom))
    element_screenshot.save('./output/oil_price.png')

    oil_price = driver.find_element(By.XPATH, '//*[@id="numbox"]/tr[2]/td[3]')

    print(f'\n{sy}-{sm}-{sd}의 휘발류 가격 : {oil_price.text}')
    return oil_price.text
def main():
    # start_year, start_month, start_day = input("시작 일자(YYYY-mm-dd)를 입력하세요 : ").split('-')
    # end_year, end_month, end_day = input("종료 일자(YYYY-mm-dd)를 입력하세요 : ").split('-')

    start_year, start_month, start_day = input('날짜를 입력하시오(YYYY-mm-dd) : ').split('-')
    end_year, end_month, end_day = start_year, start_month, start_day

    get_oil_price(start_year, start_month, start_day)

if __name__ == '__main__':
    main()