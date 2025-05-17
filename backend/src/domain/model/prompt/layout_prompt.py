from src.domain.model.prompt.base import BasePrompt
from src.domain.model.type.slide import HearingInfo
import json
import textwrap

class LayoutPrompt(BasePrompt):
    """
    PowerPointスライド構成案生成用プロンプトクラス。

    テーマとヒアリング情報をもとに、OpenAI APIへ送信するプロンプト文を生成する。
    """

    # スライドテンプレートの説明を含むプロンプトテンプレート
    PROMPT_TEMPLATE = textwrap.dedent("""
        あなたは資料作成に特化したプレゼン設計のプロです。
        以下の情報を元に、PowerPoint スライドの構成案を作成してください。

        テーマ: {title}
        ヒアリング結果: {hearing_info}
        
        制約事項：
        - スライドは1枚以上10枚以内で作成してください
        - 各スライドには必ず「タイトル（header）」「テンプレートタイプ（template）」「説明（description）」を記載してください
        - テンプレートタイプは以下から`text`, `image`, `three_images`のみ選ぶことができます（用途・特徴を参考にしてください）:

        ## PowerPoint スライドテンプレート一覧
        以下は、スライド生成において使用する各テンプレートの特徴と用途です。プロンプトでスライドレイアウトの指定を行う際に参考にしてください。

        ---
        ### 1. `text`
        - **特徴**: タイトル + 本文テキストの構成。シンプルで情報を伝えやすい。
        - **用途**: 概要説明、ポイントの列挙、ナレーションベースのスライド。

        ### 2. `image`
        - **特徴**: タイトル + 画像1枚。視覚的にインパクトを与える構成。
        - **用途**: 図やグラフの提示、キービジュアルの表示、概念のイメージ化。

        ### 3. `three_images`
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
    """)

    def __init__(self, title: str, hearing_info: HearingInfo):
        """
        Args:
            title (str): スライドのテーマ
            hearing_info (HearingInfo | dict | str): ヒアリング情報（dictまたはJSON文字列）
        """
        self.title = title
        self.hearing_info = json.dumps(hearing_info.__dict__, ensure_ascii=False, indent=2)

    def build_prompt(self) -> str:
        """
        プロンプト文を生成する。

        Returns:
            str: OpenAI API用のプロンプト文
        """
        return self.PROMPT_TEMPLATE.format(
            title=self.title,
            hearing_info=self.hearing_info
        ).strip()

if __name__ == "__main__":
    # チェック用ダミーデータ
    title = "AI活用の最新動向"
    
    hearing_info = HearingInfo(
        purpose= "AI活用の最新動向",
        target_audience= "AIに興味がある人",
        main_topics=[
            "AIとは何か、その基本概念を解説",
            "現在注目されているAI技術の紹介",
            "ビジネスや社会"
        ]
    )
    prompt = LayoutPrompt(title, hearing_info).build_prompt()
    print(prompt)
