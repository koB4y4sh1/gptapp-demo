# domain/langgraph_workflow/nodes/generate_pptx_node.py
import os

from datetime import datetime

from src.domain.model.type.page import Page
from src.utils.logger import get_logger
from src.domain.logic.generate_slide import generate_pptx
from src.domain.model.type.slide import SlideState

logger = get_logger(__name__)

def generate_pptx_node(state: SlideState) -> dict:
    """
    SlideStateからPPTXファイルを生成し、一時ファイルパスを返すノード

    Args:
        state (SlideState): スライド生成ワークフローの状態

    Returns:
        dict: {"pptx_path": 一時ファイルパス}

    Raises:
        KeyError, Exception: 必要な情報が不足している場合や生成失敗時
    """
    logger.info("🔧 PowerPoint を生成中...")

    try:
        title = state.title
        slide = state.slide

        # ファイル名用にtitleをサニタイズ
        safe_title = "".join(c for c in title if c.isalnum() or c in ("_", "-")).rstrip()
        if not safe_title:
            safe_title = "slide"

        # 一時ディレクトリを作成
        temp_dir = os.path.join("temp")
        os.makedirs(temp_dir, exist_ok=True)

        # 一時ファイルのパスを生成
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_path = os.path.join(temp_dir, f"{safe_title}_{timestamp}.pptx")

        # 実際の生成処理
        pptx_data = generate_pptx(slide)

        # 一時ファイルに保存
        with open(temp_path, "wb") as f:
            f.write(pptx_data)

        logger.info(f"✅ 一時ファイルを保存しました: {temp_path}")

        return state.model_copy(update={"pptx_path": temp_path})
    except KeyError as e:
        logger.error(f"❌ エラー: 必要なキーが存在しません - {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"❌ エラー: PowerPoint生成中に問題が発生しました - {e}", exc_info=True)
        raise

if __name__ == "__main__":
    from src.domain.model.type.template import TemplateType
    # テスト用ダミーデータ作成
    slide = [
        Page(
            header="Pythonとは",
            content="Pythonの概要を説明する",
            template=TemplateType.TEXT
        ),
        Page(
            header="プログラムの歴史",
            content="Pythonの歴史と発展を紹介する",
            template=TemplateType.IMAGE,
            images=[],
            captions=["説明するイラスト"]
        ),
        Page(
            header="活用分野",
            content="PythonはWeb開発やデータ分析など様々な分野で使われています。",
            template=TemplateType.THREE_IMAGES,
            images=[],
            captions=["Pythonについてのイラスト", "スマートデバイスを操作するイラスト", "説明するイラスト"]
        ),
        Page(
            header="他言語との比較",
            content="以下は主要な言語との比較表です。",
            template=TemplateType.TABLE,
            table=[
                ["言語", "用途", "学習難易度"],
                ["Python", "汎用", "易しい"],
                ["Java", "業務アプリ", "中"],
                ["C++", "システム", "難しい"]
            ]
        ),
    ]

    slide_state = SlideState(
        title="テストタイトル",
        slide=slide,
    )
    result = generate_pptx_node(slide_state)
    logger.debug(f"実行結果 (slide_state): {result}")
