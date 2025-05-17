import json
from typing import Optional, Any

from openai.types.chat.chat_completion import ChatCompletion

from src.infrastructure.azureopenai.client import azureopenai
from src.utils.logger import get_logger

logger = get_logger("src.infrastructure.azureopenai.chat")

DEFAULT_MODEL = "app-gpt-4o-mini-2024-07-18"

def chat_completion(
    prompt: Optional[str] = None,
    messages: Optional[list[dict[str, Any]]] = None,
    response_format: Optional[dict[str, Any]] = None,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
    **extra_kwargs
) -> dict | None:
    """
    Azure OpenAI の chat completion API を呼び出すユーティリティ関数。

    Args:
        prompt (str, optional): ユーザー発話のプロンプト。messages が指定されていない場合必須。
        messages (list[dict], optional): OpenAI chat API 形式の messages。prompt より優先。
        response_format (dict, optional): レスポンスフォーマット指定。
        model (str): 使用するモデル名。
        temperature (float): 温度パラメータ。
        **extra_kwargs: その他APIに渡す追加パラメータ。

    Returns:
        Any: 生成されたメッセージ本文（content）。通常はJSONデコード結果。デコード失敗時は生テキスト。

    Raises:
        ValueError: prompt も messages も指定されていない場合。
        RuntimeError: API呼び出し時またはレスポンス処理時のエラー。
    """
    if messages is None:
        if prompt is None:
            raise ValueError("prompt または messages のいずれかを指定してください")
        messages = [{"role": "user", "content": prompt}]

    kwargs: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    if response_format is not None:
        kwargs["response_format"] = response_format
    kwargs.update(extra_kwargs)

    try:
        response: ChatCompletion = azureopenai.chat.completions.create(**kwargs)
        content = response.choices[0].message.content.strip()
        try:
            return json.loads(content)
        except json.JSONDecodeError as je:
            logger.error(f"JSONの解析に失敗しました: {je}")
            return None
    except Exception as e:
        # エラー時にAPIリクエスト内容も含めて例外化
        raise RuntimeError(
            f"chat_completion API呼び出しに失敗しました: {e}\n"
            f"リクエスト内容: {json.dumps(kwargs, ensure_ascii=False)}"
        )

if __name__ == "__main__":
    # チェック用ダミーデータ作成
    prompt = "こんにちは"
    messages = [{"role": "user", "content": prompt}]
    response_format = {"type": "json_object"}
