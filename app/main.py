from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from config.db_config import connect_to_db, disconnect_from_db, create_user_table, create_point_table
from config.log_config import logging
from app.user_router import router as user_router
from app.point_router import router as point_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 시작 시 실행
    db_pool = await connect_to_db()
    app.state.db_pool = db_pool  # 앱 상태에 커넥션 풀 저장
    logging.info('"DB connected"')
    await create_user_table(db_pool)
    logging.info('"User table created"')
    await create_point_table(db_pool)
    logging.info('"Point table created"')
    yield  

    # 앱 종료 시 실행
    logging.info("Shutting down application...")
    await disconnect_from_db(db_pool)
    logging.info("Disconnected from the database")

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(point_router)

def get_service(id: int):
    return "service layer" + str(id)

@app.get("/service/{id}")
async def controller(service_result = Depends(get_service)):
    return service_result + "->" + "Controller layer"