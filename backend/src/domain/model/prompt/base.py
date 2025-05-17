from abc import ABC, abstractmethod
from src.domain.model.type.page import Page
from src.domain.model.type.slide import Layout
class BasePrompt(ABC):
    """
    プロンプト生成用の基底クラス
    """

    @abstractmethod
    def build_prompt(self) -> str:
        """
        プロンプト文字列を生成する抽象メソッド
        """
        pass

    @classmethod
    def model_to_dict(self,model: Layout | Page) -> dict:
        """
        BaseModelをdict化し、Enumは値に変換する

        Args:
            layout (Layout): レイアウトインスタンス

        Returns:
            dict: シリアライズ可能な辞書
        """
        d = model.__dict__.copy()
        if "template" in d and hasattr(d["template"], "value"):
            d["template"] = d["template"].value
        return d