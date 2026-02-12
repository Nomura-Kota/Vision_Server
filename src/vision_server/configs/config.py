import os
from dotenv import load_dotenv
from src.vision_server.utils.path_generator import generate_root_path

# .envファイルを読み込む。
project_root_path = generate_root_path()
env_path = project_root_path / ".env"
load_dotenv(dotenv_path=env_path)

class Config:
    def __init__(self):
        # --- ログ設定 ---
        self.LOG_LEVEL = os.getenv("LOG_LEVEL")
        
config = Config()