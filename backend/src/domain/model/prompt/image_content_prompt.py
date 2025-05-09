from src.domain.model.prompt.base import BasePrompt

class ImageContentPrompt(BasePrompt):
    """
    スライドのタイトル・内容から画像アイコン説明文を生成するプロンプトクラス
    """

    PROMPT_TEMPLATE = """
        あなたは優秀なプロンプトエンジニアです。  
        以下のスライド情報をもとに、スライドに必要な「アイコン風の画像」の説明文を日本語で考えてください。

        # 制約事項
        - 出力はリスト形式とし、要素数は**{sheets}個**になるようにしてください。
        - 各要素は以下の形式で出力してください：  
          `image_url: "", content: "<画像の説明文>", note: "<補足が必要な場合のみ追記。なければ空文字>"`
        - `image_url` は常に空文字で出力してください（画像はまだ生成されていないため）。
        - 各 `content` は**1文で簡潔に**まとめてください（画像の内容を短く明確に伝えるアイコンの説明文）。
        - `note` には、画像生成にあたり**補足情報が必要な場合**に限り、日本語で記述してください（例：構図や視点、登場人物など）。補足が不要な場合は空文字で構いません。

        # スライド情報
        - タイトル: {title}
        - 内容: {content}

        # 出力例1
        ```
        "image_url": "",
        "content": "オンライン会議をする人物のアイコン",
        "note": "3人以上のキャラクターが並んでいる構図で"
        ```
        # 出力例2
        ```
        "image_url": "",
        "content": "クラウドサーバーのシンプルなイラスト",
        "note": ""
        ```
    """

    def __init__(self, title: str, content: str, sheets: int = 1) -> None:
        self.title = title
        self.content = content
        self.sheets = sheets

    def build_prompt(self) -> str:
        return self.PROMPT_TEMPLATE.format(
            title=self.title,
            content=self.content,
            sheets=self.sheets

        )
