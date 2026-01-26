# database/repositories/user_repository.py
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from database.models import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_user(self, user_id: int, username: Optional[str], full_name: str, balance: int = 0) -> User:
        normalized_username = username.lower().lstrip('@') if username else None
        
        user = User(
            user_id=user_id,
            username=normalized_username,
            full_name=full_name,
            balance=balance
        )
        
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user
    
    async def get_by_user_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        normalized_username = username.lower().lstrip('@')
        
        result = await self.session.execute(
            select(User).where(User.username == normalized_username)
        )
        return result.scalar_one_or_none()
    
    async def update_balance(self, user_id: int, delta: int) -> bool:
        user = await self.get_by_user_id(user_id)
        if user is None:
            return False
        
        new_balance = user.balance + delta
        if new_balance < 0:
            return False
        
        result = await self.session.execute(
            update(User)
            .where(User.user_id == user_id)
            .values(balance=new_balance)
        )
        await self.session.flush()
        return result.rowcount > 0
    
    async def exists(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(User.user_id).where(User.user_id == user_id)
        )
        return result.scalar_one_or_none() is not None
    
    async def update_username(self, user_id: int, username: Optional[str]) -> bool:
        normalized_username = username.lower().lstrip('@') if username else None
        
        result = await self.session.execute(
            update(User)
            .where(User.user_id == user_id)
            .values(username=normalized_username)
        )
        await self.session.flush()
        return result.rowcount > 0