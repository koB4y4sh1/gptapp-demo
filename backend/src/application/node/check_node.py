# domain/langgraph_workflow/nodes/check_node.py

from src.utils.logger import get_logger
from src.domain.model.type.slide import SlideState

logger = get_logger(__name__)

def check_node(state: SlideState) -> SlideState:
    """
    スライド状態の確認フラグや内容をチェックし、必要に応じてconfirmed属性を更新するノード。

    Args:
        state (SlideState): 入力スライド状態

    Returns:
        SlideState: confirmed属性が更新された新しいスライド状態
    """

    if not state.confirmed:
        logger.info("🔍 入力内容の確認を行います...")
        # チェック未通過の場合はconfirmedをFalseに
        return state.model_copy(update={"confirmed": False})
    else:
        logger.info("✅ 確認済みのためスライドを生成します...")
        return state.model_copy(update={"confirmed": True})


if __name__ == "__main__":
    # ダミーデータ作成
    first_state = SlideState(
        title="AIの活用",
    )

    # 実行
    result = check_node(first_state)
    logger.debug(f"初回実行 : {result}")

    confirmed_state = first_state.model_copy(update={"confirmed": True})
    result = check_node(confirmed_state)
    logger.debug(f"確認後 : {result}")
