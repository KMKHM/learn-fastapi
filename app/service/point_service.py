from app.repository import point_repository
from app.decorator.transactional import transactional
from fastapi import Depends, HTTPException
from app.dependency.dependencies import get_db_pool
from pydantic import BaseModel

class Point(BaseModel):
    amount: int

@transactional
async def insert_point(pool=Depends(get_db_pool), *, user_id: int, point: Point):
    if point.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")
    result = await point_repository.charge_point(pool, user_id, point.amount)
    return result

@transactional
async def use_point(pool=Depends(get_db_pool), *, user_id: int, point: Point):
    result = await point_repository.use_point(pool, user_id, point.amount)

    if not result:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    return result