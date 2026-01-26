# external/monobank/models.py
from typing import Optional
from pydantic import BaseModel

class MonobankTransaction(BaseModel):
    id: str
    time: int
    description: str
    mcc: int
    amount: int
    operationAmount: int
    currencyCode: int
    commissionRate: int
    cashbackAmount: int
    balance: int
    hold: bool