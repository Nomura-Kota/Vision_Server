from pydantic import BaseModel

class VisionRequest(BaseModel):
    base64_string: str
