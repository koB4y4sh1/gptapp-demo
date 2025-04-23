from src.infrastructure.azureopenai.client import azureopenai
from openai.types.chat import ChatCompletion

MODEL = "gpt-4.1"

def chat_completion(prompt: str, response_format: dict = None) -> ChatCompletion:
    kwargs = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }
    if response_format is not None:
        kwargs["response_format"] = response_format
    return azureopenai.chat.completions.create(**kwargs)
