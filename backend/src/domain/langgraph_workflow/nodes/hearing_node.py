from typing import Dict, Any
from openai import AzureOpenAI
import os


# LangChain経由でもよいが、まずはOpenAI直叩き例
client = AzureOpenAI(
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

def hearing_node(state: Dict[str, Any]) -> Dict[str, Any]:
    title = state.get("title")
    if not title:
        raise ValueError("title が存在しません")

    prompt = f"""
あなたは優秀なプレゼン資料作成アシスタントです。
以下のテーマに基づき、どのような内容を伝えるべきかヒアリングの観点で整理してください。

テーマ: {title}

必要な情報:
- 資料の目的
- 読者の対象
- 含めるべき主要な話題や章構成
"""

    response = client.chat.completions.create(
        model="app-gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    hearing_info = response.choices[0].message.content.strip()
    return {**state, "hearing_info": hearing_info}
