import json
from src.domain.model.response_format.layout_schema import get_layout_schema
from src.domain.model.prompt.layout_prompt import LayoutPrompt
from src.domain.model.type.slide import HearingInfo, SlideState
from src.infrastructure.azureopenai.chat import chat_completion
from src.utils.logger import get_logger

logger = get_logger(__name__)

def layout_node(state: SlideState) -> SlideState:
    """
    スライド状態からタイトルとhearing_infoを抽出し、OpenAI APIを用いて
    レイアウト案を取得し、layout属性としてSlideStateに追加して返すノード。

    Args:
        state (SlideState): 入力スライド状態

    Returns:
        SlideState: layout属性が追加された新しいスライド状態

    Raises:
        ValueError: タイトルまたはhearing_infoが未設定、またはOpenAI応答のJSON解析に失敗した場合
    """
    title = state.title
    hearing_info:HearingInfo = state.hearing_info
    if not title or not hearing_info:
        raise ValueError("title または hearing_info が不足しています")

    # レイアウト生成用プロンプトを作成
    prompt = LayoutPrompt(title, hearing_info).build_prompt()
    # OpenAI APIでレイアウト案を取得
    response = chat_completion(
        prompt=prompt, response_format=get_layout_schema()
    )

    layout = response.get("pages")
    if not layout:
        logger.error("スライドの構成案の生成に失敗しました")
        raise ValueError("スライドの構成案が取得できませんでした")
    logger.debug(f"構成案: {layout}")
    
    # ワークフローの状態の更新
    return state.model_copy(update={"layout": layout})

if __name__ == "__main__":
    # チェック用ダミーデータ作成
    hearing_info = HearingInfo(
        purpose= "AI活用の最新動向",
        target_audience= "AIに興味がある人",
        main_topics=[
            "AIとは何か、その基本概念を解説",
            "現在注目されているAI技術の紹介",
            "ビジネスや社会でのAI活用例"
        ]
    )
    slide_state = SlideState(
        title="AI活用の最新動向",
        hearing_info=hearing_info
    )

    # layout_nodeを実行
    result = layout_node(slide_state)
    logger.info(f"layout_node実行結果: {result}")
