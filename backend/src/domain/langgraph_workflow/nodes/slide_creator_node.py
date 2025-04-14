from typing import Dict, Any
from openai import AzureOpenAI
import os
import json

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

    try:
        layout_json = json.loads(layout)  # layoutはJSON文字列で来る想定
    except json.JSONDecodeError as e:
        raise ValueError("layoutのJSONが不正です") from e

    prompt = f"""
        あなたは優れたスライドライターです。
        以下のテーマと構成案に従って、スライド1枚ごとの具体的な内容を JSON で作成してください。

        テーマ: {title}

        構成案:
        {json.dumps(layout_json, ensure_ascii=False, indent=2)}

        各スライドには以下の形式を使用してください：
        {{
        "pages": [
            {{
            "header": "スライドタイトル",
            "content": "このスライドに記載する説明文",
            "template": "text | image | table | two_column | three_images | three_horizontal_flow",
            "images": ["image1.png", "image2.png"], // image系テンプレートの場合のみ
            "table": [["列1", "列2"], ["データ1", "データ2"]] // tableテンプレートのみ
            }}
        ]
        }}
        """

    response = client.chat.completions.create(
        model="app-gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    slide_json = response.choices[0].message.content.strip()

    return {**state, "slide_json": slide_json}