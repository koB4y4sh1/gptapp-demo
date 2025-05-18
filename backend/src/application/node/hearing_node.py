from src.utils.logger import get_logger
from src.domain.model.response_format.hearing_schema import get_hearing_schema
from src.domain.model.prompt.hearing_prompt import HearingPrompt
from src.domain.model.type.slide import SlideState
from src.infrastructure.azureopenai.chat import chat_completion

logger = get_logger(__name__)

def hearing_node(state: SlideState) -> SlideState:
    """
    スライド状態からタイトルを抽出し、OpenAI APIを用いてヒアリング情報を取得し、
    その結果をhearing_info属性としてSlideStateに追加して返すノード。

    Args:
        state (SlideState): 入力スライド状態

    Returns:
        SlideState: hearing_info属性が追加された新しいスライド状態

    Raises:
        ValueError: タイトルが未設定、またはOpenAI応答のJSON解析に失敗した場合
    """
    title = state.title
    if not title:
        raise ValueError("title が存在しません")

    # ヒアリング用プロンプトを生成
    prompt = HearingPrompt(title).build_prompt()

    # OpenAI APIでヒアリング情報を取得
    response = chat_completion(
        prompt=prompt, response_format=get_hearing_schema()
    )

    hearing_info = response
    if not hearing_info:
        logger.error("ヒアリング結果の生成に失敗しました")
        raise ValueError("ヒアリング結果が取得できませんでした")
    logger.debug(f"ヒアリング結果: {hearing_info}")

    # ワークフローの状態の更新
    return state.model_copy(update={"hearing_info": hearing_info})

if __name__ == "__main__":
    # チェック用ダミーデータ作成
    test_state = SlideState(
        title="AI活用の最新動向"
    )
    # hearing_nodeを実行
    result_state = hearing_node(test_state)
    logger.info(f"hearing_node実行結果: {result_state}")
