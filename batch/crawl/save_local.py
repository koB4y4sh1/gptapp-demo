# save_local.py
import json
import os
import asyncio
import logging
from aiohttp import ClientSession
from urllib.parse import urlparse

SAVE_FOLDER = "data/image"

def save_to_json(data, filename='output.json'):
    """
    データをJSONファイルとして保存する関数
    """
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            # JSONファイルにデータを追加
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.write("\n")  # 各エントリーを1行で保存
    except Exception as e:
        print(f"Error saving to JSON: {e}")

async def download_png(session: ClientSession, url: str):
    """
    PNGファイルを非同期でダウンロードして保存

    Args:
        session (ClientSession): 非同期セッションオブジェクト。
        url (str): ダウンロード対象のPNG画像のURL。
    """
    try:
        filename = os.path.basename(urlparse(url).path)
        filepath = os.path.join(SAVE_FOLDER, filename)

        if os.path.exists(filepath):
            logging.debug(f"⏩ すでに存在: {filename}")
            return

        logging.debug(f"📥ダウンロード: {url}")
        async with session.get(url) as resp:
            if resp.status == 200:
                os.makedirs(SAVE_FOLDER, exist_ok=True)  # 保存先フォルダがなければ作成
                with open(filepath, "wb") as f:
                    f.write(await resp.read())
                logging.info(f"💾 保存完了: {filename}")
            else:
                logging.warning(f"❌ ダウンロード失敗: {url} (status: {resp.status})")
    except Exception as e:
        logging.error(f"🚨 ダウンロードエラー {url}: {e}")

async def download_all_images(session: ClientSession, items: list):
    """
    すべてのアイテムに関連する画像を非同期でダウンロードする関数

    Args:
        session (ClientSession): 非同期セッションオブジェクト。
        items (list): ダウンロードするアイテムのリスト。
    """
    image_urls = []
    for item in items:
        image_urls.extend(item['png_url'])

    # 重複を排除して一度だけダウンロードする
    image_urls = list(set(image_urls))

    logging.info(f"📌 {len(image_urls)} 個の画像をダウンロード中...")
    download_tasks = [download_png(session, url) for url in image_urls]
    await asyncio.gather(*download_tasks)
