import io
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from docx import Document
from docx.shared import Inches
from docx.shared import RGBColor

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from PIL import Image


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# chrome_driver_path = "/usr/bin/chromedriver"
# service = Service(chrome_driver_path)

def outo_screenshot_km(start_location, end_location, waypoints):
    chrome_driver_path = "/usr/bin/chromedriver"
    service = Service(chrome_driver_path)

    op = Options()
    # op.add_argument('headless')
    op.add_argument("--headless=new")
    op.add_argument("--disable-gpu")
    op.add_argument("--disable-software-rasterizer")
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-dev-shm-usage")

    op.add_argument('window-size=1920x1080')
    op.add_argument('--no-sandbox')
    op.add_argument('--disable-dev-shm-usage')
    # op.add_argument("disable-gpu")
    op.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0")
    op.add_argument('lang=ko_KR')

    try:
        browser = webdriver.Chrome(service=service, options=op)
    except:
        browser = webdriver.Chrome(options=op)

    url = 'https://map.naver.com/p?c=15.00,0,0,0,dh'
    try:
        browser.get(url)

        browser.maximize_window()

        side_var_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class, 'btn_navbar')])[2]"))
        )
        side_var_button.click()

        car_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class, 'btn_search_tab')])[2]"))
        )
        car_button.click()

        # if len(waypoints) != 0:
        #     for i in range(len(waypoints)):
        #         print(i, waypoints[i])
        #         waypoints_search = WebDriverWait(browser, 10).until(
        #             EC.element_to_be_clickable((By.CSS_SELECTOR,'.search_btn_area button:nth-of-type(2)'))
        #         )
        #         waypoints_search.click()
        #         print(waypoints[i])
        #
        #     search_via = browser.find_elements(By.CSS_SELECTOR, "div.search_input_box_wrap.via input.input_search")
        #     search = browser.find_elements(By.CLASS_NAME, "input.input_search")
        #
        #     print()
        #
        #     for idx, waypoint in enumerate(waypoints):
        #         print(idx)
        #         search_via[idx].send_keys(waypoint)
        #         time.sleep(2)
        #         search_via[idx].send_keys(Keys.RETURN)
        #         print(waypoint, '입력완')
        #
        #     search[-1].send_keys(f"{end_location}")
        #     time.sleep(1.5)
        #     search[-1].send_keys(Keys.RETURN)
        # 출발지 입력
        start_input = browser.find_element(By.CSS_SELECTOR, "div.search_input_box_wrap.start input.input_search")
        start_input.clear()
        start_input.send_keys(start_location)
        time.sleep(1)
        start_input.send_keys(Keys.RETURN)
        time.sleep(1)

        # 경유지 입력
        for idx, waypoint in enumerate(waypoints):
            # 경유지 input이 부족하면 버튼 클릭
            via_inputs = browser.find_elements(By.CSS_SELECTOR, "div.search_input_box_wrap.via input.input_search")
            if idx >= len(via_inputs):
                add_waypoint_btn = browser.find_element(By.CSS_SELECTOR, ".search_btn_area button:nth-of-type(2)")
                add_waypoint_btn.click()
                time.sleep(1)
                via_inputs = browser.find_elements(By.CSS_SELECTOR, "div.search_input_box_wrap.via input.input_search")

            via_inputs[idx].clear()
            via_inputs[idx].send_keys(waypoint)
            time.sleep(1)
            via_inputs[idx].send_keys(Keys.RETURN)
            time.sleep(1)

        # 도착지 입력
        goal_input = browser.find_element(By.CSS_SELECTOR, "div.search_input_box_wrap.goal input.input_search")
        goal_input.clear()
        goal_input.send_keys(end_location)
        time.sleep(1)
        goal_input.send_keys(Keys.RETURN)
        time.sleep(1)

        # else:
        search = browser.find_elements(By.CLASS_NAME, "input_search")
        print(len(search))
        search[1].send_keys(f"{end_location}")
        time.sleep(1.5)
        search[1].send_keys(Keys.RETURN)

        print(search)
        search[0].send_keys(f"{start_location}")
        time.sleep(2)
        search[0].send_keys(Keys.RETURN)

        time.sleep(1.5)

        road_search = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH,'//*[@id="section_content"]/div/div[1]/div[2]/button[3]'))
        )
        road_search.click()

        time.sleep(5)

        text = browser.page_source
        try:
            route_elem = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "route_summary_info_duration"))
            )
            distance_elem = route_elem.find_element(By.CLASS_NAME, "item_distance")
            distance = distance_elem.text
        except:
            distance = None
        # distance = distance_between_locations.text

        time.sleep(1)

        map_img = browser.find_element(By.XPATH, '//*[@id="app-layout"]')
        map_img.screenshot('./static/output/naver_map.png')

        return distance
    except Exception as e:
        browser.quit()
        raise RuntimeError(f"oil price selenium error: {e}")



