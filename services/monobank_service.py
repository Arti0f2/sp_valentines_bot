# services/monobank_service.py
import logging
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from external.monobank.client import MonobankClient
from database.repositories.transaction_repository import TransactionRepository
from database.repositories.user_repository import UserRepository
from config.constants import DONATION_STATUS_COMPLETED, DONATION_METHOD_AUTO
from utils.logger import get_logger

logger = get_logger(__name__)

class MonobankService:
    def __init__(self, session: AsyncSession, monobank_token: str):
        self.session = session
        self.client = MonobankClient(monobank_token)
        self.transaction_repo = TransactionRepository(session)
        self.user_repo = UserRepository(session)
    
    async def sync_transactions(self) -> list[tuple[int, int]]:
        from_time = datetime.now() - timedelta(hours=1)
        
        try:
            transactions = await self.client.get_statement(from_time=from_time)
        except Exception as e:
            logger.error(f"Failed to fetch Monobank statement: {e}")
            return []
        
        processed = []
        
        for transaction in transactions:
            try:
                if transaction.get('amount', 0) <= 0:
                    continue
                
                transaction_id = str(transaction.get('id'))
                description = transaction.get('description', '')
                amount_kopecks = transaction.get('amount', 0)
                amount_uah = amount_kopecks / 100
                
                exists = await self.transaction_repo.exists_by_transaction_id(transaction_id)
                if exists:
                    continue
                
                user_id = self._parse_user_id_from_comment(description)
                if user_id is None:
                    continue
                
                user_exists = await self.user_repo.exists(user_id)
                if not user_exists:
                    continue
                
                valentines_count = int(amount_uah // 10)
                if valentines_count <= 0:
                    continue
                
                await self.transaction_repo.create_transaction(
                    user_id=user_id,
                    amount=amount_uah,
                    transaction_id=transaction_id,
                    status=DONATION_STATUS_COMPLETED,
                    method=DONATION_METHOD_AUTO
                )
                
                success = await self.user_repo.update_balance(user_id, valentines_count)
                if not success:
                    logger.error(f"Failed to update balance for user {user_id}")
                    continue
                
                await self.session.commit()
                
                processed.append((user_id, valentines_count))
                
                logger.info(f"Processed donation: user_id={user_id}, amount={valentines_count}")
            
            except Exception as e:
                logger.error(f"Error processing transaction: {e}")
                try:
                    await self.session.rollback()
                except:
                    pass
                continue
        
        return processed
    
    def _parse_user_id_from_comment(self, description: str) -> int | None:
        try:
            parts = description.strip().split()
            for part in parts:
                if part.isdigit():
                    return int(part)
            return None
        except Exception:
            return None