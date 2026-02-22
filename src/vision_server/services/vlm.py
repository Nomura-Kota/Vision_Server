from src.vision_server.configs.config import config
from src.vision_server.loggers.logger import logger
from src.vision_server.services.florence2_service import Florence2VLM
import src.vision_server.utils.data_converter as data_converter

_vlm = Florence2VLM(model_id=config.VISION_MODEL)

def image_analysis(image_data: str) -> dict:

    # base64をPIL形式に変換
    try:
        image = data_converter.decode_base64_to_image(image_data)
    except Exception as e:
        logger.error(f"base64→PIL変換が失敗しました。: {e}")
        return {"description": "", "screen_text": ""}

    # CAPTION を実行
    try:
        description = next(iter(_vlm.process(image, "<CAPTION>").values()), "")
        logger.info(f"CAPTION: {description}")
        return {"description": description, "screen_text": ""}
    except Exception as e:
        logger.error(f"画像推論処理が失敗しました。: {e}")
        return {"description": "", "screen_text": ""}