def get_docx(start_location, end_location, waypoints, distance, oil_date, oil_price, color):
    doc = Document()

    title = doc.add_paragraph()
    run = title.add_run('[여비증빙]')

    if waypoints != []:
        waypoints_text = []
        for waypoint in waypoints:
            text = f'{waypoint} ->'
            waypoints_text.append(text)
        run_route = doc.add_paragraph()
        route_text = run_route.add_run(f'{start_location} -> {" ".join(waypoints_text)} {end_location}')
        route_text.bold = True
        route_text.font.color.rgb = RGBColor(color[0], color[1], color[2])

        para_distance = doc.add_paragraph(f'총 거리 : ')
        distance_text = para_distance.add_run(distance)
        distance_text.bold = True
        distance_text.font.color.rgb = RGBColor(color[0], color[1], color[2])
        #para_distance.add_run('km')

    else:
        run_route = doc.add_paragraph()
        route_text = run_route.add_run(f'{start_location} -> {end_location}')
        route_text.bold = True
        route_text.font.color.rgb = RGBColor(color[0], color[1], color[2])

        para_distance = doc.add_paragraph(f'총 거리 : ')
        distance_text = para_distance.add_run(distance)
        distance_text.bold = True
        distance_text.font.color.rgb = RGBColor(color[0], color[1], color[2])

    image_path = './static/output/naver_map.png'
    doc.add_picture(image_path, width=Inches(5.0))

    para_oilprice = doc.add_paragraph()
    oildate_text = para_oilprice.add_run(str(oil_date))   # ---------> oil_date
    oildate_text.bold = True
    oildate_text.font.color.rgb = RGBColor(color[0], color[1], color[2])
    para_oilprice.add_run('의 휘발유 가격 : ')
    oilprice_text = para_oilprice.add_run(oil_price) # ---------> oil_price
    oilprice_text.bold = True
    oilprice_text.font.color.rgb = RGBColor(color[0], color[1], color[2])
    para_oilprice.add_run('원')

    image_path_oil = './static/output/oil_price.png'
    doc.add_picture(image_path_oil, width=Inches(5.0))

    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()


def get_pdf(start_location, end_location, waypoints, distance, oil_date, oil_price, color):
    # PDF 파일을 메모리 버퍼에 저장합니다.
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setFillColorRGB(color[0], color[1], color[2]) # RGB 색상을 설정합니다.
    font_path = "static/data/malgun.ttf"
    pdfmetrics.registerFont(TTFont("맑은고딕", font_path))
    pdfmetrics.registerFont(TTFont("맑은고딕-Bold", "static/data/malgunbd.ttf"))  # 볼드체 폰트 등록

    pdf.setFont("맑은고딕", 12)
    pdf.setFillColorRGB(0, 0, 0)
    pdf.drawString(50, 810, "[여비증빙]")

    pdf.setFont("맑은고딕-Bold", 12)
    pdf.setFillColorRGB(color[0], color[1], color[2]) # RGB 색상을 설정합니다.

    x_position = 50
    y_position = 780

    if waypoints != []:
        waypoints_text = []
        for waypoint in waypoints:
            text = f'{waypoint} ->'
            waypoints_text.append(text)

        pdf.drawString(50, y_position, f'{start_location} -> {" ".join(waypoints_text)} {end_location}')
        y_position -= 12*2.4

        pdf.setFont("맑은고딕", 12)
        pdf.setFillColorRGB(0,0,0)  # 검정
        pdf.drawString(50, y_position, f'총 거리 : ', )

        pdf.setFont("맑은고딕-Bold", 12)
        pdf.setFillColorRGB(color[0], color[1], color[2])  # RGB 색상을 설정합니다.
        pdf.drawString(100, y_position, f'{distance}')
        y_position -= 12*1.2

    else:
        pdf.drawString(50, y_position, f'{start_location} -> {end_location}')
        y_position -= 12*2.4

        pdf.setFont("맑은고딕", 12)
        pdf.setFillColorRGB(0,0,0)  # 검정
        pdf.drawString(50, y_position, f'총 거리 : ', )

        pdf.setFont("맑은고딕-Bold", 12)
        pdf.setFillColorRGB(color[0], color[1], color[2])  # RGB 색상을 설정합니다.
        pdf.drawString(100, y_position, f'{distance}')
        y_position -= 12 * 1.2


    ratio = get_image_ratio('./static/output/naver_map.png')
    img_width = 500
    y_position -= img_width/ratio
    pdf.drawImage('./static/output/naver_map.png', 50, y_position, img_width, img_width/ratio)

    # 2번째 페이지 시작

    y_position -= 12 * 2.0  # 간격 확보

    # ⛽ 유가 정보 (같은 페이지)
    pdf.setFont("맑은고딕-Bold", 12)
    pdf.setFillColorRGB(color[0], color[1], color[2])
    pdf.drawString(50, y_position, f'{oil_date}')

    text_width = pdf.stringWidth(f'{oil_date}')
    pdf.setFont("맑은고딕", 12)
    pdf.setFillColorRGB(0, 0, 0)
    pdf.drawString(50 + text_width, y_position, '의 휘발유 가격 : ')

    text_width2 = pdf.stringWidth('의 휘발유 가격 : ')
    pdf.setFont("맑은고딕-Bold", 12)
    pdf.setFillColorRGB(color[0], color[1], color[2])
    pdf.drawString(50 + text_width + text_width2, y_position, f'{oil_price}원')

    # 유가 그래프 이미지
    y_position -= 12 * 1.5
    ratio = get_image_ratio('./static/output/oil_price.png')
    img_width = 420
    y_position -= img_width / ratio
    pdf.drawImage('./static/output/oil_price.png', 50, y_position, img_width, img_width / ratio)

    pdf.save()

    # Save PDF to a file
    with open('./static/output/navermap_oilprice.pdf', 'wb') as f:
        f.write(buffer.getvalue())

    buffer.seek(0)
    return buffer


def get_image_ratio(image_path):
    # 이미지를 열어 너비와 높이를 가져옵니다.
    with Image.open(image_path) as img:
        width, height = img.size

    # 비율을 계산합니다.
    ratio = width / height
    return ratio
