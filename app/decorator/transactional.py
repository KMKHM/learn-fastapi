from fastapi import Request
from asyncpg import Connection
from functools import wraps

def transactional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = next((arg for arg in args if hasattr(arg, 'app')), kwargs.get('request'))
        if not request:
            raise ValueError("Request object not found")
        
        async with request.app.state.db_pool.acquire() as conn:
            async with conn.transaction():
                return await func(*args, **kwargs)
    return wrapper