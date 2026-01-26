# external/monobank/client.py
import aiohttp
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, timedelta
from utils.logger import get_logger

logger = get_logger(__name__)

class MonobankClient:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.monobank.ua"
        self.timeout = aiohttp.ClientTimeout(total=30)
    
    async def get_statement(
        self,
        account: str = "0",  # Примечание: id аккаунта часто строка (UUID), но "0" это дефолтный
        from_time: Optional[datetime] = None,
        to_time: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        
        if from_time is None:
            from_time = datetime.now() - timedelta(hours=1)
            
        if to_time is None:
            to_time = datetime.now()
        
        from_timestamp = int(from_time.timestamp())
        to_timestamp = int(to_time.timestamp())
        
        url = f"{self.base_url}/personal/statement/{account}/{from_timestamp}/{to_timestamp}"
        
        headers = {
            "X-Token": self.token
        }
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    elif response.status == 429:
                        logger.warning("Monobank API rate limit exceeded")
                        return []
                    else:
                        logger.error(f"Monobank API error: {response.status}")
                        return []
        except aiohttp.ClientError as e:
            logger.error(f"Monobank client error: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in Monobank client: {e}")
            return []