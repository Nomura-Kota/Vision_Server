import uvicorn
from fastapi import FastAPI
from src.vision_server.routers import health, vision
import src.vision_server.loggers.log_printer as log_printer

def create_app() -> FastAPI:
    app = FastAPI(title="Vision Server")
    
    # ルーターの登録
    app.include_router(health.router)
    app.include_router(vision.router)
    
    return app

# グローバル変数として app を定義（uvicornがここを探しに来ます）
app = create_app()

def main():
    # --- 起動時のログ出力 ---
    log_printer.print_config_content()

    # --- サーバー起動 ---
    uvicorn.run(
        "src.vision_server.main:app",
        host="0.0.0.0",
        port=8001,
        reload=False
    )

if __name__ == "__main__":
    main()