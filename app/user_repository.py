
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