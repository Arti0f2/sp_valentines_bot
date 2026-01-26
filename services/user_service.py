# services/user_service.py
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database.repositories.user_repository import UserRepository
from database.models import User
from config.constants import INITIAL_BALANCE

class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
    
    async def register_user(
        self,
        user_id: int,
        username: Optional[str],
        full_name: str
    ) -> User:
        user = await self.user_repo.create_user(
            user_id=user_id,
            username=username,
            full_name=full_name,
            balance=INITIAL_BALANCE
        )
        await self.session.commit()
        return user
    
    async def is_registered(self, user_id: int) -> bool:
        return await self.user_repo.exists(user_id)
    
    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.user_repo.get_by_user_id(user_id)
    
    async def get_by_username(self, username: str) -> Optional[User]:
        return await self.user_repo.get_by_username(username)
    
    async def update_username_if_changed(
        self,
        user_id: int,
        new_username: Optional[str]
    ) -> None:
        try:
            user = await self.user_repo.get_by_user_id(user_id)
            if user is None:
                return
            
            normalized_username = new_username.lower().lstrip('@') if new_username else None
            
            if user.username != normalized_username:
                user.username = normalized_username
                await self.session.commit()
        except Exception:
            await self.session.rollback()