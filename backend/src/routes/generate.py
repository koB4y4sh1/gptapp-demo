import os

from flask import Blueprint, request, send_file, jsonify

from src.domain.langgraph_workflow.workflow import build_main_graph
from src.utils.logger import get_logger

logger = get_logger("routes.generate")

bp = Blueprint('generate', __name__)
graph = build_main_graph()

@bp.route("/generate", methods=["POST"])
def generate():
    try:
        logger.info("リクエスト受信: /generate")
        data = request.get_json()
        logger.debug(f"リクエストデータ: {data}")
        
        topic = data.get("title")

        if not topic:
            logger.error("タイトルが指定されていません")
            return jsonify({"error": "タイトルが指定されていません"}), 400

        initial_state = {
            "title": topic
        }

        final_state = graph.invoke(initial_state)
        pptx_path = final_state.get("pptx_path")

        if not pptx_path:
            logger.error("PowerPointのパスが生成されていません")
            return jsonify({"error": "PowerPoint の生成に失敗しました"}), 500

        if not os.path.exists(pptx_path):
            logger.error(f"PowerPointファイルが存在しません: {pptx_path}")
            return jsonify({"error": "PowerPoint ファイルが見つかりません"}), 500

        logger.info(f"PowerPointファイルを送信: {pptx_path}")
        
        # ファイルを送信
        response = send_file(
            pptx_path,
            as_attachment=True,
            download_name=f"{topic}.pptx",
            mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )

        # 一時ファイルを削除
        try:
            os.remove(pptx_path)
            logger.info(f"一時ファイルを削除: {pptx_path}")
        except Exception as e:
            logger.warning(f"一時ファイルの削除に失敗: {e}")

        return response

    except Exception as e:
        logger.exception("予期せぬエラーが発生しました")
        return jsonify({"error": str(e)}), 500