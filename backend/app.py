import io

from flask import Flask, request, send_file
from flask_cors import CORS

from src.application.generate import generate_ppt
from backend.src.utils.logger import get_logger

logger = get_logger("app")

app = Flask(__name__)
# CORS(app, origins=["http://localhost:5173"],  allow_headers=["Content-Type"])
CORS(app)

logger.debug("DEBUGログ: 開発者向けの詳細情報")
logger.info("INFOログ: アプリ起動しました 🚀")

@app.route('/generate', methods=['POST'])
def generate():
    try:
        logger.info("INFOログ: generate 🚀")
        data:dict = request.get_json()
        ppt_bytes = generate_ppt(data)
        return send_file(
            io.BytesIO(ppt_bytes),
            as_attachment=True,
            download_name="generate.pptx",
            mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    except Exception as e:
        logger.exception("エラーが発生しました")
        return {"error": "サーバーエラーが発生しました"}, 500

if __name__ == '__main__':
    app.run(debug=True)