import os
import uuid

from flask import Blueprint, request, jsonify

from src.application.slide_storage import save_slide
from src.domain.langgraph_workflow.workflow import build_main_graph
from src.utils.logger import get_logger

logger = get_logger("routes.generate")

bp = Blueprint('generate', __name__)
graph = build_main_graph()
state_store = {}  # セッション状態を保存（本来はRedis/DB推奨）

@bp.route("/generate", methods=["POST"])
def generate():
    try:
        logger.info("リクエスト受信: /generate")
        data = request.get_json()
        logger.debug(f"リクエストデータ: {data}")
        
        title = data.get("title")
        session_id = str(uuid.uuid4())
        if not title:
            logger.error("タイトルが指定されていません")
            return jsonify({"error": "タイトルが指定されていません"}), 400

        initial_state = {
            "title": title,
            "confirmed": False  
        }

        # フローの実行
        final_state = graph.invoke(initial_state)

        # Supabaseに保存
        save_slide(
            user_id= os.getenv("USER_ID"),
            session_id=session_id,
            title=title,
            slide_json=final_state["slide_json"]
        )
        return jsonify({ "session_id": session_id, "preview": "以下の内容でスライドを提案します。" }), 200


    except Exception as e:
        logger.exception("予期せぬエラーが発生しました")
        return jsonify({"error": str(e)}), 500