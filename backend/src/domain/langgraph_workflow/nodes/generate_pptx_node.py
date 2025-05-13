# domain/langgraph_workflow/nodes/generate_pptx_node.py
import os

from datetime import datetime

from src.utils.logger import get_logger
from src.application.generate_slide import generate_pptx
from src.domain.model.type.slide import SlideState

logger = get_logger("src.domain.langgraph_workflow.nodes.generate_pptx_node")

def generate_pptx_node(state: SlideState) -> dict:
    logger.info("🔧 PowerPoint を生成中...")

    try:
        title = state["title"]
        slides_json = state["slide_json"]

        # 一時ディレクトリを作成
        temp_dir = os.path.join("temp", "pptx")
        os.makedirs(temp_dir, exist_ok=True)

        # 一時ファイルのパスを生成
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_path = os.path.join(temp_dir, f"{title}_{timestamp}.pptx")

        # 実際の生成処理
        pptx_data = generate_pptx(slides_json)

        # 一時ファイルに保存
        with open(temp_path, "wb") as f:
            f.write(pptx_data)

        logger.info(f"✅ 一時ファイルを保存しました: {temp_path}")

        return {"pptx_path": temp_path}
    except KeyError as e:
        logger.error(f"❌ エラー: 必要なキーが存在しません - {e}")
        raise
    except Exception as e:
        logger.error(f"❌ エラー: PowerPoint生成中に問題が発生しました - {e}")
        raise
