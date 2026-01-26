# database/repositories/valentine_repository.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from database.models import Valentine

class ValentineRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_valentine(
        self,
        sender_id: int,
        recipient_username: str,
        message_text: str,
        delivery_slot: str
    ) -> Valentine:
        normalized_username = recipient_username.lower().lstrip('@')
        
        valentine = Valentine(
            sender_id=sender_id,
            recipient_username=normalized_username,
            message_text=message_text,
            delivery_slot=delivery_slot,
            status='pending'
        )
        
        self.session.add(valentine)
        await self.session.flush()
        await self.session.refresh(valentine)
        return valentine
    
    async def get_pending_for_delivery(self, delivery_slot: str) -> List[Valentine]:
        result = await self.session.execute(
            select(Valentine)
            .where(Valentine.delivery_slot == delivery_slot)
            .where(Valentine.status == 'pending')
            .order_by(Valentine.created_at)
        )
        return list(result.scalars().all())
    
    async def get_received_by_username(self, username: str, limit: int = 100) -> List[Valentine]:
        normalized_username = username.lower().lstrip('@') if username else None
        if not normalized_username:
            return []
        
        result = await self.session.execute(
            select(Valentine)
            .where(Valentine.recipient_username == normalized_username)
            .where(Valentine.status == 'sent')
            .order_by(Valentine.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def mark_sent(self, valentine_id: int) -> bool:
        result = await self.session.execute(
            update(Valentine)
            .where(Valentine.id == valentine_id)
            .where(Valentine.status == 'pending')
            .values(status='sent')
        )
        await self.session.flush()
        return result.rowcount > 0
    
    async def mark_failed(self, valentine_id: int) -> bool:
        result = await self.session.execute(
            update(Valentine)
            .where(Valentine.id == valentine_id)
            .where(Valentine.status == 'pending')
            .values(status='failed')
        )
        await self.session.flush()
        return result.rowcount > 0