import asyncio
from src.utils.logger import get_logger
from src.domain.logic.gather_similar_images import gather_similar_images
from src.domain.model.type.template import TemplateType
from src.domain.model.type.page import Page
from src.domain.model.type.slide import SlideState

logger = get_logger(__name__)


async def process_image_pages(pages: list[Page]) -> list[Page]:
    """
    各ページのテンプレート種別に応じて画像検索を行い、該当ページのimages属性を更新する非同期処理。

    Args:
        pages (list[Page]): スライド内のページリスト

    Returns:
        list[Page]: images属性が更新されたページリスト
    """
    # 画像生成対象ページごとに非同期で画像検索タスクを作成
    tasks = [
        gather_similar_images(page) if page.template.value in (TemplateType.IMAGE.value, TemplateType.THREE_IMAGES.value) else None
        for page in pages
    ]
    # 非対象ページはダミータスクで埋め、全タスクを並列実行
    results = await asyncio.gather(*[t if t else asyncio.sleep(0) for t in tasks])
    # 画像検索結果を各ページのimages属性に反映
    for page, images in zip(pages, results):
        if images:
            page.images = [f"data/image/{image.name}" for image in images]
    return pages


def image_node(state: SlideState) -> SlideState:
    """
    スライド状態から各ページのテンプレート種別を判定し、画像生成対象ページに対して
    類似画像検索を実施してimages属性を更新した新たなSlideStateを返すノード。

    Args:
        state (SlideState): 入力スライド状態

    Returns:
        SlideState: images属性が更新された新しいスライド状態
    """
    # 各ページを個別にコピー
    pages = [page.model_copy() for page in state.slide]

    # 各ページのimageを更新
    pages = asyncio.run(process_image_pages(pages))
    logger.debug(f"画像パス含むpages: {pages}")

    # ワークフローの状態の更新
    return state.model_copy(update={"pages": pages})


if __name__ == "__main__":
    # テスト用ダミーデータ作成
    pages = [
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
        pages=pages,
    )
    result = image_node(slide_state)
    logger.debug(f"実行結果 (slide_state): {result}")
