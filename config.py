import os

from dotenv import load_dotenv

load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} is required")
    return value


admin = int(_require_env("ADMIN_ID"))
bot_name = _require_env("BOT_NAME")
bot_token = _require_env("BOT_TOKEN")
