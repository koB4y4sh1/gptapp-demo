from dotenv import load_dotenv
load_dotenv('.env')

from src.domain.langgraph_workflow.graph.mini_pipeline import build_test_graph  # noqa: E402
import json

if __name__ == "__main__":
    graph = build_test_graph()

    # テスト入力
    initial_state = {
        "title": "Pythonの基本"
    }

    # ワークフローを実行
    final_state = graph.invoke(initial_state)

    # 出力確認
    print("===== Hearing =====")
    print(final_state["hearing_info"])
    print("\n===== Layout =====")
    print(final_state["layout"])
    print("\n===== Slide JSON =====")
    print(final_state["slide_json"])

    # JSON保存してもOK
    with open("slide_output.json", "w", encoding="utf-8") as f:
        json.dump(final_state, f, ensure_ascii=False, indent=2)
