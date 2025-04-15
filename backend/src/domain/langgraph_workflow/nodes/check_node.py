# domain/langgraph_workflow/nodes/check_node.py
from typing import TypedDict
from langchain_core.messages import AIMessage

class SlideState(TypedDict):
    topic: str
    hearing: str
    layout: str
    slide_json: str
    confirmed: bool

def check_node(state: SlideState) -> dict:
    print("🔍 スライド内容の確認を行います...")
    
    # デバッグやテストでは自動でTrueを返しておく
    confirmed = True  # あとでユーザー選択に切り替え可能

    return {"confirmed": confirmed}
