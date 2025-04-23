from typing import Dict, Any
from openai import AzureOpenAI
import os
import json
from src.domain.model.response_format.layout_schema import get_layout_schema
from src.infrastructure.azureopenai.chat import chat_completion
from src.utils.logger import get_logger

logger = get_logger("src.domain.langgraph_workflow.nodes.layout_node")

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
        以下の情報を元に、PowerPoint スライドの構成案を作成してください。

        テーマ: {title}
        ヒアリング結果: {json.dumps(hearing_info, ensure_ascii=False, indent=2)}
        
        制約事項：
        - スライドは1枚以上10枚以内で作成してください
        - 各スライドには必ず「タイトル（header）」「テンプレートタイプ（template）」「説明（description）」を記載してください
        - テンプレートタイプは以下から`text`, `image`のみ選ぶことができます（用途・特徴を参考にしてください）:

        ## PowerPoint スライドテンプレート一覧
        以下は、スライド生成において使用する各テンプレートの特徴と用途です。プロンプトでスライドレイアウトの指定を行う際に参考にしてください。

        ---
        ### 1. `text`
        - **特徴**: タイトル + 本文テキストの構成。シンプルで情報を伝えやすい。
        - **用途**: 概要説明、ポイントの列挙、ナレーションベースのスライド。

        ### 2. `image`
        - **特徴**: タイトル + 画像1枚。視覚的にインパクトを与える構成。
        - **用途**: 図やグラフの提示、キービジュアルの表示、概念のイメージ化。

        ### 3. `three_image`
        - **特徴**: タイトル + 横並びの3枚画像。比較や分類を明確に見せられる。
        - **用途**: 商品比較、事例紹介（ビフォー/アフター/結果など）、工程別の説明。

        ### 4. `table`
        - **特徴**: タイトル + 表。データの一覧表示や項目比較に適する。
        - **用途**: 数値データの提示、メリット・デメリット比較、仕様一覧。

        ### 5. `three_horizontal_flow`
        - **特徴**: タイトル + 左から右へ流れる3ステップの説明図。
        - **用途**: プロセス説明、手順紹介、時間的な流れの説明。

        ### 6. `quote`
        - **特徴**: タイトル + 引用文（強調された一文）。
        - **用途**: インスピレーションの提示、ユーザーの声、キーメッセージの強調。

        ### 7. `chart`
        - **特徴**: タイトル + 円グラフ／棒グラフ等のチャート挿入。
        - **用途**: 定量的データの可視化、アンケート結果の共有、業績レポート。

        ### 8. `image_text_split`
        - **特徴**: 左に画像、右にテキスト（またはその逆）の分割レイアウト。
        - **用途**: イメージと説明文のセット提示、製品紹介、具体例＋解説。

        ### 9. `timeline`
        - **特徴**: タイトル + 時系列での出来事や予定を線でつなぐ。
        - **用途**: プロジェクトスケジュール、会社沿革、ロードマップ説明。

        ### 10. `section_divider`
        - **特徴**: セクションタイトルのみ表示する大見出しスライド。
        - **用途**: 章の切り替え、新しいトピックへの導入。

        - ヒアリング結果を反映した構成にしてください
    """
    response = chat_completion(
        prompt=prompt, response_format=get_layout_schema()
    )

    try:
        layout = json.loads(response.choices[0].message.content.strip())
        logger.debug(f"構成案: {layout}")
        return {**state, "layout": layout}
    except json.JSONDecodeError as e:
        raise ValueError(f"JSONの解析に失敗しました: {e}")
