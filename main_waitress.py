from flask import Flask, request, jsonify
import threading
from flask import send_from_directory

from navermap_capture_km import outo_screenshot_km, get_docx, get_pdf
from oil_price_celenium import get_oil_price
import psutil
import os
app = Flask(__name__)

# =========================
# Selenium 동시 실행 방지용 Lock
# =========================
selenium_lock = threading.Lock()

# =========================
# Health Check
# =========================
# @app.route("/", methods=["GET"])
# def health():
#     return "OK", 200

@app.route("/")
def index():
    return send_from_directory("static", "index.html")
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(
        "static/output",
        filename,
        as_attachment=True,          # 다운로드용 헤더
        mimetype="application/pdf"   # PDF이면 PDF MIME
    )

# =========================
# Selenium 실행 엔드포인트
# =========================
@app.route("/run", methods=["POST"])
def run_selenium():
    # 🔒 이미 실행 중이면 바로 거절
    if selenium_lock.locked():
        return jsonify({
            "status": "busy",
            "message": "다른 작업이 실행 중입니다. 잠시 후 다시 시도하세요."
        }), 429

    data = request.get_json(force=True)

    start_location = data.get("start")
    end_location = data.get("end")
    waypoints = data.get("waypoints", [])

    sy = int(data["date"][0])
    sm = int(data["date"][1])
    sd = int(data["date"][2])
    log_memory("BEFORE")

    try:
        with selenium_lock:
            log_memory("AFTER LOCK")

            # =========================
            # 1️⃣ 네이버 지도 거리 계산
            # =========================
            distance = outo_screenshot_km(
                start_location=start_location,
                end_location=end_location,
                waypoints=waypoints
            )

            # =========================
            # 2️⃣ 유가 조회
            # =========================
            oil_price = get_oil_price(sy, sm, sd)

            oil_date = f'{sy}-{sm}-{sd}'
            print(f"""
            start_location: {start_location}, end_location: {end_location}
            """)
            docx_buffer = get_docx(start_location, end_location, waypoints, distance, oil_date, oil_price, color=[0,0,0])
            with open("./static/output/navermap_oilprice.docx", "wb") as f:
                f.write(docx_buffer)

            pdf_buffer = get_pdf(start_location, end_location, waypoints, distance, oil_date, oil_price, color=[0,0,0])
            # with open("./static/output/navermap_oilprice.pdf", "wb") as f:
            #     f.write(pdf_buffer.getvalue())

            log_memory("AFTER SELENIUM")
        log_memory("AFTER RELEASE")

        return jsonify({
            "status": "success",
            "distance": distance,
            "oil_price": oil_price
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
def log_memory(tag):
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / 1024 / 1024
    print(f"[MEMORY] {tag}: {mem:.2f} MB")

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )