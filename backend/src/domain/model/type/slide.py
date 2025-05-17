from typing import List
from pydantic import BaseModel
from src.domain.model.type.page import Page
from src.domain.model.type.template import TemplateType

class HearingInfo(BaseModel):
    purpose: str
    target_audience: str
    main_topics: List[str]

class Layout(BaseModel):
    header: str
    template: TemplateType
    description: str

class SlideJson(BaseModel):
    pages: List[Page]

class SlideState(BaseModel):
    title: str
    confirmed: bool = False
    pptx_path: str = None
    hearing_info: HearingInfo = None
    layout: List[Layout] = None
    slide: List[Page] = None

