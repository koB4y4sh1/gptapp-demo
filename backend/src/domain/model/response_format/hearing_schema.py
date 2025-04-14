from typing import Dict, Any

def get_hearing_schema() -> Dict[str, Any]:
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "hearing_response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "purpose": {
                        "type": "string",
                        "description": "資料の目的を簡潔に書いてください"
                    },
                    "target_audience": {
                        "type": "string",
                        "description": "読者の対象を具体的に書いてください"
                    },
                    "main_topics": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "主要な話題"
                        }
                    }
                },
                "required": ["purpose", "target_audience", "main_topics"],
                "additionalProperties": False
            }
        }
    } 