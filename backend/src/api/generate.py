import os
import uuid

from flask import Blueprint, request, jsonify

from src.domain.model.slides.utils import to_json_compatible
from src.infrastructure.supabase.slide_storage import save_slide
from src.domain.langgraph_workflow.workflow import build_main_graph
from src.domain.model.type.slide import SlideState
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
            logger.error("⛔ タイトルが指定されていません")
            return jsonify({"error": "タイトルが指定されていません"}), 400

        initial_state = SlideState(title=title,)

        # フローの実行
        final_state = graph.invoke(initial_state)
        result_json = to_json_compatible(final_state)

        # Supabaseに保存
        save_slide(
            user_id= os.getenv("USER_ID"),
            session_id=session_id,
            title=title,
            slide_json=result_json["pages"]
        )
        return jsonify({ "session_id": session_id, "preview": result_json["pages"] }), 200


    except Exception as e:
        logger.exception("予期せぬエラーが発生しました")
        return jsonify({"error": str(e)}), 500