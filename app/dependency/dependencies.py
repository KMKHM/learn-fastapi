from fastapi import Depends, Request

async def get_db_pool(request: Request):
    return request.app.state.db_pool