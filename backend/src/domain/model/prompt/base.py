from abc import ABC, abstractmethod

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
