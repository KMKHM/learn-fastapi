from app.repository import user_repository
from pydantic import BaseModel
from fastapi import Request, HTTPException, Depends
from app.decorator.transactional import transactional
from app.dependency.dependencies import get_db_pool

class User(BaseModel):
    username: str
    email: str

@transactional
async def create_user(pool= Depends(get_db_pool), *, user: User):
    await user_repository.insert_user(pool, user.username, user.email)
    return user

async def get_all_users(request: Request):
    pool = request.app.state.db_pool
    return await user_repository.select_all_users(pool)

async def get_user_by_id(request: Request, id: int):
    pool = request.app.state.db_pool
    result = await user_repository.select_user_by_id(pool, id)

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    return result

@transactional
async def remove_user_by_id(request: Request, id: int):
    pool = request.app.state.db_pool
    return await user_repository.delete_user_by_id(pool, id)

@transactional
async def update_user_by_id(request: Request, id: int, user: User):
    pool = request.app.state.db_pool
    return await user_repository.update_user_by_id(pool, id, user.username, user.email)