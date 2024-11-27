from functools import wraps
import asyncpg
import logging

def transactional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        pool = kwargs.get('pool')
        if not pool:
            pool = next((arg for arg in args if isinstance(arg, asyncpg.Pool)), None)
        if not pool:
            raise ValueError("Database pool not found")
        
        async with pool.acquire() as conn:
            try:
                async with conn.transaction():
                    return await func(*args, **kwargs)
            except Exception as e:
                logging.error(f"Transaction failed: {str(e)}")
                # 여기서 추가적인 에러 처리나 커스텀 예외를 발생시킬 수 있습니다
                raise
    return wrapper