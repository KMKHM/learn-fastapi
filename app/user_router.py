from fastapi import APIRouter, Request
from app.user_service import create_user, User, get_all_users

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