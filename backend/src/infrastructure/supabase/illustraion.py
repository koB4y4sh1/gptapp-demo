"""
Supabase を利用したイラスト画像の類似検索インターフェースを提供するモジュール。

主な機能:
- 画像の埋め込みベクトル（1536次元）を用いて、Supabase の RPC（find_similar_illustration）を呼び出し、
  類似度の高い画像を検索する非同期関数 find_similler_image を提供する。
- 検索結果は画像のパス等を含む辞書型で返却される。
- ロギング機能により、検索結果やエラー発生時の情報を記録する。

利用例:
    result = await find_similler_image(1, embedding_vector)

注意事項:
- embedding ベクトルは1536次元である必要がある。
- Supabase 側で find_similar_illustration RPC が実装されている必要がある。
"""

import asyncio
from src.utils.logger import get_logger
from src.infrastructure.supabase.client import supabase

logger = get_logger("src.infrastructure.supabase.illustraion")

async def find_similler_image(idx: int, embedding: list[float]) -> dict[str, int|dict]:
    """
    類似度の高い画像を検索し、そのレコードを返す（非同期対応）。

    Args:
        idx (int): 検索対象のインデックスやID（呼び出し元で管理する任意の値）
        embedding (list[float]): 1536次元の画像埋め込みベクトル

    Returns:
        dict[str, str] | None: 
            - 類似画像が見つかった場合は類似画像のレコードを返す。
              - name: 画像のファイル名
              - title: 画像のタイトル
              - caption: 画像の説明
              - url: 画像のURL
            - 類似画像が見つからない、またはエラー発生時は None を返す。

    Raises:
        ValueError: embeddingの長さが1536でない場合

    Note:
        Supabase側で find_similar_illustration RPC が実装されている必要があります。
    """
    try:
        if not embedding or len(embedding) != 1536:
            raise ValueError(f"不正な埋め込みベクトルの長さ (index={idx})")

        # RPC呼び出し（同期APIをスレッドでラップして非同期化）
        response = await asyncio.to_thread(
            lambda: supabase.rpc("find_similar_illustration", {"query_embedding": embedding}).execute()
        )
        if not response.data:
            logger.warning("⚠️ 類似するイラストは見つかりませんでした")
            return None

        logger.debug(f"✅ レスポンス: {response.data[0]}")
        return response.data[0]

    except Exception as e:
        logger.error(f"🚨 類似検索中にエラーが発生しました: {e}")
        return None

if __name__ == "__main__":
    async def main():
        query_embedding = [0.001] * 1536  # 実際は Azure OpenAI から取得したベクトルを使う
        result = await find_similler_image(1, query_embedding)
        print(result)
    asyncio.run(main())
