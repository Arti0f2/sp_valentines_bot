# services/valentine_service.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database.repositories.valentine_repository import ValentineRepository
from database.repositories.user_repository import UserRepository
from database.models import Valentine
from config.constants import VALENTINE_COST

class ValentineService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.valentine_repo = ValentineRepository(session)
        self.user_repo = UserRepository(session)
    
    async def create_valentine(
        self,
        sender_id: int,
        recipient_username: str,
        message_text: str,
        delivery_slot: str
    ) -> Optional[Valentine]:
        sender = await self.user_repo.get_by_user_id(sender_id)
        if sender is None or sender.balance < VALENTINE_COST:
            return None
        
        valentine = await self.valentine_repo.create_valentine(
            sender_id=sender_id,
            recipient_username=recipient_username,
            message_text=message_text,
            delivery_slot=delivery_slot
        )
        
        await self.user_repo.update_balance(sender_id, -VALENTINE_COST)
        await self.session.commit()
        
        return valentine
    
    async def get_received_valentines(self, username: str) -> List[Valentine]:
        return await self.valentine_repo.get_received_by_username(username)
    
    async def get_pending_for_delivery(self, delivery_slot: str) -> List[Valentine]:
        return await self.valentine_repo.get_pending_for_delivery(delivery_slot)
    
    async def mark_as_delivered(self, valentine_id: int) -> bool:
        success = await self.valentine_repo.mark_sent(valentine_id)
        if success:
            await self.session.commit()
        return success
    
    async def mark_as_failed(self, valentine_id: int) -> bool:
        success = await self.valentine_repo.mark_failed(valentine_id)
        if success:
            await self.session.commit()
        return success