from enum import Enum

class TemplateType(Enum):
    TEXT = "text"
    IMAGE = "image"
    THREE_IMAGES = "three_images"
    TABLE = "table"
    THREE_HORIZONTAL_FLOW = "three_horizontal_flow"
    QUOTE = "quote"
    CHART = "chart"
    IMAGE_TEXT_SPLIT = "image_text_split"
    TIMELINE = "timeline"
    SECTION_DIVIDER = "section_divider"

    @classmethod
    def get_names(cls) -> list:
        # Enum定義が増えても対応可能
        return [i.name for i in cls]
    
    @classmethod
    def get_values(cls) -> list:
        # Enum定義が増えても対応可能
        return [i.value for i in cls]