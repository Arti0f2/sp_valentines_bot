# utils/formatters.py
from datetime import datetime
from typing import Optional

def format_balance(balance: int) -> str:
    return f"{balance} 💌"

def format_datetime(dt: datetime, timezone: str = "Europe/Kyiv") -> str:
    import pytz
    tz = pytz.timezone(timezone)
    local_dt = dt.astimezone(tz)
    return local_dt.strftime("%d.%m.%Y %H:%M")

def format_username(username: Optional[str]) -> str:
    if not username:
        return "немає"
    return f"@{username.lstrip('@')}"