from typing import Dict, Any, List
from openai import AzureOpenAI
import os
import json
from src.utils.logger import get_logger
from src.domain.model.response_format.hearing_schema import get_hearing_schema

logger = get_logger("domain.langgraph_workflow.nodes.hearing_node")

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

        制約事項：
        - 主要トピックは3つ以上5つ以内で作成してください
        - 各トピックは簡潔に、かつ具体的に記載してください
        - テーマに沿った内容であることを確認してください
    """

    response = client.chat.completions.create(
        model="app-gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        response_format=get_hearing_schema()
    )
    

    try:
        hearing_info = json.loads(response.choices[0].message.content.strip())
        logger.debug(f"hearing_info: {hearing_info}")
        return {**state, "hearing_info": hearing_info}
    except json.JSONDecodeError as e:
        raise ValueError(f"JSONの解析に失敗しました: {e}")
