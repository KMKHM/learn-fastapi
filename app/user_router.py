from fastapi import APIRouter, Request
from app.user_service import create_user, User, get_all_users, get_user_by_id, remove_user_by_id

router = APIRouter()

@router.get("/")
async def root():
    return "hello"

@router.post("/users")
async def sign_up(user: User, request: Request):
    result = await create_user(request, user)
    return {"message": "User created successfully", "user": result}

@router.get("/users")
async def get_users(request: Request):
    result = await get_all_users(request)
    return {"message": "Users fetched successfully", "users": result}

@router.get("/users/{id}")
async def get_user(request: Request, id: int):
    result = await get_user_by_id(request, id)
    return {"message": "User fetched successfully", "user": result}

@router.delete("/users/{id}")
async def delete_user(request: Request, id: int):
    await remove_user_by_id(request, id)
    return {"message": "User deleted successfully"}