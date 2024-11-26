import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

# 데이터베이스 설정
DB_SETTINGS = {
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "database": os.getenv("DATABASE"),
    "host": os.getenv("HOST")
}

async def setup_database():
    """테이블 초기화 및 데이터 삽입"""
    conn = await asyncpg.connect(**DB_SETTINGS)
    await conn.execute("""
        DROP TABLE IF EXISTS point;
        CREATE TABLE point (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            balance NUMERIC NOT NULL DEFAULT 0,
            reward_status BOOLEAN NOT NULL DEFAULT FALSE
        );
    """)
    await conn.execute("""
        INSERT INTO point (user_id, balance, reward_status)
        VALUES 
            (1, 1000, FALSE),
            (2, 500, FALSE);
    """)
    await conn.close()
    print("Database setup complete.")

async def reward_points(pool, user_id, reward_amount):
    """포인트 지급 로직"""
    async with pool.acquire() as conn:
        async with conn.transaction():
            # 비관적 락 설정
            # user = await conn.fetchrow("SELECT id, balance, reward_status FROM point WHERE user_id = $1;", user_id)
            user = await conn.fetchrow("SELECT id, balance, reward_status FROM point WHERE user_id = $1 FOR UPDATE;", user_id)

            if not user:
                print(f"User {user_id} not found.")
                return

            if user['reward_status']:
                print(f"User {user_id} already rewarded. Skipping.")
                return

            # 포인트 지급
            new_balance = user['balance'] + reward_amount
            await conn.execute(
                "UPDATE point SET balance = $1, reward_status = $2 WHERE id = $3;",
                new_balance, True, user['id']
            )
            print(f"User {user_id}: Rewarded {reward_amount} points. New balance: {new_balance}")

async def simulate_concurrent_rewards():
    """동시성 테스트 실행"""
    pool = await asyncpg.create_pool(**DB_SETTINGS)

    # 두 개의 트랜잭션을 동시에 실행 (동일 사용자 ID 1에 대해 포인트 지급 요청)
    await asyncio.gather(
        reward_points(pool, user_id=1, reward_amount=100),  # 트랜잭션 A
        reward_points(pool, user_id=1, reward_amount=100)   # 트랜잭션 B
    )

    # 최종 결과 확인
    async with pool.acquire() as conn:
        result = await conn.fetch("SELECT * FROM point;")
        print("Final Table State:")
        for row in result:
            print(dict(row))

    await pool.close()

async def main():
    await setup_database()  # 데이터베이스 초기화
    await simulate_concurrent_rewards()  # 동시성 테스트 실행

asyncio.run(main())
