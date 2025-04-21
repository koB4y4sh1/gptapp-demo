import os

from flask import Blueprint, request, jsonify, send_file

from src.infrastructure.supabase.slide_storage import update_slide
from src.infrastructure.supabase.slide_storage import get_session_state
from src.domain.langgraph_workflow.workflow import build_main_graph
from src.utils.logger import get_logger

bp = Blueprint("confirm", __name__)
graph = build_main_graph()
logger = get_logger("src.routes.confirm")
state_store = {}  # セッション状態を保存（本来はRedis/DB推奨）

@bp.route("/confirm", methods=["POST"])
def confirm_and_continue():
    try:
        logger.info("リクエスト受信: /confirm")
        data = request.get_json()
        logger.debug(f"リクエストデータ: {data}")
        session_id = data.get("session_id")
        logger.debug(f"セッションID: {session_id}")
        
        if not session_id:
            logger.error("セッションIDが指定されていません")
            return jsonify({ "error": "セッションIDが必要です" }), 400
        
        # Supabaseから状態を取得
        record = get_session_state(
            user_id= os.getenv("USER_ID"),
            session_id=session_id)  
        if not record:
            logger.error(f"セッションが存在しません: {session_id}")
            return jsonify({ "error": "セッションが存在しません" }), 404

        prev_state = {
            "title": record.get("title"),
            "slide_json": record.get("slide_json"),
            "confirmed": record.get("confirmed")
        }
        logger.debug(f"前回の状態: {prev_state}")

        new_state = { **prev_state, "confirmed": True }
        final_state = graph.invoke(new_state)

        pptx_path = final_state.get("pptx_path")
        logger.debug(f"生成されたファイルパス: {pptx_path}")

        # Supabaseに更新
        update_slide(os.getenv("USER_ID"), session_id, pptx_path ,final_state["confirmed"])

        if not pptx_path:
            logger.error("PowerPointのパスが生成されていません")
            return jsonify({ "error": "生成に失敗しました" }), 500

        if not os.path.exists(pptx_path):
            logger.error(f"PowerPointファイルが存在しません: {pptx_path}")
            return jsonify({ "error": "生成に失敗しました" }), 500

        logger.info(f"PowerPointファイルを送信: {pptx_path}")
        return send_file(
            pptx_path,
            as_attachment=True,
            download_name=f"{new_state.get('title', 'slide')}.pptx",
            mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )

    except Exception as e:
        logger.exception("予期せぬエラーが発生しました")
        return jsonify({ "error": str(e) }), 500