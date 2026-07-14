# config/constants.py
from datetime import time

# моделі
VALENTINE_COST = 1 # вартість однієї валентинки
INITIAL_BALANCE = 0 # безкоштовні листівки при старті
MONOBANK_POLL_INTERVAL = 70 # як часто опитуємо monobank

# дата доставки
DELIVERY_DATE_DAY = 14 # 14 лютого
DELIVERY_DATE_MONTH = 2
DELIVERY_TIME = time(0, 0, 0) # формально

# валідація
MAX_VALENTINE_TEXT_LENGTH = 500
MIN_AGE = 10 
MAX_AGE = 100

# monobank
MONOBANK_DONATION_COMMENT_PREFIX = "valentine"
MONOBANK_JAR_LINK = "https://send.monobank.ua/jar/your_jar_id"

# статуси
DONATION_METHOD_AUTO = "monobank_auto"
DONATION_METHOD_MANUAL = "manual_screen"
DONATION_STATUS_PENDING = "pending"
DONATION_STATUS_COMPLETED = "completed"
DONATION_STATUS_REJECTED = "rejected"