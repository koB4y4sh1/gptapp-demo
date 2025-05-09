def get_image_content_schema():
    """
    画像アイコン説明文リスト用のレスポンスフォーマットスキーマ
    """
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "image_conetnt_response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "images": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "image_url": {
                                    "type": "string",
                                    "description": "画像のURL"
                                },
                                "content": {
                                    "type": "string",
                                    "description": "画像の内容"
                                },
                                "note": {
                                    "type": "string",
                                    "description": "画像についての補足説明"
                                }
                            },
                            "required": ["image_url", "content", "note"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["images"],
                "additionalProperties": False
            }
        }
    }
