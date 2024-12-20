from fastapi import APIRouter, Depends
from app.service import point_service
from app.service.point_service import Point

router = APIRouter()

@router.post("/points/{user_id}")
async def insert_point(user_id: int, point: Point, result=Depends(point_service.insert_point)):
    return {"message": "Point created successfully", "point": result}

@router.post("/points/use/{user_id}")
async def use_point(user_id: int, point: Point, result=Depends(point_service.use_point)):
    return {"message": "Point used successfully", "point": result}