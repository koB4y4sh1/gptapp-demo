from flask import Blueprint, request, send_file
import io

from src.application.generate import generate_ppt
from src.utils.logger import get_logger

logger = get_logger("routes.generate")

bp = Blueprint('generate', __name__, url_prefix='/api')

@bp.route('/generate', methods=['POST'])
def generate():
    try:
        logger.info("リクエスト受信: /generate")
        data = request.get_json()
        logger.debug(f"リクエストデータ: {data}")
        
        ppt_bytes = generate_ppt(data)
        
        logger.info("PPTファイル生成完了")
        return send_file(
            io.BytesIO(ppt_bytes),
            as_attachment=True,
            download_name="generate.pptx",
            mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    except Exception as e:
        logger.exception("エラーが発生しました")
        return {"error": "サーバーエラーが発生しました"}, 500 