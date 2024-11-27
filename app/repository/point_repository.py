async def charge_point(pool, user_id: int, amount: int):
    """
    사용자 포인트 충전 로직
    - user_id: 충전할 사용자 ID
    - amount: 충전할 금액
    """
    async with pool.acquire() as conn:
        # 비관적 락으로 현재 포인트 정보 조회
        point = await conn.fetchrow("""
            SELECT id, user_id, balance 
            FROM point 
            WHERE user_id = $1 
            FOR UPDATE
            """, user_id)
        
        if not point:
            # 포인트 정보가 없으면 새로 생성
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