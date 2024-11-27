async def charge_point(pool, user_id: int, amount: int):
    """
    사용자 포인트 충전 로직
    Args:
        user_id (int): 충전할 사용자 ID
        amount (int): 충전할 금액
    """
    async with pool.acquire() as conn:
        # 포인트 조회 로직
        point = await conn.fetchrow("""
            SELECT id, user_id, balance 
            FROM point 
            WHERE user_id = $1 
            FOR UPDATE
            """, user_id)
        
        if not point:
            # 정보없으면 생성
            return await conn.fetchrow("""
                INSERT INTO point (user_id, balance)
                VALUES ($1, $2)
                RETURNING *
                """, user_id, amount)
        
        # 기존 포인트에 충전
        return await conn.fetchrow("""
            UPDATE point 
            SET 
                balance = balance + $2,
                modified_at = CURRENT_TIMESTAMP
            WHERE user_id = $1
            RETURNING *
            """, user_id, amount)

async def get_point_by_user_id(pool, user_id: int):
    """사용자의 포인트 정보 조회"""
    async with pool.acquire() as conn:
        return await conn.fetchrow("""
            SELECT * FROM point WHERE user_id = $1
            """, user_id)
    
async def use_point(pool, user_id: int, amount: int):
    """
    사용자의 포인트 사용 로직
    Args:
        user_id (int): 사용할 사용자 ID
        amount (int): 사용할 금액
    Returns:
        업데이트된 포인트  / 진액 부족
    """
    async with pool.acquire() as conn:
        # 포인트 조회 및 잔액 확인을 위한 FOR UPDATE 락
        point = await conn.fetchrow(
            """
            SELECT id, user_id, balance 
            FROM point 
            WHERE user_id = $1 
            FOR UPDATE
            """, user_id)
        
        if not point or point['balance'] < amount:
            return None
            
        return await conn.fetchrow(
            """
            UPDATE point 
            SET 
                balance = balance - $2,
                modified_at = CURRENT_TIMESTAMP
            WHERE user_id = $1 AND balance >= $2
            RETURNING *
            """, user_id, amount)