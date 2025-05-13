from typing import List, Dict
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
    hearing_info: HearingInfo
    layout: Dict[str, Layout]
    slide_json: Dict[str, List[Page]]
    confirmed: bool
    pptx_path: str
