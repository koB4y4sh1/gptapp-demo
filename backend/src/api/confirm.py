import os

from flask import Blueprint, request, jsonify, send_file

from src.domain.model.slides.utils import from_json_to_slidestate, to_json_compatible
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
        temp_dir = os.path.join("temp")
        print("================")
        print(os.getcwd())
        logger.info("リクエスト受信: /confirm")
        data = request.get_json()
        logger.debug(f"リクエストデータ: {data}")
        session_id = data.get("session_id")
        logger.debug(f"セッションID: {session_id}")
        
        if not session_id:
            logger.error("⛔ セッションIDが指定されていません")
            return jsonify({ "error": "セッションIDが必要です" }), 400
        
        # Supabaseから状態を取得
        record = get_session_state(
            user_id= os.getenv("USER_ID"),
            session_id=session_id)  
        if not record:
            logger.error(f"⛔セッションが存在しません: {session_id}")
            return jsonify({ "error": "セッションが存在しません" }), 404

        # 前回の状態を復元
        prev_state = {
            "title": record.get("title"),
            "slide": record.get("slide_json"),
            "confirmed": record.get("confirmed")
        }
        logger.debug(f"前回の状態: {prev_state}")

        # 状態の更新
        new_state = from_json_to_slidestate(prev_state)
        new_state.confirmed = True

        # フローの実行
        final_state = to_json_compatible(graph.invoke(new_state))

        pptx_path = final_state.get("pptx_path")
        logger.debug(f"生成されたファイルパス: {pptx_path}")

        # Supabaseに更新
        update_slide(os.getenv("USER_ID"), session_id, final_state["slide"], pptx_path ,final_state["confirmed"])

        if not pptx_path:
            logger.error("❌ PowerPointのパスが生成されていません")
            return jsonify({ "error": "生成に失敗しました" }), 500

        if not os.path.exists(pptx_path):
            logger.error(f"❌ PowerPointファイルが存在しません: {pptx_path}")
            return jsonify({ "error": "生成に失敗しました" }), 500

        logger.info(f"📦 PowerPointファイルを送信: {pptx_path}")
        file_path = os.path.join(os.getcwd(), pptx_path)
        return send_file(
            path_or_file = file_path,
            as_attachment=True,
            download_name=f"{final_state.get('title', 'slide')}.pptx",
            mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )

    except Exception as e:
        logger.exception("🚨 予期せぬエラーが発生しました")
        return jsonify({ "error": str(e) }), 500

if __name__ == "__main__":
    from flask import Flask
    import threading
    import time

    app = Flask(__name__)
    app.register_blueprint(bp)

    def run_server():
        app.run(host="0.0.0.0", port=5002, debug=True, use_reloader=False)

    # サーバを別スレッドで起動
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # サーバ起動待ち
    time.sleep(1)

    try:
        import requests
        # session_id を取得
        session_id = "f7123419-4176-441b-92f6-292ac793e068"

        # /confirm にPOST
        conf_url = "http://127.0.0.1:5002/confirm"
        conf_payload = {"session_id": session_id}
        conf_resp = requests.post(conf_url, json=conf_payload)
        print("----- /confirm レスポンス -----")
        print("Status:", conf_resp.status_code)
        # バイナリ(PPTX)の場合はtextでなくcontent
        if "application/json" in conf_resp.headers.get("Content-Type", ""):
            print("Body:", conf_resp.text)
        else:
            print("Body: (バイナリデータ, 長さ", len(conf_resp.content), ")")
    except Exception as e:
        print("テストリクエスト送信中にエラー:", e)

    # サーバをしばらく生かしておく
    time.sleep(3)
