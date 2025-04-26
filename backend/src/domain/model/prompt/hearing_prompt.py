from src.domain.model.prompt.base import BasePrompt

class HearingPrompt(BasePrompt):
    """
    ヒアリング観点整理用プロンプトクラス
    """

    PROMPT_TEMPLATE = """
        あなたは優秀なプレゼン資料作成アシスタントです。
        以下のテーマに基づき、どのような内容を伝えるべきかヒアリングの観点で整理してください。

        テーマ: {title}

        制約事項：
        - 主要トピックは3つ以上5つ以内で作成してください
        - 各トピックは簡潔に、かつ具体的に記載してください
        - テーマに沿った内容であることを確認してください
    """

    def __init__(self, title: str):
        self.title = title

    def build_prompt(self) -> str:
        return self.PROMPT_TEMPLATE.format(
            title=self.title
        )
