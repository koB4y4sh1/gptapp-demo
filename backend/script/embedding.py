# embedding.py
import os
import logging

from openai import AzureOpenAI

# Azure OpenAI APIの設定
client = AzureOpenAI(
    api_version=os.getenv("OPENAI_EMBEDDING_API_VERSION"),
    azure_endpoint=os.getenv("OPENAI_EMBEDDING_ENDPOINT"),
    api_key=os.getenv("OPENAI_EMBEDDING_API_KEY")
)

async def generate_embedding(text: str) -> list:
    """
    Azure OpenAIのtext-embedding-ada-002モデルを使って、テキストの埋め込みを生成します。

    引数:
        text (str): 埋め込みを生成したいテキスト。例えば、タイトルとキャプションの結合。

    戻り値:
        list: 生成された埋め込みベクトル。
    """
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        for item in response.data:
            length = len(item.embedding)
            logging.debug(
                f"data[{item.index}]: length={length}, "
                f"[{item.embedding[0]}, {item.embedding[1]}, "
                f"..., {item.embedding[length-2]}, {item.embedding[length-1]}]"
            )
        embedding = response.data[0].embedding
        logging.info("✅ 埋め込み生成が完了しました。")
        return embedding
    except Exception as e:
        logging.error(f"❌ 埋め込み生成失敗: {e}")
        return []
