from pydantic import BaseModel
class Image(BaseModel):
    """
    画像付きアイテムのデータモデル

    Attributes:
        name (str): 画像ファイル名または識別子。
        title (str): 画像のタイトル。
        caption (str): 画像の説明文やキャプション。
        url (List[str]): 画像のURLリスト。
        embedding (Optional[List[float]]): ベクトル埋め込み（初期値はNone）。
    """
    name: str
    title: str
    caption: str
    url: list[str]
    embedding: None|list[float] = None

    def set_name(self, name: str):
        self.name = name

    def set_title(self, title: str):
        self.title = title

    def set_caption(self, caption: str):
        self.caption = caption

    def set_url(self, url: list[str]):
        self.url = url

    def set_embedding(self, embedding: list[float]):
        self.embedding = embedding
