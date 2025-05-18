from langgraph.graph import StateGraph
import os
import shutil

from src.application.node.check_node import check_node
from src.application.node.hearing_node import hearing_node
from src.application.node.layout_node import layout_node
from src.application.node.slide_creator_node import slide_creator_node
from src.application.node.image_node import image_node
from src.application.node.generate_pptx_node import generate_pptx_node
from src.domain.model.slides.utils import to_json_compatible
from src.domain.model.type.slide import SlideState
from src.utils.logger import get_logger

logger = get_logger(__name__)

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

    def check_conditional_edge(state: SlideState) -> str:
        return "image_node" if state.confirmed else "hearing_node"

    builder.add_conditional_edges(
        "check",
        check_conditional_edge
    )
    builder.add_edge("hearing_node", "layout_node")
    builder.add_edge("layout_node", "slide_creator")
    builder.add_edge("image_node", "generate_pptx")

    return builder.compile()


if __name__ == "__main__":
    # ダミーデータ作成
    
    first_state = SlideState(
        title="AIの活用",
    )
    # 実行
    result = build_main_graph().invoke(first_state)
    logger.debug(f"初回実行 : {result}")
    
    confirmed_state = SlideState(**result)
    confirmed_state.confirmed = True
    logger.debug(f"chechkkkkkkkkkkkkkkkkkkkkkkkk : {confirmed_state}")

    result = build_main_graph().invoke(confirmed_state)
    logger.debug(f"確認後 : {result}")
    print("=======================================================================")
    logger.debug(f"JSON : {to_json_compatible(result)}")