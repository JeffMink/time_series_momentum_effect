from pathlib import Path

# Project root = parent of the src/ folder, so paths work no matter where scripts are run from.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "market_data.db"
