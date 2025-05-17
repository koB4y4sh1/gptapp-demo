import json
import enum
from dataclasses import is_dataclass, asdict

from .base_slide import BaseSlide
from .image_slide import ImageSlide
from .table_slide import TableSlide
from .text_slide import TextSlide
from .three_horizontal_flow_slide import ThreeHorizontalFlowSlide
from .three_image_slide import ThreeImageSlide

from src.domain.model.type.slide import SlideState, HearingInfo, Layout
from src.domain.model.type.page import Page
from src.domain.model.type.template import TemplateType

def from_json_to_slidestate(json_dict: dict) -> SlideState:
    """
    dict(JSON)からSlideStateインスタンスへ変換する。
    layout, pagesの'template'はstr→TemplateTypeへ変換する。
    """
    def convert_template(item):
        if "template" in item and isinstance(item["template"], str):
            item = item.copy()
            item["template"] = TemplateType(item["template"])
        return item

    data = json_dict.copy()
    if "layout" in data and data["layout"] is not None:
        data["layout"] = [convert_template(l) for l in data["layout"]]
    if "pages" in data and data["pages"] is not None:
        data["pages"] = [convert_template(p) for p in data["pages"]]
    return SlideState.parse_obj(data)

def to_json_compatible(obj):
    """
    任意のPythonオブジェクトをHTTPボディ用のJSON互換な型（dict, list, str, int, float, bool, None）に再帰変換する。
    - dataclass: asdictで展開
    - Enum: value
    - __dict__持ち: dict化
    - list/tuple: 再帰
    - dict: 再帰
    - 基本型/None: そのまま
    """
    if is_dataclass(obj):
        return {k: to_json_compatible(v) for k, v in asdict(obj).items()}
    elif isinstance(obj, enum.Enum):
        return obj.value
    elif isinstance(obj, dict):
        return {to_json_compatible(k): to_json_compatible(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [to_json_compatible(v) for v in obj]
    elif hasattr(obj, "__dict__") and not isinstance(obj, type):
        # dataclass以外のカスタムクラス
        return {k: to_json_compatible(v) for k, v in vars(obj).items() if not k.startswith("_")}
    else:
        return obj

def slide_to_dict(slide: BaseSlide) -> dict:
    """
    BaseSlideまたはそのサブクラスのインスタンスをdictに変換する。
    prs(Presentation)は含めない。
    """
    base = {
        "type": slide.__class__.__name__,
        "header": slide.header,
        "content": slide.content,
    }
    # サブクラス固有属性を追加
    if isinstance(slide, ImageSlide):
        base["image_path"] = slide.image_path
    elif isinstance(slide, TableSlide):
        base["table_data"] = slide.table_data
    elif isinstance(slide, ThreeHorizontalFlowSlide):
        base["steps"] = slide.steps
    elif isinstance(slide, ThreeImageSlide):
        base["image_paths"] = slide.image_paths
    # TextSlideはbaseのみ
    return base

def slide_to_json(slide: BaseSlide, ensure_ascii=False, indent=2) -> str:
    """
    BaseSlideまたはそのサブクラスのインスタンスをJSON文字列に変換する。
    """
    return json.dumps(slide_to_dict(slide), ensure_ascii=ensure_ascii, indent=indent)

def to_json(obj, ensure_ascii=False, indent=2) -> str:
    """
    任意のPythonオブジェクトをHTTPボディ用のJSON文字列に変換する。
    """
    return json.dumps(to_json_compatible(obj), ensure_ascii=ensure_ascii, indent=indent)
