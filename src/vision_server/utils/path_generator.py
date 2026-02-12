from pathlib import Path

ANCHOR_FILES = [".env", "requirements.txt"]

# ルートディレクトリのパスを返す。
def generate_root_path() -> Path:
    current_path = Path(__file__).resolve()

    for parent in [current_path] + list(current_path.parents):
        for anchor in ANCHOR_FILES:
            if (parent / anchor).exists():
                return parent
        
    raise FileNotFoundError(f"プロジェクトルートが見つかりませんでした。探索対象: {ANCHOR_FILES}")