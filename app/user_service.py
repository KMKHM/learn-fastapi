from app import user_repository
from pydantic import BaseModel
from fastapi import Request

class User(BaseModel):
    username: str
    email: str

async def create_user(request: Request, user: User):
    pool = request.app.state.db_pool
    await user_repository.insert_user(pool, user.username, user.email)
    return user

async def get_all_users(request: Request):
    pool = request.app.state.db_pool
    return await user_repository.select_all_users(pool)

async def get_user_by_id(request: Request, id: int):
    pool = request.app.state.db_pool
    return await user_repository.select_user_by_id(pool, id)

async def remove_user_by_id(request: Request, id: int):
    pool = request.app.state.db_pool
    return await user_repository.delete_user_by_id(pool, id)

async def update_user_by_id(request: Request, id: int, user: User):
    pool = request.app.state.db_pool
    return await user_repository.update_user_by_id(pool, id, user.username, user.email)