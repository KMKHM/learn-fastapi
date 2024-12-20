from fastapi import APIRouter, Request, Depends
from app.service import user_service
from app.service.user_service import User
router = APIRouter()

@router.get("/")
async def root():
    return "hello"

@router.post("/users")
async def sign_up(user: User, result = Depends(user_service.create_user)):
    return {"message": "User created successfully", "user": result}

@router.get("/users")
async def get_users(request: Request):
    result = await user_service.get_all_users(request)
    return {"message": "Users fetched successfully", "users": result}

@router.get("/users/{id}")
async def get_user(request: Request, id: int):
    result = await user_service.get_user_by_id(request, id)
    return {"message": "User fetched successfully", "user": result}

@router.delete("/users/{id}")
async def delete_user(request: Request, id: int):
    await user_service.remove_user_by_id(request, id)
    return {"message": "User deleted successfully"}

@router.put("/users/{id}")
async def update_user(result=Depends(user_service.update_user_by_id)):
    return {"message": "User updated successfully", "user": result}