from typing import Dict, Any
from src.domain.model.type.slide_template import TemplateType

def get_slide_creator_schema() -> Dict[str, Any]:
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "slide_creator_response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "pages": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "header": {
                                    "type": "string",
                                    "description": "スライドのタイトル"
                                },
                                "content": {
                                    "type": "string",
                                    "description": "スライドの内容"
                                },
                                "template": {
                                    "type": "string",
                                    "enum": TemplateType.get_values(),
                                    "description": "スライドのテンプレートタイプ"
                                },
                            },
                            "required": ["header", "content", "template"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["pages"],
                "additionalProperties": False
            }
        }
    }
