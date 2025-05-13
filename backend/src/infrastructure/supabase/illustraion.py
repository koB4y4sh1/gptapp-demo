import asyncio
from src.utils.logger import get_logger
from src.infrastructure.supabase.client import supabase

logger = get_logger("src.infrastructure.supabase.illustraion")

async def find_similler_image(idx: int, embedding: list[float]) -> dict[str, int|dict]:
    """
    類似度の高い画像を検索し、そのパスを返す（非同期対応）
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
        return {"idx": idx, "data": response.data[0]}

    except Exception as e:
        logger.error(f"🚨 類似検索中にエラーが発生しました: {e}")
        return None

if __name__ == "__main__":
    async def main():
        query_embedding = [0.001] * 1536  # 実際は Azure OpenAI から取得したベクトルを使う
        result = await find_similler_image(1, query_embedding)
        print(result)
    asyncio.run(main())
