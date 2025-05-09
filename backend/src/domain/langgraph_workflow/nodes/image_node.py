from typing import Dict, List
from src.utils.logger import get_logger
from src.application.generate_images import generate_images
from src.application.generate_image_prompts import generate_prompt
from src.domain.model.type.slide_template import TemplateType

logger = get_logger("domain.langgraph_workflow.nodes.image_node")


def image_node(state: Dict[str, (dict|list)]) -> Dict[str, (dict|list)]:
    """
    スライド内容から画像生成プロンプトを抽出し、templateがimage/three_imageの時だけ画像生成APIを呼び出すノード
    """
    logger.info("🔧 画像を生成中...")
    slide_json = state.get("slide_json")
    if not slide_json:
        raise ValueError("slide_jsonが存在しません")

    # プロンプトとスライド・画像インデックスのリストを作成
    prompt_tuples = generate_prompt(slide_json)
    prompts = [pt[0] for pt in prompt_tuples]

    # 画像をローカル保存し、そのパスを返す
    image_paths = generate_images(prompts, save_local=True) if prompts else []
    logger.info("✅ 画像生成に成功しました")

    # 各スライドのimages欄に正しく格納
    pages:List[dict] = slide_json.get("pages", [])
    
    # images欄の初期化
    for page in pages:
        if page.get("template") in (TemplateType.TABLE.value, TemplateType.THREE_IMAGES.value):
            page["images"] = []

    # 必要なスライドのimagesリストにappend
    for idx, (_, slide_idx) in enumerate(prompt_tuples):
        if idx < len(image_paths) and image_paths[idx]:
            pages[slide_idx]["images"].append(image_paths[idx])

    # 画像パスリストもstateに追加
    logger.debug(f"画像パス含むslide_json: {slide_json}")
    return {**state, "slide_json": slide_json}
