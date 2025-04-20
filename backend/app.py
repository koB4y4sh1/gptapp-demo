from flask import Flask
from flask_cors import CORS

from src.utils.logger import get_logger
from src.routes.generate import bp as generate_bp
from src.routes.confirm import bp as confirm_bp

logger = get_logger("app")

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Blueprintの登録
    app.register_blueprint(generate_bp)
    app.register_blueprint(confirm_bp)
    
    logger.debug("DEBUGログ: 開発者向けの詳細情報")
    logger.info("INFOログ: アプリ起動しました 🚀")
    # そのほかの設定を記載する
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)