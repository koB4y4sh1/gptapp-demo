from pptx import Presentation
from io import BytesIO
from src.domain.model.slides.text_slide import TextSlide
from src.domain.model.slides.image_slide import ImageSlide
from src.domain.model.slides.three_image_slide import ThreeImageSlide
from src.domain.model.slides.table_slide import TableSlide
from src.domain.model.slides.three_horizontal_flow_slide import ThreeHorizontalFlowSlide
from src.domain.model.type.template import TemplateType

def generate_pptx(data: dict) -> bytes:
    prs = Presentation()
    slides = data.get("pages", [])

    for page in slides:
        header = page.get("header", "")
        content = page.get("content", "")
        template = page.get("template", "text")
        image_paths = page.get("images", [])
        table_data = page.get("table", [])
        steps = page.get("steps", [])

        if template == TemplateType.TEXT.value:
            slide = TextSlide(prs, header, content)
        elif template == TemplateType.IMAGE.value:
            slide = ImageSlide(prs, header, content, image_paths[0] if image_paths else None)
        elif template == TemplateType.THREE_IMAGES.value:
            slide = ThreeImageSlide(prs, header, content, image_paths)
        elif template == TemplateType.TABLE.value:
            slide = TableSlide(prs, header, content, table_data)
        elif template == TemplateType.THREE_HORIZONTAL_FLOW.value:
            slide = ThreeHorizontalFlowSlide(prs, header, content, steps)
        else:
            continue

        slide.build()

    output = BytesIO()
    prs.save(output)
    output.seek(0)
    return output.read()
