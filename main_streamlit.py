import datetime

import streamlit as st
from navermap_capture_km import outo_screenshot_km, get_docx, get_pdf
from PIL import Image
from oil_price_celenium import get_oil_price

from io import BytesIO
import os

if not os.path.exists("./output"):
    os.makedirs("./output")

st.header(":world_map:지도:world_map: 와 ⛽휘발유 가격⛽을 한번에!!")
layout = st.columns([1,3])

# 세션 상태 초기화
if 'distance' not in st.session_state:
    st.session_state.distance = None
if 'oil_price' not in st.session_state:
    st.session_state.oil_price = None
if 'start_location' not in st.session_state:
    st.session_state.start_location = '전북대'
if 'end_location' not in st.session_state:
    st.session_state.end_location = ''
if 'waypoints' not in st.session_state:
    st.session_state.waypoints = []
if 'oil_date' not in st.session_state:
    st.session_state.oil_date = datetime.datetime.today() - datetime.timedelta(days=1)
if 'route' not in st.session_state:
    st.session_state.route = None
def main():
    with layout[0]:

        # 왕복조건 체크박스 추가

        # 8/19 왕복 활성화 형태 변경 시도
        ## 기본 형태
        # checkbox = st.checkbox('왕복 활성화', value=True)

        ## 형태 변경 시도 1
        checkbox = st.radio(
            '왕복/편도 선택',
            ("왕복", "편도")
        )

        start_location = st.text_input("출발지를 입력하세요", value=st.session_state.start_location)
        waypoints_count = st.number_input("경유지 수를 입력하세요", min_value=0, max_value=10, step=1, value=1, )




        waypoints = []
        for i in range(waypoints_count):
            waypoint = st.text_input(f"경유지 {i + 1}:world_map:")
            waypoints.append(waypoint)

        if checkbox == '왕복':
            end_location = start_location
            st.markdown(f"<p>도착지 : <span style='font-size:20px;  font-weight:bold; color:blue;'>{start_location}</span></p>", unsafe_allow_html=True)
        else:
            end_location = st.text_input("도착지를 입력하세요")

        # 오일 가격
        oil_date = st.date_input("날짜를 입력하세요", value=datetime.datetime.today() - datetime.timedelta(days=1))
        if oil_date == datetime.datetime.today().date():
            st.markdown("<p style='font-size:14px; color:red;'>오늘의 휘발유 가격은 업데이트 되지 않습니다</p>", unsafe_allow_html=True)
        else:
            button = None
            sy, sm, sd = oil_date.year, oil_date.month, oil_date.day
            if start_location == end_location and len(waypoints) == 0:
                st.markdown("<p style='font-size:14px; color:red;'>경유지를 입력해주세요</p>", unsafe_allow_html=True)

            else:
                button = st.button("실행")


        waypoints_text = []
        for waypoint in waypoints:
            text = f'{waypoint}-'
            waypoints_text.append(text)
        route = f'{start_location}-{" ".join(waypoints_text)}{end_location}'

        st.write('--------')

        st.write('🔧 __파일 설정 변경__ 🔧', )
        color_radio = st.radio(label='강조색을 선택하세요(RGB)', options=['빨간색', '파란색', '검정색'], index=1)

        if color_radio == '빨간색':
            color = '255,0,0'.split(',')
        elif color_radio == '파란색':
            color = '0,0,255'.split(',')
        elif color_radio == '검정색':
            color = '0,0,0'.split(',')

        color = [int(c) for c in color]

        st.session_state.start_location = start_location
        st.session_state.end_location = end_location
        st.session_state.waypoints = waypoints
        st.session_state.oil_date = oil_date

    with layout[1]:
        text1, img_btn1 = st.columns([1.5, 1.5])

        with text1:

            print(st.session_state.start_location)
            print(st.session_state.end_location)
            print(st.session_state.waypoints)


            if oil_date != datetime.datetime.today().date() and st.session_state.end_location is not None:
                if button:
                    if waypoints != []:
                        with st.spinner('지도를 생성중입니다...'):
                            # time.sleep(5)
                            waypoints_text = []
                            for waypoint in waypoints:
                                text = f'{waypoint}-'
                                waypoints_text.append(text)
                            route = f'{start_location}-{" ".join(waypoints_text)}{end_location}'
                            st.markdown(f'<span style="color:rgb{color[0],color[1],color[2]}; font-weight:700">{route}</span>', unsafe_allow_html=True)

                            st.session_state.distance = '255km'
                            # st.session_state.distance = outo_screenshot_km(st.session_state.start_location, st.session_state.end_location, st.session_state.waypoints)

                    else:
                        with st.spinner('지도를 생성중입니다...'):
                            route = f'{start_location}-{end_location}'
                            st.markdown(f'<span style="color:rgb{color[0],color[1],color[2]}; font-weight:700">{route}</span>', unsafe_allow_html=True)
                            st.session_state.distance = '255km'
                            # st.session_state.distance = outo_screenshot_km(st.session_state.start_location, st.session_state.end_location, st.session_state.waypoints)

                    st.session_state.route = route



            if st.session_state.distance is not None:
                st.markdown(
                    f"총 거리 : <span style='color:rgb{color[0], color[1], color[2]}; font-weight:700'>{st.session_state.distance} </span>",
                    unsafe_allow_html=True)
            #
            #     st.markdown(f"총 거리 : <span style='color:rgb{color[0],color[1],color[2]}; font-weight:700'>{st.session_state.distance} km</span>", unsafe_allow_html=True)

        with img_btn1:
            if st.session_state.distance is not None:
                st.download_button(
                    label="지도 이미지 다운로드",
                    data=img2bytes('./output/naver_map.png'),
                    file_name=f'{route}.png',
                    mime='image/png'
                )

        if st.session_state.distance is not None:
            map_img = Image.open('./output/naver_map.png')
            st.image(map_img)

        text2, img_btn2 = st.columns([1.5, 1.5])
        with text2:
            if button:
                with st.spinner('휘발유 가격을 찾는중입니다...'):
                    # st.session_state.oil_price = 1999.99
                    st.session_state.oil_price = get_oil_price(sy, sm, sd).replace(',', '')
                    st.session_state.oil_price = f'{float(st.session_state.oil_price):.0f}'

            if st.session_state.oil_price != None:


                st.markdown(f"<span style='color:rgb{color[0], color[1], color[2]}; font-weight:700'>{st.session_state.oil_date}</span>"
                            f"의 휘발유 가격 : <span style='color:rgb{color[0], color[1], color[2]}; font-weight:700'>{st.session_state.oil_price}</span>원", unsafe_allow_html=True)

        with img_btn2:
            if st.session_state.oil_price is not None:

                st.download_button(
                    label="휘발유 가격 이미지 다운로드",
                    data=img2bytes('./output/oil_price.png'),
                    file_name=f'{oil_date}.png',
                    mime='image/png'
                )

        if st.session_state.oil_price is not None:
            oil_img = Image.open('output/oil_price.png')
            st.image(oil_img)

        btn2, btn3 = st.columns([1.5, 1.5])
        if st.session_state.oil_price is not None and st.session_state.distance is not None:
            with btn2:
                st.download_button(
                    label="docx 파일 다운로드",
                    data=get_docx(st.session_state.start_location, st.session_state.end_location,
                                  st.session_state.waypoints, st.session_state.distance, st.session_state.oil_date,
                                  st.session_state.oil_price, color),
                    file_name=f"여비증빙_{st.session_state.oil_price}_{route}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            with btn3:
                st.download_button(
                    label="PDF 파일 다운로드",
                    data=get_pdf(st.session_state.start_location, st.session_state.end_location,
                                 st.session_state.waypoints, st.session_state.distance, st.session_state.oil_date,
                                 st.session_state.oil_price, color),
                    file_name=f"여비증빙_{st.session_state.oil_price}_{route}.pdf",
                    mime="application/pdf"
                )


def img2bytes(img_path):
    img = Image.open(img_path)  # ----> PIL
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    val = buffer.getvalue()
    return val

if __name__ == '__main__':
    distance, oil_price = None, None
    main()
