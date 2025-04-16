# domain/langgraph_workflow/nodes/generate_pptx_node.py
import os
from datetime import datetime
from src.application.generate import generate_pptx

class SlideState(dict):
    pass  # TypedDictと互換性あるようにしておくと便利

def generate_pptx_node(state: SlideState) -> dict:
    print("📦 PowerPoint を生成中...")

    try:
        title = state["title"]
        slides_json = state["slide_json"]

        # 一時ディレクトリを作成
        temp_dir = os.path.join("temp", "pptx")
        os.makedirs(temp_dir, exist_ok=True)

        # 一時ファイルのパスを生成
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_path = os.path.join(temp_dir, f"{title}_{timestamp}.pptx")

        # 実際の生成処理
        pptx_data = generate_pptx(slides_json)

        # 一時ファイルに保存
        with open(temp_path, "wb") as f:
            f.write(pptx_data)

        print(f"✅ 一時ファイルを保存しました: {temp_path}")

        return {"pptx_path": temp_path}
    except KeyError as e:
        print(f"❌ エラー: 必要なキーが存在しません - {e}")
        raise
    except Exception as e:
        print(f"❌ エラー: PowerPoint生成中に問題が発生しました - {e}")
        raise
