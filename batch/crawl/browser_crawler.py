import asyncio
import logging
import os
import re
import random

from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, BrowserContext

from type.Image import ItemImage

# --- 設定 ---
BASE_DOMAIN = "soco-st.com"
BASE_PAGE_URL = "https://soco-st.com/illust/page/"
MAX_DEPTH: int = 1 # クロールの最大深度
MAX_CONCURRENCY: int = 5 # 並列処理の最大数

# --- グローバル変数 ---
visited = set()

def is_valid_path(url: str) -> bool:
    """
    URLが有効かどうかを判定する関数。

    URLのアンカー部分（#以降）をチェックし、特定のキーワード（例: 'keyword'）を含むURLはクロール対象から除外します。
    また、URLのホスト部分がBASE_DOMAINに一致し、パスが整数を含むページURLであれば有効とみなします。
    例: https://soco-st.com/24917 → OK
        https://soco-st.com/24917#keyword_anchor → NG アンカーは対象外
        https://soco-st.com/category/tag → NG

    Args:
        url (str): クロール対象のURL。

    Returns:
        bool: URLが有効な場合はTrue、無効な場合はFalse。
    """
    parsed = urlparse(url)
    return parsed.netloc.endswith(BASE_DOMAIN) and re.fullmatch(r"/\d+/?", parsed.path) and not parsed.fragment


async def crawl_page(html: str, url: str, context: BrowserContext, depth: int = 0, semaphore: asyncio.Semaphore = None) -> list[ItemImage]:
    """
    指定されたHTMLとURLをもとにページをクロールし、画像・タイトル・キャプションを抽出する。

    - ページ内の 'color.png' を含むリンクを画像として抽出。
    - タイトル（h1.post_title）とキャプション（div.post_caption）も取得。
    - URLが未訪問かつ有効な場合のみ再帰的にクロール。
    - depth により再帰の最大深度を制御。
    - `visited` セットでURLの重複クロールを防止（並列処理のため将来的にはasync-safe対応が必要）。
    - `semaphore` により同時リクエスト数を制限。
    - Playwrightの `BrowserContext` を使って各リンクを新しいページで開き、HTMLを取得。

    Args:
        html (str): 対象ページのHTML文字列。
        url (str): 対象ページのURL。
        context (BrowserContext): Playwrightによるブラウザコンテキスト。
        depth (int): 再帰クロールの深さ。MAX_DEPTH以上の場合は再帰しない。
        semaphore (asyncio.Semaphore): 並列アクセス制御用のセマフォ。

    Returns:
        list[dict]: 以下の情報を含む辞書のリスト：
            - title: ページタイトル
            - caption: ページの説明文
            - images: 画像ファイル名（color.pngのみ）
            - png_url: 対応する画像URLのリスト
    """
    items = []

    async with semaphore:
        try:
            logging.debug(f"📌 {url} (depth={depth})")
            soup = BeautifulSoup(html, "html.parser")

            # メタ情報抽出
            title_tag = soup.find("h1", class_="post_title")
            caption_tag = soup.find("div", class_="post_caption")
            image_tags = soup.find_all("a", href=True)

            title = title_tag.get_text(strip=True) if title_tag else None
            caption = caption_tag.get_text(strip=True) if caption_tag else None
            png_url = [
                urljoin(url, a["href"]) for a in image_tags if a["href"].endswith("color.png")
            ]
            image_names = [os.path.basename(urlparse(u).path) for u in png_url]

            if title and caption and image_names:
                items.append(ItemImage(
                    title=title,
                    caption=caption,
                    images=png_url,
                    embedding=[]  # 後工程で埋め込みを付与
                ))
                logging.debug(f"🔍 PNGリンク発見: {png_url}")

            if depth >= MAX_DEPTH:
                logging.debug(f"⏩ 最大深度 {MAX_DEPTH} に達したため、再帰しません: {url}")
                return items

            # 再帰クロール対象URLの収集と visited フィルタ
            ## 最大深度を2以上にする場合はvisitedへの追加をスレッドセーフにする必要がある
            full_urls = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]
            valid_full_urls = []
            for url in full_urls:
                if is_valid_path(url) and url not in visited:
                    visited.add(url)
                    valid_full_urls.append(url)

            # 並列実行のタスク作成
            async def crawl_nested_page(target_url: str) -> list[ItemImage]:
                page = await context.new_page()
                try:
                    await page.goto(target_url, timeout=15000)
                    nested_html = await page.content()
                    nested_items = await crawl_page(
                        nested_html, target_url, context, depth + 1, semaphore
                    )
                    await asyncio.sleep(random.uniform(5.0, 10.0))
                    return nested_items
                except Exception as e:
                    logging.warning(f"⚠️ 再帰クロール失敗 {target_url}: {e}")
                    return []
                finally:
                    await page.close()

            # asyncio.gather で並列にクロール (最大並列数はMAX_CONCURRENCY)
            tasks = [crawl_nested_page(u) for u in valid_full_urls]
            nested_results = await asyncio.gather(*tasks)

            for nested_items in nested_results:
                items.extend(nested_items)

        except Exception as e:
            logging.error(f"❌ クロール失敗 {url}: {e}")

    return items


async def crawl_all_pages() -> list[ItemImage]:
    """
    サイト内のすべてのページをクロールし、結果を収集する関数。

    各ページを順番に取得し、そのページ内で画像やタイトル、キャプションを抽出します。
    再帰的に内部リンクをクロールし、すべてのページの情報をまとめて結果として返します。

    Returns:
        list[ItemPage]: クロールしたすべてのページの情報（crawl_pageの返却値のリスト）。
    """
    semaphore = asyncio.Semaphore(MAX_CONCURRENCY)
    page_num = 1
    results: list[ItemImage] = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        while True:
            page_url = f"{BASE_PAGE_URL}{page_num}"
            logging.info(f"📌 ページ確認中: {page_url}")

            try:
                await page.goto(page_url, timeout=15000)
                html = await page.content()

                if "イラストがありません。" in html:
                    logging.debug("✅ ページにイラストが見つかりません。終了します。")
                    break

                # 1ページ分のクロール（再帰も含める）
                items = await crawl_page(html, page_url, context, depth=0, semaphore=semaphore)
                results.extend(items)

                sleep_sec = random.uniform(1.0, 3.0)
                logging.debug(f"⏸️ 次のページまで {sleep_sec:.2f} 秒待機中...")
                await asyncio.sleep(sleep_sec)

                page_num += 1

            except Exception as e:
                logging.error(f"❌ ページ取得失敗 {page_url}: {e}")
                break

        await page.close()
        await context.close()
        await browser.close()
    return results


if __name__ == "__main__":
    asyncio.run(crawl_all_pages())
