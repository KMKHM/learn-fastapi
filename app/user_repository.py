
async def insert_user(pool, username: str, email: str):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO users (username, email) VALUES ($1, $2)
             """, username, email)

async def select_all_users(pool):
    async with pool.acquire() as conn:
        return await conn.fetch("""
                SELECT * FROM users
                """)
    
async def select_user_by_id(pool, id: int):
    async with pool.acquire() as conn:
        return await conn.fetchrow("""
                SELECT * FROM users WHERE id = $1
                """, id)

async def delete_user_by_id(pool, id: int):
    async with pool.acquire() as conn:
        await conn.execute("""
                DELETE FROM users WHERE id = $1
                """, id)

async def update_user_by_id(pool, id: int, username: str, email: str):
    async with pool.acquire() as conn:
        await conn.execute("""
                UPDATE users SET username = $2, email = $3 WHERE id = $1
                """, id, username, email)