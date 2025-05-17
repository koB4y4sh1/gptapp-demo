import json
import textwrap
from typing import List

from src.domain.model.prompt.base import BasePrompt
from src.domain.model.type.slide import Layout

class SlideCreatorPrompt(BasePrompt):
    """
    スライド内容生成用プロンプトクラス

    Args:
        title (str): スライド全体のテーマ
        layout (List[Layout]): スライド構成案（各スライドのレイアウト情報リスト）
    """

    PROMPT_TEMPLATE = textwrap.dedent("""
        あなたは優れたスライドライターかつ構造化データ設計者です。
        以下のテーマと構成案に基づき、プレゼンテーション用スライドの内容をJSON形式で作成してください。

        テーマ: {title}
        構成案: {layout}

        ## 要件
        - スライド枚数は1枚以上10枚以内とし、構成案（layout）の項目数に従ってください。
        - 各スライドには以下の項目を含めてください：
        - `header`（スライドのタイトル）
        - `content`（簡潔かつ具体的な説明文）
        - `template`（使用テンプレート。例: "text", "image", "three_images", "table" など。構成案の指示に従って適切に指定）
        - `captions`（`template`が`image`,`three_imagesの場合に、画像に対応するキャプションを含める）
            - `image`の場合は1つのキャプションを指定
            - `three_images`の場合は3つのキャプションを指定
        - `table`（`template`が`table`の場合に、2次元配列の表データを指定）

        ## Example JSON Response:
        ```json
        {{
            "title": "Pythonの基礎",
            "pages": [
                {{
                "header": "Pythonとは？",
                "content": "Pythonはシンプルで読みやすい構文を持つプログラミング言語です。",
                "template": "text",
                "captions": [],
                "table": []
                }},
                {{
                "header": "プログラムの歴史",
                "content": "Pythonの歴史と発展を紹介する",
                "template": "image",
                "captions": ["Pythonの歴史と発展を説明するイラスト1"],
                "table": []
                }},
                {{
                "header": "活用分野",
                "content": "PythonはWeb開発やデータ分析など様々な分野で使われています。",
                "template": "three_images",
                "captions": ["活用分野を説明するイラスト1", "Pの活用分野を説明するイラスト2", "活用分野を説明するイラスト3"],
                "table": []
                }},
                {{
                "header": "他言語との比較",
                "content": "以下は主要な言語との比較表です。",
                "template": "table",
                "captions": [],
                "table": [
                    ["言語", "用途", "学習難易度"],
                    ["Python", "汎用", "易しい"],
                    ["Java", "業務アプリ", "中"],
                    ["C++", "システム", "難しい"]
                ]
                }}
            ]
        }}
        ```
    """)

    def __init__(self, title: str, layouts: List[Layout]):
        """
        Args:
            title (str): スライド全体のテーマ
            layouts (List[Layout]): スライド構成案
        """
        super().__init__()
        self.title = title
        self.layout = json.dumps(
            [self._layout_to_dict(layout) for layout in layouts],
            ensure_ascii=False,
            indent=2
        )

    @staticmethod
    def _layout_to_dict(layout: Layout) -> dict:
        d = layout.__dict__.copy()
        if "template" in d and hasattr(d["template"], "value"):
            d["template"] = d["template"].value
        return d

    def build_prompt(self) -> str:
        """
        プロンプト文字列を生成

        Returns:
            str: LLMに渡すプロンプト
        """
        return self.PROMPT_TEMPLATE.format(
            title=self.title,
            layout=self.layout
        )

if __name__ == "__main__":
    # チェック用ダミーデータ
    title = "AI活用の最新動向"
    from src.domain.model.type.template import TemplateType
    
    layout=[
        Layout(
            header="Pythonとは？",
            template=TemplateType.TEXT,
            description="Pythonの概要と特徴を紹介する"
        ),
        Layout(
            header="Pythonの歴史",
            template=TemplateType.IMAGE,
            description="Pythonの歴史と発展を紹介する"
        ),
        Layout(
            header="Pythonの活用分野",
            template=TemplateType.THREE_IMAGES,
            description="Pythonが使われる具体的な分野を視覚的に示す"
        ),
        Layout(
            header="他言語との比較",
            template=TemplateType.TABLE,
            description="JavaやC++と比較してPythonの利点を説明する"
        )
    ]
    prompt = SlideCreatorPrompt(title, layout).build_prompt()
    print(prompt)


    # PROMPT_TEMPLATE = textwrap.dedent("""
    #     あなたは優れたスライドライターです。
    #     以下のテーマと構成案に従って、スライド1枚ごとの具体的な内容を作成してください。

    #     テーマ: {title}
    #     構成案: {layout}

    #     制約事項：
    #     - スライドは1枚以上10枚以内で作成してください
    #     - 各スライドには必ず「タイトル（header）」「内容（content）」「テンプレートタイプ（template）」「images（画像URLリスト。初期値は空リスト[]でOK）」を含めてください
    #     - imagesは将来的に画像生成APIで埋めるため、現時点では空リスト[]で出力してください
    #     - テンプレートタイプは"text"以外も将来的に拡張される可能性があるため、構成案に従って適切な値を設定してください
    #     - 内容は簡潔かつ具体的に記載してください
    #     - 構成案に沿った内容であることを確認してください
    # """)
