import os.path
import time

from selenium.webdriver.common.by import By
from PIL import Image

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def get_oil_price(sy, sm, sd):
    chrome_driver_path = "/usr/bin/chromedriver"
    service = Service(chrome_driver_path)
    # 서버에서 selenium을 돌리기 위한 설정
    op = Options()
    op.add_argument('--headless=new')
    op.add_argument('--window-size=1920,3000')
    op.add_argument('--no-sandbox')
    op.add_argument('--disable-dev-shm-usage')
    op.add_argument("--disable-gpu")
    op.add_argument("--disable-software-rasterizer")
    op.add_argument('lang=ko_KR')

    op.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0")

    try:
        driver = webdriver.Chrome(service=service, options=op)
    except:
        driver = webdriver.Chrome(options=op)

    url = 'https://www.opinet.co.kr/user/dopospdrg/dopOsPdrgSelect.do'

    # ================================ 설정 완료 ===============================
    try:
        driver.get(url)
        # driver.maximize_window()    # start_year

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

        # time.sleep(1)
        #
        # btn_search = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.ID, 'btn_search'))
        # )
        # btn_search.click()

        wait = WebDriverWait(driver, 10)

        btn = wait.until(EC.presence_of_element_located((By.ID, "btn_search")))

        driver.execute_script("""
        arguments[0].scrollIntoView({block:'center'});
        arguments[0].click();
        """, btn)

        time.sleep(1)

        if not os.path.exists("./output"):
            os.makedirs("./output")

        driver.save_screenshot("./static/output/oil_price.png")

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

        image = Image.open('static/output/oil_price.png')

        element_screenshot = image.crop((content_left, header_top, content_right, content_bottom))
        element_screenshot.save('./static/output/oil_price.png')

        oil_price = driver.find_element(By.XPATH, '//*[@id="numbox"]/tr[2]/td[3]')

        print(f'\n{sy}-{sm}-{sd}의 휘발류 가격 : {oil_price.text}')
        return oil_price.text

    except Exception as e:
        driver.quit()
        raise RuntimeError(f"oil price selenium error: {e}")

