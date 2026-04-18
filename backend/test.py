import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("Проверка всех импортов...\n")

to_check = [
    ("src.core.config", "settings"),
    ("src.core.security", "create_access_token"),
    ("src.core.dependencies", "get_current_user"),
    ("src.database.engine", "engine"),
    ("src.database.session", "SessionLocal"),
    ("src.db_models.user", "User"),
    ("src.schemas.user", "UserCreate"),
    ("src.api.auth", "router"),
    ("src.api.user", "router"),
]

for module, attr in to_check:
    try:
        imported = __import__(module, fromlist=[attr])
        getattr(imported, attr)
        print(f"✅ {module}.{attr}")
    except Exception as e:
        print(f"❌ {module}.{attr}: {e}")