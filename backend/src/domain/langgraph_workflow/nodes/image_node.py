from typing import Dict, Any, List, Tuple
from src.utils.logger import get_logger
from src.application.generate_images import generate_images

logger = get_logger("domain.langgraph_workflow.nodes.image_node")


def extract_image_prompts_and_indices(slide_json: Dict[str, Any]) -> List[Tuple[str, int, int]]:
    """
    スライド内容から画像生成用プロンプトと、どのスライド・何枚目かのインデックスを抽出する
    Returns: List[Tuple[prompt, slide_idx, image_idx]]
    """
    prompts = []
    pages = slide_json.get("pages", [])
    for i, page in enumerate(pages):
        template = page.get("template", "")
        header = page.get("header", "")
        desc = page.get("description", "") or page.get("content", "")
        base_prompt = f"{header}: {desc}".strip(": ")
        if template == "image":
            if base_prompt:
                prompts.append((base_prompt, i, 0))
        elif template == "three_image":
            for j in range(3):
                # 3枚分のプロンプト。用途に応じて工夫したい場合はここでpromptを変えてもよい
                prompt = f"{base_prompt} ({j+1}/3)" if base_prompt else f"スライド{i+1}の画像{j+1}"
                prompts.append((prompt, i, j))
        # 他のtemplateは画像生成しない
    return prompts



def image_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    スライド内容から画像生成プロンプトを抽出し、templateがimage/three_imageの時だけ画像生成APIを呼び出すノード
    """
    slide_json = state.get("slide_json")
    if not slide_json:
        raise ValueError("slide_jsonが存在しません")

    # プロンプトとスライド・画像インデックスのリストを作成
    prompt_tuples = extract_image_prompts_and_indices(slide_json)
    prompts = [pt[0] for pt in prompt_tuples]

    # 画像をローカル保存し、そのパスを返す（失敗時はURL）
    print(prompts)
    image_paths = generate_images(prompts, save_local=True) if prompts else []

    # 各スライドのimages欄に正しく格納
    pages = slide_json.get("pages", [])
    # まず全images欄を空リストで初期化
    for page in pages:
        page["images"] = []

    for idx, (prompt, slide_idx, image_idx) in enumerate(prompt_tuples):
        if idx < len(image_paths) and image_paths[idx]:
            # 必要なスライドのimagesリストにappend
            pages[slide_idx]["images"].append(image_paths[idx])

    # 画像パスリストもstateに追加
    return {**state, "slide_json": slide_json, "image_paths": image_paths}
