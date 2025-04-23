from typing import Dict, Any

def get_layout_schema() -> Dict[str, Any]:
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "layout_response",
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
                                "template": {
                                    "type": "string",
                                    "enum": ["text","images","three_images"],
                                    "description": "スライドのテンプレートタイプ"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "スライドの内容の説明"
                                }
                            },
                            "required": ["header", "template", "description"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["pages"],
                "additionalProperties": False
            }
        }
    } 