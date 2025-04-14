from typing import Dict, Any, List
from openai import AzureOpenAI
import os
import json
from src.domain.model.response_format.slide_creator_schema import get_slide_creator_schema

client = AzureOpenAI(
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

def slide_creator_node(state: Dict[str, Any]) -> Dict[str, Any]:
    title = state.get("title")
    layout = state.get("layout")

    if not title or not layout:
        raise ValueError("title または layout が不足しています")

    prompt = """
        あなたは優れたスライドライターです。
        以下のテーマと構成案に従って、スライド1枚ごとの具体的な内容を作成してください。
        
        制約事項：
        - スライドは1枚以上10枚以内で作成してください
        - 各スライドには必ずタイトル、内容、テンプレートタイプを記載してください
        - テンプレートタイプは"text"のみ使用可能です
        - 内容は簡潔かつ具体的に記載してください
    """

    response = client.chat.completions.create(
        model="app-gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        response_format=get_slide_creator_schema()
    )

    try:
        slide_json = json.loads(response.choices[0].message.content.strip())
        return {**state, "slide_json": slide_json}
    except json.JSONDecodeError as e:
        raise ValueError(f"JSONの解析に失敗しました: {e}")