from typing import Dict, Any
from openai import AzureOpenAI
import os

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
        以下の情報を元に、PowerPoint スライドの構成案を JSON 形式で提案してください。
        必ず指定された形式のJSONを返してください。

        テーマ: {title}

        ヒアリング情報:
        {hearing_info}

        フォーマット:
        {{
            "pages": [
                {{
                    "header": "セクションタイトル",
                    "template": "text",
                    "description": "ページの要点や狙いを簡潔に書いてください"
                }}
            ]
        }}

        注意点:
        - 必ず上記の形式のJSONを返してください
        - 余計な説明やコメントは含めないでください
        - テンプレートは "text" のみ使用してください
        """

    response = client.chat.completions.create(
        model="app-gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    layout = response.choices[0].message.content.strip()

    return {**state, "layout": layout}
