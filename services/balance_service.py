# services/balance_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from database.repositories.user_repository import UserRepository
from database.repositories.transaction_repository import TransactionRepository
from config.constants import DONATION_STATUS_COMPLETED, DONATION_METHOD_MANUAL
from datetime import datetime

class BalanceService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.transaction_repo = TransactionRepository(session)
    
    async def add_balance(self, user_id: int, amount: int) -> bool:
        if amount <= 0:
            return False
        
        success = await self.user_repo.update_balance(user_id, amount)
        await self.session.commit()
        return success
    
    async def manual_topup(self, user_id: int, amount: int, admin_id: int) -> bool:
        if amount <= 0:
            return False
        
        timestamp = int(datetime.now().timestamp())
        transaction_id = f"manual_{user_id}_{admin_id}_{timestamp}"
        
        exists = await self.transaction_repo.exists_by_transaction_id(transaction_id)
        if exists:
            return False
        
        await self.transaction_repo.create_transaction(
            user_id=user_id,
            amount=float(amount * 10),
            transaction_id=transaction_id,
            status=DONATION_STATUS_COMPLETED,
            method=DONATION_METHOD_MANUAL
        )
        
        await self.user_repo.update_balance(user_id, amount)
        await self.session.commit()
        
        return True
    
    async def get_balance(self, user_id: int) -> int:
        user = await self.user_repo.get_by_user_id(user_id)
        if user is None:
            return 0
        return user.balance
    
    async def can_afford(self, user_id: int, cost: int) -> bool:
        balance = await self.get_balance(user_id)
        return balance >= cost
    
    async def deduct_balance(self, user_id: int, amount: int) -> bool:
        if amount <= 0:
            return False
        
        user = await self.user_repo.get_by_user_id(user_id)
        if user is None or user.balance < amount:
            return False
        
        success = await self.user_repo.update_balance(user_id, -amount)
        await self.session.commit()
        return success