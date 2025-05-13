from langgraph.graph import StateGraph
import os
import shutil

from src.domain.langgraph_workflow.nodes.check_node import check_node
from src.domain.langgraph_workflow.nodes.hearing_node import hearing_node
from src.domain.langgraph_workflow.nodes.layout_node import layout_node
from src.domain.langgraph_workflow.nodes.slide_creator_node import slide_creator_node
from src.domain.langgraph_workflow.nodes.image_node import image_node
from src.domain.langgraph_workflow.nodes.generate_pptx_node import generate_pptx_node
from src.domain.model.type.slide import SlideState
from src.utils.logger import get_logger

logger = get_logger("src.domain.langgraph_workflow.workflow")

# 一時ファイルのクリーンアップ
def cleanup_temp_files():
    temp_dir = os.path.join("temp", "pptx")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        logger.info("✅ 一時ファイルをクリーンアップしました")

# LangGraphセットアップ
def build_main_graph():
    # 一時ファイルのクリーンアップ
    cleanup_temp_files()

    builder = StateGraph(SlideState)

    builder.add_node("check", check_node)
    builder.add_node("hearing_node", hearing_node)
    builder.add_node("layout_node", layout_node)
    builder.add_node("slide_creator", slide_creator_node)
    builder.add_node("image_node", image_node)
    builder.add_node("generate_pptx", generate_pptx_node)

    builder.set_entry_point("check")
    builder.add_conditional_edges(
        "check",
        lambda state: "image_node" if state["confirmed"] else "hearing_node"
    ) 
    builder.add_edge("hearing_node", "layout_node")
    builder.add_edge("layout_node", "slide_creator")
    builder.add_edge("image_node", "generate_pptx")

    return builder.compile()
