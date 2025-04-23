import os
import requests
from datetime import datetime
from typing import  List
from src.utils.logger import get_logger
from src.infrastructure.azureopenai.images import images_generate
from openai.types.images_response import ImagesResponse

logger = get_logger("application.generate_images")

def generate_images(prompts: List[str], save_local: bool = True) -> List[str]:
    """
    OpenAI Image API（DALL·E 3）で画像を生成し、画像URLリストまたはローカルパスリストを返す
    """
    results = []
    for idx, prompt in enumerate(prompts):
        logger.debug(f"画像生成プロンプト: {prompt}")
        try:
            response:ImagesResponse = images_generate(
                prompt=prompt
            )
            url = response.data[0].url
            if save_local and url:
                # 画像をダウンロードして一時保存
                try:
                    img_data = requests.get(url).content
                    temp_dir = os.path.join("temp", "images")
                    os.makedirs(temp_dir, exist_ok=True)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"slideimg_{timestamp}_{idx}.png"
                    local_path = os.path.join(temp_dir, filename)
                    with open(local_path, "wb") as f:
                        f.write(img_data)
                    results.append(local_path)
                except Exception as e:
                    logger.error(f"⚠️ 画像のダウンロード失敗 リトライ回数: {last_error}")
                    raise RuntimeError("画像のダウンロードに失敗しました")
            else:
                results.append(url)
        except Exception as e:
            logger.error(f"❌ 画像生成APIエラー: {e}")
            results.append("")  # 失敗時は空文字
    return results