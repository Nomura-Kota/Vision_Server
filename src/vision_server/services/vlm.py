from typing import Any
from PIL import Image
from src.vision_server.loggers.logger import logger
from src.vision_server.services.florence2_service import Florence2VLM
import src.vision_server.utils.data_converter as data_converter

_vlm = Florence2VLM()

def image_analysis(image_data :str, task_prompt :str) -> Any:

    # base64をPLI形式に変換
    try:    
        image = data_converter.decode_base64_to_image(image_data)
        logger.info(f"base64→PLI変換が成功しました。: {image}")
    except Exception as e:
        logger.error(f"base64→PLI変換が失敗しました。: {e}")
        return {"error": "画像データの形式が不正です。"}
    
    # 画像推論を実行
    try:
        result = _vlm.process(image, task_prompt)
        logger.info(f"画像推論処理が成功しました。: {result}")
        return result
    except Exception as e:
        logger.error(f"画像推論処理が失敗しました。: {e}")
        return {"error": str(e)}