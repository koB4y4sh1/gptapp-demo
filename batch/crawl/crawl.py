# crawl.py
import os
import re

import aiohttp
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE_DOMAIN = "soco-st.com"
BASE_PAGE_URL = "https://soco-st.com/illust/page/"
visited = set()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://soco-st.com/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
}
cookies = {
    '__gads': 'ID=e8f2d75d9e318889:T=1721132071:RT=1746902449:S=ALNI_MY7G9MMtaRa3JLbO-Sjbp7AnsZJPA',
    '__gpi': 'UID=00000e94dc820350:T=1721132071:RT=1746902449:S=ALNI_MapxzGalrCgeDDs2cnx_yG94yJMVQ',
    '_ga': 'GA1.1.1861132468.1745496132',
    '_ga_4GPZ9EMKV6': 'GS2.1.s1746900063$o6$g1$t1746902706$j60$l0$h0',
    'FCNEC': '%5B%5B%22AKsRol8_qa5tTarz2UwEp7wPQNBfxbMzAQiwNj7sEhEcy1ZhfO8LlY2xjOgVYQQocFM7yxoRMHck5-tMM2EIMVUjag0dHV35IQ9WKAQYjVbudNo4PhyesjJbOvGvru-eojkDb0qOjJ7gOsyWVQCNthE3s4Cxe66Q0g%3D%3D%22%5D%5D',
    '__eoi': 'ID=255eaa90779dcec3:T=1745496132:RT=1746902449:S=AA-AfjaNwDHDExnov8bEemTibTL6',
}

def is_valid_path(url: str) -> bool:
    """
    URLが有効かどうかを判定する関数。

    URLのホスト部分がBASE_DOMAINに一致し、パスが整数を含むページURLであれば有効とみなします。
    例: https://soco-st.com/24917 → OK
        https://soco-st.com/24917#keyword_anchor → OK アンカーはurlparseで自動的に除外されてしまうため検出不可
        https://soco-st.com/category/tag → NG

    Args:
        url (str): クロール対象のURL。

    Returns:
        bool: URLが有効な場合はTrue、無効な場合はFalse。
    """
    parsed = urlparse(url)
    return parsed.netloc.endswith(BASE_DOMAIN) and re.fullmatch(r"/\d+/?", parsed.path)

async def crawl_page(session, url):
    if url in visited:
        return []
    visited.add(url)
    logging.debug(f"📌 クロール中: {url}")
    items = []

    try:
        async with session.get(url) as resp:
            if resp.status != 200:
                return []
            soup = BeautifulSoup(await resp.text(), "html.parser")
            title_tag = soup.find("h1", class_="post_title")
            caption_tag = soup.find("div", class_="post_caption")
            image_tags = soup.find_all("a", href=True)
            title = title_tag.get_text(strip=True) if title_tag else None
            caption = caption_tag.get_text(strip=True) if caption_tag else None
            images_url = [
                urljoin(url, a["href"]) for a in image_tags if a["href"].endswith("color.png")
            ]
            image_names = [os.path.basename(urlparse(u).path) for u in images_url]

            if title and caption and image_names:
                logging.debug(f"🔍 PNGリンク発見: {images_url}")
                items.append({"title": title, "caption": caption, "images": image_names,"png_url":images_url})

            for a in soup.find_all("a", href=True):
                full_url = urljoin(url, a["href"])
                if is_valid_path(full_url) and full_url not in visited:

                    await crawl_page(session, full_url)
    except Exception as e:
        logging.error(f"❌ クロール失敗 {url}: {e}")
    return items


async def crawl_all_pages():
    results = []
    async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
        page_num = 2
        while True:
            page_url = f"{BASE_PAGE_URL}{page_num}"
            logging.info(f"📌 ページ確認中: {page_url}")
            try:
                async with session.get(page_url) as res:
                    html = await res.text()
                    if "イラストがありません。" in html:
                        break
                items = await crawl_page(session, page_url)
                results.extend(items)
                page_num += 1
            except Exception as e:
                logging.error(f"❌ ページ取得失敗: {e}")
                break
    return results
