from app.user_repository import insert_user, select_all_users, select_user_by_id, delete_user_by_id
from pydantic import BaseModel
from fastapi import Request

class User(BaseModel):
    username: str
    email: str

async def create_user(request: Request, user: User):
    pool = request.app.state.db_pool
    await insert_user(pool, user.username, user.email)
    return user

async def get_all_users(request: Request):
    pool = request.app.state.db_pool
    return await select_all_users(pool)

async def get_user_by_id(request: Request, id: int):
    pool = request.app.state.db_pool
    return await select_user_by_id(pool, id)

async def remove_user_by_id(request: Request, id: int):
    pool = request.app.state.db_pool
    return await delete_user_by_id(pool, id)