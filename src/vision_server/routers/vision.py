from fastapi import APIRouter, HTTPException, Response
from src.vision_server.models.schemas import VisionRequest
from src.vision_server.services.vlm import image_analysis

router = APIRouter()

@router.post("/vision")
async def vision(req: VisionRequest):
    try:
        # VLMへ画像データを送信し、解析結果を受け取る。
        result = image_analysis(req.base64_string)

        return {"status": "success", "result": result}
    
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))