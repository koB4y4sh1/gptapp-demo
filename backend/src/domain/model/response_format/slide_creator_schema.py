from typing import Dict, Any

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
                                    "enum": ["text", "image", "three_images"],
                                    "description": "スライドのテンプレートタイプ"
                                },
                                "images": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "画像パス"
                                }
                            },
                            "required": ["header", "content", "template", "images"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["pages"],
                "additionalProperties": False
            }
        }
    }
