from langgraph.graph import StateGraph
from typing import TypedDict, Annotated

from src.domain.langgraph_workflow.nodes.hearing_node import hearing_node
from src.domain.langgraph_workflow.nodes.layout_node import layout_node
from src.domain.langgraph_workflow.nodes.slide_creator_node import slide_creator_node

# 状態管理用の型
class SlideState(TypedDict):
    title: str
    hearing_info: str
    layout: str
    slide_json: str

# LangGraphセットアップ
def build_test_graph():
    builder = StateGraph(SlideState)

    builder.add_node("hearing_node", hearing_node)
    builder.add_node("layout_node", layout_node)
    builder.add_node("slide_creator", slide_creator_node)

    builder.set_entry_point("hearing_node")
    builder.add_edge("hearing_node", "layout_node")
    builder.add_edge("layout_node", "slide_creator")

    graph = builder.compile()
    return graph
