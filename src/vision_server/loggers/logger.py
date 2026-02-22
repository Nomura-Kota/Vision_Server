import io
import logging
import sys
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from src.vision_server.configs.config import config
from src.vision_server.utils.path_generator import generate_root_path

def logger_init(name=__name__):
    # ログの出力形式
    log_format = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 1. コンソール出力用（Windows の cp932 対策として utf-8 で出力）
    stdout_utf8 = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    console_handler = logging.StreamHandler(stdout_utf8)
    console_handler.setFormatter(log_format)

    # 2. ファイル出力用
    project_root_path = generate_root_path()
    log_file = Path(project_root_path / "datas" / "logs" / "vision_server.log")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # 毎日0時に切り替える
    file_handler = TimedRotatingFileHandler(
        log_file,
        when="midnight", 
        interval=1,
        backupCount=30,
        encoding="utf-8"
    )
    # ローテーションされたファイル名に日付が入るようにする
    file_handler.suffix = "%Y-%m-%d"
    file_handler.setFormatter(log_format)

    # ロガーの作成
    logger = logging.getLogger(name)
    
    # LOG_LEVEL 適用
    level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)

    # 二重出力防止
    logger.propagate = False
    
    # ハンドラ追加
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# デフォルトロガー
logger = logger_init("System")