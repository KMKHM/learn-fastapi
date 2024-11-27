import asyncpg

DATABASE_URL = "postgresql://root:postgres@localhost:5432/postgres"


# db_pool = None

async def connect_to_db():
    return await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)


async def disconnect_from_db(pool):
    await pool.close()

async def create_user_table(pool):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                modified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            
            """)

async def create_point_table(pool):
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS point (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                balance NUMERIC NOT NULL DEFAULT 0,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                modified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_user
                    FOREIGN KEY (user_id)
                    REFERENCES users (id)
                    ON DELETE CASCADE
            );
        """)