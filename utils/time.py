# utils/time.py
from datetime import datetime
from pytz import timezone
from config.constants import DELIVERY_DATE_DAY, DELIVERY_DATE_MONTH

KYIV_TZ = timezone('Europe/Kyiv')

def now_kyiv() -> datetime:
    return datetime.now(KYIV_TZ)

def is_february_14() -> bool:
    now = now_kyiv()
    return now.month == DELIVERY_DATE_MONTH and now.day == DELIVERY_DATE_DAY

def current_delivery_slot() -> str:
    now = now_kyiv()
    hour = now.hour
    
    if 10 <= hour < 14:
        return 'morning'
    elif 14 <= hour < 20:
        return 'afternoon'
    elif hour >= 20 or hour < 10:
        return 'evening'
    else:
        return 'morning'

def get_kyiv_hour() -> int:
    return now_kyiv().hour