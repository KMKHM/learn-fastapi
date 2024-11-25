from app.user_repository import insert_user, select_all_users
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