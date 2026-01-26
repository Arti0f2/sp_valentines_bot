# database/repositories/transaction_repository.py
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database.models import Donation

class TransactionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_transaction(
        self,
        user_id: int,
        amount: float,
        transaction_id: str,
        status: str,
        method: str
    ) -> Donation:
        donation = Donation(
            user_id=user_id,
            amount=amount,
            transaction_id=transaction_id,
            status=status,
            method=method
        )
        
        self.session.add(donation)
        await self.session.flush()
        await self.session.refresh(donation)
        return donation
    
    async def exists_by_transaction_id(self, transaction_id: str) -> bool:
        result = await self.session.execute(
            select(Donation.id).where(Donation.transaction_id == transaction_id)
        )
        return result.scalar_one_or_none() is not None
    
    async def get_by_user(self, user_id: int, limit: int = 100) -> List[Donation]:
        result = await self.session.execute(
            select(Donation)
            .where(Donation.user_id == user_id)
            .order_by(Donation.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def sum_by_user(self, user_id: int) -> float:
        result = await self.session.execute(
            select(func.sum(Donation.amount))
            .where(Donation.user_id == user_id)
            .where(Donation.status == 'completed')
        )
        total = result.scalar_one_or_none()
        return total if total is not None else 0.0
    