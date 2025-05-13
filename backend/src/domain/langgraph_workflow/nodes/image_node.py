
import asyncio
from src.utils.logger import get_logger
from src.application.gather_similar_images import gather_similar_images
from src.domain.model.type.template import TemplateType
from src.domain.model.type.page import Page
from src.domain.model.type.slide import SlideState

logger = get_logger("domain.langgraph_workflow.nodes.image_node")


def image_node(state: SlideState) -> SlideState:
    """
    スライド内容から画像生成プロンプトを抽出し、templateがimage/three_imageの時だけ画像の類似検索を呼び出すノード
    """
    logger.info("🔧 画像を生成中...")

    # ページオブジェクトを作成
    pages: list[Page] = [Page(**page_dict) for page_dict in state["slide_json"].get("pages", [])]
    
    for page in pages:
        print(page.template.value)
        # 画像生成の対象外のページはスキップ
        if page.template.value not in (TemplateType.IMAGE.value, TemplateType.THREE_IMAGES.value):
            continue

        # ページのキャプションをもとに類似する画像を取得
        images = asyncio.run(gather_similar_images(page))

        # imagesをpageのimagesに破壊的に代入
        page.images = [image.url for image in images]

    # 画像パスリストをstateに追加
    new_slide_json = {"pages": [page.model_dump() for page in pages]}
    logger.debug(f"画像パス含むslide_json: {new_slide_json}")
    return {**state, "slide_json": new_slide_json}

if __name__ == "__main__":
    # テスト用のダミーのスライド状態
    slide_state = {
        "title": "テストタイトル",
        # hearing_info:{}
        # layout:{}
        "slide_json": {
            "pages": [
                {
                "header": "Pythonとは",
                "content": "Pythonの概要を説明する",
                "template": TemplateType.TEXT,
                },
                {
                "header": "プログラムの歴史",
                "content": "Pythonの歴史と発展を紹介する",
                "template": TemplateType.IMAGE,
                "images": [],
                "captions": ["説明するイラスト"],
                },
                {
                "header": "活用分野",
                "content": "PythonはWeb開発やデータ分析など様々な分野で使われています。",
                "template": TemplateType.THREE_IMAGES,
                "images": [],
                "captions": ["活用分野を説明するイラスト1", "Pの活用分野を説明するイラスト2", "活用分野を説明するイラスト3"],
                },
                {
                "header": "他言語との比較",
                "content": "以下は主要な言語との比較表です。",
                "template": TemplateType.TABLE,
                "table": [
                    ["言語", "用途", "学習難易度"],
                    ["Python", "汎用", "易しい"],
                    ["Java", "業務アプリ", "中"],
                    ["C++", "システム", "難しい"]
                ]
                },
            ]
        }
    }
    # テスト用のダミーの画像
    result = image_node(slide_state)
    logger.debug(f"実行結果 (slide_state): {result}")
