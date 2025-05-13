import asyncio
from src.utils.logger import get_logger
from src.domain.model.type.image import Image
from src.domain.model.type.page import Page
from src.domain.model.type.template import TemplateType
from src.infrastructure.azureopenai.embedding import generate_embedding
from src.infrastructure.supabase.illustraion import find_similler_image

logger = get_logger("application.gather_similar_images")

async def gather_similar_images(page: Page):
    """
    指定したPageオブジェクトのcontentから埋め込みベクトルを生成し、
    各埋め込みに対してSupabase経由で類似するイラスト検索を非同期で実行する。
    検索結果から、類似するイラストのリストを返す。

    Args:
        page (Page): 類似するイラスト検索対象のページ

    Returns:
        list[Image]: 類似するイラストのリスト
    """
    logger.info("🔍 類似するイラスト検索を開始します")
    
    # 生成した埋め込みをもとに、類似するイラストを検索
    tasks = [
        asyncio.create_task(find_similler_image(idx, embedding))
        for idx, embedding in enumerate(generate_embedding(page.captions))
    ]
    results = await asyncio.gather(*tasks)
    logger.debug(f"result: {results}")

    images: list[tuple[int, Image]] = []
    for res in results:
        # 類似するイラストが見つからない場合はスキップ
        if res is None:
            continue
        images.append(
            (
                res["idx"],
                Image(
                    name=res["data"]["name"],
                    title=res["data"]["title"],
                    caption=res["data"]["caption"],
                    url=res["data"]["url"],
                )
            )
        )
    
    # 順序を元のインデックスに合わせてソート
    sorted_images = [img for _, img in sorted(images, key=lambda x: x[0])]
    logger.info(f"🔍 検索結果: {len(sorted_images)}件の画像が見つかりました")
    return sorted_images

if __name__ == "__main__":

    async def main():
        # デバッグ用: ダミーのPageオブジェクトを作成
        page_image = Page(
            header="テストヘッダー",
            content="テスト用のページコンテンツ",
            template=TemplateType.IMAGE.value,
            captions=["イラスト1のキャプション"]
            )
        page_three_images = Page(
            header="テストヘッダー",
            content="テスト用のページコンテンツ",
            template=TemplateType.THREE_IMAGES.value,
            captions=["イラスト1のキャプション", "イラスト2のキャプション", "イラスト3のキャプション"]
            )
        logger.debug("デバッグ実2行: gather_similar_imagesを呼び出します")
        images = await gather_similar_images(page_image)
        logger.debug("")
        for img in images:
            logger.debug(f"[IMAGE] Image: {img.name}, URL: {img.url}")
        images = await gather_similar_images(page_three_images)
        logger.debug("TemplateType.THREE_IMAGESの実行結果:")
        for idx,img in enumerate(images):
            logger.debug(f"[THREE_IMAGES {idx}] Image: {img.name}, URL: {img.url}")

    asyncio.run(main())
