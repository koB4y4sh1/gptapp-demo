
from openai.types.images_response import ImagesResponse

from src.infrastructure.azureopenai.client import dall_e
MODEL = "dall-e-3"

def images_generate(prompt: str) -> ImagesResponse:
    return dall_e.images.generate(
                model=MODEL,
                prompt=prompt,
                n=1,
                size="1024x1024",
                response_format="url"
            )