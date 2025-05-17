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
        final_state = to_json_compatible(graph.invoke(initial_state))
        # Supabaseに保存
        save_slide(
            user_id= os.getenv("USER_ID"),
            session_id=session_id,
            title=title,
            slide_json=final_state["slide"]
        )
        return jsonify({ "session_id": session_id, "preview": final_state["slide"] }), 200


    except Exception as e:
        logger.exception("予期せぬエラーが発生しました")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    from flask import Flask
    import threading
    import time

    app = Flask(__name__)
    app.register_blueprint(bp)

    def run_server():
        app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)

    # サーバを別スレッドで起動
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # サーバ起動待ち
    time.sleep(1)

    # テストリクエスト送信
    try:
        import requests
        url = "http://127.0.0.1:5001/generate"
        payload = {"title": "デバッグ用テストタイトル"}
        response = requests.post(url, json=payload)
        print("----- /generate レスポンス -----")
        print("Status:", response.status_code)
        print("Body:", response.text)
    except Exception as e:
        print("テストリクエスト送信中にエラー:", e)

    # サーバをしばらく生かしておく
    time.sleep(3)
