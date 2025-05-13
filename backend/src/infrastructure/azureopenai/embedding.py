# embedding.py
import os
from src.utils.logger import get_logger
from openai import AzureOpenAI

logger = get_logger("src.infrastructure.supabase.illustraion")

# Azure OpenAI APIの設定
client = AzureOpenAI(
    api_version=os.getenv("OPENAI_EMBEDDING_API_VERSION"),
    azure_endpoint=os.getenv("OPENAI_EMBEDDING_ENDPOINT"),
    api_key=os.getenv("OPENAI_EMBEDDING_API_KEY")
)

def generate_embedding(text: str|list[str]) -> list[tuple[str,str]]:
    """
    Azure OpenAIのtext-embedding-ada-002モデルを使って、テキストの埋め込みを生成します。

    引数:
        text (str|list[str]): 埋め込みを生成したいテキスト。例えば、タイトルとキャプションの結合。

    戻り値:
        list: 生成された埋め込みベクトル。
            - "object": "embedding"
            - "embedding": 埋め込みベクトルは浮動小数点数のリスト
            - "index": リストのインデックス。
    """
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        result= []
        for item in response.data:
            result.append(item.embedding)
            length = len(item.embedding)
            logger.debug(
                f"data[{item.index}]: length={length}, "
                f"[{item.embedding[0]}, {item.embedding[1]}, "
                f"..., {item.embedding[length-2]}, {item.embedding[length-1]}]"
            )

        logger.info("✅ 埋め込み生成が完了しました。")
        return result
    
    except Exception as e:
        logger.error(f"❌ 埋め込み生成失敗: {e}")
        return []

if  __name__ == "__main__":
    text = ["これはテストです。", "今日の天気は?", "手を挙げている人のイラストです。"]
    result = generate_embedding(text)
    logger.debug(f"埋め込みベクトル生成の結果:{result}")