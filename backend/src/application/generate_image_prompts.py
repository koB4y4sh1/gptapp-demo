import json
from typing import List, Dict, Tuple, Any
from src.domain.model.prompt.image_prompt import ImagePrompt
from src.domain.model.type.template import TemplateType
from src.domain.model.prompt.image_content_prompt import ImageContentPrompt
from src.domain.model.response_format.image_content_schema import get_image_content_schema
from src.infrastructure.azureopenai.chat import chat_completion

def generate_prompt(slide_json: Dict[str, Any]) -> List[Tuple[str, int, int]]:
    """
    スライド内容から画像生成用プロンプトと、どのスライド・何枚目かのインデックスを抽出する
    Returns: List[Tuple[prompt, slide_idx, image_idx]]
    """
    
    prompts = []
    pages: List[dict] = slide_json.get("pages", [])
    for i, page in enumerate(pages):
        template = page.get("template", "")
        header = page.get("header", "")
        content = page.get("content", "")
        sheets = 3 if template == TemplateType.THREE_IMAGES.value else 1

        # image,three_imagesでない場合はスキップ
        if template not in [TemplateType.IMAGE.value, TemplateType.THREE_IMAGES.value]:
            continue
        # ヘッダーとコンテンツが両方空の場合はスキップ
        if not header and not content:
            continue
        # title,contentを元に画像の生成に必要な情報を取得する
        image_content_prompt = ImageContentPrompt(title=header, content=content, sheets=sheets).build_prompt()
        response = chat_completion(image_content_prompt, response_format=get_image_content_schema())
        images_info = json.loads(response.choices[0].message.content.strip())
        # 画像生成用のプロンプトの作成
        for image in images_info.get("images", []):
            prompt = ImagePrompt(title=header,content=image.get("content",""), note=image.get("note","")).build_prompt()
    return prompts
