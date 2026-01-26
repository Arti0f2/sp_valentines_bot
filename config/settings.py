# config/settings.py
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    MONOBANK_TOKEN: str = os.getenv("MONOBANK_TOKEN", "")
    ADMIN_IDS: List[int] = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
    TIMEZONE: str = os.getenv("TIMEZONE", "Europe/Kyiv")
    
    def validate(self) -> None:
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не встановлено")
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL не встановлено")
        if not self.MONOBANK_TOKEN:
            raise ValueError("MONOBANK_TOKEN не встановлено")
        if not self.ADMIN_IDS:
            raise ValueError("ADMIN_IDS не встановлено")

settings = Settings()
settings.validate()