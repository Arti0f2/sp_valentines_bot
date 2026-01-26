# config/constants.py
from datetime import time

VALENTINE_COST = 1 # вартість однієї валентинки у кредитах
INITIAL_BALANCE = 3 # кількість безкоштовних валентинок при реєстрації ОБНУЛИТЬ 
MONOBANK_POLL_INTERVAL = 70 # інтервал опитування монобанку в секундах

DELIVERY_DATE_DAY = 14 # число місяця доставки валентинок
DELIVERY_DATE_MONTH = 2     # місяць доставки валентинок
DELIVERY_TIME = time(0, 0, 0) # час доставки валентинок (00:00)

MAX_VALENTINE_TEXT_LENGTH = 500  # максимальна довжина тексту валентинки
MIN_AGE = 10 # мінімальний вік отримувача валентинки
MAX_AGE = 100 # максимальний вік отримувача валентинки

MONOBANK_DONATION_COMMENT_PREFIX = "valentine" # префікс коментаря для автоматичного донату
MONOBANK_JAR_LINK = "https://send.monobank.ua/jar/your_jar_id" # посилання на банку для донатів

DONATION_METHOD_AUTO = "monobank_auto" # метод донату - автоматичний через монобанк
DONATION_METHOD_MANUAL = "manual_screen" # метод донату - ручний через скріншот

DONATION_STATUS_PENDING = "pending" # статус донату - очікує обробки
DONATION_STATUS_COMPLETED = "completed" # статус донату - успішно завершено
DONATION_STATUS_REJECTED = "rejected" # статус донату - відхилено