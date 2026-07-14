# external/monobank/models.py
# модель транзакції від monobank api
from typing import Optional
from pydantic import BaseModel

class MonobankTransaction(BaseModel):
    id: str
    time: int
    description: str  # юзер пише туди свій id
    mcc: int
    amount: int  # копійки
    operationAmount: int
    currencyCode: int
    commissionRate: int
    cashbackAmount: int
    balance: int
    hold: bool