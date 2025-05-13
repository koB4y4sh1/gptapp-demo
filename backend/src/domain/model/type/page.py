from typing import  Optional
from pydantic import BaseModel
from src.domain.model.type.template import TemplateType


class Page(BaseModel):
    header: str
    content: str
    template: TemplateType
    images: list[str] = None
    captions: Optional[list[str]] = None
    table: Optional[list[list[str]]] = None
