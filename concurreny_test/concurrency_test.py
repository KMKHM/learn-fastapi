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

# 계좌 초기화
async def setup_database():
    conn = await asyncpg.connect(**DB_SETTINGS)
    await conn.execute("""
        DROP TABLE IF EXISTS accounts;
        CREATE TABLE accounts (
            id SERIAL PRIMARY KEY,
            balance NUMERIC NOT NULL
        );
    """)
    # 초기 데이터 삽입
    await conn.execute("INSERT INTO accounts (balance) VALUES (1000);")
    await conn.close()
    print("Database setup complete.")

# 동시성 테스트 함수 (트랜잭션 내에서 실행)
async def update_balance(pool, delta, delay=0):
    async with pool.acquire() as conn:
        async with conn.transaction():
            # 계좌 정보 읽기
            account = await conn.fetchrow("SELECT id, balance FROM accounts WHERE id = 1;")
            # account = await conn.fetchrow("SELECT id, balance FROM accounts WHERE id = 1 FOR UPDATE;") #비관적 락
            current_balance = account['balance']
            print(f"Current balance: {current_balance}")

            # 테스트용 딜레이 추가
            await asyncio.sleep(delay)

            # 새로운 잔액 계산 및 업데이트
            new_balance = current_balance + delta
            await conn.execute("UPDATE accounts SET balance = $1 WHERE id = $2;", new_balance, account['id'])
            print(f"Updated balance: {new_balance}")

# 동시성 테스트 실행
async def run_concurrent_updates():
    pool = await asyncpg.create_pool(**DB_SETTINGS)

    # 두 트랜잭션을 동시에 실행
    await asyncio.gather(
        update_balance(pool, delta=-500, delay=1),  # 첫 번째 트랜잭션 (출금)
        update_balance(pool, delta=300, delay=0)   # 두 번째 트랜잭션 (입금)
    )

    # 결과 확인
    async with pool.acquire() as conn:
        final_balance = await conn.fetchval("SELECT balance FROM accounts WHERE id = 1;")
        print(f"Final balance: {final_balance}")
    
    await pool.close()

# 실행
async def main():
    await setup_database()      # 데이터베이스 초기화
    await run_concurrent_updates()  # 동시성 테스트 실행

asyncio.run(main())
