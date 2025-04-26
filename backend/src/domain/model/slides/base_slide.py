from abc import ABC, abstractmethod
from pptx.presentation import Presentation
from pptx.util import Cm

SLIDE_WIDTH_CM = 25.4
SLIDE_HEIGHT_CM = 14.29

class BaseSlide(ABC):
    def __init__(self, prs: Presentation, header: str, content: str):
        self.prs = prs
        self.header = header
        self.content = content
        prs.slide_width = Cm(SLIDE_WIDTH_CM)
        prs.slide_height = Cm(SLIDE_HEIGHT_CM)
        
    @abstractmethod
    def build(self):
        pass
