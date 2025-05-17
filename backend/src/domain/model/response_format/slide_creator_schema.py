from typing import Dict, Any
from src.domain.model.type.template import TemplateType

def get_slide_creator_schema() -> Dict[str, Any]:
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "slide_creator_response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "スライド全体のタイトル"
                    },
                    "pages": {
                        "type": "array",
                        "description": "各スライドの情報",
                        "items": {
                            "type": "object",
                            "properties": {
                                "header": {
                                    "type": "string",
                                    "description": "スライドのタイトル"
                                },
                                "content": {
                                    "type": "string",
                                    "description": "スライドの本文内容"
                                },
                                "template": {
                                    "type": "string",
                                    "enum": TemplateType.get_values(),
                                    "description": "使用するテンプレートタイプ"
                                },
                                "captions": {
                                    "type": "array",
                                    "description": "スライドの補足画像のキャプションのリスト",
                                    "items": {
                                        "type": "string"
                                    }
                                },
                                "table": {
                                    "type": "array",
                                    "description": "テーブルの行データ（2次元配列）",
                                    "items": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "description": "テーブルのセル内容"
                                        }
                                    }
                                }
                            },
                            "required": ["header", "content", "template", "captions", "table"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["title", "pages"],
                "additionalProperties": False
            }
        }
    }
