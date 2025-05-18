
from src.domain.model.response_format.slide_creator_schema import get_slide_creator_schema
from src.domain.model.prompt.slide_creator_prompt import SlideCreatorPrompt
from src.domain.model.type.slide import Layout, SlideState
from src.infrastructure.azureopenai.chat import chat_completion
from src.utils.logger import get_logger

logger = get_logger(__name__)

def slide_creator_node(state: SlideState) -> SlideState:
    """
    SlideState からプロンプトを生成し、Azure OpenAI API でスライド原本を生成するノード。

    Args:
        state (SlideState): スライド生成ワークフローの状態

    Returns:
        SlideState: pages が追加された新しい状態

    Raises:
        ValueError: title, layout, またはAPIレスポンスに不備がある場合
    """
    title = state.title
    layout = state.layout

    if not title or not layout:
        logger.error(f"title または layout が不足しています: title={title}, layout={layout}")
        raise ValueError("title または layout が不足しています")

    # スライド生成用プロンプトを作成
    prompt = SlideCreatorPrompt(title, layout).build_prompt()

    # OpenAI APIでスライド原本を生成
    response = chat_completion(prompt=prompt, response_format=get_slide_creator_schema())

    if not isinstance(response, dict):
        logger.error(f"APIレスポンスがdict型ではありません: {response}")
        raise ValueError("スライド生成APIのレスポンス形式が不正です")

    pages = response.get("pages")
    if not pages:
        logger.error(f"スライドの原本の生成に失敗しました。レスポンス: {response}")
        raise ValueError("スライドの原本が取得できませんでした")
    logger.debug(f"スライド: {pages}")

    # ワークフローの状態の更新
    return state.model_copy(update={"slide": pages})

if __name__ == "__main__":
    from src.domain.model.type.template import TemplateType

    # テスト用 SlideState を作成
    slide_state = SlideState(
        title="Pythonの基礎",
        layout=[
            Layout(
                header="Pythonとは？",
                template=TemplateType.TEXT,
                description="Pythonの概要と特徴を紹介する"
            ),
            Layout(
                header="Pythonの歴史",
                template=TemplateType.IMAGE,
                description="Pythonの歴史と発展を紹介する"
            ),
            Layout(
                header="Pythonの活用分野",
                template=TemplateType.THREE_IMAGES,
                description="Pythonが使われる具体的な分野を視覚的に示す"
            ),
            Layout(
                header="他言語との比較",
                template=TemplateType.TABLE,
                description="JavaやC++と比較してPythonの利点を説明する"
            )
        ]
    )

    # slide_creator_node を実行
    result = slide_creator_node(slide_state)
    logger.debug(result)
