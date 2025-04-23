from typing import Dict, Any, List
from openai import AzureOpenAI
import os
import json
from src.domain.model.response_format.slide_creator_schema import get_slide_creator_schema
from src.utils.logger import get_logger

logger = get_logger("domain.langgraph_workflow.nodes.hearing_node")

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

    prompt = f"""
        あなたは優れたスライドライターです。
        以下のテーマと構成案に従って、スライド1枚ごとの具体的な内容を作成してください。

        テーマ: {title}
        構成案: {json.dumps(layout, ensure_ascii=False, indent=2)}
        
        制約事項：
        - スライドは1枚以上10枚以内で作成してください
        - 各スライドには必ず「タイトル（header）」「内容（content）」「テンプレートタイプ（template）」「images（画像URLリスト。初期値は空リスト[]でOK）」を含めてください
        - imagesは将来的に画像生成APIで埋めるため、現時点では空リスト[]で出力してください
        - テンプレートタイプは"text"以外も将来的に拡張される可能性があるため、構成案に従って適切な値を設定してください
        - 内容は簡潔かつ具体的に記載してください
        - 構成案に沿った内容であることを確認してください
    """

    response = client.chat.completions.create(
        model="app-gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        response_format=get_slide_creator_schema()
    )

    try:
        slide_json = json.loads(response.choices[0].message.content.strip())
        # images欄がなければ空リストで補完（安全策）
        for page in slide_json.get("pages", []):
            if "images" not in page:
                page["images"] = []
                
        logger.debug(f"スライド: {slide_json}")
        return {**state, "slide_json": slide_json}
    except json.JSONDecodeError as e:
        raise ValueError(f"JSONの解析に失敗しました: {e}")
