from src.domain.model.prompt.base import BasePrompt
import json

class SlideCreatorPrompt(BasePrompt):
    """
    スライド内容生成用プロンプトクラス
    """

    PROMPT_TEMPLATE = """
        あなたは優れたスライドライターです。
        以下のテーマと構成案に従って、スライド1枚ごとの具体的な内容を作成してください。

        テーマ: {title}
        構成案: {layout}
        
        制約事項：
        - スライドは1枚以上10枚以内で作成してください
        - 各スライドには必ず「タイトル（header）」「内容（content）」「テンプレートタイプ（template）」「images（画像URLリスト。初期値は空リスト[]でOK）」を含めてください
        - imagesは将来的に画像生成APIで埋めるため、現時点では空リスト[]で出力してください
        - テンプレートタイプは"text"以外も将来的に拡張される可能性があるため、構成案に従って適切な値を設定してください
        - 内容は簡潔かつ具体的に記載してください
        - 構成案に沿った内容であることを確認してください
    """

    def __init__(self, title: str, layout: dict):
        self.title = title
        self.layout = json.dumps(layout, ensure_ascii=False, indent=2)

    def build_prompt(self) -> str:
        return self.PROMPT_TEMPLATE.format(
            title=self.title,
            layout=self.layout
        )
