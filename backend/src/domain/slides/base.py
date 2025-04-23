from abc import ABC, abstractmethod
from pptx.presentation import Presentation

class Base(ABC):
    def __init__(self, prs: Presentation, header: str, content: str):
        self.prs = prs
        self.header = header
        self.content = content

    @abstractmethod
    def build(self):
        pass