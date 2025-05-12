# main.py
import json
import asyncio
import logging

from aiohttp import ClientSession
from pydantic import TypeAdapter
from dotenv import load_dotenv

load_dotenv()

from browser_crawler import crawl_all_pages
from script.embedding import generate_embedding
from save_supabase import save_to_supabase
from save_local import save_to_json, download_all_images 
from type.Image import ItemImage

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def process_item(image:ItemImage):
    """
    アイテムを処理して埋め込みを生成し、データベースに保存する

    Args:
        item (dict): 処理するアイテム（タイトル、キャプション、画像URLなどを含む）。
    """
    # 埋め込み生成
    embedding = await generate_embedding(image.caption)
    image.set_embedding(embedding)

    # データベースに保存
    await save_to_supabase(image.model_dump())

async def main():
    """
    メイン処理

    ページをクロールし、アイテムを取得し、その後画像のダウンロードとアイテムの処理を行う
    """
    # Webクロール処理
    images:list[ItemImage] = await crawl_all_pages()
    logging.info(f"✅ {len(images)} 件のデータを取得しました。")

    # # JSONファイルに保存
    save_to_json(images)

    # # 画像のダウンロード処理
    async with ClientSession() as session:
        await download_all_images(session, images)

    # output.jsonを読み込む
    with open("output.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    adapter = TypeAdapter(list[ItemImage])
    images = adapter.validate_python(data)

    # アイテムの埋め込み生成と保存処理
    tasks = [process_item(image) for image in images]
    await asyncio.gather(*tasks)

    logging.info("✅ すべての処理が完了しました。")

if __name__ == "__main__":
    asyncio.run(main())
