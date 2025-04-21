from typing import Dict, Any
from openai import AzureOpenAI
import os
import json
from src.domain.model.response_format.layout_schema import get_layout_schema
from backend.src.infrastructure.azureopenai.chat import chat_completion

client = AzureOpenAI(
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

def layout_node(state: Dict[str, Any]) -> Dict[str, Any]:
    title = state.get("title")
    hearing_info = state.get("hearing_info")

    if not title or not hearing_info:
        raise ValueError("title または hearing_info が不足しています")

    prompt = f"""
        あなたは資料作成に特化したプレゼン設計のプロです。
        以下の情報を元に、PowerPoint スライドの構成案を作成してください。

        テーマ: {title}
        ヒアリング結果: {json.dumps(hearing_info, ensure_ascii=False, indent=2)}
        
        制約事項：
        - スライドは1枚以上10枚以内で作成してください
        - 各スライドには必ずタイトル、テンプレートタイプ、説明を記載してください
        - テンプレートタイプは"text"のみ使用可能です
        - ヒアリング結果を反映した構成にしてください
    """
    response = chat_completion(
        prompt=prompt, response_format=get_layout_schema()
    )

    try:
        layout = json.loads(response.choices[0].message.content.strip())
        return {**state, "layout": layout}
    except json.JSONDecodeError as e:
        raise ValueError(f"JSONの解析に失敗しました: {e}")
