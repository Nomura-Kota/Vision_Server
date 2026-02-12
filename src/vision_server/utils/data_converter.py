import base64
import io
from PIL import Image

def decode_base64_to_image(base64_string: str) -> Image.Image:
    # base64をバイナリデータへ変換
    image_data = base64.b64decode(base64_string)
    # バイナリをメモリ上のファイルストリームとして扱い、PLIで開く
    image = Image.open(io.BytesIO(image_data))
    # 透明度を省き、RGBに変換して返す
    return image.convert("RGB")