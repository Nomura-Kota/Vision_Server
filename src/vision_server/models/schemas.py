from pydantic import BaseModel

class VisionRequest(BaseModel):
    base64_string: str # base64形式
    task_prompt: str = "<CAPTION>"