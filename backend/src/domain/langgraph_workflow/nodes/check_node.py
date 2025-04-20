# domain/langgraph_workflow/nodes/check_node.py
from typing import TypedDict
from langchain_core.messages import AIMessage

from src.utils.logger import get_logger

logger = get_logger("src.domain.langgraph_workflow.nodes.check_node")
class SlideState(TypedDict):
    topic: str
    hearing: str
    layout: str
    slide_json: str
    confirmed: bool

def check_node(state: SlideState) -> dict:
    if not state.get("confirmed"):
        logger.info("🔍 入力内容の確認を行います...")
        return {
            **state,
            "confirmed": False  # 初回は必ず False
        }
    logger.info("✅ 確認済みのためスライドを生成します...")
    return {
            **state,
            "confirmed": True
        }
